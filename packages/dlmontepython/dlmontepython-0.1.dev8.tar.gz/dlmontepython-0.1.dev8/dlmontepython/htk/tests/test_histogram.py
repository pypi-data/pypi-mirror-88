"""Test histogram reweighting basics"""

# Shut up pylint "no-member" errors arising from numpy, Parameter
# pylint: disable=E1101

import unittest
import numpy
import numpy.testing

from dlmontepython.htk.util import Label
from dlmontepython.htk.util import Observable

import dlmontepython.htk.histogram as hist
from dlmontepython.htk.histogram import BetaReweighter
from dlmontepython.htk.histogram import KTReweighter
from dlmontepython.htk.parameter import Parameter

class TestBoltzmannWeights(unittest.TestCase):

    """The Boltzmann weights"""

    def test_weights(self):

        """Basic weights"""

        e = numpy.exp(1.0)
        obs = numpy.array([0.0, 1.0])

        weights = hist.boltzmann_weights(0.0, 0.0, 0.0, obs)
        numpy.testing.assert_allclose(weights, [1.0, 1.0])

        weights = hist.boltzmann_weights(1.0, 0.0, 0.0, obs)
        numpy.testing.assert_allclose(weights, [1.0, 1.0])

        weights = hist.boltzmann_weights(1.0, 1.0, 1.0, obs)
        numpy.testing.assert_allclose(weights, [1.0, 1.0])

        weights = hist.boltzmann_weights(1.0, 2.0, 1.0, obs)
        numpy.testing.assert_allclose(weights, [1.0, e])

        weights = hist.boltzmann_weights(1.0, 1.0, 2.0, obs)
        numpy.testing.assert_allclose(weights, [1.0, 1.0/e])

        weights = hist.boltzmann_weights(-1.0, 2.0, 1.0, obs)
        numpy.testing.assert_allclose(weights, [1.0, 1.0/e])


    def test_reweighting(self):

        """Reweighting factors"""

        action = numpy.array([0.0, 1.0])
        obs = numpy.array([-1.0, 2.0])

        sobs = numpy.sum(obs)

        rewght = hist.boltzmann_reweight_obs(obs, 1.0, 0.0, 0.0, action)
        self.assertEqual(rewght, sobs/2.0)


    def test_large_obsevations(self):

        """Large exponents via obsevations"""

        action1 = numpy.array([800.0, 800.0])
        action2 = numpy.array([0.0, 1.0])
        obs = numpy.array([-1.0, 2.0])

        sobs = numpy.sum(obs)

        reweight = hist.boltzmann_reweight_obs(obs, 1.0, 1.0, 0.0, action1)
        self.assertEqual(reweight, sobs/2.0)

        reweight = hist.boltzmann_reweight_obs(obs, -1.0, 1.0, 0.0, action1)
        self.assertEqual(reweight, sobs/2.0)


        action = action1[:] + action2[:]
        wgts = hist.boltzmann_weights(-1.0, 1.0, 0.0, action2)
        test = numpy.sum(obs[:]*wgts[:])/numpy.sum(wgts[:])

        rewtd = hist.boltzmann_reweight_obs(obs, -1.0, 1.0, 0.0, action)
        self.assertEqual(rewtd, test)

        wgts = hist.boltzmann_weights(1.0, 1.0, 0.0, action2)
        test = numpy.sum(obs[:]*wgts[:])/numpy.sum(wgts[:])

        rewght = hist.boltzmann_reweight_obs(obs, 1.0, 1.0, 0.0, action)
        self.assertEqual(rewght, test)


    def test_large_constant_factors(self):

        """Large exponents via constant factor"""

        action = numpy.array([-1.0, 0.0, 1.0])
        obs = numpy.array([1.0, 1.0, 1.0])

        rewght = hist.boltzmann_reweight_obs(obs, 800.0, 1.0, 0.0, action)
        self.assertEqual(rewght, 1.0)
        rewght = hist.boltzmann_reweight_obs(obs, -800.0, 1.0, 0.0, action)
        self.assertEqual(rewght, 1.0)


class BetaReweighterTestCase(unittest.TestCase):

    """Beta reweighter tests"""

    def setUp(self):

        """Set up a reweighter"""

        self.alpha = -1.0
        self.b_old = 0.52
        self.sobs = numpy.array([0.0, 1.0, 2.0, 3.0, 4.0])

        alpha = Parameter(self.alpha, Label("a", "Get sign right!", None))
        beta = Parameter(self.b_old, Label("beta", "1/k_bT", "1/E"))
        action = Observable(self.sobs, Label("E", "Energy", "E"))

        self.reweighter = BetaReweighter("Beta", beta, alpha, action)


    def test_rewighter(self):

        """BetaReweighter"""

        rewghter = self.reweighter

        self.assertEqual("Beta", rewghter.name)
        self.assertEqual("beta", rewghter.rid())
        self.assertEqual(self.alpha, rewghter.alpha)
        self.assertEqual(self.b_old, rewghter.b_old)
        numpy.testing.assert_allclose(self.sobs, rewghter.sobs.data)

        rstr = "name= {!r}, beta_old= {!r}, alpha= {!r}, sobs= {}"\
            .format("Beta", rewghter.b_old, rewghter.alpha, rewghter.sobs)
        rstr = "BetaReweighter({})".format(rstr)

        self.assertEqual(rstr, str(rewghter))
        #self.assertEqual(rep, repr(rewghter))


    def test_reweighter_weights(self):

        """BetaReweighter weights"""

        b_new = 0.42

        weights = hist.boltzmann_weights(self.alpha, self.b_old, b_new,
                                         self.sobs)
        test = numpy.exp(self.alpha*(self.b_old - b_new)*self.sobs[:])

        numpy.testing.assert_allclose(weights, test)

        weights = self.reweighter.compute_weights(b_new)
        numpy.testing.assert_allclose(weights, test)


    def test_reweighter_reweighting(self):

        """BetaReweighter reweighting"""

        alpha = self.alpha
        b_old = self.b_old
        b_new = -0.1

        # used for obs and action
        obs = self.sobs

        test = hist.boltzmann_reweight_obs(obs, alpha, b_old, b_new, obs)

        rwght = self.reweighter.reweight_obs(obs, b_new)
        self.assertEqual(rwght, test)

        b_newarray = numpy.array([b_new, 2.0*b_new])
        rwght = self.reweighter.reweight_obs(obs, b_newarray)

        test = numpy.zeros(2)
        test[0] = hist.boltzmann_reweight_obs(obs, alpha, b_old, b_new, obs)
        test[1] = hist.boltzmann_reweight_obs(obs, alpha, b_old, 2.0*b_new, obs)

        numpy.testing.assert_allclose(rwght, test)


class KTReweighterTestCase(unittest.TestCase):

    """KTReweighter tests"""

    def setUp(self):

        self.alpha = -1.0
        self.kt_old = 2.0
        self.sobs = numpy.array([2.0, 3.0, 4.0, 5.0, 6.0])

        alpha = Parameter(self.alpha, Label("a", "constant", None))
        beta = Parameter(self.kt_old, Label("kt", "Temp", "K"))
        action = Observable(self.sobs, Label("E", "Energy", "E"))

        self.reweighter = KTReweighter("kT", beta, alpha, action)


    def test_rewwighter(self):

        """KTReweighter class"""

        reweighter = self.reweighter

        self.assertEqual(reweighter.name, "kT")
        self.assertEqual(reweighter.alpha, self.alpha)
        self.assertEqual(reweighter.b_old, 1.0/self.kt_old)

        self.assertEqual(reweighter.rid(), "kt")

        strme = "KTReweighter(name={!r}, kt_old={!r}, alpha={!r}, sobs={})" \
            .format(reweighter.name, reweighter.kt_old,
                    reweighter.alpha, reweighter.sobs)

        self.assertEqual(strme, str(reweighter))
        #self.assertEqual(strme, repr(reweighter))


    def test_reweighter_weights(self):

        """KT weights"""

        kt_new = 1.5

        b_old = 1.0/self.kt_old
        b_new = 1.0/kt_new

        weights = hist.boltzmann_weights(self.alpha, b_old, b_new, self.sobs)
        test = numpy.exp(self.alpha*(b_old - b_new)*self.sobs[:])
        numpy.testing.assert_allclose(weights, test)

        weights = self.reweighter.compute_weights(kt_new)
        numpy.testing.assert_allclose(weights, test)
