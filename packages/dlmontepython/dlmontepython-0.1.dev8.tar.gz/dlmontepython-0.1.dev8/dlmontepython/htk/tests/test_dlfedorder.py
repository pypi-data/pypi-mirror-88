"""Tests for FEDOrderParameter continaer"""

import unittest

import dlmontepython.htk.sources.dlfedorder as order

class FEDOrderParameterTestCase(unittest.TestCase):

    """FED Order parameter (synthetic) tests"""

    def test_volume(self):

        """fed order parameter volume"""

        name, ngrid, xmin, xmax = "volume", 2, 3.0, 4.0

        dlstr = "fed order {} {} {} {}".format(name, ngrid, xmin, xmax)

        param = order.from_string(dlstr)
        self.assertEqual(name, param.name)
        self.assertEqual(ngrid, param.ngrid)
        self.assertEqual(xmin, param.xmin)
        self.assertEqual(xmax, param.xmax)
        # 'npow' is an optional parameter which should default to 1
        self.assertEqual(1, param.npow)

        repme = "name= {!r}, ngrid= {!r}, xmin= {!r}, xmax= {!r}, npow= {!r}"\
            .format(name, ngrid, xmin, xmax, 1)
        repme = "FEDOrderParameter({})".format(repme)

        self.assertEqual(repme, repr(param))



    def test_temp(self):

        """fed order parameter temp"""

        name, ngrid, xmin, xmax = "temp", 3, 4.0, 5.0
        dlstr = "fed order param {} {} {} {}".format(name, ngrid, xmin, xmax)

        param = order.from_string(dlstr)
        self.assertEqual(name, param.name)
        self.assertEqual(dlstr, str(param))


    def test_beta(self):

        """fed order parameter beta"""

        name, ngrid, xmin, xmax, npow = "beta", 4, 5.0, 6.0, 7
        dlstr = "fed order param {} {} {} {} {}"\
            .format(name, ngrid, xmin, xmax, npow)

        param = order.from_string(dlstr)
        self.assertEqual(name, param.name)
        self.assertEqual(npow, param.npow)
        self.assertEqual(dlstr, str(param))


    def test_psmc(self):

        """fed order parameter ps[mc]"""

        name, ngrid, xmin, xmax = "ps", 5, 6.0, 7.0

        param = order.FEDOrderParameter(name, ngrid, xmin, xmax)
        self.assertEqual(name, param.name)

        param = order.FEDOrderParameter("psmc", 5, 6, 7)
        self.assertEqual("psmc", param.name)


    def test_hardps(self):

        """fed order parameter hardps"""

        name, ngrid, xmin, xmax = "hardps", 10, 11.0, 12.0
        dlstr = "fed order param {} {} {} {}".format(name, ngrid, xmin, xmax)

        param = order.from_string(dlstr)
        self.assertEqual(dlstr, str(param))


    def test_com2(self):

        """fed order param com2"""

        # This is more complex; the parsing of com1, com2 is pending

        lines = []
        lines.append("fed order param com2 -1 0.0 1.0")
        lines.append("  com1 molecule  1 atoms 2 5 .. 8 10 12 .. 14 19")
        lines.append("  com2 molecules 3 .. 7")
        lines.append("com sampling correction 1")
        lines.append("fed order param done")
        dlstr = "\n".join(lines)

        param = order.OrderCentreOfMass2.from_string(dlstr)
        self.assertEqual("com2", param.name)

        param = order.from_string(dlstr)
        self.assertEqual("com2", param.name)
        self.assertEqual(1, param.ncorrect)


    def test_exceptions(self):

        """Common mistakes should raise an exception"""

        wrongs = []
        wrongs.append("fed odor")
        wrongs.append("fed order param cm2")
        wrongs.append("fed order param beta a b c")
        wrongs.append("fed order param beta 1.0 2.0 3.0") # bad int() format

        for dlstr in wrongs:
            with self.assertRaises(ValueError):
                order.from_string(dlstr)
