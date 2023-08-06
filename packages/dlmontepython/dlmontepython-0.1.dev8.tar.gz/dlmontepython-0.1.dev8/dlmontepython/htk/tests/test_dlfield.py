"""Tests for FIELD object

Real test cases are taken from the DL_MONTE test suite,
the location of which is obtained from the environment 
variable DLM_TEST_SUITE. Hence this environment variable 
must be set before the tests here can be used.
"""

import os.path
import unittest
import numpy as np

import dlmontepython.htk.sources.dlfield
from dlmontepython.htk.sources.dlfieldspecies import Atom
from dlmontepython.htk.sources.dlfieldspecies import AtomType
from dlmontepython.htk.sources.dlfield import BondTwoBody
from dlmontepython.htk.sources.dlfieldspecies import MolType

class AtomTypeTestCase(unittest.TestCase):

    """AtomType synthetic test"""

    def test_atomtype(self):

        """Simple atom type"""

        name = "Test"
        atype = "core"
        mass = 1.0
        charge = 2.0

        atomtype = AtomType(name, atype, mass, charge)

        self.assertEqual(atomtype.name, name)
        self.assertEqual(atomtype.type, atype)
        self.assertEqual(atomtype.mass, mass)
        self.assertEqual(atomtype.charge, charge)

        dct = atomtype.to_dct()
        self.assertEqual(dct["NAME"], name)
        self.assertEqual(dct["TYPE"], atype)
        self.assertEqual(dct["MASS"], mass)
        self.assertEqual(dct["CHARGE"], charge)

        strme = "{} {} {} {}".format(name, atype, mass, charge)
        self.assertEqual(str(atomtype), strme)

        repme = "name= {!r}, type= {!r}, mass= {!r}, charge= {!r}"\
            .format(name, atype, mass, charge)
        repme = "AtomType({!s})".format(repme)
        self.assertEqual(repr(atomtype), repme)


    def test_atomtype_atomic(self):

        """With integer mass"""

        dlstr = "H Hydrogen 1 1.0"

        atomtype = AtomType.from_string(dlstr)
        self.assertEqual(atomtype.name, "H")
        self.assertEqual(atomtype.type, "Hydrogen")
        self.assertEqual(atomtype.mass, 1)
        self.assertEqual(atomtype.charge, 1.0)


    def test_atomtype_bad(self):

        """Test exception"""

        dlstr = "Rubbish"

        with self.assertRaises(ValueError) as ctxt:
            AtomType.from_string(dlstr)

        msg = str(ctxt.exception)
        self.assertTrue(msg.startswith("Failed to parse atom type:"))


class AtomTestCase(unittest.TestCase):

    """Atom class synthetic tests"""

    def test_atom(self):

        """No position"""

        name = "Testatom"
        core = "core"

        atom = Atom(name, core)
        self.assertEqual(atom.name, name)
        self.assertEqual(atom.type, core)

        strme = "{!s} {!s}".format(name, core)
        self.assertEqual(str(atom), strme)

        repme = "name= {!r}, type= {!r}".format(name, core)
        repme = "Atom({!s})".format(repme)
        self.assertEqual(repr(atom), repme)


    def test_atom_with_pos(self):

        """With position"""

        name = "Li"
        core = "shell"
        rpos = np.asarray([1.0, 2.0, 3.0])
        atom = Atom(name, core, rpos[0], rpos[1], rpos[2])
        self.assertEqual(atom.rpos.tolist(), rpos.tolist())

        dct = atom.to_dct()
        self.assertEqual(dct["NAME"], name)
        self.assertEqual(dct["TYPE"], core)
        self.assertEqual(dct["RELPOS"].tolist(), rpos.tolist())

        strme = "{} {} {} {} {}".format(name, core, rpos[0], rpos[1], rpos[2])
        self.assertEqual(str(atom), strme)


class MoltypeTestCase(unittest.TestCase):

    """Moltype synthetic test"""

    def test_moltype(self):

        """Moltype synthetic test"""

        ref_name = "Test"
        ref_nmaxatom = 1

        obj = MolType(ref_name, ref_nmaxatom)
        self.assertEqual(obj.name, ref_name)
        self.assertEqual(obj.nmaxatom, ref_nmaxatom)

        dct = obj.to_dct()
        self.assertEqual(dct["NAME"], ref_name)
        self.assertEqual(dct["MAXATOM"], ref_nmaxatom)
        self.assertEqual(dct["ATOMS"], [])


class BondTwoBodyTestCase(unittest.TestCase):

    """BondTwoBody synthetic test"""

    def test_bond2body(self):

        """No interaction specified"""

        atom1 = Atom("A", "core")
        atom2 = Atom("B", "shell")

        bond = BondTwoBody(atom1, atom2, None)

        self.assertEqual(bond.atom1.name, "A")
        self.assertEqual(bond.atom2.name, "B")
        self.assertEqual(bond.atom1.type, "core")
        self.assertEqual(bond.atom2.type, "shell")

        self.assertEqual(str(bond), "A core B shell None")

        repme = "atom1= {!r}, atom2= {!r}, interaction= {!r}"\
            .format(atom1, atom2, None)
        repme = "BondTwoBody({!s})".format(repme)

        self.assertEqual(repr(bond), repme)


    def test_from_string(self):

        """A core B shell lj 2.0 3.0"""

        dlstr = "A core B shell lj 2.0 3.0"""

        bond = BondTwoBody.from_string(dlstr)

        self.assertEqual(bond.atom1.name, "A")
        self.assertEqual(bond.atom2.name, "B")
        self.assertEqual(bond.atom1.type, "core")
        self.assertEqual(bond.atom2.type, "shell")

        ljones = dlmontepython.htk.sources.dlinteraction.Interaction
        self.assertIsInstance(bond.interaction, ljones)
        self.assertEqual(bond.interaction.epsilon, 2.0)
        self.assertEqual(bond.interaction.sigma, 3.0)


    def test_wrong(self):

        """Check exceptions"""

        dlstr = "Bond not present"

        with self.assertRaises(ValueError) as ctxt:
            BondTwoBody.from_string(dlstr)

        msg = str(ctxt.exception)
        self.assertTrue(msg.startswith("Cannot parse bond:"))


class RegressionFIELDTestCase(unittest.TestCase):

    """FIELD files from the regression test directories"""

    def setUp(self):

        """Get path to DL_MONTE test directory from environment 
        variable DLM_TEST_SUITE"""

        self.tests = os.getenv("DLM_TEST_SUITE")


    def test_gcmc_lj(self):

        """GCMC_LJ"""

        test = os.path.join(self.tests, "gcmc_lj", "short-abw-2017jan-alpha", "input")
        filename = os.path.join(test, "FIELD")

        self.assertTrue(os.path.exists(filename))

        dlfield = dlmontepython.htk.sources.dlfield.from_file(filename)

        self.assertEqual(dlfield.description[0:13], "Lennard-Jones")
        self.assertEqual(dlfield.units, "eV".lower())
        self.assertEqual(dlfield.nconfigs, 1)
        self.assertEqual(dlfield.cutoff, 2.5)

        self.assertEqual(len(dlfield.atomtypes), 1)
        self.assertEqual(len(dlfield.moltypes), 1)
        self.assertEqual(len(dlfield.vdw), 1)

        # AtomType
        atom = dlfield.atomtypes[0]

        self.assertEqual(atom.name, "LJ")
        self.assertEqual(atom.type, "core")
        self.assertEqual(atom.mass, 1.0)
        self.assertEqual(atom.charge, 0.0)

        # MolType
        mol = dlfield.moltypes[0]

        self.assertEqual(mol.name, "lj")
        self.assertEqual(mol.nmaxatom, 1)

        self.assertEqual(len(mol.atoms), 1)
        self.assertEqual(mol.atoms[0].name, "LJ")
        self.assertEqual(mol.atoms[0].type, "core")
        self.assertEqual(mol.atoms[0].rpos.tolist(), [0.0, 0.0, 0.0])

        # vdw
        vdw = dlfield.vdw[0]
        ljones = vdw.interaction

        self.assertEqual(vdw.atom1.name, "LJ")
        self.assertEqual(vdw.atom1.type, "core")
        self.assertEqual(vdw.atom2.name, "LJ")
        self.assertEqual(vdw.atom2.type, "core")
        self.assertEqual(ljones.epsilon, 1.0)
        self.assertEqual(ljones.sigma, 1.0)

        original = dlmontepython.htk.sources.dlutil.load_ascii(filename)
        processed = list(str(dlfield).split("\n"))
        self.assertListEqual(original, processed)


    def test_gcmc_c02_zeolite(self):

        """GCMC_CO2_ZEOLITE regression test FIELD file"""

        test = os.path.join(self.tests, "gcmc_co2_zeolite")
        filename = os.path.join(test, "FIELD")

        self.assertTrue(os.path.exists(filename))

        dlfield = dlmontepython.htk.sources.dlfield.from_file(filename)

        # Check the bond indices in the CO2 molecule

        mol = dlfield.moltypes[1]
        self.assertEqual(len(mol.bonds), 3)
        self.assertEqual(mol.bonds[0], [1, 2, 1])
        self.assertEqual(mol.bonds[1], [1, 3, 1])
        self.assertEqual(mol.bonds[2], [2, 3, 2])

        # Check the 12-6 has come through

        vdw = dlfield.vdw
        self.assertEqual(len(vdw), 6)
        self.assertEqual(vdw[5].atom1.name, "O_C")
        self.assertEqual(vdw[5].atom2.name, "Xe")
        self.assertEqual(vdw[5].interaction.key, "12-6")
        self.assertEqual(vdw[5].interaction.a, 16777216.0)
        self.assertEqual(vdw[5].interaction.b, 0.0)

        # Check that the bond descriptions are correct

        bonds = dlfield.bonds2body
        self.assertEqual(len(bonds), 2)
        self.assertEqual(bonds[0].atom1.name, "C_")
        self.assertEqual(bonds[0].atom2.name, "O_C")
        self.assertEqual(bonds[0].interaction.key, "buck")
        self.assertEqual(bonds[0].interaction.a, 0.0)
        self.assertEqual(bonds[0].interaction.rho, 0.1)
        self.assertEqual(bonds[0].interaction.c, 0.0)

        self.assertEqual(bonds[1].atom1.name, "O_C")
        self.assertEqual(bonds[1].atom2.name, "O_C")

        original = dlmontepython.htk.sources.dlutil.load_ascii(filename)
        processed = list(str(dlfield).split("\n"))

        # It's hard to get floating point format right, but at least...
        self.assertEqual(len(original), len(processed))


    def test_psmc_hs_nvt(self):

        """PSMC hard sphere FIELD file"""

        filename = os.path.join(self.tests, "psmc_hs_nvt", "FIELD")
        self.assertTrue(os.path.exists(filename))

        field = dlmontepython.htk.sources.dlfield.from_file(filename)

        # A subset of pertinant features...
        self.assertEqual(field.cutoff, 1.1)
        self.assertEqual(field.units, "internal")
        self.assertEqual(field.nconfigs, 2)
        self.assertEqual(field.moltypes[0].nmaxatom, 216)
        self.assertEqual(field.vdw[0].interaction.sigma, 1.0)


    def test_water_spce_nist(self):

        """Water SPCE NIST"""

        filename = os.path.join(self.tests, "nist_spce_water", "FIELD")
        self.assertTrue(os.path.exists(filename))

        field = dlmontepython.htk.sources.dlfield.from_file(filename)

        self.assertEqual(field.cutoff, 10.0)
        self.assertEqual(field.atomtypes[0].name, "OW")
        self.assertEqual(field.atomtypes[0].mass, 16.0)
        self.assertEqual(field.atomtypes[0].charge, -0.8476)

        self.assertEqual(field.moltypes[0].exc_coul_ints, True)


    def test_ewald_nacl_atm(self):

        """Ewald NaCl atom"""

        filename = os.path.join(self.tests, "ewald_nacl_atm", "FIELD")
        self.assertTrue(os.path.exists(filename))

        field = dlmontepython.htk.sources.dlfield.from_file(filename)

        self.assertEqual(field.atomtypes[1].name, "Cl")
        self.assertEqual(field.atomtypes[1].charge, -2.0)
        self.assertEqual(field.moltypes[0].nmaxatom, 8)


    def tearDown(self):

        """Finish"""

        self.tests = None
