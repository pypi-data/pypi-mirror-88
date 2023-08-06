"""Test ensembles"""

import unittest

import dlmontepython.htk.ensemble
from dlmontepython.htk.ensemble import EnsembleNVT, EnsembleNPT, EnsembleMuVT, \
                         EnsembleNVE

class EnsembleTestCase(unittest.TestCase):

    """Ensemble class"""

    def test_ensemble(self):

        """KEY_ENSEMBLES"""

        self.assertEqual(dlmontepython.htk.ensemble.KEY_ENSEMBLE["nvt"], EnsembleNVT)
        self.assertEqual(dlmontepython.htk.ensemble.KEY_ENSEMBLE["npt"], EnsembleNPT)


    def test_ensemble_nvt(self):

        """NVT"""

        nvt = EnsembleNVT()

        self.assertEqual(nvt.name, "NVT")
        self.assertEqual(nvt.longname, "Canonical")

        with self.assertRaises(AttributeError):
            del nvt.longname

        self.assertTrue(nvt == EnsembleNVT())

        nvt = dlmontepython.htk.ensemble.from_string("NVt")
        self.assertIsInstance(nvt, EnsembleNVT)


    def test_emsemble_npt(self):

        """NPT"""

        npt = EnsembleNPT()
        self.assertEqual(npt.name, "NPT")
        self.assertEqual(npt.longname, "Isothermal-Isobaric")

        npt = dlmontepython.htk.ensemble.from_string("npt")
        self.assertIsInstance(npt, EnsembleNPT)


    def test_ensemble_nve(self):

        """NVE"""

        nve = EnsembleNVE()
        self.assertEqual(nve.name, "NVE")
        self.assertEqual(nve.longname, "Microcanonical")

        nve = dlmontepython.htk.ensemble.from_string("nvE")
        self.assertIsInstance(nve, EnsembleNVE)


    def test_ensemble_muvt(self):

        """muVT"""

        muvt = EnsembleMuVT()
        self.assertEqual(muvt.name, "muVT")
        self.assertEqual(muvt.longname, "Grand Canonical")

        muvt = dlmontepython.htk.ensemble.from_string("muvt")
        self.assertIsInstance(muvt, EnsembleMuVT)
