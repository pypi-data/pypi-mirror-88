"""Atom and molecular species in DL-MONTE FIELD input

This module contains classes representing atomic and molecular
species in the DL-MONTE input file FIELD. 

These classes are used elsewhere, in particular by the FIELD 
class, which itself is a representation of FIELD input.

"""

from collections import OrderedDict
import numpy as np


class Atom(object):

    """FIELD file Atom entry"""

    def __init__(self, name, atype, x = None, y = None, z = None, mass = None, chg = None, site = None):

        """Initialise container content

        Arguments:
          name (string):                  descriptive name
          atype (string):                 core|shell
          x (float):                      relative position (x coord)
          y (float):                      relative position (y coord)
          z (float):                      relative position (z coord)
          mass (float):                   the particle mass
          charge (float):                 the particle charge
          site (string):                  the symmetry type of atom
        """
        self.name = name
        self.charge = 0.0
        self.mass = 0.0
        self.type = atype
        self.site = " "

        if (x is not None) or (y is not None) or (z is not None):
            self.rpos = np.zeros(3)
        
        if x is not None:
            self.rpos[0] = x
        if y is not None:
            self.rpos[1] = y
        if z is not None:
            self.rpos[2] = z

        if mass is not None:
            self.mass = mass

        if chg is not None:
            self.charge = chg

        if site is not None:
            self.site = site


    def __repr__(self):

        """Return internal representation"""

        atom = "name= {!r}, type= {!r}"\
            .format(self.name, self.type)

        if hasattr(self, "rpos"):
            atom += ", rpos= {!r}".format(self.rpos)

        return "Atom({!s})".format(atom)


    def __str__(self):

        """Return string intended to reproduce DL FIELD file string"""

        atom = "{!s} {!s}".format(self.name, self.type)

        if hasattr(self, "rpos"):
            atom = "{!s} {!s} {!s} {!s}"\
                .format(atom, self.rpos[0], self.rpos[1], self.rpos[2])

        return atom


    def to_dct(self):

        """Return a dict in keeping with DLFIELD style"""

        dct = OrderedDict()
        dct.update({"NAME" : self.name})
        dct.update({"TYPE" : self.type})
        dct.update({"RELPOS" : self.rpos})

        return dct

    def set_name(self, sym = " "):
        self.name = sym

    def set_position(self, x, y, z):
        self.rpos[0] = x
        self.rpos[1] = y
        self.rpos[2] = z

    def set_mass(self, m):
        self.mass = m

    def set_charge(self, c):
        self.charge = c

    def set_site(self, t):
        self.site = t

    def set_type(self, typ):
        self.type = typ

    def get_name(self):
        return self.name

    def get_mass(self):
        return self.mass

    def get_charge(self):
        return self.charge

    def get_site(self):
        return self.site

    def get_type(self):
        return self.type

    def get_position(self):
        """
        Returns the position of the atom
        """

        return self.rpos

    def get_distance(self, v):
        """
        get the vector difference between the two atoms
        """

        d = np.zeros(3)

        d[0] = v[0] - self.rpos[0]
        d[1] = v[1] - self.rpos[1]
        d[2] = v[2] - self.rpos[2]

        return d

    def write_atom_dlpoly(self, out, i = -1):

        out.write(self.name)

        if i == -1:
            out.write("\n")
        else:
            out.write("{:15d}".format(i))
            out.write("\n")

        #line = str(self.posn[0]) + '   ' + str(self.posn[1]) + '   ' + str(self.posn[2])
        out.write("{:15.8f}".format(self.rpos[0]))
        out.write("{:15.8f}".format(self.rpos[1]))
        out.write("{:15.8f}".format(self.rpos[2]))
        out.write("{0}     ".format("   "))
        out.write("{0}     ".format(self.site))
        out.write("\n")

    def write_atom_dlmonte(self, out, i = None):

        out.write("{}  {}".format(self.name, self.type))

        if i is None:
            out.write("\n")
        else:
            out.write("{:15d}".format(i))
            out.write("\n")

        #line = str(self.posn[0]) + '   ' + str(self.posn[1]) + '   ' + str(self.posn[2])
        out.write("{:15.8f}".format(self.rpos[0]))
        out.write("{:15.8f}".format(self.rpos[1]))
        out.write("{:15.8f}".format(self.rpos[2]))
        out.write("{0}     ".format("   "))
        out.write("{0}     ".format(self.site))
        out.write("\n")

    def write_atom_xyz(self, out):

        out.write("{0}     ".format(self.name))
        out.write("{:15.8f}".format(self.rpos[0]))
        out.write("{:15.8f}".format(self.rpos[1]))
        out.write("{:15.8f}".format(self.rpos[2]))
        out.write("\n")

    def write_atom_gen(self, out):

        out.write("{0}     ".format(self.name))
        out.write("{0}     ".format(self.type))
        out.write("{:15.8f}".format(self.rpos[0]))
        out.write("{:15.8f}".format(self.rpos[1]))
        out.write("{:15.8f}".format(self.rpos[2]))
        out.write("{:15.8f}".format(self.mass))
        out.write("{:15.8f}".format(self.charge))
        out.write("{0}     ".format("   "))
        out.write("{0}     ".format(self.site))
        out.write("\n")

    def write_atom_gulp(self, out):

        out.write("{0}     ".format(self.name))
        out.write("{0}     ".format(self.type))
        out.write("{:15.8f}".format(self.rpos[0]))
        out.write("{:15.8f}".format(self.rpos[1]))
        out.write("{:15.8f}".format(self.rpos[2]))
        out.write("{0}     ".format("   "))
        out.write("{0}     ".format(self.site))
        out.write("\n")

class AtomType(object):

    """FIELD file AtomType entry"""

    def __init__(self, name, atype, mass, charge):

        """Initialise content

        Arguments:
          name (string):       descriptive
          atype (string):      ["core"|"shell"|"metal"]
          mass (int/float):    mass
          charge (float):      charge

        Note mass for truly atomic species is generally an integer,
        while can be float. We keep the destinction.
        """

        self.name = name
        self.type = atype
        self.mass = mass
        self.charge = charge


    def __repr__(self):

        """Return internal representation"""

        atom = "name= {!r}, type= {!r}, mass= {!r}, charge= {!r}" \
            .format(self.name, self.type, self.mass, self.charge)
        return "AtomType({!s})".format(atom)


    def __str__(self):

        """Return string for DL FIELD file style output"""

        str1 = "{!s} {!s}".format(self.name, self.type)
        str2 = "{!s} {!s}".format(self.mass, self.charge)
        return "{} {}".format(str1, str2)


    def to_dct(self):

        """Return dict in the DL FIELD style"""

        dct = OrderedDict()
        dct.update({"NAME": self.name})
        dct.update({"TYPE": self.type})
        dct.update({"MASS": self.mass})
        dct.update({"CHARGE": self.charge})

        return dct


    @staticmethod
    def from_string(dlstr):

        """Generate AtomType from string"""

        try:
            name, atype, strmass, charge = dlstr.split()

            # Parse mass as float if a decimal point appears in the string
            if "." in strmass:
                mass = float(strmass)
            else:
                mass = int(strmass)
            charge = float(charge)
            atomtype = AtomType(name, atype, mass, charge)

        except (ValueError, IndexError):
            raise ValueError("Failed to parse atom type: {!r}".format(dlstr))

        return atomtype

class Molecule(object):

    """
    FIELD file Molecule entry. The Molecule type is used in gen-config to manipulate 
    atoms positions, type etc
    """

    def __init__(self, name):

        """Initialise content

        Arguments:
          name       string
        """

        self.name = name
        self.atoms = []

    def add_atom(self, at):
        """
        adds an atom to the molecule
        """
        self.atoms.append(at)

class MolType(object):

    """FIELD file MOLTYPE entry"""

    # Structureless types have only "MAXATOM"
    # Structures have an ATOM list as well

    # Note that the bonds are specfied as an integer triple
    # relating to the order in which atoms and bond types
    # appear in the FIELD file.

    # As both python and json lists maintain order, we can
    # use the same mechanism reliably here provided the
    # file is parsed in the correct order.

    def __init__(self, name, nmaxatom):

        """Initialise content

        Arguments:
          name       string
          nmaxatom   integer  maximum number of atoms allowed in molecule
        """

        self.name = name
        self.nmaxatom = nmaxatom
        self.atoms = []
        self.bonds = []
        self._exc_coul_ints = False
        self._rigid = False

    #get/set exc_coul_ints
    def set_exc_coul_ints(self, exc_coul_ints):

        self._exc_coul_ints = exc_coul_ints

    def get_exc_coul_ints(self):

        return self._exc_coul_ints

    exc_coul_ints = property(get_exc_coul_ints, set_exc_coul_ints)

    #get/set rigid flag
    def set_rigid(self, rigid):

        self._rigid = rigid

    def get_rigid(self):

        return self._rigid

    rigid = property(get_rigid, set_rigid)

    def __repr__(self):

        """Return internal representation"""

        str1 = "name={!r}, nmaxatom={!r}, atoms={!r}, bonds={!r}" \
            .format(self.name, self.nmaxatom, self.atoms, self.bonds)
        str2 = "exc_coul_ints={!r}".format(self.exc_coul_ints)
        str3 = "rigid= {!r}".format(self.rigid)
        return "MolType({!s}, {!s}, {!s})".format(str1, str2, str3)


    def __str__(self):

        """Return string in keeping with the FIELD style"""

        listme = []
        listme.append(str(self.name))

        if not self.atoms:
            listme.append("MAXATOM {!s}".format(self.nmaxatom))
        else:
            atoms = "ATOMS {!s} {!s}".format(len(self.atoms), self.nmaxatom)
            listme.append(atoms)
            for atom in self.atoms:
                listme.append(str(atom))

        if self.bonds:
            listme.append("BONDS {!s}".format(len(self.bonds)))
            for bond in self.bonds:
                listme.append(" ".join(map(str, bond)))

        if self.exc_coul_ints:
            listme.append("EXCLUDE")
        if self.rigid:
            listme.append("RIGID")

        return "\n".join(listme)


    def to_dct(self):

        """Return a dict in keeping with DLFIELD style"""

        dct = OrderedDict()
        atoms = []
        for atom in self.atoms:
            atoms.append(atom.to_dct())

        dct.update({"NAME" : self.name})
        dct.update({"MAXATOM" : self.nmaxatom})
        dct.update({"ATOMS" : atoms})
        dct.update({"BONDS" : self.bonds})

        dct.update({"EXCLUDE": self.exc_coul_ints})
        dct.update({"RIGID": self.rigid})

        return dct
