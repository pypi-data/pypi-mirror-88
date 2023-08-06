"""Tests for FEDMethod classes"""

import unittest

import dlmontepython.htk.sources.dlfedmethod as fed

class FEDMethodTestCase(unittest.TestCase):

    """FED methods (synthetic) tests"""

    def test_bias_smoother(self):

        """BiasSmoother utility"""

        n_itr, i_beg, i_end, omega = 1, 2, 3, 0.4

        bias = fed.BiasSmoother(n_itr, i_beg, i_end, omega)
        self.assertEqual(n_itr, bias.n_itr)
        self.assertEqual(i_beg, bias.i_beg)
        self.assertEqual(i_end, bias.i_end)
        self.assertEqual(omega, bias.omega)

        strme = "{} {} {} {}".format(n_itr, i_beg, i_end, omega)
        self.assertEqual(strme, str(bias))
        strme = "n_itr= {}, i_beg= {}, i_end= {}, omega= {}"\
            .format(n_itr, i_beg, i_end, omega)
        reprme = "BiasSmoother({!s})".format(strme)
        self.assertEqual(reprme, repr(bias))


    def test_umbrella_sampling(self):

        """fed method us ..."""

        x0, kf, n_upd = 1.0, 2.0, 10
        dlstr = "us {} {} {}".format(x0, kf, n_upd)

        umbrella = fed.UmbrellaSampling(x0, kf, n_upd)
        self.assertEqual(x0, umbrella.x0)
        self.assertEqual(kf, umbrella.kf)
        self.assertEqual(n_upd, umbrella.n_upd)

        reprme = "x0= {!r}, kf= {!r}, n_upd= {!r}".format(x0, kf, n_upd)
        reprme = "UmbrellaSampling({!s})".format(reprme)
        self.assertEqual(reprme, repr(umbrella))

        umbrella = fed.UmbrellaSampling.from_string(dlstr)
        self.assertEqual(x0, umbrella.x0)
        self.assertEqual(kf, umbrella.kf)
        self.assertEqual(n_upd, umbrella.n_upd)

        dlstr = "fed method us {} {} {}".format(x0, kf, n_upd)
        umbrella = fed.from_string(dlstr)
        self.assertEqual(dlstr, str(umbrella))


    def test_expanded_ensemble(self):

        """fed method ee ..."""

        eta0, c_upd, n_upd = 0.5, 2.0, 10
        dlstr = "ee {} {} {}".format(eta0, c_upd, n_upd)

        expand = fed.ExpandedEnsemble(eta0, c_upd, n_upd)
        self.assertEqual(eta0, expand.eta0)
        self.assertEqual(c_upd, expand.c_upd)
        self.assertEqual(n_upd, expand.n_upd)
        self.assertEqual(None, expand.smooth)

        reprme = "eta0= {!r}, c_upd= {!r}, n_upd= {!r}, smooth= {!r}"\
            .format(eta0, c_upd, n_upd, None)
        reprme = "ExpandedEnsemble({!s})".format(reprme)
        self.assertEqual(reprme, repr(expand))

        expand = fed.ExpandedEnsemble.from_string(dlstr)
        self.assertEqual(eta0, expand.eta0)
        self.assertEqual(c_upd, expand.c_upd)
        self.assertEqual(n_upd, expand.n_upd)

        dlstr = "fed method ee {} {} {}".format(eta0, c_upd, n_upd)
        expand = fed.from_string(dlstr)
        self.assertEqual(dlstr, str(expand))


    def test_wang_landau(self):

        """fed method wl ..."""

        delta0, c_upd, n_upd = 0.5, 0.9, 11
        dlstr = "wl {} {} {}".format(delta0, c_upd, n_upd)

        wang = fed.WangLandau(delta0, c_upd, n_upd)
        self.assertEqual(delta0, wang.delta0)
        self.assertEqual(c_upd, wang.c_upd)
        self.assertEqual(n_upd, wang.n_upd)
        self.assertEqual(None, wang.smooth)

        reprme = "delta0= {!r}, c_upd= {!r}, n_upd= {!r}, smooth= {!r}"\
            .format(delta0, c_upd, n_upd, None)
        reprme = "WangLandau({!s})".format(reprme)
        self.assertEqual(reprme, repr(wang))

        wang = fed.WangLandau.from_string(dlstr)
        self.assertEqual(delta0, wang.delta0)
        self.assertEqual(c_upd, wang.c_upd)
        self.assertEqual(n_upd, wang.n_upd)

        dlstr = "fed method wl {} {} {}".format(delta0, c_upd, n_upd)
        wang = fed.from_string(dlstr)
        self.assertEqual(dlstr, str(wang))

        # Optional smoother

        n_itr, i_beg, i_end, omega = 1, 2, 3, 0.4
        smooth = fed.BiasSmoother(n_itr, i_beg, i_end, omega)
        dlstr = "{!s} {!s}".format(dlstr, smooth)
        wang = fed.from_string(dlstr)
        self.assertEqual(dlstr, str(wang))


    def test_transition_matrix(self):

        """fed method tm ..."""

        nout, n_upd = 1, 2
        dlstr = "tm {} {}".format(nout, n_upd)

        tmatrix = fed.TransitionMatrix(nout, n_upd)
        self.assertEqual(nout, tmatrix.nout)
        self.assertEqual(n_upd, tmatrix.n_upd)
        self.assertEqual("new", tmatrix.mode)

        reprme = "nout= {!r}, n_upd= {!r}, mode= {!r}, tri= {!r}"\
            .format(nout, n_upd, "new", False)
        reprme = "TransitionMatrix({!s})".format(reprme)
        self.assertEqual(reprme, repr(tmatrix))

        tmatrix = fed.TransitionMatrix.from_string(dlstr)
        self.assertEqual(nout, tmatrix.nout)
        self.assertEqual(n_upd, tmatrix.n_upd)

        mode = "resume"
        dlstr = "fed method tm {} {} {}".format(nout, n_upd, mode)
        tmatrix = fed.from_string(dlstr)
        self.assertEqual(dlstr, str(tmatrix))
