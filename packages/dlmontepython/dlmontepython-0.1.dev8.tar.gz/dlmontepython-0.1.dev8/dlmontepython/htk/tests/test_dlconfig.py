"""Tests for dlconfig includes:

Synthetic tests
Real tests against standard regression inputs

Real test cases are taken from the DL_MONTE test suite,
the location of which is obtained from the environment 
variable DLM_TEST_SUITE. Hence this environment variable 
must be set before the tests here can be used.
"""

import os.path
import unittest

import dlmontepython.htk.sources.dlconfig as dlconfig


class CONFIGTestCase(unittest.TestCase):

    """Synthetic tests"""


    def test_dlconfig_bare_minimum(self):

        """Made-up minimal example"""

        title = "A test title"
        dlformat = 1
        level = 2
        vcell = [[1., 2., 3.], [4., 5., 6.], [7., 8., 9.]]
        nummol = [10, 11, 12]

        conf = dlconfig.CONFIG(title, level, dlformat, vcell, nummol)

        self.assertEqual(title, conf.title)
        self.assertEqual(level, conf.level)
        self.assertEqual(dlformat, conf.dlformat)
        self.assertEqual(vcell, conf.vcell)
        self.assertEqual(nummol, conf.nummol)


class RegressionCONFIGTestCase(unittest.TestCase):

    """Real CONFIG files from main tests directory"""

    def setUp(self):

        """Get path to DL_MONTE test directory from environment 
        variable DLM_TEST_SUITE"""

        self.tests = os.getenv("DLM_TEST_SUITE")

    def test_gcmc_lj(self):

        """GCMC_LJ CONFIG file"""

        filename = os.path.join(self.tests, "gcmc_lj", "short-abw-2017jan-alpha", "input", "CONFIG")
        self.assertTrue(os.path.exists(filename))

        conf = dlconfig.from_file(filename)

        # Lattice vectors

        self.assertEqual(conf.vcell[0], [10.0, 0.0, 0.0])
        self.assertEqual(conf.vcell[1], [0.0, 10.0, 0.0])
        self.assertEqual(conf.vcell[2], [0.0, 0.0, 10.0])

        self.assertEqual(conf.volume(), 1000.0)

        # 8 molecules, 2 lines per atom
        self.assertEqual(8, len(conf.molecules))
        self.assertEqual(2, len(conf.molecules[0]["atoms"]))


    def test_gcmc_co2_zeolite(self):

        """GCMC Co2 Zeolite test"""

        filename = os.path.join(self.tests, "gcmc_co2_zeolite", "CONFIG")
        self.assertTrue(os.path.exists(filename))

        conf = dlconfig.from_file(filename)

        self.assertEqual(conf.level, dlconfig.DLPOLY_LEVEL_ZERO)
        self.assertEqual(conf.dlformat, dlconfig.DLMONTE_FORMAT_FRACTIONAL)

        # Cell lengths
        clen = 24.4750735

        self.assertEqual(conf.vcell[0], [clen, 0.0, 0.0])
        self.assertEqual(conf.vcell[1], [0.0, clen, 0.0])
        self.assertEqual(conf.vcell[2], [0.0, 0.0, clen])

        self.assertEqual(conf.volume(), clen*clen*clen)


    def test_water_spce_nist(self):

        """Water SPCE NIST"""

        filename = os.path.join(self.tests, "nist_spce_water", "CONFIG")
        conf = dlconfig.from_file(filename)

        clen = 20.0

        self.assertEqual(conf.vcell[0], [clen, 0.0, 0.0])
        self.assertEqual(conf.vcell[1], [0.0, clen, 0.0])
        self.assertEqual(conf.vcell[2], [0.0, 0.0, clen])


    def test_npt_water_spce(self):

        """NPT water has Cartesian format"""

        fname = os.path.join(self.tests, "npt_water_spce", "short-abw-2017jan-alpha", "input", "CONFIG")
        conf = dlconfig.from_file(fname)

        self.assertEqual(conf.level, dlconfig.DLPOLY_LEVEL_ZERO)
        self.assertEqual(conf.dlformat, dlconfig.DLMONTE_FORMAT_CARTESIAN)

        self.assertEqual(conf.nummol, [512, 512])

        mol = conf.molecules[0]
        self.assertEqual(mol["name"], "water")
        self.assertEqual(mol["natom"], 3)
        #TU: Removed test for nmaxatom because it is apparently deprecated in
        #TU: DL_MONTE, and also htk in response
        #self.assertEqual(mol["nmaxatom"], 3)


    def tearDown(self):

        """Release test resoueces"""

        self.tests = None
