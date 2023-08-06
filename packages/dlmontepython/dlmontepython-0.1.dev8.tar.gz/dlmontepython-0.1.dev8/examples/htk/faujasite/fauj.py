# -*- coding: utf-8 -*-
"""
Created on Tue May  5 10:44:13 2015

A demonstration and test python script to generate the
unit cell of Faujasite

@author: jap93
"""
import os
import sys
import subprocess
import numpy as np

#Import the dlmonte (htk) module with alias "dlmonte"
import dlmontepython.htk.sources.dlmonte as dlmonte
import dlmontepython.htk.sources.dlfield as dlfield
import dlmontepython.htk.sources.dlmonte_filter as dlfilter


#create an instance of the unit cell
fauj = dlmonte.dlcell.Cell()

#give the cell a name
name = 'fauj'

#cell parameters etc
a = b = c = 24.268
alpha = beta = gamma = 90.0

fauj.set_cell(name, a, b, c, alpha, beta, gamma)
fauj.print_cell_parameters()

#symmetry class required
name = 'FD3-MZ'
fauj.set_symmetry_class_name(name)
fauj.set_size('FULL')

number = 227
fauj.set_symmetry_class_number(number)

fauj.print_symmetry_class()

#add the atoms to the cell
x = 0.0364
y = 0.1262
z = 0.3027
a1 = dlfield.Atom('Si', 'core', x, y, z, 24.0, 2.4)
fauj.add_atom(a1)

x = 0.0000
y = 0.3945
z = 0.6055
a2 = dlfield.Atom('O', 'core', x, y, z, 16.0, -1.2)
fauj.add_atom(a2)

x = 0.2522
y = 0.2522
z = 0.1392
a2 = dlfield.Atom('O', 'core', x, y, z, 16.0, -1.2)
fauj.add_atom(a2)

x = 0.3265
y = 0.3265
z = 0.0215
a2 = dlfield.Atom('O', 'core', x, y, z, 16.0, -1.2)
fauj.add_atom(a2)

x = 0.0718
y = 0.0718
z = 0.3152
a2 = dlfield.Atom('O', 'core', x, y, z, 16.0, -1.2)
fauj.add_atom(a2)

#generate the new atomic positions
fauj.create_cell()

#uncomment if you want to see the vectors/atoms
#fauj.print_lattice_vectors()
#fauj.print_atoms()

#uncomment below if you want symmetry matrices
#fauj.print_symmetry_matrices()

#check that cell is charge neutral
cell_charge = fauj.cell_charge()
print(" ") # a bit of padding
print ("The unit cell has a charge of : ", cell_charge)

#expand the unit cell
fauj.expand_cell(2, 2, 2)

#sort the types to make things easier to understand
types = ['Si', 'O']
fauj.sort_by_type(types)


#############################################################
# create the configuration for use in DL_MONTE
#############################################################

cfg = dlmonte.dlgenconfig.GenConfig()

cfg.create_config(fauj, "Faujasite example")

############################################################
# add a molecule to the configuration
############################################################
mol = dlfield.Molecule('co2')
a = dlfield.Atom('C_', 'core', 0.0, 0.0, 0.0, 12.0, 0.6512)
mol.add_atom(a)
a = dlfield.Atom('O_C', 'core', 1.163, 0.0, 0.0, 16.0, -0.3256)
mol.add_atom(a)
a = dlfield.Atom('O_C', 'core', -1.163, 0.0, 0.0, 16.0, -0.3256)
mol.add_atom(a)

cfg.add_molecule(mol)

cfg.set_maxnumber_molecule('co2', 200)

cfg.print_config_vectors()
cfg.print_config_atoms()

#open the file
filename = "CONFIG"
try:
    outstream = open(filename, 'w')

except:
    print('cant open output file')
    sys.exit(1)


#create an instance of input output filter for DL_POLY
dout = dlfilter.MonteFilter()
dout.write_frame(cfg, outstream)
