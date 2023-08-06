# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 08:07:48 2015

@author: jap93
"""

import dlmontepython.htk.sources.dlmonte as dlmonte
import dlmontepython.htk.sources.dlfieldspecies as dlfieldspecies

class MonteFilter (object):
    
    #reads a single frame of atoms        
    def read_config(self, instream):

        cfg = dlmonte.dlgenconfig.GenConfig()
                    
        #read two lines from top of the file
        # the first is title, the second has levcfg, periodic boundary cond
        # and the number of atoms
        cfg.title = instream.readline()

        #amount of info and pbc
        line = instream.readline()
        words = line.split()  
      
        cfg.levcfg = int(words[0])
        cfg.pbc = int(words[1])
        cfg.natoms = int(words[2])

        #first read in the lattice vectors
        line = instream.readline()
        words = line.split()
        
        cfg.vectors[0][0] = float(words[0])
        cfg.vectors[0][1] = float(words[1])
        cfg.vectors[0][2] = float(words[2])
        
        line = instream.readline()
        words = line.split()
        
        cfg.vectors[1][0] = float(words[0])
        cfg.vectors[1][1] = float(words[1])
        cfg.vectors[1][2] = float(words[2])
        
        line = instream.readline()
        words = line.split()
        
        cfg.vectors[2][0] = float(words[0])
        cfg.vectors[2][1] = float(words[1])
        cfg.vectors[2][2] = float(words[2])

        #read the NUMMOL line containing the number of molecules to read
        line = instream.readline()
        words = line.split()
        nummol = int(words[1])

        #next read in the atom positions
        for im in range(nummol):
            
            #read molecule keyword, name and the number of atoms in the molecule
            line = instream.readline()
            words = line.split()
            
            name = words[1]
            natoms = int(words[2])
            

            #create an instance of a molecule with the correct name
            mol = dlfieldspecies.Molecule(name)

            for i in range(natoms):
            
                line = instream.readline()
                words = line.split()
                el = words[0]
                typ = words[1]
            
                line = instream.readline()
                words = line.split()
                x = float(words[0])
                y = float(words[1])
                z = float(words[2])
            
                a = dlfieldspecies.Atom(el, typ, x, y, z)

                mol.add_atom(a)
        
            cfg.add_molecule(mol)
            
        return cfg      
        
    #writes out a config frame to a file
    def write_frame(self, c, outstream):
        
        if isinstance(c, dlmonte.dlgenconfig.GenConfig) == False:
            
            print('write_frame routine is expecting a Config type')
            return
 
        #the unit cell must run from -0.5 to 0.5 for dlmonte

        #make sure there is no carriage return on the string
        new_title = c.title

        outstream.write(new_title.rstrip())
        outstream.write("\n")

        outstream.write("{:d}".format(c.levcfg))
        outstream.write("{:8d}".format(c.pbc))
        outstream.write("{:15d}".format(c.natoms))
        outstream.write("\n")

        outstream.write("{:15.8f}".format(c.vectors[0][0]))
        outstream.write("{:15.8f}".format(c.vectors[1][0]))
        outstream.write("{:15.8f}".format(c.vectors[2][0]))
        outstream.write("\n")

        outstream.write("{:15.8f}".format(c.vectors[0][1]))
        outstream.write("{:15.8f}".format(c.vectors[1][1]))
        outstream.write("{:15.8f}".format(c.vectors[2][1]))
        outstream.write("\n")

        outstream.write("{:15.8f}".format(c.vectors[0][2]))
        outstream.write("{:15.8f}".format(c.vectors[1][2]))
        outstream.write("{:15.8f}".format(c.vectors[2][2]))
        outstream.write("\n")

        tmp = []
        for k, v in c.nummols.items():
            tmp.append(v)

        nummol = len(c.data)
        outstream.write("NUMMOL {:d}".format(nummol))

        for i in range(len(tmp)):
            outstream.write(" {}".format(tmp[i]))

        outstream.write("\n")

        idx = 0 # this is a counter

        for im in range(nummol):

            mol = c.data[im]

            outstream.write("MOLECULE {} {:d}".format(mol.name, len(mol.atoms)))
            outstream.write("\n")
            
            for a in mol.atoms:
                idx += 1
                a.write_atom_dlmonte(outstream, idx)
            
