"""Test the PTFILE loader and comparison functions

Real test cases are taken from the DL_MONTE test suite,
the location of which is obtained from the environment 
variable DLM_TEST_SUITE. Hence this environment variable 
must be set before the tests here can be used.
"""

import os.path
import unittest

import dlmontepython.htk.sources.dlptfile as dlptfile
from dlmontepython.htk.sources.dlptfile import KEY_NMOL
from dlmontepython.htk.sources.dlptfile import KEY_TIMESTEP
from dlmontepython.htk.sources.dlptfile import PTFILE

class PTFILETestCase(unittest.TestCase):

    """Tests against synthetic data"""

    def test_allclose0(self):

        """Duff data"""

        pt1 = PTFILE(data=None)
        pt2 = PTFILE(data=1.2)

        with self.assertRaises(TypeError):
            pt1.allclose(pt2)

    def test_allclose1(self):

        """Good time step"""

        pt1 = PTFILE(data=[{KEY_TIMESTEP: 1000}])
        pt2 = PTFILE(data=[{KEY_TIMESTEP: 1000}])

        self.assertEqual(True, pt1.allclose(pt2))


    def test_allcose2(self):

        """Mismatch timestep value"""

        pt1 = PTFILE(data=[{KEY_TIMESTEP: 1000}])
        pt2 = PTFILE(data=[{KEY_TIMESTEP: 100}])

        with self.assertRaises(ValueError):
            pt1.allclose(pt2)


    def test_allclose3(self):

        """No timestep"""

        pt1 = PTFILE(data=[{KEY_TIMESTEP: 1000}])
        pt2 = PTFILE(data=[{}])

        with self.assertRaises(KeyError):
            pt1.allclose(pt2)


    def test_allclose4(self):

        """Check energy"""

        pt1 = PTFILE(data=[{KEY_TIMESTEP: 1000, "energy": -1.2}])
        pt2 = PTFILE(data=[{KEY_TIMESTEP: 1000, "energy": -1.20}])

        self.assertEqual(True, pt1.allclose(pt2))

        pt2.data[0]["energy"] = -1.20000000001
        self.assertEqual(True, pt1.allclose(pt2))

        pt2.data[0]["energy"] = -1.201
        self.assertEqual(False, pt1.allclose(pt2))


    def test_allclose5(self):

        """Check nmol"""

        pt1 = PTFILE([{KEY_TIMESTEP: 1, KEY_NMOL: [1, 2]}])
        pt2 = PTFILE([{KEY_TIMESTEP: 1, KEY_NMOL: [1, 2]}])

        self.assertEqual(True, pt1.allclose(pt2))

        pt2.data[0][KEY_NMOL] = [1]
        self.assertEqual(False, pt1.allclose(pt2))

        pt2.data[0][KEY_NMOL] = [1, 3]
        self.assertEqual(False, pt1.allclose(pt2))


class PTFILERegressionTestCase(unittest.TestCase):

    """Tests against a selection of regression test data"""

    def setUp(self):

        """Get path to DL_MONTE test directory from environment 
        variable DLM_TEST_SUITE"""

        self.tests = os.getenv("DLM_TEST_SUITE")

    def test_gcmc_lj_short(self):

        """GCMC LJ"""

        location = os.path.join(self.tests, "gcmc_lj", "short-abw-2017jan-alpha", "benchmark")
        filename = os.path.join(location, "PTFILE.000")
        self.assertTrue(os.path.exists(filename))

        ptfile = dlptfile.load(location)

        # Time steps 1000, ..., 10000

        data = ptfile.time_steps()
        self.assertEqual(len(data), 10)
        self.assertEqual(data[0], 1000)
        self.assertEqual(data[-1], 10000)

        # Two energies

        ref = [-59.6825, -94.0929, -109.123] # etc...

        data = ptfile.time_series("energy")
        self.assertEqual(len(data), 10)
        self.assertEqual(data[0:3], ref)

        data = ptfile.time_series("energyvdw")
        self.assertEqual(len(data), 10)
        self.assertEqual(data[0:3], ref)

        # Atoms (and molecules)

        ref = [93, 113, 125, 123, 111, 125, 148, 139, 114, 108] 

        natomtypes, atomdata = ptfile.natom()
        self.assertEqual(natomtypes, 1)
        self.assertEqual(atomdata[0], ref)

        nmoltypes, moldata = ptfile.nmol()
        self.assertEqual(nmoltypes, natomtypes)
        self.assertEqual(moldata, atomdata)


    def test_gcmc_co2_zeolite(self):

        """GCMC CO_2 and Zeolite ... a largeish file"""

        location = os.path.join(self.tests, "gcmc_co2_zeolite", "short-abw-2017jan-alpha", "benchmark")
        filename = os.path.join(location, "PTFILE.000")
        self.assertTrue(os.path.exists(filename))

        ptfile = dlptfile.load(location)

        data = ptfile.time_steps()
        self.assertEqual(len(data), 100)
        self.assertEqual(data[0], 1000)
        self.assertEqual(data[-1], 100000)

        # Atoms

        ref_atom0 = [192, 192, 192]
        ref_atom1 = [384, 384, 384]
        ref_atom2 = [4, 0, 1, 1]
        ref_atom3 = [8, 0, 2, 2]
        ref_atom4 = [8, 8, 8, 8]

        natomtypes, data = ptfile.natom()
        self.assertEqual(natomtypes, 5)
        self.assertEqual(data[0][0:3], ref_atom0)
        self.assertEqual(data[1][0:3], ref_atom1)
        self.assertEqual(data[2][0:4], ref_atom2)
        self.assertEqual(data[3][0:4], ref_atom3)
        self.assertEqual(data[4][0:4], ref_atom4)

        # Molecules

        ref_mol0 = [1, 1, 1, 1]
        ref_mol1 = [4, 0, 1, 1]

        nmoltypes, data = ptfile.nmol()
        self.assertEqual(nmoltypes, 2)
        self.assertEqual(data[0][0:4], ref_mol0)
        self.assertEqual(data[1][0:4], ref_mol1)
