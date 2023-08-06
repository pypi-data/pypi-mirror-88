"""DL Interaction Class tests"""

import unittest

import dlmontepython.htk.sources.dlinteraction as dli

class InteractionTestCase(unittest.TestCase):

    """Unit tests for DL Interaction descriptions"""

    def test_lj(self):

        """Lennard Jones"""

        epsilon, sigma = (2.0, 1.0)
        dlstr = "lj {!s} {!s}".format(epsilon, sigma)

        lj = dli.InteractionLJ(epsilon, sigma)
        self.assertEqual(epsilon, lj.epsilon)
        self.assertEqual(sigma, lj.sigma)

        me = "Interaction(key={!r}, type={!r}, epsilon={!r}, sigma={!r})" \
            .format("lj", "Lennard-Jones", epsilon, sigma)
        self.assertEqual(me, repr(lj))
        self.assertEqual(dlstr, str(lj))

        flj = dli.from_string(dlstr)
        self.assertEqual(epsilon, flj.epsilon)
        self.assertEqual(sigma, flj.sigma)


    def test_nm(self):

        """Lennard Jones NM"""

        e0, n, m, r0 = (1.0, 2, 3, 4.0)
        dlstr = "nm {!s} {!s} {!s} {!s}".format(e0, n, m, r0)

        nm = dli.InteractionNM(e0, n, m, r0)
        self.assertEqual(e0, nm.e0)
        self.assertEqual(n, nm.n)
        self.assertEqual(m, nm.m)
        self.assertEqual(r0, nm.r0)

        me = "Interaction(key={!r}, type={!r}, e0={}, n={}, m={}, r0={})" \
            .format("nm", "Lennard Jones General N-M", e0, n, m, r0)
        self.assertEqual(me, repr(nm))
        self.assertEqual(dlstr, str(nm))

        fnm = dli.from_string(dlstr)
        self.assertEqual(e0, fnm.e0)
        self.assertEqual(n, fnm.n)
        self.assertEqual(m, fnm.m)
        self.assertEqual(r0, fnm.r0)


    def test_12_6(self):

        """General 12-6"""

        a, b = (1.0, 2.0)
        dlstr = "12-6 {!s} {!s}".format(a, b)

        six12 = dli.Interaction12_6(a, b)
        self.assertEqual(a, six12.a)
        self.assertEqual(b, six12.b)

        me = "Interaction(key={!r}, type={!r}, a={}, b={})" \
            .format("12-6", "Lennard-Jones-like 12-6", a, b)
        self.assertEqual(me, repr(six12))
        self.assertEqual(dlstr, str(six12))

        fsix12 = dli.from_string(dlstr)
        self.assertEqual(a, fsix12.a)
        self.assertEqual(b, fsix12.b)


    def test_buckingham(self):

        """Buckingham"""

        a, rho, c = (1.0, 2.0, 3.0)
        dlstr = "buck {!s} {!s} {!s}".format(a, rho, c)

        buck = dli.InteractionBuckingham(a, rho, c)
        self.assertEqual(a, buck.a)
        self.assertEqual(rho, buck.rho)
        self.assertEqual(c, buck.c)

        me = "Interaction(key={!r}, type={!r}, a={}, rho={}, c={})" \
            .format("buck", "Buckingham", a, rho, c)
        self.assertEqual(me, repr(buck))
        self.assertEqual(dlstr, str(buck))

        fbuck = dli.from_string(dlstr)
        self.assertEqual(a, fbuck.a)
        self.assertEqual(rho, fbuck.rho)
        self.assertEqual(c, fbuck.c)

        self.assertRaises(ValueError, dli.InteractionBuckingham.from_string,
                          "buck")


    def test_hard_sphere(self):

        """Hard spheres"""

        sigma = 2.0
        dlstr = "hs {}".format(sigma)

        hs = dli.InteractionHS(sigma)
        self.assertEqual(sigma, hs.sigma)

        me = "Interaction(key={!r}, type={!r}, sigma={})" \
            .format("hs", "Hard Sphere", sigma)
        self.assertEqual(me, repr(hs))
        self.assertEqual(dlstr, str(hs))

        fhs = dli.from_string(dlstr)
        self.assertEqual(sigma, fhs.sigma)

        self.assertRaises(ValueError, dli.InteractionHS.from_string, "hs")
