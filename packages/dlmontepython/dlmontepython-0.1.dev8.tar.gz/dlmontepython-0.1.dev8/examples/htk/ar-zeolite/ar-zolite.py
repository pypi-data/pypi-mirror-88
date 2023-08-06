# workflow to simulate Ar in a zeolite

import subprocess
import os
import sys
import numpy as np

from collections import OrderedDict

#Import the dlmonte (htk) module with alias "dlmonte"
import dlmontepython.htk.sources.dlmonte as dlmonte


##############################################################################
# Produce the FIELD file for the calculation
##############################################################################
def create_field_file():

    """ function to create and write out a FIELD file for use in DL_MONTE
    It does not take any arguments and does not return anything. TODO error checking in non existant
    """

    #if you want to read the field file from a file
    #filename = "FIELD.ORIGINAL"
    #field1 = dlmonte.dlfield.from_file(filename)
    #print(repr(field1))

    #else if you want an instance then the components of the FIELD have to added
    # manually
    field = dlmonte.dlfield.FIELD()

    #set the parameters
    field.description = "MgO interactions using Lewis-Catlow potentials"
    field.cutoff = 12.0

    #create a list of atomic types
    atype1 = dlmonte.dlfield.AtomType("Si","core", 24.0, 4.0)
    field.atomtypes.append(atype1)
    atype2 = dlmonte.dlfield.AtomType("O","core", 16.0, -2.0)
    field.atomtypes.append(atype2)
    atype3 = dlmonte.dlfield.AtomType("Ar","core", 39.9, 0.0)
    field.atomtypes.append(atype3)
    #print ("Atomtypes: ", field.atomtypes)

    #create a list of molecular types
    mol1 = dlmonte.dlfield.MolType("zeolite", 2304) #there are 2304 atoms in the config
    mol2 = dlmonte.dlfield.MolType("argon", 200) #there are 200 atoms in the config
    field.moltypes.append(mol1)
    field.moltypes.append(mol2)
    #print ("Moltypes: ", field.moltypes)


    #now for the tricky bit - building the VdW interactions
    field.vdw_ecap = 1.0e10
    atom1 = dlmonte.dlfield.Atom("Si","core")
    atom2 = dlmonte.dlfield.Atom("O","core")
    atom3 = dlmonte.dlfield.Atom("Ar","core")
    int1 = dlmonte.dlinteraction.InteractionLJ(0.010315, 3.405)  # Ar-Ar parameters
    int2 = dlmonte.dlinteraction.InteractionLJ(0.0028437, 2.04105) # Ar-Si parameters
    int3 = dlmonte.dlinteraction.InteractionLJ(0.0094790, 3.05660) # Ar-O parameters

    vdw1 = dlmonte.dlfield.VDW(atom3, atom3, int1)
    vdw2 = dlmonte.dlfield.VDW(atom3, atom1, int2)
    vdw3 = dlmonte.dlfield.VDW(atom3, atom2, int2)

    field.vdw.append(vdw1)
    field.vdw.append(vdw2)
    field.vdw.append(vdw3)

    return field

##############################################################################
# Produce the CONTROL file for the calculation
##############################################################################
def create_control_file():

    """ creates and writes out a control file for use in DL_MONTE using the HTK.
    The HTK defines the CONTROL as three parts: title, use_block and main_block
    The function niether takes input nor returns anything. TODO again put error checking in
    """

    #if you want to directly read the CONTROL file uncomment the next two lines
    #filename = "CONTROL"
    #ctrl = dlmonte.dlcontrol.from_file(filename)
    #print(dir(ctrl))

    #start to create a CONTROL file for DL_MONTE
    title = "Control file for Ar in zeolite"

    # this is the 'use' keyword for DL_MONTE - we are not using any here
    lines = []
    lines.append("use gaspressure")
    lines.append("finish use-block")
    dlstr = "\n".join(lines)
    use = dlmonte.dlcontrol.UseBlock.from_string(dlstr)

    print(repr(use))

    #the main control commands
    d = OrderedDict()
    d['steps'] = 1000000
    d['temperature'] = 300.0
    d['maxatmdist'] = 0.001
    d['equilibration'] = 100000
    d['print'] = 1000
    d['noewald'] = "all"
    #d['paratom'] = ""
    d['acceptatmmoveupdate'] = 100
    #d['distewald'] = ""
    d['acceptvolupdate'] = 100
    d['stack'] = 100

    main = dlmonte.dlcontrol.MainBlock(d)

    #the movers are the MC moves
    movers = []
    mover = dlmonte.dlmove.parse_atom("Ar core")
    movers.append(mover) 
    amove = dlmonte.dlmove.AtomMove(80, movers)

    gcmovers = []
    gcmover = dlmonte.dlmove.parse_atom_gcmc("Ar core 0.02")
    print ("gcmover", gcmover)
    gcmovers.append(gcmover)
    gcmover = dlmonte.dlmove.parse_atom_gcmc("Xe core 0.02")
    gcmovers.append(gcmover)
    gmove = dlmonte.dlmove.InsertAtomMove(20, 1.0, gcmovers)
    print ("gmove", repr(gmove))
    main.moves.append(amove)
    main.moves.append(gmove)
    print("main move ", repr(main.moves))

    print("fabricated control")

    #create the instance of the control file
    cntrl = dlmonte.dlcontrol.CONTROL(title, use, main)

    #control file to stdout
    print(cntrl)

    return cntrl

##############################################################################
# The 'main' program starts here
##############################################################################
field = create_field_file()
#it is possible to get HTK to spit out the FIELD file to stdout
#print(field)
#also in json format
#print(field.to_json())
field.to_file()


# CONTROL file creation
cntrl = create_control_file()

pot = 0.001
typ = "Ar core"
cntrl.set_atom_gcmc_potential(typ, pot)

cntrl.to_file()

#this follows the document doc/tutorial/util-dlmonte.html
#set the path to the DL_MONTE executable
DL_MONTE_HOME = "/home/jap93/DLMONTE3/DL_MONTE-2/bin/"
input_dir = "/home/jap93/DLMONTE3/dl_monte-python/examples/ar-zeolite"


#create the input
myinput = dlmonte.DLMonteInput.from_directory(input_dir)


dlx = os.path.join(DL_MONTE_HOME, "DLMONTE-SRL-VDW_dir-opt.X")

#create the working directory
work_dir = "workspace"
cmd = "mkdir " + work_dir
status = subprocess.call(cmd, shell=True)

# Copy the input to the working directory

myinput.to_directory(work_dir)

# Set up a DLMonteRunner object linked to the directory work_dir
# and the executable dlx
myrun = dlmonte.DLMonteRunner(dlx, work_dir)

# Execute the runner - the output files from the simulation will be in work_dir
myrun.execute()
