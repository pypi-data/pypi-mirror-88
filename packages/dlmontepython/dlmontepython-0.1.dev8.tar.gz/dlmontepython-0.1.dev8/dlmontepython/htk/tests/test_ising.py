"""Test for Ising model code"""

import unittest
import os
import numpy

import dlmontepython.htk.histogram
from dlmontepython.htk.sources.ising import IsingModel
from dlmontepython.htk.sources.isingdata import IsingModelData

class IsingModelTestCase(unittest.TestCase):

    """IsingiModel tests"""

    def setUp(self):

        """Temperature unity"""

        self.kT = 1.0

    def test_ising_init(self):

        """Initialisations"""

        self.ising_init(8, 1.0, 0.5, 3)
        self.ising_init(16, 0.1, 0.0, 3)
        self.ising_init(32, 0.0, 0.1, 5)


    def test_ising_energies(self):

        """Energies"""

        self.ising_uniform_energy(1.0, 0.0)
        self.ising_uniform_energy(0.0, 1.0)
        self.ising_uniform_energy(1.0, 1.0)


    def ising_init(self, nlen, j, h, seed):

        """Test an initialisation"""

        model = IsingModel(nlen, j, h, self.kT, seed)
        self.assertEqual(model.nlen, nlen)
        self.assertEqual(model.seed, seed)
        self.assertEqual(model.j, j)
        self.assertEqual(model.h, h)

        self.assertEqual(numpy.sum(model.s), 0)
        self.assertEqual(numpy.sum(model.s[model.s == -1]), -nlen*nlen/2)
        self.assertEqual(numpy.sum(model.s[model.s == +1]), +nlen*nlen/2)


    def ising_uniform_energy(self, j, h):

        """
        For a system of uniform spin (s0 = +/-1), check the energies
        are coorect
        """

        nlen = 8
        seed = 3

        model = IsingModel(nlen, j, h, self.kT, seed)
        s0 = +1
        model.s[:, :] = s0
        [s, m] = model.observables()

        self.assertEqual(s, 2.0)
        self.assertEqual(m, s0)

        s0 = -1
        model.s[:, :] = s0
        [s, m] = model.observables()
        self.assertEqual(s, 2.0)
        self.assertEqual(m, s0)

        # Flip one spin: S changes by 2x4/V ; M changes by 2x1/V
        model.s[0, 0] = -s0
        [s, m] = model.observables()
        rv = 1.0/nlen**2
        self.assertEqual(s, 2.0*(1.0 - 4.0*rv))
        self.assertEqual(m, s0*(1.0 - 2.0*rv))


class IsingModelDataTestCase(unittest.TestCase):

    """Test IsingModel obsevable data"""

    def setUp(self):

        """Store a small data set to file"""

        self.model = IsingModel(4, 1.0, 2.0, 2.1, 37)
        self.filename = "ising_test.dat"
        self.model.run(100, file=self.filename)

        self.data = IsingModelData(filename=self.filename)


    def test_ising_data(self):

        """Create Obsevable data"""

        data = IsingModelData(filename=self.filename)
        t = data.to_table()
        self.assertIsInstance(t, str)


    def test_ising_parameters(self):

        """Check obsevable parameters"""

        data = self.data

        nspin = data.parameter("N")
        self.assertEqual(nspin, self.model.nlen**2)
        self.assertEqual(nspin.label.units, None)

        volume = data.parameter("V")
        self.assertEqual(volume, 1.0*self.model.nlen**2)
        self.assertEqual(volume.label.name, "Volume")

        temperature = data.parameter("kT")
        self.assertEqual(temperature, self.model.kT)
        self.assertEqual(temperature.label.name, "Temperature")

        param = data.parameter("J")
        self.assertEqual(param, self.model.j)
        field = data.parameter("H")
        self.assertEqual(field, self.model.h)


    def test_ising_observables(self):

        """Check observable data"""

        data = self.data

        obs = data.observable("t")
        self.assertEqual(obs.label.name, "Time")
        self.assertEqual(obs.data[-1], 100.0)

        obs = data.observable("m")
        self.assertEqual(obs.label.name, "Magnetisation")

        obs = data.observable("e")
        self.assertEqual(obs.data[-1], -4.0)


    def test_ising_reweighters(self):

        """Check reweighter initialistion"""

        data = self.data

        reweighter = data.reweighter("beta")
        self.assertIsInstance(reweighter, dlmontepython.htk.histogram.BetaReweighter)


    def tearDown(self):

        """Clear up the temporary file"""

        os.remove(self.filename)

