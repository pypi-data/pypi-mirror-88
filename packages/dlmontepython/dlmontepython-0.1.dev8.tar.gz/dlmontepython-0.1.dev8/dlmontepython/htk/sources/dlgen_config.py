# -*- coding: utf-8 -*-
"""
The generic configuration object. This should only contain actions on the 
atoms/positions. This config is different from CONFIG in dlconfig.py as it
stores the positions/vectors as floats etc. This allows for converting atom
and or molecule types etc.

The coordinates should be stored within cartesian frame

Created on Tue Aug 19 16:30:57 2014

@author: john
"""

import numpy as np
from numpy import linalg

import dlmontepython.htk.sources.dlfieldspecies as dlfieldspecies
from dlmontepython.htk.sources.dlcell import Cell as unitcell

class GenConfig (object):
    
    def __init__(self):
        
        self.title = 'untitled config'
        self.levcfg = 0
        self.pbc = 3
        self.natoms = 0
        self.vectors = np.zeros((3,3))
        self.data = []
        self.nummols = {}
        #self.molnames = []

    def reset_config(self):

        self.title = 'untitled config'
        self.levcfg = 0
        self.pbc = 3
        self.natoms = 0
        self.vectors = np.zeros((3,3))
        del self.data [:]

    #returns the number of atoms in a list to controling program
    def get_number_of_atoms(self):
        return self.natoms
        
    def get_atom(self, i):

        return self.data[i]

    def reset_number_of_atoms(self):
        self.natoms = len(self.data)
    
    #calculates volume assuming an orthorhombic cell
    def get_volume(self):
        a = self.vectors[0]
        b = self.vectors[1]
        c = self.vectors[2]

        return np.dot(a, np.cross(b, c))
        
    def create_config(self, c, title = ' '):
        """
        generate the configuration from a unit cell

        @param    c   The unit cell from which the configuration is created
        @param    title    Optional title for configuration
        """
        if isinstance(c, unitcell) == False:
            
            print ('create_config routine is expecting a Cell type')
            return 

        if len(self.data) > 0:

            print ("you can only use create config once")
            return

        self.title = title

        self.vectors = c.latvec

        self.natoms = len(c.data)

        if self.natoms == 0:
            print ('the unit cell contains no atoms') 
            return

        else:

            #the unit cell is fractional from cell so convert
            mol = dlfieldspecies.Molecule(c.name)
            mol.atoms = c.data
            self.data.append(mol)
            self.fractional_to_cartesian()
            self.nummols[mol.name] = 1
    
    def add_molecule(self, mol):
        """
        Adds a molecule to the list of data
        @param  mol An instance of the dlfieldspecies.Molecule
        """
        self.data.append(mol)
        self.natoms = self.natoms + len(mol.atoms)

        try:    #this molecule name is in the dictionary
            num = self.nummols[mol.name]
            num += 1
            self.nummols[mol.name] = num

        except: #need to add to the list
            num = 1
            self.nummols[mol.name] = num

    def set_maxnumber_molecule(self, typ, num):

        #this molecule name is in the dictionary
        self.nummols[typ] = num

        ##except: #need to add to the list
        ##    self.nummols[typ] = num

    #create a copy of the config
    def copy_config(self, c):
        
        c.title = self.title
        c.levcfg = self.levcfg
        c.pbc = self.pbc
        c.natoms = self.natoms

        c.nummols[:] = self.nummols[:]
        
        np.copyto(c.vectors, self.vectors)
        
        for i in range(self.data):

            mol = self.data[i]

            c.data.append(mol)

    def expand_config(self, nx, ny, nz):
        """
        grow the configuration in x y and z

        @param nx    expand the cell n times in the x direction
        @param ny    expand the cell in the y direction
        @param nz    expand the cell in the z direction
        """

        if nx < 1 or ny < 1 or nz < 1:
            print ("expansion coffcicients must be >= 1")
            return

        self.cartesian_to_fractional()

        pos = np.zeros(3)
        posnew = np.zeros(3)

        #make a cop of the data
        tmp = []
        tmp[:] = self.data[:]

        #clear the original list
        del self.data[:]

        nxx = nx + 1
        nyy = ny + 1
        nzz = nz + 1

        #loop over vectors first to keep atoms in order for dlpoly
        for ix in range(1, nxx):

            for iy in range(1, nyy):

                for iz in range(1, nzz):

                    for im in range(len(tmp)):

                        mol = tmp[im]
                    
                        print(" the number of atoms in molecule ", im, " is ", len(mol.atoms))
                        new_mol = dlfieldspecies.Molecule(mol.name)
                        
                        for i in range(len(mol.atoms)):

                            a = mol.atoms[i]
                            sym = a.get_name()
                            pos = a.get_position()
                            mass = a.get_mass()
                            chg = a.get_charge()
                            typ = a.get_type()
                            tag = a.get_site()

                            posnew[0] = (pos[0] + (ix - 1)) / nx
                            posnew[1] = (pos[1] + (iy - 1)) / ny
                            posnew[2] = (pos[2] + (iz - 1)) / nz

                            new_atm = dlfieldspecies.Atom(sym, typ, posnew[0], posnew[1], posnew[2], mass, chg, tag)

                            new_mol.atoms.append(new_atm)

                        self.data.append(new_mol)

        self.natoms = len(self.data)

        #expand the lattice vectors
        self.vectors[0][0] *= nx
        self.vectors[1][0] *= nx
        self.vectors[2][0] *= nx
        self.vectors[0][1] *= ny
        self.vectors[1][1] *= ny
        self.vectors[2][1] *= ny
        self.vectors[0][2] *= nz
        self.vectors[1][2] *= nz
        self.vectors[2][2] *= nz
        print ("after")
        print (self.vectors[0][:])
        print (self.vectors[1][:])
        print (self.vectors[2][:])
        self.fractional_to_cartesian()

    def calculate_total_charge(self):
        """
        Calculates the total charge of the configuration
        @retval the charge is returned to the calling function
        """
        total_charge = 0.0

        for im in range(len(self.data)):

            mol = self.data[im]

            for i in range(len(mol.atoms)):

                a = mol.atoms[i]

                chg = a.get_charge()
                total_charge += chg

        return total_charge

    def morph_config_types(self, typ1, atm, num):
        """
        Changes num atoms of typ1 into typ2 for all the atoms in the configuration.
        @param string typ1 - first type of atom to be changed
        @param AtomType atm - an AtomType object of the second type as this allows mass, charge etc to be set
        @param int num - the number of changes of typ 1 to typ 2
        
        """
        
        m = []   # has the molecule number
        a = []   # atom number within a given molecule
        
        for im in range(len(self.data)):

            mol = self.data[im]

            for i in range(len(mol.atoms)):
            
                tmp = mol.atoms[i]
            
                if (tmp.name == typ1):
                
                    m.append(im)
                    a.append(i)
        
        #if there are no types to change then bail out        
        if (len(a) == 0):
            print ("failed to find atom of type ", typ1)
            return
            
        latom = len(a)
        
        for i in range(num):
            
            choice = int(latom * np.random.random_sample())
            im = m[choice]
            n = a[choice]
            
            #choice is the atom number
            self.data[im].atoms[n].name = atm.name
            self.data[im].atoms[n].type = atm.type
            self.data[im].atoms[n].charge = atm.charge
            self.data[im].atoms[n].mass = atm.mass
            
            #remove that molecule/atom from the list
            a.pop(choice)
            m.pop(choice)
            latom = latom - 1

    def shift(self, xshift = 0.0, yshift = 0.0, zshift = 0.0):
        """
        Function to do a simple displacement of all the atoms
        """
             
        for im in range(len(self.data)):

            mol = self.data[im]

            for i in range(len(mol.atoms)):

                a = mol.atoms[i]
            
                a.rpos[0] += xshift
                a.rpos[1] += yshift
                a.rpos[2] += zshift
            
                mol.atoms[i] = a

    def scale(self, xscale = 0.0, yscale = 0.0, zscale = 0.0):
        """
        Function to do a simple scaling of all the atom positions
        """
             
        for im in range(len(self.data)):

            mol = self.data[im]

            for i in range(len(mol.atoms)):

                a = mol.atoms[i]
            
                a.rpos[0] *= xscale
                a.rpos[1] *= yscale
                a.rpos[2] *= zscale
            
                mol.atoms[i] = a  
                      
    def centre_configuration(self):
        """
        the config is setup to run from -0.5 to 0.5
        """
        
        self.cartesian_to_fractional()
        
        for im in range(len(self.data)):

            mol = self.data[im]

            for i in range(len(mol.atoms)):

                a = mol.atoms[i]
            
                a.rpos[0] -= np.rint(a.rpos[0])
                a.rpos[1] -= np.rint(a.rpos[1])
                a.rpos[2] -= np.rint(a.rpos[2])
            
                mol.atoms[i] = a
            
        self.fractional_to_cartesian()

            
    def cartesian_to_fractional(self):
        """
        Converts the config from Cartesian to fractional coordinates
        """
        rcpvec = linalg.inv(self.vectors)

        for im in range(len(self.data)):

            mol = self.data[im]

            for i in range(len(mol.atoms)):

                a = mol.atoms[i]
 
                rx = a.rpos[0]
                ry = a.rpos[1]
                rz = a.rpos[2]

                a.rpos[0] = rx * rcpvec[0][0] + ry * rcpvec[0][1] + rz * rcpvec[0][2]
                a.rpos[1] = rx * rcpvec[1][0] + ry * rcpvec[1][1] + rz * rcpvec[1][2]
                a.rpos[2] = rx * rcpvec[2][0] + ry * rcpvec[2][1] + rz * rcpvec[2][2]

                mol.atoms[i] = a
            
    def fractional_to_cartesian(self):
        
        latvector = self.vectors
        
        for im in range(len(self.data)):

            mol = self.data[im]

            for i in range(len(mol.atoms)):

                a = mol.atoms[i]
 
                rx = a.rpos[0]
                ry = a.rpos[1]
                rz = a.rpos[2]

                a.rpos[0] = rx * latvector[0][0] + ry * latvector[0][1] + rz * latvector[0][2]
                a.rpos[1] = rx * latvector[1][0] + ry * latvector[1][1] + rz * latvector[1][2]
                a.rpos[2] = rx * latvector[2][0] + ry * latvector[2][1] + rz * latvector[2][2]

                mol.atoms[i] = a        
        
    def print_config_vectors(self):
        """
        Prints the lattice vectors to screen
        """
        
        print (' ')
        print ('lattice vectors of the config')
        print (' ')
        
        for i in range(3):
            print (self.vectors[:][i])
                    
    def print_config_atoms(self):
        """
        Prints the atom symbol and position to screen
        """
        tmp = []
        for k, v in self.nummols.items():
            tmp.append(v)

        print (' ')
        print ('the number of molecules in the config = ', len(self.data), tmp[:])
        print (' ')
        
        for im in range(len(self.data)):
            
            mol = self.data[im]
            print("MOLECULE ", mol.name, len(mol.atoms))

            for a in mol.atoms:
                     
                print (a.name, a.type, a.rpos[:] )
            
           
    def read_dlmonte_config(self, instream):
        """
        Function to read in a configuration in DL_MONTE format
        @param instream   The stream being employed to obtain the data
        """
        #read two lines from top of the file
        # the first is title, the second has levcfg, periodic boundary cond
        # and the number of atoms
        self.title = instream.readline()

        #amount of info and pbc
        line = instream.readline()
        words = line.split()  
      
        self.levcfg = int(words[0])
        self.pbc = int(words[1])

        #first read in the lattice vectors
        line = instream.readline()
        words = line.split()
        
        self.vectors[0][0] = float(words[0])
        self.vectors[0][1] = float(words[1])
        self.vectors[0][2] = float(words[2])
        
        line = instream.readline()
        words = line.split()
        
        self.vectors[1][0] = float(words[0])
        self.vectors[1][1] = float(words[1])
        self.vectors[1][2] = float(words[2])
        
        line = instream.readline()
        words = line.split()
        
        self.vectors[2][0] = float(words[0])
        self.vectors[2][1] = float(words[1])
        self.vectors[2][2] = float(words[2])

        line = instream.readline()
        words = line.split()
        #check that words[0] is keyword
        nummol = words[1]

        pos = np.zeros(3)

        for im in range(nummol): # get molecules - does not sort

            line = instream.readline()
            words = line.split()
            natom = words[2]
            mol = dlfieldspecies.Molecule(words[1])

            for i in range(natom): #read in atom data
                    
                line = instream.readline()
            
                words = line.split()
                symbol = words[0]
            
                typ = words[1]

                words = line.split()
                symbol = words[0]

                pos[0] = float(words[0])
                pos[1] = float(words[1])
                pos[2] = float(words[2])
            
                if len(words) > 3:
                    tag = words[3]
                else:
                    tag = ' '
            
                mass = 0.0
                charge = 0.0
                a = dlfieldspecies.Atom(symbol, typ, pos, mass, charge, tag)
            
                mol.atoms.append(a)
            
                if self.levcfg > 0:
                    line = instream.readline()
                
                if self.levcfg > 1:
                    line = instream.readline()

            self.data.append(mol)
                
    
