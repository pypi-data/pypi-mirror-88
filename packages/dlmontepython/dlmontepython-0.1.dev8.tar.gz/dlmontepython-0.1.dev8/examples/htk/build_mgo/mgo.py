# -*- coding: utf-8 -*-
"""
Created on Tue May  5 10:44:13 2015

A demonstration and test python script to generate the
unit cell of MgO

@author: jap93
"""
import os
import subprocess
import numpy as np

#Import the dlmonte (htk) module with alias "dlmonte"
import dlmontepython.htk.sources.dlmonte as dlmonte
import dlmontepython.htk.sources.dlfield as dlfield
import dlmontepython.htk.sources.dlmonte_filter as dlfilter

#create an instance of the unit cell
mgo = dlmonte.dlcell.Cell()

#give the cell a name
name = 'mgo'

#cell parameters etc
a = b = c = 4.3164  #from DL_MONTE @ 800 K
alpha = beta = gamma = 90.0

mgo.set_cell(name, a, b, c, alpha, beta, gamma)
mgo.print_cell_parameters()

#symmetry class required
name = 'FM3-M'
mgo.set_symmetry_class_name(name)
mgo.set_size('FULL')

number = 225
mgo.set_symmetry_class_number(number)

mgo.print_symmetry_class()

#add the atoms to the cell
x = 0.0
y = 0.0
z = 0.0
a1 = dlfield.Atom('Mg', 'core', x, y, z, 24.0, 2.0)
mgo.add_atom(a1)

x = 0.5
y = 0.5
z = 0.5
a2 = dlfield.Atom('O', 'core', x, y, z, 16.0, -2.0)
mgo.add_atom(a2)

#generate the new atomic positions
mgo.create_cell()

mgo.expand_cell(4, 4, 4)
#mgo.print_lattice_vectors()
#mgo.print_atoms()

#uncomment below if you want symmetry matrices
#mgo.print_symmetry_matrices()


cfg = dlmonte.dlgenconfig.GenConfig()

cfg.create_config(mgo, "MgO test example")

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
