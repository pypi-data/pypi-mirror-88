"""Tests for dlunits module"""

# Shut up pylint "no-member" errors arising from Parameter
# pylint: disable=E1101

import unittest

import dlmontepython.htk.sources.dlunits

class DLUnitsTestCase(unittest.TestCase):

    """Units"""

    def test_constants(self):

        """Electronic charge, etc"""

        qe_si = dlmontepython.htk.sources.dlunits.QE_SI
        na_si = dlmontepython.htk.sources.dlunits.NA_SI
        kb_si = dlmontepython.htk.sources.dlunits.KB_SI

        self.assertEqual(qe_si, 1.602176e-19)
        self.assertEqual(qe_si.label.units, "Coulomb")

        self.assertEqual(kb_si, 1.3806488e-23)
        self.assertEqual(kb_si.label.units, "Joules per Kelvin")

        self.assertEqual(na_si, 6.02214e+23)
        self.assertEqual(na_si.label.units, "per mole")


    def test_k_boltzmann(self):

        """Boltzmann constant in various DL units"""

        qe_si = dlmontepython.htk.sources.dlunits.QE_SI
        na_si = dlmontepython.htk.sources.dlunits.NA_SI
        kb_si = dlmontepython.htk.sources.dlunits.KB_SI

        kb_ev = dlmontepython.htk.sources.dlunits.k_boltzmann("ev")
        self.assertEqual(kb_ev.label.units, "eV per Kelvin")
        self.assertEqual(kb_ev, kb_si*(1.0/qe_si))

        kb_kcal = dlmontepython.htk.sources.dlunits.k_boltzmann("kcal")
        self.assertEqual(kb_kcal.label.units, "kCal per mole per Kelvin")
        self.assertEqual(kb_kcal, (1.0/4184.0)*kb_si*na_si)

        kb_kj = dlmontepython.htk.sources.dlunits.k_boltzmann("kJ")
        self.assertEqual(kb_kj.label.units, "kJoules per mole per Kelvin")
        self.assertEqual(kb_kj, (1.0/1000.0)*kb_si*na_si)

        kb_int = dlmontepython.htk.sources.dlunits.k_boltzmann("internal")
        self.assertEqual(kb_int.label.units, "10 Joules per mole per Kelvin")
        self.assertEqual(kb_int, (1.0/10.0)*kb_si*na_si)

        # "k" same as "internal"
        kb_k = dlmontepython.htk.sources.dlunits.k_boltzmann("K")
        self.assertEqual(kb_k.label.units, "10 Joules per mole per Kelvin")
        self.assertEqual(kb_k, (1.0/10.0)*kb_si*na_si)
