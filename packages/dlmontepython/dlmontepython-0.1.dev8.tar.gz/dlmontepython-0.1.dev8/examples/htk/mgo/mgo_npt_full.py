"""
DL_MONTE python script to run MgO NPT simulation at multiple pressures.
This is an example of how to setup workflow style calculation

NB the simulation only runs for 100000 steps which is too short for meaningful results
"""

import os
import subprocess
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
    field.cutoff = 8.0

    #create a list of atomic types
    atype1 = dlmonte.dlfield.AtomType("Mg","core", 24.0, 2.0)
    field.atomtypes.append(atype1)
    atype2 = dlmonte.dlfield.AtomType("O","core", 16.0, -2.0)
    field.atomtypes.append(atype2)
    #print ("Atomtypes: ", field.atomtypes)

    #create a list of molecular types
    mol1 = dlmonte.dlfield.MolType("MgO", 512) #there are 512 atoms in the config
    field.moltypes.append(mol1)
    #print ("Moltypes: ", field.moltypes)


    #now for the tricky bit - building the VdW interactions
    field.vdw_ecap = 1.0e8
    atom1 = dlmonte.dlfield.Atom("Mg","core")
    atom2 = dlmonte.dlfield.Atom("O","core")
    int1 = dlmonte.dlinteraction.InteractionBuckingham(1007.4, 0.3262, 0.0)
    int2 = dlmonte.dlinteraction.InteractionBuckingham(22764.3, 0.149, 20.37)

    vdw1 = dlmonte.dlfield.VDW(atom1, atom2, int1)
    vdw2 = dlmonte.dlfield.VDW(atom2, atom2, int2)

    field.vdw.append(vdw1)
    field.vdw.append(vdw2)

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
    title = "Control file for MgO NVT"

    # this is the 'use' keyword for DL_MONTE - we are not using any here
    use = dlmonte.dlcontrol.UseBlock()
    #print(repr(use))

    #the main control commands
    d = OrderedDict()
    d['steps'] = 100000
    d['temperature'] = 800.0
    d['maxatmdist'] = 0.001
    d['maxvolchange'] = 0.01
    d['equilibration'] = 50000
    d['print'] = 1000
    #d['paratom'] = ""
    d['acceptatmmoveupdate'] = 100
    #d['distewald'] = ""
    d['acceptvolupdate'] = 100
    d['stack'] = 100

    main = dlmonte.dlcontrol.MainBlock(d)

    #the movers are the MC moves
    movers = []
    mover = dlmonte.dlmove.parse_atom("Mg core")
    movers.append(mover)
    mover = dlmonte.dlmove.parse_atom("O core")
    movers.append(mover)
    amove = dlmonte.dlmove.AtomMove(80, movers)
    vmove = dlmonte.dlmove.VolumeVectorMove(20) #adjust all lattice vectors
    main.moves.append(amove)
    main.moves.append(vmove)

    print("fabricated control")

    #create the instance of the control file
    cntrl = dlmonte.dlcontrol.CONTROL(title, use, main)


    return cntrl



##############################################################################
# The 'main' program starts here
##############################################################################
field = create_field_file()
#it is possible to get HTK to spit out the FIELD file to stdout
#print(field)
#also in json format
#print(field.to_json())

#actually produce the FIELD file
field.to_file()


cntrl = create_control_file()
#create a file
cntrl.temperature = 100.0
#control file to stdout
temperature = cntrl.temperature
print(" I have updated temperature to ", temperature)
cntrl.to_file()

#this follows the document doc/tutorial/util-dlmonte.html
#set the path to the DL_MONTE executable
DL_MONTE_HOME = "/home/jap93/DLMONTE3/DL_MONTE-2/bin/"
input_dir = "/home/jap93/DLMONTE3/dl_monte-python/examples/mgo"


#create the input
myinput = dlmonte.DLMonteInput.from_directory(input_dir)


dlx = os.path.join(DL_MONTE_HOME, "DLMONTE-SRL-VDW_dir-opt.X")

#starting pressure
press = 0.001

for i in range(10):                

    #create the control file with the desired pressure (in katms)
    pressuretag = {"pressure": press}
    myinput.control.main_block.statements.update(pressuretag)

    #create the working directory
    work_dir = "pressure_workspace_" + str(i)
    cmd = "mkdir " + work_dir
    status = subprocess.call(cmd, shell=True)

    # Copy the input to the working directory

    myinput.to_directory(work_dir)

    # Set up a DLMonteRunner object linked to the directory work_dir
    # and the executable dlx
    myrun = dlmonte.DLMonteRunner(dlx, work_dir)

    # Execute the runner - the output files from the simulation will be in work_dir
    myrun.execute()

    #increment pressure
    press += 0.1
