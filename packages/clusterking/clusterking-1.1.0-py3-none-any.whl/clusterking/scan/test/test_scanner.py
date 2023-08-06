#!/usr/bin/env python3

# std
import unittest
from pathlib import Path
import tempfile
import copy

# 3rd
import numpy as np

# ours
from clusterking.util.testing import MyTestCase
from clusterking.scan.scanner import Scanner
from clusterking.data.data import Data


# noinspection PyUnusedLocal
def func_zero(coeffs):
    return 0.0


def func_identity(coeffs):
    return coeffs


# noinspection PyUnusedLocal
def func_zero_bins(coeffs, x):
    return coeffs


def func_sum_indentity_x(coeffs, x):
    return sum(coeffs) * x


class TestScanner(MyTestCase):
    def setUp(self):
        # We also want to test writing, to check that there are e.g. no
        # JSON serialization problems.
        self.tmpdir = tempfile.TemporaryDirectory()

    def cleanUp(self):
        self.tmpdir.cleanup()

    def test_set_spoints_grid(self):
        s = Scanner()
        s.set_spoints_grid({"c": [1, 2], "a": [3], "b": [1j, 1 + 1j]})
        self.assertAllClose(
            s.spoints,
            np.array([[3, 1j, 1], [3, 1j, 2], [3, 1 + 1j, 1], [3, 1 + 1j, 2]]),
        )

    def test_set_spoints_grid_empty(self):
        s = Scanner()
        s.set_spoints_grid({})
        self.assertEqual(len(np.squeeze(s.spoints)), 0)

    def test_set_spoints_equidist(self):
        s = Scanner()
        s.set_imaginary_prefix("xxx")
        s.set_spoints_equidist(
            {"a": (1, 2, 2), "xxxa": (3, 4, 2), "c": (1, 1, 1)}
        )
        self.assertAllClose(
            s.spoints,
            np.array([[1 + 3j, 1], [1 + 4j, 1], [2 + 3j, 1], [2 + 4j, 1]]),
        )

    def test_run_zero(self):
        s = Scanner()
        d = Data()
        s.set_spoints_equidist({"a": (0, 1, 2)})
        s.set_dfunction(func_zero)
        s.run(d).write()
        self.assertEqual(sorted(list(d.df.columns)), ["a", "bin0"])
        self.assertAllClose(d.df.values, np.array([[0.0, 0.0], [1.0, 0.0]]))
        d.write(Path(self.tmpdir.name) / "test.sql")

    def test_run_identity(self):
        s = Scanner()
        d = Data()
        s.set_spoints_equidist({"a": (0, 1, 2)})
        s.set_dfunction(func_identity)
        s.run(d).write()
        self.assertEqual(sorted(list(d.df.columns)), ["a", "bin0"])
        self.assertAllClose(d.df.values, np.array([[0.0, 0.0], [1.0, 1.0]]))
        d.write(Path(self.tmpdir.name) / "test.sql")

    def test_run_identity_singlecore(self):
        s = Scanner()
        d = Data()
        s.set_spoints_equidist({"a": (0, 1, 2)})
        s.set_dfunction(func_identity)
        s.set_no_workers(1)
        s.run(d).write()
        self.assertEqual(sorted(list(d.df.columns)), ["a", "bin0"])
        self.assertAllClose(d.df.values, np.array([[0.0, 0.0], [1.0, 1.0]]))
        d.write(Path(self.tmpdir.name) / "test.sql")

    def test_run_simple_bins(self):
        s = Scanner()
        d = Data()
        s.set_spoints_equidist({"a": (0, 1, 2)})
        s.set_dfunction(func_zero_bins, binning=[0, 1, 2])
        s.run(d).write()
        self.assertEqual(sorted(list(d.df.columns)), ["a", "bin0", "bin1"])
        self.assertAllClose(
            d.df.values, np.array([[0.0, 0.0, 0.0], [1.0, 1.0, 1.0]])
        )
        d.write(Path(self.tmpdir.name) / "test.sql")

    def test_run_simple_bins_sample(self):
        s = Scanner()
        d = Data()
        s.set_spoints_equidist({"a": (0, 2, 3)})
        s.set_dfunction(func_sum_indentity_x, sampling=[0, 1, 2])
        s.run(d).write()
        self.assertEqual(
            sorted(list(d.df.columns)), ["a", "bin0", "bin1", "bin2"]
        )
        print(d.df.values)
        self.assertAllClose(
            d.df.values,
            np.array(
                [
                    [0.0, 0.0, 0.0, 0.0],
                    [1.0, 0.0, 1.0, 2.0],
                    [2.0, 0.0, 2.0, 4.0],
                ]
            ),
        )
        d.write(Path(self.tmpdir.name) / "test.sql")

    def test_run_simple_bins_singlecore(self):
        s = Scanner()
        d = Data()
        s.set_spoints_equidist({"a": (0, 1, 2)})
        s.set_dfunction(func_zero_bins, binning=[0, 1, 2])
        s.set_no_workers(1)
        s.run(d).write()
        self.assertEqual(sorted(list(d.df.columns)), ["a", "bin0", "bin1"])
        self.assertAllClose(
            d.df.values, np.array([[0.0, 0.0, 0.0], [1.0, 1.0, 1.0]])
        )
        d.write(Path(self.tmpdir.name) / "test.sql")

    def test_add_gaussian_noise(self):
        s = Scanner()
        s.set_spoints_equidist({"a": (-1, 1, 10), "b": (-1, 1, 10)})
        unmodified_spoints = copy.copy(s.spoints)
        # Note: sigma = 0. results in an error in some versions, so we choose
        # a very small value instead.
        s.add_spoints_noise("gauss", mean=0.0, sigma=10 ** -10)
        self.assertAllClose(unmodified_spoints, s.spoints)
        s.add_spoints_noise("gauss", mean=1.0, sigma=10 ** -10)
        self.assertAllClose(unmodified_spoints + 1, s.spoints)


if __name__ == "__main__":
    unittest.main()
