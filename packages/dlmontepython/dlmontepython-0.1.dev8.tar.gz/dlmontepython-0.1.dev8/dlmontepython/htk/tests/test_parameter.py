"""Test ParameterInt and ParameterFloat"""

import unittest

import dlmontepython.htk.parameter
from dlmontepython.htk.parameter import ParameterInt
from dlmontepython.htk.parameter import ParameterFloat

class ParameterTestCase(unittest.TestCase):

    """Test dlmontepython.htk.parameter"""

    def test_parameter_int(self):

        """ParameterInt"""

        a = ParameterInt(1, "One")
        self.assertEqual(a, 1)
        self.assertEqual(a.label, "One")

        repme = "ParameterInt(value= {!s}, label= {!r})".format(int(a), a.label)
        self.assertEqual(repr(a), repme)

        b = dlmontepython.htk.parameter.Parameter(2, "Two")
        self.assertIsInstance(b, ParameterInt)
        self.assertEqual(b, 2)
        self.assertEqual(b.label, "Two")


    def test_parameter_float(self):

        """ParameterFloat"""

        a = ParameterFloat(1.0, "One")
        self.assertEqual(a, 1.0)
        self.assertEqual(a.label, "One")

        repme = "ParameterFloat(value= {!s}, label= {!r})".format(float(a), a.label)
        self.assertEqual(repr(a), repme)

        b = dlmontepython.htk.parameter.Parameter(2.0, "Two")
        self.assertIsInstance(b, ParameterFloat)
        self.assertEqual(b, 2.0)
        self.assertEqual(b.label, "Two")
