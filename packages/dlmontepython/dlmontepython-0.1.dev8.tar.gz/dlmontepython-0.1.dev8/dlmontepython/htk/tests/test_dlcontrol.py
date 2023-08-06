"""Check we can read and parse all the Regression Test CONTROL files

Real test cases are taken from the DL_MONTE test suite,
the location of which is obtained from the environment 
variable DLM_TEST_SUITE. Hence this environment variable 
must be set before the tests here can be used.
"""

import os
import unittest

import dlmontepython.htk.sources.dlcontrol as dlcontrol
import dlmontepython.htk.sources.dlmove as dlmove
import dlmontepython.htk.sources.dlfedflavour as flavour
import dlmontepython.htk.sources.dlfedmethod as method
import dlmontepython.htk.sources.dlfedorder as order


class FEDBlockTestCase(unittest.TestCase):

    """FEDBlock is a component of the UseBlock"""

    def test_fed_block_generic(self):

        """use fed generic..."""

        lines = []
        lines.append("use fed generic")
        lines.append("fed method tm 200 20 new")
        lines.append("fed order param beta 1 2.0 3.0")
        lines.append("fed done")
        dlstr = "\n".join(lines)

        fed = dlcontrol.FEDBlock.from_string(dlstr)
        self.assertIsInstance(fed.flavour, flavour.Generic)
        self.assertIsInstance(fed.method, method.TransitionMatrix)
        self.assertIsInstance(fed.orderparam, order.FEDOrderParameter)

        self.assertEqual(str(fed), dlstr)

        repme = "FEDBlock(flavour= {!r}, method= {!r}, orderparam= {!r})"\
            .format(fed.flavour, fed.method, fed.orderparam)
        self.assertEqual(repme, repr(fed))


class ControlUseBlockTestCase(unittest.TestCase):

    """Synthetic control block"""

    def test_control(self):

        """Test use statement plus fed block"""

        lines = []
        lines.append("use gaspressure")
        lines.append("use fed generic")
        lines.append("  fed method tm 200 20")
        lines.append("  fed order param beta 1 2.0 3.0")
        lines.append("fed done")
        lines.append("finish use-block")
        dlstr = "\n".join(lines)

        block = dlcontrol.UseBlock.from_string(dlstr)
        self.assertIn("gaspressure", block.use_statements)
        self.assertEqual(1, len(block.use_statements))
        self.assertNotIn("fed", block.use_statements)


class ControlMainBlockTestCase(unittest.TestCase):

    """MainBlock (somewhat) artificial test cases"""

    def test_main_block_statements(self):

        """Test some statements"""

        lines = []
        lines.append("seeds 12 23 37 47")
        lines.append("nbrlist auto")
        lines.append("start simulation")
        dlstr = "\n".join(lines)

        block = dlcontrol.MainBlock.from_string(dlstr)
        self.assertEqual(2, len(block.statements))
        self.assertEqual("auto", block.statements["nbrlist"])
        self.assertEqual(47, block.statements["seeds"]["seed3"])


    def test_main_block_bad(self):

        """Incomplete main block"""

        dlstr = "no such statement"

        with self.assertRaises(ValueError) as ctxt:
            dlcontrol.MainBlock.from_string(dlstr)

        msg = str(ctxt.exception)
        self.assertTrue(msg.startswith("MainBlock: unrecognised"))


    def test_main_block_move_atom(self):

        """An atom move"""

        lines = []
        lines.append("move atom 1 99")
        lines.append("hs core")
        lines.append("start simulation")
        dlstr = "\n".join(lines)

        block = dlcontrol.MainBlock.from_string(dlstr)

        self.assertEqual(1, len(block.moves))
        self.assertIsInstance(block.moves[0], dlmove.AtomMove)


    def test_main_block_move_mol(self):

        """A molecule move"""

        lines = []
        lines.append("move molecule 1 20")
        lines.append("c02")
        lines.append("start simulation")
        dlstr = "\n".join(lines)

        block = dlcontrol.MainBlock.from_string(dlstr)

        self.assertEqual(1, len(block.moves))
        self.assertIsInstance(block.moves[0], dlmove.MoleculeMove)


    def test_main_block_move_rot(self):

        """A rotation"""

        lines = []
        lines.append("move rotatemol 3 70")
        lines.append(" molx")
        lines.append(" moly")
        lines.append(" molz")
        lines.append("start simulation")
        dlstr = "\n".join(lines)

        block = dlcontrol.MainBlock.from_string(dlstr)

        self.assertEqual(1, len(block.moves))
        self.assertIsInstance(block.moves[0], dlmove.RotateMoleculeMove)


    def test_main_block_move_gcmc(self):

        """A grand canonical move with chemical potential"""

        lines = []
        lines.append("move gcinsertmol 1 60 0.5")
        lines.append("co2 0.1")
        lines.append("start")
        dlstr = "\n".join(lines)

        block = dlcontrol.MainBlock.from_string(dlstr)
        self.assertEqual(1, len(block.moves))

        move = block.moves[0]
        self.assertIsInstance(move, dlmove.InsertMoleculeMove)
        self.assertEqual(move.pfreq, 60)
        self.assertEqual(move.rmin, 0.5)

        self.assertEqual(1, len(move.movers))
        self.assertEqual(move.movers[0]["id"], "co2")
        self.assertEqual(move.movers[0]["molpot"], 0.1)


class ControlInputTestCase(unittest.TestCase):

    """ControlInput artificial test cases"""

    def test_control_input(self):

        """A minimal CONTROL input"""

        title = "A title"
        use_str = "finish use-block"
        main_str = "start simulation"
        dlstr = "{}\n{}\n{}".format(title, use_str, main_str)

        ctrl = dlcontrol.CONTROL.from_string(dlstr)
        self.assertEqual(title, ctrl.title)
        self.assertEqual({}, ctrl.use_block.use_statements)
        self.assertEqual(None, ctrl.use_block.fed_block)

        # MainBlock present but no content
        self.assertEqual({}, ctrl.main_block.statements)
        self.assertEqual([], ctrl.main_block.moves)
        self.assertEqual({}, ctrl.main_block.samples)

        with self.assertRaises(ValueError) as ctxt:
            dlstr = "{}\n{}".format(title, use_str)
            ctrl = dlcontrol.CONTROL.from_string(dlstr)

        msg = str(ctxt.exception)
        self.assertEqual(msg, "ControlInput: no 'start' statement")

        with self.assertRaises(ValueError) as ctxt:
            dlstr = "{}\n{}".format(title, main_str)
            ctrl = dlcontrol.CONTROL.from_string(dlstr)

        msg = str(ctxt.exception)
        self.assertEqual(msg, "ControlInput: no 'finish [use-block]'")

        # Note that a lack of title will cause the first use statement
        # (or the "finish" to be interpreted as the title.
        # This is almost certainly an error, but not sure what main
        # code does with this.



class RegressionCONTROLTestCase(unittest.TestCase):

    """Tests based on real test input files"""

    def setUp(self):

        """Get path to DL_MONTE test directory from environment 
        variable DLM_TEST_SUITE"""

        self.tests = os.getenv("DLM_TEST_SUITE")


    def test_fed_lj(self):

        """FED LJ CONTROL"""

        filename = os.path.join(self.tests, "fed_lj", "CONTROL")
        self.assertTrue(os.path.exists(filename))

        ctrl = dlcontrol.from_file(filename)

        keys = ctrl.main_block.statements
        self.assertEqual(keys["check"], 1000000)

        self.assertEqual(2, len(ctrl.main_block.samples))

        sample = ctrl.main_block.samples["rdfs"]
        self.assertEqual(sample["ngrid"], 300)
        self.assertEqual(sample["rcut"], 30.0)
        self.assertEqual(sample["nfreq"], 10)

        sample = ctrl.main_block.samples["coords"]
        self.assertEqual(sample["nfreq"], 10000)

        repexch = ctrl.use_block.use_statements["repexch"]
        self.assertEqual(repexch["nr"], 4)
        self.assertEqual(repexch["deltat"], -0.2)
        self.assertEqual(repexch["nstep"], 500)

        fed = ctrl.use_block.fed_block
        self.assertIsInstance(fed.flavour, flavour.Generic)

        self.assertIsInstance(fed.method, method.WangLandau)
        self.assertEqual(fed.method.delta0, 0.002)
        self.assertEqual(fed.method.c_upd, 0.5)
        self.assertEqual(fed.method.n_upd, 500000)

        self.assertIsInstance(fed.orderparam, order.OrderCentreOfMass2)
        self.assertEqual(fed.orderparam.ngrid, 250)


    def test_gcmc_co2_zeolite(self):

        """GCMC CO2 Zeolite CONTROL file"""

        filename = os.path.join(self.tests, "gcmc_co2_zeolite", "CONTROL")
        self.assertTrue(os.path.exists(filename))

        ctrl = dlcontrol.from_file(filename)

        # Check quantities not exmained elsewhere...

        self.assertIn("gaspressure", ctrl.use_block.use_statements)

        keys = ctrl.main_block.statements

        self.assertEqual(keys["temperature"], 273.0)
        self.assertEqual(keys["acceptmolmoveupdate"], 200)
        self.assertEqual(keys["acceptmolrotupdate"], 200)
        self.assertEqual(keys["steps"], 100000)
        self.assertEqual(keys["maxmolrot"], 0.005)

        self.assertEqual(3, len(ctrl.main_block.moves))

        move = ctrl.main_block.moves[0]
        self.assertIsInstance(move, dlmove.MoleculeMove)
        self.assertEqual(move.pfreq, 20)
        self.assertEqual(1, len(move.movers))
        self.assertEqual(move.movers[0]["id"], "co2")

        move = ctrl.main_block.moves[1]
        self.assertIsInstance(move, dlmove.RotateMoleculeMove)
        self.assertEqual(move.pfreq, 20)
        self.assertEqual(1, len(move.movers))
        self.assertEqual(move.movers[0]["id"], "co2")

        move = ctrl.main_block.moves[2]
        self.assertIsInstance(move, dlmove.InsertMoleculeMove)
        self.assertEqual(move.pfreq, 60)
        self.assertEqual(move.rmin, 0.5)
        self.assertEqual(1, len(move.movers))
        self.assertEqual(move.movers[0]["id"], "co2")
        self.assertEqual(move.movers[0]["molpot"], 0.0001)


    def test_gcmc_lj(self):

        """GCMC_LJ CONTROL file"""

        filename = os.path.join(self.tests, "gcmc_lj", "short-abw-2017jan-alpha", "input", "CONTROL")
        self.assertTrue(os.path.exists(filename))

        ctrl = dlcontrol.from_file(filename)

        keys = ctrl.main_block.statements
        self.assertEqual(keys["seeds"]["seed0"], 12)
        self.assertEqual(keys["seeds"]["seed1"], 34)
        self.assertEqual(keys["seeds"]["seed2"], 56)
        self.assertEqual(keys["seeds"]["seed3"], 78)
        self.assertEqual(keys["temperature"], 13754.88)
        self.assertEqual(keys["steps"], 10000)
        self.assertEqual(keys["equilibration"], 100000)
        self.assertEqual(keys["print"], 1000)
        self.assertEqual(keys["stack"], 1000)
        self.assertEqual(keys["revconformat"], "dlpoly")

        self.assertEqual(1, len(ctrl.main_block.moves))

        move = ctrl.main_block.moves[0]
        self.assertIsInstance(move, dlmove.InsertMoleculeMove)
        self.assertEqual(move.pfreq, 100)
        self.assertEqual(move.rmin, 0.7)

        self.assertEqual(1, len(move.movers))
        self.assertEqual(move.movers[0]["id"], "lj")
        self.assertEqual(move.movers[0]["molpot"], 0.06177)



    def test_psmc_hs_nvt(self):

        """PSMC Hard Sphere NVT CONTROL file"""

        filename = os.path.join(self.tests, "psmc_hs_nvt", "CONTROL")
        self.assertTrue(os.path.exists(filename))

        ctrl = dlcontrol.from_file(filename)
        fed = ctrl.use_block.fed_block

        # Check PSMC stuff
        self.assertIsInstance(fed.flavour, flavour.PhaseSwitch)

        self.assertEqual(fed.flavour.keys["switchfreq"], 4)
        self.assertEqual(fed.flavour.keys["initactive"], 1)
        self.assertEqual(fed.flavour.keys["meltcheck"], True)
        self.assertEqual(fed.flavour.keys["meltthresh"], 10.0)
        self.assertEqual(fed.flavour.keys["meltfreq"], 10000)

        self.assertEqual(fed.orderparam.ngrid, 220)
        self.assertEqual(fed.orderparam.xmin, -110.0)
        self.assertEqual(fed.orderparam.xmax, +110.0)
        self.assertEqual(fed.orderparam.npow, -1)


    def test_psmc_hs_npt(self):

        """PSMC Hard Sphere NPT CONTROL file"""

        filename = os.path.join(self.tests, "psmc_hs_npt", "CONTROL")
        self.assertTrue(os.path.exists(filename))

        ctrl = dlcontrol.from_file(filename)

        fed = ctrl.use_block.fed_block
        self.assertEqual(fed.orderparam.ngrid, 200)
        self.assertEqual(fed.orderparam.xmin, -100.0)
        self.assertEqual(fed.orderparam.xmax, +100.0)
        self.assertEqual(fed.orderparam.npow, -1)

        keys = ctrl.main_block.statements
        self.assertEqual(keys["pressure"], 1.98667591093546)


    def test_psmc_lj_npt(self):

        """PSMC LJ NPT CONTROL"""

        filename = os.path.join(self.tests, "psmc_lj_npt", "CONTROL")
        self.assertTrue(os.path.exists(filename))

        ctrl = dlcontrol.from_file(filename)
        fed = ctrl.use_block.fed_block

        self.assertIsInstance(fed.method, method.TransitionMatrix)
        self.assertIsInstance(fed.flavour, flavour.PhaseSwitch)

        self.assertEqual(fed.orderparam.ngrid, 100)
        self.assertEqual(fed.orderparam.xmin, -22.0)
        self.assertEqual(fed.orderparam.xmax, +22.0)
        self.assertEqual(fed.orderparam.npow, 1)

        keys = ctrl.main_block.statements
        self.assertEqual(keys["seeds"]["seed0"], 12)


    def test_psmc_sync_ewald(self):

        """PSMC sync Ewald CONTROL"""

        filename = os.path.join(self.tests, "psmc_sync_ewald_atm", "CONTROL")
        self.assertTrue(os.path.exists(filename))

        ctrl = dlcontrol.from_file(filename)

        keys = ctrl.main_block.statements
        self.assertEqual(keys["ewald sum"]["alpha"], 0.31748)
        self.assertEqual(keys["ewald sum"]["kmax1"], 3)
        self.assertEqual(keys["ewald sum"]["kmax2"], 3)
        self.assertEqual(keys["ewald sum"]["kmax3"], 3)
        self.assertEqual(keys["toler"], 1.0e+100)


    def test_water_spce_nist(self):

        """Water SPCE NIST"""

        filename = os.path.join(self.tests, "nist_spce_water", "CONTROL")
        self.assertTrue(os.path.exists(filename))

        ctrl = dlcontrol.from_file(filename)

        keys = ctrl.main_block.statements
        self.assertEqual(keys["ewald sum"]["alpha"], 0.28)
        self.assertEqual(keys["ewald sum"]["kmax1"], 5)


    def test_ewald_nacl_atm(self):

        """Ewald NaCl atomic"""

        filename = os.path.join(self.tests, "ewald_nacl_atm", "CONTROL")
        self.assertTrue(os.path.exists(filename))

        ctrl = dlcontrol.from_file(filename)
        keys = ctrl.main_block.statements

        self.assertEqual(keys["ewald precision"], 1.0e-20)


    def tearDown(self):

        """Just finish"""

        self.tests = None
