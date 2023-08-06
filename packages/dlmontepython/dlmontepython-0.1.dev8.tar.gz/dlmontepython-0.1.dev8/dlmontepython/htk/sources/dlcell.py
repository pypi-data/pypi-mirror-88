# -*- coding: utf-8 -*-
"""
Unit cell 
Purpose to generate a unit cell of a solid state material for later construction
of a configuration (possible in DL_POLY style). The coordinates are assumed to
be fractional throughout for the cell class.

The symmetry stuff is a hack of the DELTAPOCS code written by Steve Parker (Bath)

@author John
"""
import numpy as np
import numpy.linalg as lalg
import sys

import dlmontepython.htk.sources.dlfieldspecies as dlfieldspecies
from dlmontepython.htk.sources.dlspcgroup import Spcgroup as spc

def _multiply_rot_mat(mat, vec):
    """
    matrix-vector multiply - this is here for historical reasons and I could
    not find a numpy routine to what I wanted. 
    
    @param mat    The 3x3 matrix
    @param vec    The vector
    
    @retval v     The return vector
    """

    v = np.zeros(3)
      
    for i in range(3):
            
        csum = 0.0
            
        for j in range(3):
                
            csum += mat[i][j] * vec[j]
                
        v[i] = csum
    
    return v



class Cell:
                            
    
    def _rhombahedral_center(self):
        """
        checks and sets up the rhobahedral classes.
        """
        ninety = 90.00
        hundred20 = 120.00

        if abs(self.alpha - ninety) < self._accuracy and abs(self.beta - ninety) < self._accuracy and abs(self.gamma - hundred20) < self._accuracy:

            self.symmetry_name = self.symmetry_name + '(H)'
            self._iorig = 1
          
        elif abs(self.alpha - self.beta) < self._accuracy and abs(self.beta -self.gamma) < self._accuracy and abs(self.gamma - ninety) > self._accuracy:
              
            self.symmetry_name = self.symmetry_name + '(R)'
            self._iorig = 2
              
        else:
              
            print ('Error: Rhombahedral space group entered with wrong cell constants')
            print ('either alpha = beta = 90 and gamma = 120 (Hexagonal)')
            print ('or alpha = beta = gamma but not = 90 (Rhombahedral)')
            print ('program stopping')
              
            sys.exit(1)
              
     
    def _check_spacegroup(self):
        """
        checks to see whether a valid space group has been given.
        """
        #set up sum arrays for lattice parameters as it is quicker
        # to code
        ra = np.zeros(3)  #side
        rb = np.zeros(3)  # angle
        
        ra[0] = self.a
        ra[1] = self.b
        ra[2] = self.c
        
        rb[0] = self.alpha
        rb[1] = self.beta
        rb[2] = self.gamma
        
        #the centering type that is expected
        centyp = self.symmetry_name[0]
        
        #check that centring is compatible with the class no
        minno = 1
        maxno = 230
        
        check = False
        
        #zero counters 
        n90 = 0
        n120 = 0
        nside = 0
        ntheta = 0
        
        nel = np.zeros(3)
        nr = np.zeros(3)
        
        for i in range(3):

            nr[i] = 0
            nel[i] = 0
            
            #check to for 90 degree angles
            if abs((rb[i] / 90.0) - 1.0) < self._accuracy :
                
                n90 += 1
                nr[i] = 1
            
            #find which angle is 120 degrees
            elif abs((rb[i]/120.0)-1.0) < self._accuracy :
                
                n120 = i

            j = i + 1
            if j == 3:
                j = 0
                
            #compare cell lengths    
            if abs((ra[i]/ra[j]) - 1.0) < self._accuracy :
                nside += 1
                nel[i] = 1

            if abs((rb[i]/rb[j]) - 1.0) < self._accuracy:
                ntheta += 1

        #now check we have got what is expected
        if centyp == 'P':
            
            check = True
            # triclinic   P  1-2
            self._lattice_type = 1
            minno = 1
            maxno = 2
       
        #no angles are 90 degrees
        if n90 == 0:
            
            #trigonal P,R  143-167
            if nside == 3 and ntheta == 3:
                
                self._lattice_type = 7
                minno = 143
                maxno = 167
                
                if centyp == 'R':
                    
                    check = True

        elif n90 == 1:
            
            self._lattice_type = 1
        
        #cell has two ninety degree angles
        elif n90 == 2:
            
            if n120 > 0:
                #hexagonal  P  168-194  n.b. P,R for trigonal 143-167 in hexagonal mode
                self._lattice_type = 8
                minno = 143
                maxno = 194
                
                if centyp == 'R':
                    check = True 
                    
                if n120 != 3:
 
                    print ('need to rotate axes !')
                    
                    self._rota = True
                    if n120 == 1:
                        
                        self._rot_axis[0] = 3
                        self._rot_axis[1] = 1
                        self._rot_axis[2] = 2
                        
                    else:
                        
                        self._rot_axis[0] = 2
                        self._rot_axis[1] = 3
                        self._rot_axis[2] = 1

            else:
                 
                # monoclinic  P,A,B,C  3-15
                if nr[0] == 0:
                    self._lattice_type = 2
                    
                if nr[1] == 0:
                    self._lattice_type = 4
                    
                if nr[2] == 0:
                    self._lattice_type = 3
                
                minno = 3
                maxno = 15
                
                if centyp != 'I' or centyp != 'F':
                    check = True
            
        elif n90 == 3:
            
            #orthorhombic P,A,B,C,I,F  16-74
            self._lattice_type = 5
            minno = 16
            maxno = 74
            
            if centyp != 'R':
                check = True
                
            if nside == 2:
                
                # tetragonal P,I  75-142
                self._lattice_type = 6
                minno = 75
                maxno = 142
                
                if centyp == 'I':
                    check = True
                    
                if nel[0] == 0:
                    
                    print (' tetragonal lattice given with 4 fold axis not c')

                    self._rota = True
                    
                    if nel[1] == 1:
                        
                        self._rot_axis[0] = 3
                        self._rot_axis[1] = 1
                        self._rot_axis[2] = 2
                        
                    else:
                        
                        self._rot_axis[0] = 2
                        self._rot_axis[1] = 3
                        self._rot_axis[2] = 1
                        
            # cubic  P,I,F  195-230
            if nside == 3:
                
                 self._lattice_type = 9
                 minno = 195
                 maxno = 230
                 
                 if centyp == 'I' or centyp == 'F':
                     check = True
                 
        # self._lattice_type now set, check that centering is valid for these
        # lattice constants. If not write a warning.
        if check == False:
       
            print (' warning - invalid centring for given lattice')
            print (' this may be due to equal but inequivalent lattice constants')
        
        return check
    
    def _create_sym_matrices(self):
        """
        Creates the symmetry matrices from the space group provided.
        The function also sets up the lattice vectors with the correct
        symmetry
        """
        s = spc()
        symop = s.get_spacegroup(self.number, self.setting, self.symmetry_name)
        
        no_symops = len(symop)
        
        if no_symops == 0:
            
            print ('no symmetry operations were found')
            sys.exit(1)
            
            
            
        # setup some work arrays
        #-----------------------------------------------------------------#
        xlatt = []
        mlat = np.array([[6.,0.,0.],[0.,6.,0.],[0.,0.,6.]], order = 'F')
        xlatt.append(mlat)
        mlat = np.array([[6.,0.,0.],[0.,6.,0.],[0.,3.,3.]], order = 'F')
        xlatt.append(mlat)
        mlat = np.array([[6.,0.,0.],[0.,6.,0.],[3.,0.,3.]], order = 'F')
        xlatt.append(mlat)
        mlat = np.array([[6.,0.,0.],[3.,3.,0.],[0.,0.,6.]], order = 'F')
        xlatt.append(mlat)
        mlat = np.array([[-3.,3.,3.],[3.,-3.,3.],[3.,3.,-3.]], order = 'F')
        xlatt.append(mlat)
        mlat = np.array([[0.,3.,3.],[3.,0.,3.],[3.,3.,0.]], order = 'F')
        xlatt.append(mlat)
        mlat = np.array([[4.,2.,2.],[-2.,2.,2.],[-2.,-4.,2.]], order = 'F')
        xlatt.append(mlat)
        
        xrcpp = []
        mrcp = np.array([[1.,0.,0.],[0.,1.,0.],[0.,0.,1.]], order = 'F')
        xrcpp.append(mrcp)
        mrcp = np.array([[1.,0.,0.],[0.,1.,0.],[0.,-1.,2.]], order = 'F')
        xrcpp.append(mrcp)
        mrcp = np.array([[1.,0.,0.],[0.,1.,0.],[-1,0.,2.]], order = 'F')
        xrcpp.append(mrcp)
        mrcp = np.array([[1.,0.,0.],[-1.,2.,0.],[0.,0.,1.]], order = 'F')
        xrcpp.append(mrcp)
        mrcp = np.array([[0.,1.,1.],[1.,0.,1.],[1.,1.,0.]], order = 'F')
        xrcpp.append(mrcp)
        mrcp = np.array([[-1.,1.,1.],[1.,-1.,1.],[1.,1.,-1.]], order = 'F')
        xrcpp.append(mrcp)
        mrcp = np.array([[1.,-1.,0.],[0.,1.,-1.],[1.,1.,1.]], order = 'F')
        xrcpp.append(mrcp)
        #-----------------------------------------------------------------#
        
        # set extra symmetry matrices for different centring
        ixtra = 0

        centyp = self.symmetry_name[0]
        
        xsym = np.zeros((3,3))
        
        if centyp == 'P':
            icent = 0
            
        if centyp == 'A':
            
            icent = 1
            ixtra = 1
            xsym[0][0] = 0.0
            xsym[1][0] = 0.5
            xsym[2][0] = 0.5
         
        if centyp == 'B':
            
            icent = 2
            ixtra = 1
            xsym[0][0] = 0.5
            xsym[1][0] = 0.0
            xsym[2][0] = 0.5
         
        if centyp == 'C':
            
            icent = 3
            ixtra = 1
            xsym[0][0] = 0.5
            xsym[1][0] = 0.5
            xsym[2][0] = 0.0
          
        if centyp == 'I':
            
            icent = 4
            ixtra = 1
            xsym[0][0] = 0.5
            xsym[1][0] = 0.5
            xsym[2][0] = 0.5
          
        if centyp == 'F':
            
            icent = 5
            ixtra = 3
            xsym[0][0] = 0.0
            xsym[1][0] = 0.5
            xsym[2][0] = 0.5
            xsym[0][1] = 0.5
            xsym[1][1] = 0.0
            xsym[2][1] = 0.5
            xsym[0][2] = 0.5
            xsym[1][2] = 0.5
            xsym[2][2] = 0.0
          
        if centyp == 'R':
            
            if self.reduced == True:
            #if(iset.eq.2.or.expnd.eq.'REDU') then
                icent = 6
                
            else:
            #dummy setting for trigonal in hexagonal setting

                ixtra = 2
                xsym[0][0] = 2.0 / 3.0
                xsym[1][0] = 1.0 / 3.0
                xsym[2][0] = 1.0 / 3.0
                xsym[0][1] = 1.0 / 3.0
                xsym[1][1] = 2.0 / 3.0
                xsym[2][1] = 2.0 / 3.0
                centyp = 'P'
                icent = 0

        if self.reduced == False: #if FULL symm specified reset centyp=P
        
            centyp = 'P'
            icent = 0
            
        #prime the lattice vectors with the correct symmetry
        mlat = xlatt[icent]
        
        self.latvec = mlat / 6 #copy of matrix here!
        
        #construct the symmetry matrices
        for i in range(no_symops):
            
            fsym = np.zeros((4,4))
      
            fsym[3][3] = 1.0
            
            #start munching the symmetry opeartions to produce
            #symmetry matrix
            l = 0
            sym = symop[i]
            line = sym.get_symmetry_operation()
            
            iflag = 1
            jjnum =1
            
            #loop over the characters in the string
            for j in range(len(line)):
                
                if line[j] == ',':
                    l = l + 1
                    
                if l <= 2:
                    
                    if line[j] == 'x':
                        
                        fsym[l][0] = 1.0 * iflag
                        iflag = 1
                 
                    if line[j] == 'y':
                        fsym[l][1] = 1.0 * iflag
                        iflag=1

                    if line[j] == 'z':
                        fsym[l][2] = 1.0 * iflag
                        iflag=1
                 
                    if line[j] == '-':
                        iflag=-1
                        
                else:
                    
                    if line[j] != '0' or line[j] != ',':
                        
                        if line[j] == '1':
                       
                            jnum = jjnum
                            jjnum = 1
                        
                            if iflag == 3:
                            
                                fsym[l-3][3] = float(jnum) / float(jjnum)
                                iflag = 0
                        
                            iflag = iflag + 1
                           
                        if line[j] == '2':
                        
                            jnum = jjnum
                            jjnum = 2
                        
                            if iflag == 3:
                            
                                fsym[l-3][3] = float(jnum) / float(jjnum)
                                iflag = 0
                          
                            iflag = iflag + 1
        
                        if line[j] == '3':
                        
                            jnum = jjnum
                            jjnum = 3
                            
                            if iflag == 3:
                            
                                fsym[l-3][3] = float(jnum) / float(jjnum)
                                iflag = 0
                    
                            iflag = iflag + 1
                          
                        if line[j] == '4':
                         
                            jnum = jjnum
                            jjnum = 4
                            
                            if iflag == 3:
                            
                                fsym[l-3][3] = float(jnum) / float(jjnum)
                                iflag = 0
                            
                            iflag = iflag + 1

                        if line[j] == '5':
                         
                            jnum = jjnum
                            jjnum = 5
                        
                            if iflag == 3:
                            
                                fsym[l-3][3] = float(jnum) / float(jjnum)
                                iflag = 0
                            
                            iflag = iflag + 1                  

                        if line[j] == '6':
                         
                            jnum = jjnum
                            jjnum = 6
                        
                            if iflag == 3:
                            
                                fsym[l-3][3] = float(jnum) / float(jjnum)
                                iflag = 0
                            
                            iflag = iflag + 1                    
                   
                        if line[j] == '/':
                        
                            iflag = iflag + 1

            #add the symmetry matrices to list
            self._sym_mats.append(fsym)

        #  check if full symmetry required            
        if self.reduced == True or ixtra == 0:
            return
        
        no_sym_elements = len(self._sym_mats)
        
        for i in range(ixtra):
            
            for j in range(no_sym_elements):

                fsym = self._sym_mats[j]
                
                mat = np.zeros((4,4))
                
                for l in range(3):

                    mat[l][3] = fsym[l][3] + xsym[l][i]
                    isym = int(mat[l][3])
                    mat[l][3] = mat[l][3] - isym
                    
                    if mat[l][3] < self._accuracy:
                        mat[l][3] = mat[l][3] + 1.0
                        
                    for m in range(3):
                        
                        mat[l][m] = fsym[l][m]
                        
                self._sym_mats.append(mat)

    def _orthogonalise(self):
        """
        Provides orthogonal unit cell
        """
        cpi = np.pi / 180.0

        orthog_mat = np.zeros((3,3), order = 'F')
        
        a = self.a
        b = self.b
        c = self.c
        
        alpha = self.alpha
        beta = self.beta
        gamma = self.gamma
        
        #special case for hexagonal crystal
        if self._lattice_type == 8:
            
            orthog_mat[0][0] = a
            orthog_mat[1][0] = 0.0
            orthog_mat[2][0] = 0.0
            orthog_mat[0][1] = -a * 0.5
            orthog_mat[1][1] = a * np.sqrt(3.0) * 0.5
            orthog_mat[2][1] = 0.0
            orthog_mat[0][2] = 0.0
            orthog_mat[1][2] = 0.0
            orthog_mat[2][2] = c
            
        else:
            
            dmt = np.zeros((3,3), order = 'F')
            
            dmt[0][0] = a * a
            dmt[1][1] = b * b
            dmt[2][2] = c * c
            dmt[0][1] = a * b * np.cos(cpi*gamma)
            dmt[0][2] = a * c * np.cos(cpi*beta)
            dmt[1][2] = b * c * np.cos(cpi*alpha)
            dmt[1][0] = dmt[0][1]
            dmt[2][0] = dmt[0][2]
            dmt[2][1] = dmt[1][2]
            
            dmt = lalg.inv(dmt)
            
            astar = np.sqrt(dmt[0][0])
            
            orthog_mat[0][0] = (1.0/astar)
            orthog_mat[1][0] = a * (np.cos(cpi*gamma) - np.cos(cpi*alpha) * np.cos(cpi*beta)) / np.sin(cpi*alpha)
            orthog_mat[2][0] = a * np.cos(cpi*beta)
            orthog_mat[0][1] = 0.0
            orthog_mat[1][1] = b * np.sin(cpi*alpha)
            orthog_mat[2][1] = b * np.cos(cpi*alpha)
            orthog_mat[0][2] = 0.0
            orthog_mat[1][2] = 0.0
            orthog_mat[2][2] = c
            
        #orthonormalise lattice vectors
        xlat = self.latvec
        x = np.zeros((3))
        
        for i in range(3):

            x[0] = orthog_mat[0][0]*xlat[0][i]+orthog_mat[0][1]*xlat[1][i]+orthog_mat[0][2]*xlat[2][i]
            x[1] = orthog_mat[1][0]*xlat[0][i]+orthog_mat[1][1]*xlat[1][i]+orthog_mat[1][2]*xlat[2][i]
            x[2] = orthog_mat[2][0]*xlat[0][i]+orthog_mat[2][1]*xlat[1][i]+orthog_mat[2][2]*xlat[2][i]
      
            #xlat[i][0] = x[0]
            #xlat[i][1] = x[1]
            #xlat[i][2] = x[2]
            xlat[0][i] = x[0]
            xlat[1][i] = x[1]
            xlat[2][i] = x[2]
            
        accx2 = self._accuracy * self._accuracy
        
        for i in range(3):
            for j in range(3):
                
                if abs(xlat[i][j]) < accx2:
                    xlat[i][j] = 0.0

        self.latvec = xlat
        
        print (' orthogonal coordinate system defined such that')
        
        if self._lattice_type < 5 or self._lattice_type == 7:
            
            print (' x is parallel to reciprocal a, z is parallel to c')
            print (' y is orthogonal to x and z and forms a right handed set')
            
        else:
            
            print (' x is parallel to a, z is parallel to c,')
            print (' y is orthogonal to x and z')
      
    def __init__(self):
        """
        Initialise the unit cell object with the default values
        """
        self.a = 1.0
        self.b = 1.0
        self.c = 1.0
        self.alpha = 90.0
        self.beta = 90.0
        self.gamma = 90.0
        
        self.name = " "
        self.latvec = np.zeros((3,3), order = 'F')
        
        self.reduced = True
        self.symmetry_name = "P1"
        self.number = "1"
        self.setting = 1
        self.data = []
        self.ionic = False
        self.molecular = False
        
        self._accuracy = 1.0e-6
        self._iorigin = 1

        #integer identifying the type of lattice
        self._lattice_type = 0
        
        #set up rotation of axis if incorrectly set
        self._sym_mats = []
        
        self._rot_axis = np.zeros(3)
        self._rota = False
        
    #adds a molecule - once this done the cell is a molecular solid
    # this can not be undone
    def add_molecule(self, mol):
        
        if (self.ionic == True):
            print ("atomic data has already been added")
            sys.exit(-1)
            
        self.ionic = False
        self.molecular = True


        self.data.append(mol)
    
    def add_atom(self, atm):
        """
        Add an atom to the unit cell
        
        @param atm    An atom object
        """

        if (self.molecular == True):
            print ("molecular data has already been declared")
            sys.exit(-1)
            
        self.ionic = True
        self.molecular = False
        
        self.data.append(atm)

    def set_cell_name(self, name):

        self.name = name

    # set the cell parameers
    def set_cell(self, name, a, b, c, alpha, beta, gamma):
        """
        Function to set the cell parameters.
        
        @param a    Length of x axis in Angstroms
        @param b    Length of y axis in Angstroms
        @param c    Length of z axis in Angstroms
        @param alpha Angle in degrees
        @param beta  Angle in degrees
        @param gamma Angle in degrees
        """

        self.name = name
        self.a = a
        self.b = b
        self.c = c
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
    
    def print_cell_parameters(self):
        """
        Prints the cell parameters to the terminal
        """
        print (' ')
        print ('cell parameters')
        print ('---------------')
        print (' ')
        print ('a       :', self.a)
        print ('b       :', self.b)
        print ('c       :', self.c)
        print ('alpha   :', self.alpha)
        print ('beta    :', self.beta)
        print ('gama    :', self.gamma)
        
    def set_size(self, size):
        """
        Set whether reduced or full unit cell is required    .
        
        @param size    Must be either REDU(ced) or FULL
        """
        test = size.upper()
        
        if test == 'REDU':
            
            self.reduced = True
            
        elif test == 'FULL':
            
            self.reduced = False
            
        else:
            
            print ('the wrong cell size has been requested')
            print ('setting to the reduced unit cell')
            self.reduced = True
        
    def set_symmetry_class_number(self, number):
        """
        Set the number of the symmetry class.
        
        @param number    The class number
        """
        self.number = number

    def set_symmetry_class_name(self, symmetry_name):
        """
        The name of the symmetry class.
        
        @param symmetry_name    The class symmetry_name
        """
        self.symmetry_name = symmetry_name.upper()
        
    
    def set_class_setting(self, setting):
        """
        setting for the symmetry class.
        
        @param setting    Any special setting of the class
        """
        self.setting = setting
    
    def print_symmetry_class(self):
        """
        Prints out the symmetry class to screen
        """
        
        print (' ')
        print ('symmetry class ')
        print ('--------------')
        print (' ')
        print ('name     :', self.symmetry_name)
        print ('number   :', self.number)
        print ('setting  :', self.setting)
    
    def print_symmetry_properties(self):
        """
        Print out symmetry operations to screen
        """
        s = spc()
        symop = s.get_spacegroup(self.number, self.setting, self.symmetry_name)
        
        no_symops = len(symop)
        print (' ')
        print ('symmetry operations')
        print ('-------------------')
        print ('the number of symmetry operations', no_symops)
        print (' ')
        
        for i in range(no_symops):
            
            sym = symop[i]
            
            sym.print_operation()
            
    def print_symmetry_matrices(self):
        """
        print out symmetry matrices (this is mostly for debugging)
        """
        self._create_sym_matrices()
        no_symops = len(self._sym_mats)
        print (' ')
        print ('symmetry matrices  ')
        print ('-------------------')
        print ('the number of symmetry matrices', no_symops)
        print (' ')
        
        for i in range(no_symops):
            
            sym = self._sym_mats[i]
            
            print ('------------------------')
            print (' matrix ',i + 1)
            print ('------------------------')
            
            for j in range(4):
                
                print (sym[j][:])
        
            
    def create_cell(self):
        """
        Call this function to generate the unit cell once the symmetry
        group has been defined and the atoms added to the unit cell
        """
        
        if self.symmetry_name[0] == 'R':
            
            self._rhombahedral_center()
            
        #check cell parameters and angles are valid
        check = self._check_spacegroup()
        
        if check == True:
            self._create_sym_matrices()
            
        else:
            
            print ('error in unit cell formation')
            return

        #lattice vectors
        self._orthogonalise()
        
        #atoms must be inside the box - make sure this is the case

        #make a copy of the original atoms
        original_atms = list(self.data)
        
        #generate 'new' positions using symmetry            
        nsym = len(self._sym_mats)
        newpos = np.zeros(3)
        
        for i in range(nsym):
            
            m = self._sym_mats[i]
            
            for j in range(len(original_atms)):
                
                a = original_atms[j]
                
                newpos = a.get_position()
                
                #muliply position by symmetry matrix
                newpos = _multiply_rot_mat(m, newpos)
                newpos[0] += m[0][3]
                newpos[1] += m[1][3]
                newpos[2] += m[2][3]
                
                #check that the atoms has not been displaced out of the box
                
                if newpos[0] > 1.0 - self._accuracy:
                    newpos[0] -= int(newpos[0])
                if newpos[0] < -self._accuracy:
                    newpos[0] += 1.0 #int(newpos[0])
                if newpos[1] > 1.0 - self._accuracy:
                    newpos[1] -= int(newpos[1])
                if newpos[1] < -self._accuracy:
                    newpos[1] += 1.0 #int(newpos[1])
                if newpos[2] > 1.0 - self._accuracy:
                    newpos[2] -= int(newpos[2])
                if newpos[2] < -self._accuracy:
                    newpos[2] += 1.0 #int(newpos[2])                    
                #now check that the new atom does not overlap with the remaining atoms
                overlap = False
                for k in range(len(self.data)):
                    
                    oldatm = self.data[k]
                    
                    diff = oldatm.get_distance(newpos)
                    #print 'difference ', diff[:]
                    if abs(diff[0]) < self._accuracy and abs(diff[1]) < self._accuracy and abs(diff[2]) < self._accuracy:
                        overlap = True
                        break
                    
                #if no overlap is found at to the list making sure to copy properties
                if overlap == False:
                    
                    sym = a.get_name()
                    mass = a.get_mass()
                    chg = a.get_charge()
                    tag = a.get_site()
                    typ = a.get_type()
        
                    newatm = dlfieldspecies.Atom(sym, typ, newpos[0], newpos[1], newpos[2], mass, chg, tag)
                    self.data.append(newatm)
                    
    def print_lattice_vectors(self):

        print (' ')
        print ('lattice vectors for the unit cell')
        print (' ')
        
        print ("{:15.8f}".format(self.latvec[0][0]))
        print ("{:15.8f}".format(self.latvec[1][0]))
        print ("{:15.8f}".format(self.latvec[2][0]))
        print ("\n")
        
        print ("{:15.8f}".format(self.latvec[0][1]))
        print ("{:15.8f}".format(self.latvec[1][1]))
        print ("{:15.8f}".format(self.latvec[2][1]))
        print ("\n")
        
        print ("{:15.8f}".format(self.latvec[0][2]))
        print ("{:15.8f}".format(self.latvec[1][2]))
        print ("{:15.8f}".format(self.latvec[2][2]))
        print ("\n") 
        print ("\n")
                   
    def print_atoms(self):
        
        print (' ')
        print ('the number of atoms in the unit cell = ', len(self.data))
        print (' ')
        
        for i in range(len(self.data)):
            
            a = self.data[i]
            
            print (a.name, a.rpos[:])
            
    def cell_charge(self):
        """
        Calculates to total charge on the unit cell (if it is not 0.0 something may have gone wrong)
        @retval sum of the charges
        """
        
        chg = 0.0
        
        for i in range(len(self.data)):
            
            a = self.data[i]
            
            chg += a.charge
            
        if abs(chg) > 1.0e-6:
            print ('*** WARNING: cell has a charge ', chg)
            
        return chg
            
    def expand_cell(self, nx, ny, nz):
        """
        grow the configuration in x y and z

        @param nx    expand the cell n times in the x direction
        @param ny    expand the cell in the y direction
        @param nz    expand the cell in the z direction
        """

        if nx < 1 or ny < 1 or nz < 1:
            print ("expansion coffcicients must be >= 1")
            return

        pos = np.zeros(3)
        posnew = np.zeros(3)

        #make a cop of the data
        atmp = []
        atmp[:] = self.data[:]

        #clear the original list
        del self.data[:]

        nxx = nx + 1
        nyy = ny + 1
        nzz = nz + 1

        #loop over vectors first to keep atoms in order for dlpoly
        for ix in range(1, nxx):

            for iy in range(1, nyy):

                for iz in range(1, nzz):

                    for i in range(len(atmp)):

                        a = atmp[i]

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

                        self.data.append(new_atm)

        self.natoms = len(self.data)
        #expand the lattice vectors
        self.latvec[0][0] *= nx
        self.latvec[1][0] *= nx
        self.latvec[2][0] *= nx
        self.latvec[0][1] *= ny
        self.latvec[1][1] *= ny
        self.latvec[2][1] *= ny
        self.latvec[0][2] *= nz
        self.latvec[1][2] *= nz
        self.latvec[2][2] *= nz

    def sort_by_type(self, types):

        if len(types) == 0:
            return

        #make a cop of the data
        atmp = []
        atmp[:] = self.data[:]
        
        #clear the data
        del self.data[:]

        for j in range(len(types)):

            t = types[j]

            for i in range(self.natoms):

                a = atmp[i]

                if a.name == t:
                    self.data.append(a)
