"""Tests for DL MONTE FED Flavour containers"""

import unittest

import dlmontepython.htk.sources.dlfedflavour as fed

class FEDFlavourTestCase(unittest.TestCase):

    """Test flavoyrs"""

    def test_generic(self):

        """Gen or Generic case"""

        dlstr = "use fed gen"
        flavour = fed.Generic.from_string(dlstr)
        self.assertEqual("use fed generic", str(flavour))

        dlstr = "use fed generic 2"
        flavour = fed.Generic.from_string(dlstr)
        self.assertEqual(2, flavour.nfreq)
        self.assertEqual(dlstr, str(flavour))

        repme = "Generic(nfreq= 2)"
        self.assertEqual(repme, repr(flavour))

        for dlstr in ["useless", "use fred", "use fed general nonsense"]:
            with self.assertRaises(ValueError):
                flavour = fed.Generic.from_string(dlstr)


    def test_phase_switch(self):

        """Phase switch case"""

        # The ps block is quite long:

        nfreq = None
        switchfreq = 1
        initactive = 1
        datafreq = 200
        meltcheck = True
        meltthresh = 10.0
        meltfreq = 1000

        lines = []
        lines.append("use fed ps")
        lines.append("  switchfreq {}".format(switchfreq))
        lines.append("  initactive {}".format(initactive))
        lines.append("  datafreq {}".format(datafreq))
        lines.append("  meltthresh {}".format(meltthresh))
        lines.append("  meltcheck")
        lines.append("  meltfreq {}".format(meltfreq))
        lines.append("ps done")

        dlstr = "\n".join(lines)

        flavour = fed.PhaseSwitch.from_string(dlstr)
        self.assertEqual(switchfreq, flavour.keys["switchfreq"])
        self.assertEqual(meltcheck, flavour.keys["meltcheck"])
        self.assertEqual(meltfreq, flavour.keys["meltfreq"])
        self.assertEqual(meltthresh, flavour.keys["meltthresh"])

        # This test is sensitive to whitespace, so care with the above...
        self.assertEqual(dlstr, str(flavour))

        repme = "nfreq= {!r}, switchfreq= {!r}".format(nfreq, switchfreq)
        repme += ", initactive= {!r}".format(initactive)
        repme += ", datafreq= {!r}".format(datafreq)
        repme += ", meltthresh= {!r}".format(meltthresh)
        repme += ", meltcheck= {!r}".format(meltcheck)
        repme += ", meltfreq= {!r}".format(meltfreq)
        repme = "PhaseSwitch({})".format(repme)

        self.assertEqual(repme, repr(flavour))
