#!/usr/bin/env python3

""" Scans the NP parameter space in a grid and also q2, producing the
normalized q2 distribution. """

# std
import functools
import multiprocessing
import os
import time
from typing import Callable, Sized, Dict, Iterable, Optional, List
import itertools

# 3rd party
import numpy as np
import pandas as pd
import tqdm.auto

# ours
from clusterking.worker import DataWorker
from clusterking.data.data import Data
import clusterking.maths.binning
from clusterking.util.metadata import (
    version_info,
    failsafe_serialize,
    nested_dict,
)
from clusterking.util.log import get_logger
from clusterking.result import DataResult


class SpointCalculator(object):
    """ A class that holds the function with which we calculate each
    point in sample space. Note that this has to be a separate class from
    Scanner to avoid problems related to multiprocessing's use of the pickle
    library, which are described here:
    https://stackoverflow.com/questions/1412787/
    """

    def __init__(self):
        # All of these have to be set!
        #: Function to run
        self.func = None
        #: When function should be binned, this should be an array
        #: of the bin edge points, if the function should be sampled, an array
        #: of the sample points.
        self.binning = None
        #: 'sample', 'integrate'
        self.binning_mode = "integrate"
        #: Normalize distribution if binning is specified
        self.normalize = False
        self.kwargs = {}

    # todo: doc
    # todo: ignore static warning
    def _prepare_spoint(self, spoint):
        return spoint

    def calc(self, spoint) -> np.array:
        """Calculates one point in wilson space.

        Args:
            spoint: Wilson coefficients

        Returns:
            np.array of the integration results
        """

        spoint = self._prepare_spoint(spoint)
        if self.binning is not None:
            if self.binning_mode == "integrate":
                return clusterking.maths.binning.bin_function(
                    functools.partial(self.func, spoint, **self.kwargs),
                    self.binning,
                    normalize=self.normalize,
                )
            elif self.binning_mode == "sample":
                func = functools.partial(self.func, spoint, **self.kwargs)
                res = np.array(list(map(func, self.binning)))
                if self.normalize:
                    res /= sum(res)
                print("results", res)
                return res
        else:
            return self.func(spoint, **self.kwargs)


# todo: also allow to disable multiprocessing if there are problems.
class Scanner(DataWorker):
    """
    This class is set up with a function
    (specified in :meth:`.set_dfunction`) that depends
    on points in parameter space and a set of sample points in this parameter
    space (specified via one of the ``set_spoints_...`` methods).
    The function is then run for every sample point (in the :meth:`.run` method)
    and the results are written to a :class:`~clusterking.data.Data`-like
    object.

    Usage example:

    .. code-block:: python

        import clusterking as ck

        def myfunction(parameters, x):
            return sum(parameters) * x

        # Initialize Scanner class
        s = ck.scan.Scanner()

        # Set the function
        s.set_dfunction(myfunction)

        # Set the sample points
        s.set_spoints_equidist({
            "a": (-1, 1, 10),
            "b": (-1, 1, 10)
        })

        # Initialize a Data class to write to:
        d = ck.data.Data()

        # Run it
        r = s.run(d)

        # Write back results to data
        r.write()
    """

    # **************************************************************************
    # Constructor
    # **************************************************************************

    def __init__(self):
        """ Initializes the :class:`clusterking.scan.Scanner` class. """
        super().__init__()
        # todo: move
        self.log = get_logger("Scanner")

        #: Points in wilson space
        #:  Use self.spoints to access this
        self._spoints = None  # type: Optional[np.ndarray]

        #: Instance of SpointCalculator to perform the claculations of
        #:  the wilson space points.
        self._spoint_calculator = SpointCalculator()

        # todo: move
        self.md = nested_dict()
        self.md["git"] = version_info(self.log)
        self.md["time"] = time.strftime("%a %d %b %Y %H:%M", time.gmtime())

        # todo: shouldn't that be in metadata?
        #: Names of the parameters
        self._coeffs = []  # type: List[str]

        self._no_workers = None  # type: Optional[int]

        self._progress_bar = True
        self._tqdm_kwargs = {}

        self.set_imaginary_prefix("im_")

    # **************************************************************************
    # Convenience properties
    # **************************************************************************

    @property
    def imaginary_prefix(self) -> str:
        """ Prefix for the name of imaginary parts of coefficients.
        Also see e.g. :meth:`.set_spoints_equidist`. Read only.
        """
        return self.md["imaginary_prefix"]

    @property
    def spoints(self):
        """ Points in parameter space that are sampled (read-only)."""
        return self._spoints

    @property
    def coeffs(self):
        """ The name of the parameters/coefficients/dimensions of the spoints
        (read only).
        Set after spoints are set.
        Does **not** include the names of the columns of the imaginary parts.
        """
        return self._coeffs.copy()

    # **************************************************************************
    # Settings
    # **************************************************************************

    def set_progress_bar(self, show: bool, **kwargs) -> None:
        """ Settings for progress bar

        Args:
            show: Show progress bar?
            **kwargs: Keyword arguments for tqdm progress bar

        Returns:

        """
        self._progress_bar = show
        self._tqdm_kwargs = kwargs

    def set_dfunction(
        self,
        func: Callable,
        binning: Optional[Sized] = None,
        sampling: Optional[Sized] = None,
        normalize=False,
        xvar="xvar",
        yvar="yvar",
        **kwargs
    ):
        """ Set the function that generates the distributions that are later
        clustered (e.g. a differential cross section).

        Args:
            func: A function that takes the point in parameter space
                as the first argument (**Note**: The parameters are given in
                alphabetically order with respect to the parameter name!).
                It should either return a ``float`` or a ``np.ndarray``.
                If the ``binning`` or ``sampling`` options are specified, only
                ``float`` s as return value are allowed.
            binning: If this parameter is set to an array-like object, we will
                integrate the function over the specified bins for every point
                in parameter space.
            sampling: If this parameter is set to an array-like object, we will
                apply the function to these points for every point in parameter
                space.
            normalize: If a binning is specified, normalize the resulting
                distribution.
            xvar: Name of variable on x-axis
            yvar: Name of variable on y-axis
            **kwargs: All other keyword arguments are passed to the function.

        Returns:
            None
        """
        if normalize and binning is None and sampling is None:
            raise ValueError(
                "The setting normalize=True only makes sense if a binning or "
                "sampling is specified."
            )
        if binning is not None and sampling is not None:
            raise ValueError("Please specify EITHER sampling OR binning.")

        # The block below just wants to put some information about the function
        # in the metadata. Can be ignored if you're only interested in what's
        # happening.
        md = self.md["dfunction"]
        try:
            md["name"] = func.__name__
            md["doc"] = func.__doc__
        except AttributeError:
            try:
                # For functools.partial objects
                # noinspection PyUnresolvedReferences
                md["name"] = "functools.partial({})".format(func.func.__name__)
                # noinspection PyUnresolvedReferences
                md["doc"] = func.func.__doc__
            except AttributeError:
                pass

        md["kwargs"] = failsafe_serialize(kwargs)

        md["binning"] = binning

        # This is the important thing: We set all required attributes of the
        # spoint calculator!
        self._spoint_calculator.func = func
        if binning is not None:
            self._spoint_calculator.binning = binning
            self._spoint_calculator.binning_mode = "integrate"
            md["binning"] = list(binning)
            md["binning_mode"] = "integrate"
            md["nbins"] = len(binning) - 1
        elif sampling is not None:
            self._spoint_calculator.binning = sampling
            md["binning"] = list(sampling)
            self._spoint_calculator.binning_mode = "sample"
            md["binning_mode"] = "sample"
            md["nbins"] = len(sampling)

        md["xvar"] = xvar
        md["yvar"] = yvar

        self._spoint_calculator.normalize = normalize
        self._spoint_calculator.kwargs = kwargs

    def set_spoints_grid(self, values: Dict[str, Iterable[float]]) -> None:
        """ Set a grid of points in sampling space.

        Args:
            values: A dictionary of the following form:

                .. code-block:: python

                    {
                        <coeff name>: [
                            value_1,
                            ...,
                            value_n
                        ]
                    }

                where ``value_1``, ..., ``value_n`` can be complex numbers in
                general.
        """

        # IMPORTANT to keep this order!
        self._coeffs = sorted(list(values.keys()))

        # Nowe we collect all lists of values.
        values_lists = [values[coeff] for coeff in self._coeffs]
        # Now we build the cartesian product, i.e.
        # [a1, a2, ...] x [b1, b2, ...] x ... x [z1, z2, ...] =
        # [(a1, b1, ..., z1), ..., (a2, b2, ..., z2)]
        self._spoints = np.array(list(itertools.product(*values_lists)))

        self.md["spoints"]["grid"] = failsafe_serialize(values)

    def set_spoints_equidist(self, ranges: Dict[str, tuple]) -> None:
        """ Set a list of 'equidistant' points in sampling space.

        Args:
            ranges: A dictionary of the following form:

                .. code-block:: python

                    {
                        <coeff name>: (
                            <Minimum of coeff>,
                            <Maximum of coeff>,
                            <Number of bins between min and max>,
                        )
                    }

        .. note::

            In order to add imaginary parts to your coefficients,
            prepend their name with ``im_`` (you can customize this prefix by
            setting the :attr:`.imaginary_prefix` attribute to a custom value.)

            Example:

            .. code-block:: python

                s = Scanner()
                s.set_spoints_equidist(
                    {
                        "a": (-2, 2, 4),
                        "im_a": (-1, 1, 10),
                    },
                    ...
                )

            Will sample the real part of ``a`` in 4 points between -2 and 2 and
            the imaginary part of ``a`` in 10 points between -1 and 1.

        Returns:
            None
        """
        # Because of our hack with the imaginary prefix, let's first see which
        # coefficients we really have

        def is_imaginary(name: str) -> bool:
            return name.startswith(self.imaginary_prefix)

        def real_part(name: str) -> str:
            if is_imaginary(name):
                return name.replace(self.imaginary_prefix, "", 1)
            else:
                return name

        def imaginary_part(name: str) -> str:
            if not is_imaginary(name):
                return self.imaginary_prefix + name
            else:
                return name

        coeffs = list(set(map(real_part, ranges.keys())))

        grid_config = {}
        for coeff in coeffs:
            # Now let's always collect the values of the real part and of the
            # imaginary part
            res = [0.0]
            ims = [0.0]
            is_complex = False
            if real_part(coeff) in ranges:
                res = list(np.linspace(*ranges[real_part(coeff)]))
            if imaginary_part(coeff) in ranges:
                ims = list(np.linspace(*ranges[imaginary_part(coeff)]))
                is_complex = True
            # And basically take their cartesian product, alias initialize
            # the complex number.
            if is_complex:
                grid_config[coeff] = [complex(x, y) for x in res for y in ims]
            else:
                grid_config[coeff] = res

        self.set_spoints_grid(grid_config)
        # Make sure to do this after set_spoints_grid, so we overwrite
        # the relevant parts.
        md = self.md["spoints"]
        md["sampling"] = "equidistant"
        md["ranges"] = ranges

    # todo: Apply to only one dimension?
    def add_spoints_noise(self, generator="gauss", **kwargs) -> None:
        """ Add noise to existing sample points.

        Args:
            generator: Random number generator. Default is ``gauss``.
                Currently supported: ``gauss``.

            **kwargs: Additional keywords to configure the generator. These
                keywords are as follows (value assignments are the default
                values): ``gauss``: ``mean = 0``, ``sigma = 1``
        """
        if self.spoints is None:
            raise ValueError(
                "This method can only be applied after spoints"
                " have been set."
            )
        if generator == "gauss":
            gauss_kwargs = {"mean": 0.0, "sigma": 1.0}
            gauss_kwargs.update(kwargs)
            rand = np.random.normal(
                loc=gauss_kwargs["mean"],
                scale=gauss_kwargs["sigma"],
                size=self.spoints.shape,
            )
        else:
            raise ValueError("Unknown generator {}.".format(generator))
        if "noise" not in self.md:
            self.md["noise"] = []
        self.md["noise"].append({"generator": generator, "kwargs": kwargs})
        self._spoints += rand

    def set_no_workers(self, no_workers: int) -> None:
        """ Set the number of worker processes to be used. This will usually
        translate to the number of CPUs being used.

        Args:
            no_workers: Number of worker processes

        Returns:
            ``None``
        """
        self._no_workers = no_workers

    def set_imaginary_prefix(self, value: str) -> None:
        """ Set prefix to be used for imaginary parameters in
        :meth:`set_spoints_grid` and :meth:`set_spoints_equidist`.

        Args:
            value: Prefix string

        Returns:
            ``None``
        """
        self.md["imaginary_prefix"] = value

    # **************************************************************************
    # Run
    # **************************************************************************

    def run(self, data: Data) -> Optional["ScannerResult"]:
        """Calculate all sample points and writes the result to a dataframe.

        Args:
            data: Data object.

        Returns:
            :class:`ScannerResult` or None

        .. warning::

            The function set in :meth:`set_dfunction` has to be a globally
            defined function in order to do multiprocessing, else
            you will probably run into the error
            ``Can't pickle local object ...`` that is issued by the python
            multiprocessing module.
            If you run into any probelms like this, you can always run in
            single core mode by specifying ``no_workes=1``.

        """

        # todo: rather raise exceptions?
        if not self._spoints.any():
            self.log.error(
                "No sample points specified. Returning without doing "
                "anything."
            )
            return
        if not self._spoint_calculator:
            self.log.error(
                "No function specified. Please set it "
                "using ``Scanner.set_dfunction``. Returning without doing "
                "anything."
            )
            return

        no_workers = self._no_workers
        if not self._no_workers:
            no_workers = os.cpu_count()
        if not no_workers:
            # os.cpu_count() didn't work
            self.log.warn(
                "os.cpu_count() not determine number of cores. Fallling "
                "back to single core mode."
            )
            no_workers = 1

        start_time = time.time()

        if no_workers >= 2:
            rows = self._run_multicore(no_workers)
        else:
            rows = self._run_singlecore()

        end_time = time.time()
        run_time = end_time - start_time
        self.md["run_time"] = run_time

        return ScannerResult(
            data=data,
            rows=rows,
            spoints=self._spoints,
            md=self.md,
            coeffs=self._coeffs,
        )

    # todo: shouldn't this rather return numpy arrays than List2
    def _run_multicore(self, no_workers: int) -> List[List[float]]:
        """ Calculate spoints in parallel processing mode.

        Args:
            no_workers: Number of workers.

        Returns:
            Rows of the dataframe.
        """
        # pool of worker nodes
        pool = multiprocessing.Pool(processes=no_workers)

        # this is the worker function.
        worker = self._spoint_calculator.calc

        results = pool.imap(worker, self._spoints)

        # close the queue for new jobs
        pool.close()

        self.log.info(
            "Started queue with {} job(s) distributed over up to {} "
            "core(s)/worker(s).".format(len(self._spoints), no_workers)
        )

        rows = []

        if self._progress_bar:
            tqdm_kwargs = dict(
                desc="Scanning: ", unit=" spoint", total=len(self._spoints)
            )
            tqdm_kwargs.update(self._tqdm_kwargs)
            iterator = tqdm.auto.tqdm(enumerate(results), **tqdm_kwargs)
        else:
            iterator = enumerate(results)

        for index, result in iterator:
            md = self.md["dfunction"]

            if not isinstance(result, Iterable):
                result = [result]

            if "nbins" not in md:
                md["nbins"] = len(result)

            rows.append([*self._spoints[index], *result])

        # Wait for completion of all jobs here
        pool.join()

        return rows

    # todo: shouldn't this rather return numpy arrays than List2
    def _run_singlecore(self) -> List[List[float]]:
        """ Calculate spoints in single core processing mode. This is sometimes
        useful because multiprocessing has its quirks.

        Returns:
            Rows of the dataframe.
        """
        self.log.info(
            "Started queue with {} job(s) in single core mode.".format(
                len(self._spoints)
            )
        )

        rows = []
        for index, spoint in tqdm.auto.tqdm(
            enumerate(self._spoints),
            desc="Scanning: ",
            unit=" spoint",
            total=len(self._spoints),
        ):
            result = self._spoint_calculator.calc(spoint)

            md = self.md["dfunction"]

            if not isinstance(result, Iterable):
                result = [result]

            if "nbins" not in md:
                md["nbins"] = len(result)

            rows.append([*self._spoints[index], *result])

        return rows


class ScannerResult(DataResult):
    def __init__(
        self, data: Data, rows: List[List[float]], spoints, md, coeffs
    ):
        super().__init__(data=data)
        self._rows = rows
        self._spoints = spoints
        self.md = md  # type: nested_dict
        self._coeffs = coeffs

    # **************************************************************************
    # Convenience properties
    # **************************************************************************

    @property
    def imaginary_prefix(self) -> str:
        """ Prefix for the name of imaginary parts of coefficients.
        Also see e.g. :meth:`.set_spoints_equidist`. Read only.
        """
        return self.md["imaginary_prefix"]

    @property
    def spoints(self):
        """ Points in parameter space that are sampled (read-only)."""
        return self._spoints

    @property
    def coeffs(self):
        """ The name of the parameters/coefficients/dimensions of the spoints
        (read only).
        Set after spoints are set.
        Does **not** include the names of the columns of the imaginary parts.
        """
        return self._coeffs.copy()

    # **************************************************************************
    # Write
    # **************************************************************************

    def write(self) -> None:
        self.log.debug("Converting data to pandas dataframe.")
        cols = self.coeffs
        cols.extend(
            [
                "bin{}".format(no_bin)
                for no_bin in range(self.md["dfunction"]["nbins"])
            ]
        )

        # Now we finally write everything to data
        self._data.df = pd.DataFrame(data=self._rows, columns=cols)

        # todo: Shouldn't we do that above already? This sounds not so
        #   great performance wise...
        # Special handling for complex numbers
        coeffs_with_im = []
        for coeff in self.coeffs:
            coeffs_with_im.append(coeff)
            if not list(self._data.df[coeff].apply(np.imag).unique()) == [0.0]:
                values = self._data.df[coeff]
                self._data.df[coeff] = values.apply(np.real)
                loc = list(self._data.df.columns).index(coeff)
                self._data.df.insert(
                    loc + 1,
                    self.imaginary_prefix + coeff,
                    values.apply(np.imag),
                )
                coeffs_with_im.append(self.imaginary_prefix + coeff)
            else:
                self._data.df[coeff] = self._data.df[coeff].apply(np.real)

        self._data.df.index.name = "index"

        # fixme: Should already be set in worker class
        self.md["spoints"]["coeffs"] = coeffs_with_im

        self._data.md["scan"] = self.md

        self.log.info("Integration done.")
