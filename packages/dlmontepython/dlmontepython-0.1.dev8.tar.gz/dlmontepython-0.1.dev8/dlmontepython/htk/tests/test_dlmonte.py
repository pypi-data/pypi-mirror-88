"""Tests for DLMonte helper classes


Real test cases are taken from the DL_MONTE test suite,
the location of which is obtained from the environment 
variable DLM_TEST_SUITE. Hence this environment variable 
must be set before the tests here can be used.
Moreover, the variable PATH is assumed to be set such 
that it includes the path to the DL_MONTE executable
DLMONTE-SRL.X.
"""

import os.path
import unittest
import numpy

from dlmontepython.htk.ensemble import EnsembleNPT, EnsembleMuVT
from dlmontepython.htk.sources.dlmonte import DLMonteData
import dlmontepython.htk.sources.dlmonte as dlmonte

class DLMonteTest(unittest.TestCase):

    """Specific case cases pending"""

    def setUp(self):

        """Get path to DL_MONTE test directory from environment 
        variable DLM_TEST_SUITE. Assume path is set up so that
        DL_MONTE executable DLMONTE-SRL.X is visible."""

        self.exe = "DLMONTE-SRL.X"

        self.tests = os.getenv("DLM_TEST_SUITE")
        self.tmp = os.curdir

    def test_dlmonte_input(self):

        """Check input read and write"""

        location = os.path.join(self.tests, "gcmc_lj", "short-abw-2017jan-alpha")
        input_dir = os.path.join(location, "input")
        inputs = dlmonte.DLMonteInput.from_directory(input_dir)

        inputs.to_directory(self.tmp)

        files = ["CONFIG", "CONTROL", "FIELD"]

        for name in files:
            filename = os.path.join(self.tmp, name)
            self.assertTrue(os.path.exists(filename))
            os.remove(filename)


    def test_dlmonte_output(self):

        """Check output read"""

        pass


    def test_dlmonte_run(self):

        """A complete DL MONTE run"""

        location = os.path.join(self.tests, "gcmc_lj", "short-abw-2017jan-alpha")
        input_dir = os.path.join(location, "input")
        ref_dir = os.path.join(location, "benchmark")

        runner = dlmonte.DLMonteRunner(self.exe, self.tmp)
        runner.clone_input(input_dir)

        runner.execute()

        orig = dlmonte.DLMonteOutput.load(ref_dir)

        self.assertTrue(orig.ptfile.allclose(runner.output.ptfile))

        # Test may not produce yaml data at the moment 

        if orig.yamldata is not None:
            self.assertTrue(orig.yamldata.allclose(runner.output.yamldata))

        runner.cleanup()


    def test_gcmc_lj(self):

        """GCMC_LJ PTFILE.000"""

        location = os.path.join(self.tests, "gcmc_lj", "short-abw-2017jan-alpha")
        input_dir = os.path.join(location, "input")
        res_dir = os.path.join(location, "benchmark")

        ensemble = EnsembleMuVT()
        data = DLMonteData(directory=input_dir, results_dir=res_dir)

        self.assertEqual(data.parameter("volume"), 1000.0)
        self.assertEqual(data.parameter("zLJ"), 0.06177)
        self.assertEqual(ensemble, data.ensemble)

        # Observables (a sample)

        self.assertEqual(data.observable("t").data.size, 10)
        times = numpy.array(range(1000, 11000, 1000))
        numpy.testing.assert_allclose(data.observable("t").data, times)

        nmol = [93, 113, 125, 123, 111, 125, 148, 139, 114, 108]
        numpy.testing.assert_allclose(data.observable("natomLJ").data, nmol)

        self.assertRaises(ValueError, data.observable, "e3bd")
        self.assertRaises(ValueError, data.observable, "la")
        self.assertRaises(ValueError, data.observable, "lcos1")

    def tearDown(self):

        self.tests = None
