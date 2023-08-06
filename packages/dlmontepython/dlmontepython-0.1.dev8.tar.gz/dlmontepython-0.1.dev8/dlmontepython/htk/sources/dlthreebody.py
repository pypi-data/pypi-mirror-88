"""DL-MONTE Three body and Angle descriptions

In a similar style to the Interaction types, ThreeBody and Angles are merely to identify and to hold the parameters
associated with the different types of non-bonded and bonded three body interactions

No computation takes place.
"""

from collections import OrderedDict

import dlmontepython.htk.sources.dlfieldspecies as dlfieldspecies
#TU: Used in patch to resolve clash in module- and class-level 'from_string' function names - see nelow
import sys

class THB(object):

    """A three body non-bonded interaction"""

    def __init__(self, atomj, atomi, atomk, interaction):

        """Initialise description

        Arguments:
          atomj (dlfieldspecies.Atom):                at one end
          atomi (dlfieldspecies.Atom):                at the center of the triplet
          atomk (dlfieldspecies.Atom):                at the other end
          interaction (THBInteration):  DLInteraction description
        """

        self.atomj = atomj
        self.atomi = atomi
        self.atomk = atomk
        self.interaction = interaction


    def __repr__(self):

        """Return internal representation"""

        tb = "atomj={!r}, atomi={!r}, atomi={!r}, interaction={!r}" \
            .format(self.atomj, self.atomi, self.atomk, self.interaction)

        return "TBP({!s})".format(tb)


    def __str__(self):

        """Return form appropriate for DL FIELD file"""

        atomj = "{!s} {!s}".format(self.atomj.name, self.atomj.type)
        atomi = "{!s} {!s}".format(self.atomi.name, self.atomi.type)
        atomk = "{!s} {!s}".format(self.atomk.name, self.atomk.type)
        return "{!s} {!s} {!s} {!s}".format(atomj, atomi, atomk, self.interaction)

    def __thb_to_dlpoly(self):
        """ convert the Vdw potential to a formattted string"""
        line = str(self)
        line.replace('core', '')

        return line

    def to_dct(self):

        """Translate to dict in keeping with FIELD style"""

        dct = OrderedDict()
        # Could use the dlfieldspecies.AtomType object here, but don't replicate mass etc
        # at the moment
        atj = self.atomj
        ati = self.atomi
        atk = self.atomk

        dct.update({"ATOMJ" : atj.name})
        dct.update({"TYPEJ" : atj.type})
        dct.update({"ATOMI" : ati.name})
        dct.update({"TYPEI" : ati.type})
        dct.update({"ATOMK" : atk.name})
        dct.update({"TYPEK" : atk.type})
        dct.update({"INTERACTION" : self.interaction.to_dct()})

        return dct

    @staticmethod
    def from_string(dlstr, types = True):

        """Return instance from FIELD file string"""

        try:

            if types == True:
                # Split off the interaction key string
                atstrj, typej, atstri, typei, atstrk, typek, key = dlstr.split(None, 6)
            else:
                atstrj, atstri, atstrk, key = dlstr.split(None, 3)
                typei = "core" 
                typej = "core"  
                typek = "core"

        except ValueError:
            raise ValueError("Could not parse VDW: {!r}".format(dlstr))

        atj = dlfieldspecies.Atom(atstrj, typej)
        ati = dlfieldspecies.Atom(atstri, typei)
        atk = dlfieldspecies.Atom(atstrk, typek)

        #TU: Use the 'from_string' function at the module level: the stuff in
        #TU: parenthesis refers to this module. This surely could be cleaner though?        
        interaction = (sys.modules[__name__]).from_string(key)

        thb = THB(atj, ati, atk, interaction)

        return thb

class THBInteraction(object):

    """The interaction abstract class, or interface for bonded three body

    Attributes:
      key (string): each concrete class has a key which identifies
      it in the DL-MONTE FIELD file format, e.g., "harm" for harmonic
    """

    def to_dct(self):

        """Implemented by child classes"""

        raise NotImplementedError()

    @classmethod
    def from_string(cls, dlstr):

        """Implmented by child classes as factory method"""

        raise NotImplementedError()


class THBHarm(THBInteraction):

    """Standard Harmonic (bonded or non-bonded)

    U(r) = 1/2 * k (theta - theta_0)^2
    """

    key = "harm"

    def __init__(self, spring, theta, rij_max, rik_max, rjk_max):

        """
        Arguemnts:
          spring  (float): the spring constant
          theta   (float): the ideal angle
          rij_max (float): the maximum allowed distance between particles i and j
          rik_max (float): as above except for particles i and k
          rjk_max (float): as above except for particles j and k
        """

        self.key = THBHarm.key
        self.type = "harm"
        self.spring = spring
        self.theta = theta
        self.rij_max = rij_max
        self.rik_max = rik_max
        self.rjk_max = rjk_max

    def __str__(self):

        """Return (sub-) string relevant for DL FIELD file"""
        str1 = "{!s} {!s} {!s}".format(self.key, self.spring, self.theta)
        str2 = "{!s} {!s} {!s}".format(self.rij_max, self.rik_max, self.rjk_max)
        return str1 + " " + str2


    def __repr__(self):

        """Return internal representation"""

        rep = "key={!r}, type={!r}, spring constant={!r}, theta zero={!r}, rij_max={!r}, rik_max={!r}, rjk_max={!r}" \
            .format(self.key, self.type, self.spring, self.theta, self.rij_max, self.rik_max, self.rjk_max)
        return "Angle({!s})".format(rep)


    def to_dct(self):

        """Construct and return a dictionary description"""

        dct = OrderedDict()
        dct.update({"KEY" : self.key})
        dct.update({"SPRING" : self.spring})
        dct.update({"THETA" : self.theta})
        dct.update({"RIJMAX" : self.rij_max})
        dct.update({"RIKMAX" : self.rik_max})
        dct.update({"RJKMAX" : self.rjk_max})

        return dct


    @classmethod
    def from_string(cls, dlstr):

        """Generate and return an object from DL-MONTE style string

        Arguments:
          dlstr (string): description

        Example:
        TODO

        """

        try:
            name, spring, theta, rij_max, rik_max, rjk_max = dlstr.split()
            if name.lower() != cls.key:
                raise ValueError()

        except ValueError:
            raise ValueError("Require `harm k theta_0 rij rik rjk` not {!r}".format(dlstr))

        spring = float(spring)
        theta = float(theta)
        rij_max = float(rij_max)
        rik_max = float(rik_max)
        rjk_max = float(rjk_max)

        return cls(spring, theta, rij_max, rik_max, rjk_max)

class THBScreenedHarmonic(THBInteraction):

    """Standard Harmonic (bonded or non-bonded)

    U(r) = 1/2 * k (theta - theta_0)^2 * exp(-(r_ij / rho1 + r_ik / rho2))
    """

    key = "shrm"

    def __init__(self, spring, theta, rho1, rho2, rij_max = 0.0, rik_max = 0.0, rjk_max = 0.0):

        """
        Arguemnts:
          spring  (float): the spring constant
          theta   (float): the ideal angle
          rho1    (float): value of rho1
          rho2    (float): value of rho2
          rij_max (float): the maximum allowed distance between particles i and j
          rik_max (float): as above except for particles i and k
          rjk_max (float): as above except for particles j and k
        """

        self.key = THBScreenedHarmonic.key
        self.type = "shrm"
        self.spring = spring
        self.theta = theta
        self.rho1 = rho1
        self.rho2 = rho2
        self.rij_max = rij_max
        self.rik_max = rik_max
        self.rjk_max = rjk_max

    def __str__(self):

        """Return (sub-) string relevant for DL FIELD file"""
        str1 = "{!s} {!s} {!s} {!s} {!s}".format(self.key, self.spring, self.theta, self.rho1, self.rho2)
        str2 = "{!s} {!s} {!s}".format(self.rij_max, self.rik_max, self.rjk_max)
        return str1 + " " + str2


    def __repr__(self):

        """Return internal representation"""

        rep = "key={!r}, type={!r}, spring constant={!r}, theta zero={!r}, rho1={!r}, rho2={!r}, rij_max={!r}, rik_max={!r}, rjk_max={!r}" \
            .format(self.key, self.type, self.spring, self.theta, self.rho1, self.rho2, self.rij_max, self.rik_max, self.rjk_max)
        return "Angle({!s})".format(rep)


    def to_dct(self):

        """Construct and return a dictionary description"""

        dct = OrderedDict()
        dct.update({"KEY" : self.key})
        dct.update({"SPRING" : self.spring})
        dct.update({"THETA" : self.theta})
        dct.update({"RHO1" : self.rho1})
        dct.update({"RHO2" : self.rho2})
        dct.update({"RIJMAX" : self.rij_max})
        dct.update({"RIKMAX" : self.rik_max})
        dct.update({"RJKMAX" : self.rjk_max})

        return dct


    @classmethod
    def from_string(cls, dlstr):

        """Generate and return an object from DL-MONTE style string

        Arguments:
          dlstr (string): description

        Example:
        TODO

        """

        words = dlstr.split()

        name = words[0].lower()
        spring = words[1]
        theta = words[2]
        rho1 = words[3]
        rho2 = words[4]
        rij_max = 0.0
        rik_max = 0.0
        rjk_max = 0.0
        
        if len(words) == 8:

            rij_max = words[5]
            rik_max = words[6]
            rjk_max = words[7]

        else:
            ValueError("Require `shrm k theta_0 rho1 rho2 rij rik rjk` not {!r}".format(dlstr))

        if name.lower() != cls.key:
            ValueError("Require `shrm k theta_0 rho1 rho2 rij rik rjk` not {!r}".format(dlstr))

        #except ValueError:
        #    raise ValueError("Require `harm k theta_0 rho1 rho2 rij rik rjk` not {!r}".format(dlstr))

        spring = float(spring)
        theta = float(theta)
        rho1 = float(rho1)
        rho2 = float(rho2)
        rij_max = float(rij_max)
        rik_max = float(rik_max)
        rjk_max = float(rjk_max)

        return cls(spring, theta, rho1, rho2, rij_max, rik_max, rjk_max)

def from_string(dlstr):

    """Factory method taking the string as appearing in FIELD input"""

    input_key = dlstr.split()[0].lower()

    for subcls in THBInteraction.__subclasses__():
        if subcls.key == input_key:
            return subcls.from_string(dlstr)

    raise ValueError("No THB interaction available for {!r}".format(str))
