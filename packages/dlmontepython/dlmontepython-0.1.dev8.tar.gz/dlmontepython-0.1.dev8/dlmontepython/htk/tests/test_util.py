"""Tests for dlmontepython.htk.util"""

import unittest
import numpy

from dlmontepython.htk.util import Label
from dlmontepython.htk.util import Observable

class UtilTestCase(unittest.TestCase):

    """Test classes"""

    def test_label(self):

        """Test Label"""

        lid = "eV"
        name = "Electron Volts"
        unit = "kg m^2 s^{-2}"

        label = Label(lid, name, unit)

        self.assertEqual(label.id, lid)
        self.assertEqual(label.name, name)
        self.assertEqual(label.units, unit)

        repme = "Label(id={!r}, name={!r}, units={!r})".format(lid, name, unit)
        self.assertEqual(repme, str(label))
        self.assertEqual(repme, repr(label))


    def test_observable(self):

        """Test Observable"""

        label = Label("t", "Test obseravble", "units")
        data = numpy.array([0.0, 1.0, 2.0, 3.0])

        obs = Observable(data, label)
        self.assertEqual(obs.id(), "t")
        self.assertEqual(obs.data.size, 4)

        repme = "Observable(label={!r}, data={!r})".format(label, data)
        self.assertEqual(repme, str(obs))
