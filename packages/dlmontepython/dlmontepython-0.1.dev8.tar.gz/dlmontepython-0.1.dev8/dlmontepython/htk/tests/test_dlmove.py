"""Tests for dlmove types"""

import unittest

import dlmontepython.htk.sources.dlmove as dlmove


class DLMoveTestCase(unittest.TestCase):

    """Move (synthetic) tests"""

    def test_atom_move(self):

        """move atom ..."""

        dlstr = "move atom 2 20\nAg core\nPt core"

        move = dlmove.AtomMove.from_string(dlstr)
        self.assertEqual(20, move.pfreq)
        self.assertEqual(2, len(move.movers))
        self.assertEqual(dlstr, str(move))

        move = dlmove.from_string(dlstr)
        self.assertIsInstance(move, dlmove.AtomMove)
        self.assertEqual(dlstr, str(move))


    def test_molecule_move(self):

        """move molecule ..."""

        dlstr = "move molecule 1 100\nZeolite"

        move = dlmove.MoleculeMove.from_string(dlstr)
        self.assertEqual(100, move.pfreq)
        self.assertEqual(dlstr, str(move))

        move = dlmove.from_string(dlstr)
        self.assertIsInstance(move, dlmove.MoleculeMove)
        self.assertEqual(dlstr, str(move))


    def test_rotate_molecule_move(self):

        """move rotatemol ..."""

        dlstr = "move rotatemol 1 45\nRotor"

        move = dlmove.RotateMoleculeMove.from_string(dlstr)
        self.assertEqual(45, move.pfreq)
        self.assertEqual(dlstr, str(move))


    def test_swap_atom_move(self):

        """move swapatoms ..."""

        dlstr = "move swapatoms 1 1\nE1 core E2 core"

        move = dlmove.SwapAtomMove.from_string(dlstr)
        self.assertEqual(1, move.pfreq)
        self.assertEqual(dlstr, str(move))


    def test_swap_molecule_move(self):

        """move swapmols..."""

        dlstr = "move swapmols 1 2\nMolA MolB"

        move = dlmove.SwapMoleculeMove.from_string(dlstr)
        self.assertEqual(2, move.pfreq)
        self.assertEqual(dlstr, str(move))


    def test_gcinsertatom_move(self):

        """Grand Canonical..."""

        dlstr = "move gcinsertatom 1 20 0.01\nO core 0.1"

        move = dlmove.InsertAtomMove.from_string(dlstr)
        self.assertEqual(20, move.pfreq)
        self.assertEqual(0.01, move.rmin)
        self.assertEqual(0.1, move.movers[0]["molpot"])
        self.assertEqual(dlstr, str(move))


    def test_volume_vector_move(self):

        """Volume move..."""

        dlstr = "move volume vector 50"

        move = dlmove.VolumeVectorMove.from_string(dlstr)
        self.assertEqual(50, move.pfreq)
        self.assertEqual(dlstr, str(move))

        move = dlmove.from_string(dlstr)
        self.assertIsInstance(move, dlmove.VolumeVectorMove)
        self.assertEqual(dlstr, str(move))


    def test_volume_ortho_move(self):

        """Ortho..."""

        dlstr = "move volume ortho log 99"

        move = dlmove.VolumeOrthoMove.from_string(dlstr)
        self.assertEqual(99, move.pfreq)
        self.assertEqual("log", move.sampling)
        self.assertEqual(dlstr, str(move))

        move = dlmove.from_string(dlstr)
        self.assertIsInstance(move, dlmove.VolumeOrthoMove)
        self.assertEqual(dlstr, str(move))

        repme = "pfreq= {!r}, sampling= {!r}".format(99, "log")
        repme = "VolumeOrthoMove({})".format(repme)
        self.assertEqual(repme, repr(move))


    def test_volume_cubic_move(self):

        """move volume cubic...."""

        dlstr = "move volume cubic linear dim 10"

        move = dlmove.VolumeCubicMove.from_string(dlstr)
        self.assertEqual(10, move.pfreq)
        self.assertEqual("linear dim", move.sampling)
        self.assertEqual(dlstr, str(move))

        move = dlmove.from_string(dlstr)
        self.assertIsInstance(move, dlmove.VolumeCubicMove)
        self.assertEqual(dlstr, str(move))


    def test_wrongs(self):

        """Some poorly formed input"""

        dlstr = "mofe volume vector 1"

        with self.assertRaises(ValueError) as ctxt:
            dlmove.from_string(dlstr)

        msg = str(ctxt.exception)
        self.assertTrue(msg.startswith("Expected: 'move key ...'"))


        dlstr = "move nosuchmove 10 20"

        with self.assertRaises(ValueError) as ctxt:
            dlmove.from_string(dlstr)

        msg = str(ctxt.exception)
        self.assertTrue(msg.startswith("Move unrecognised"))
