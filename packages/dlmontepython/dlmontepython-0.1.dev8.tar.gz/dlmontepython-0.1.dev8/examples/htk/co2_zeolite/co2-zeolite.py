# workflow to simulate CO2 in a zeolite

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
    It does not take any arguments, but returns the field to the main function. 
    TODO error checking in non existant

    """

    #if you want to read the field file from a file
    #filename = "FIELD.ORIGINAL"
    #field1 = dlmonte.dlfield.from_file(filename)
    #print(repr(field1))

    #else if you want an instance then the components of the FIELD have to added
    # manually
    field = dlmonte.dlfield.FIELD()

    #set the parameters
    field.description = "CO2 (EPM2) zeolite test interaction"
    field.cutoff = 12.0

    #create a list of atomic types
    atype1 = dlmonte.dlfield.AtomType("Si","core", 24.0, 2.4)
    field.atomtypes.append(atype1)
    atype2 = dlmonte.dlfield.AtomType("O_","core", 16.0, -1.2)
    field.atomtypes.append(atype2)
    atype3 = dlmonte.dlfield.AtomType("C_","core", 12.0, 0.6512)
    field.atomtypes.append(atype3)
    atype4 = dlmonte.dlfield.AtomType("O_C","core", 16.0, -0.3256)
    field.atomtypes.append(atype4)
    atype5 = dlmonte.dlfield.AtomType("Xe","core", 1.0, 0.0)  # Xe is a ghost atom to stop CO2 going into inaccessible pores
    field.atomtypes.append(atype5)
    #print ("Atomtypes: ", field.atomtypes)

    #create a list of molecular types
    mol1 = dlmonte.dlfield.MolType("zeolite", 584) #there are 584 atoms in the config
    field.moltypes.append(mol1)
    mol2 = dlmonte.dlfield.MolType("co2", 3) #there are 3 atoms in each CO2 molecule
    pos1 = [0.0000, 0.0000, 0.0000]
    pos2 = [1.1630, 0.0000, 0.0000]
    pos3 = [-1.1630, 0.0000, 0.0000]
    a1 = dlmonte.dlfield.Atom("C_","core", pos1[0], pos1[1], pos1[2])
    a2 = dlmonte.dlfield.Atom("O_C","core", pos2[0], pos2[1], pos2[2])
    a3 = dlmonte.dlfield.Atom("O_C","core", pos3[0], pos3[1], pos3[2])
    mol2.atoms.append(a1)
    mol2.atoms.append(a2)
    mol2.atoms.append(a3)
    bond1 = [1, 2, 1]
    bond2 = [1, 3, 1]
    bond3 = [2, 3, 2]
    mol2.bonds.append(bond1)
    mol2.bonds.append(bond2)
    mol2.bonds.append(bond3)
    field.moltypes.append(mol2)
    #print ("Moltypes: ", field.moltypes)


    #now for the tricky bit - building the VdW interactions
    field.vdw_ecap = 1.0e10
    atom1 = dlmonte.dlfield.Atom("Si","core")
    atom2 = dlmonte.dlfield.Atom("O_","core")
    atom3 = dlmonte.dlfield.Atom("C_","core")
    atom4 = dlmonte.dlfield.Atom("O_C","core")
    atom5 = dlmonte.dlfield.Atom("Xe","core")
    int1 = dlmonte.dlinteraction.InteractionLJ(0.094566874, 2.892)  
    int2 = dlmonte.dlinteraction.InteractionLJ(0.15998351, 3.033) 
    int3 = dlmonte.dlinteraction.InteractionLJ(0.055892323, 2.757) 
    int4 = dlmonte.dlinteraction.InteractionLJ(0.094566874, 2.892)
    int5 = dlmonte.dlinteraction.InteractionLJ(0.15998351, 3.033)
    int6 = dlmonte.dlinteraction.Interaction12_6(16777216, 0.0)

    vdw1 = dlmonte.dlfield.VDW(atom2, atom3, int1)
    vdw2 = dlmonte.dlfield.VDW(atom2, atom4, int2)
    vdw3 = dlmonte.dlfield.VDW(atom3, atom3, int3)
    vdw4 = dlmonte.dlfield.VDW(atom3, atom4, int4)
    vdw5 = dlmonte.dlfield.VDW(atom4, atom4, int5)
    vdw6 = dlmonte.dlfield.VDW(atom4, atom5, int6)

    field.vdw.append(vdw1)
    field.vdw.append(vdw2)
    field.vdw.append(vdw3)
    field.vdw.append(vdw4)
    field.vdw.append(vdw5)
    field.vdw.append(vdw6)

    #the bonded interactions - dummies are used to demonstarte how it is done rather
    #than exclude all interactions
    bint1 = dlmonte.dlinteraction.InteractionBuckingham(0.0, 0.1, 0.0)
    bint2 = dlmonte.dlinteraction.InteractionBuckingham(0.0, 0.1, 0.0)
    bnd1 = dlmonte.dlfield.BondTwoBody(atom3, atom4, bint1)
    bnd2 = dlmonte.dlfield.BondTwoBody(atom4, atom4, bint2)
    field.bonds2body.append(bnd1)
    field.bonds2body.append(bnd2)

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
    title = "Control file for CO2 in zeolite"

    # this is the 'use' keyword for DL_MONTE - we are not using any here
    lines = []
    lines.append("use gaspressure")
    lines.append("finish use-block")
    dlstr = "\n".join(lines)
    use = dlmonte.dlcontrol.UseBlock.from_string(dlstr)

    #print(repr(use))

    #the main control commands
    d = OrderedDict()
    d['steps'] = 1000000
    d['temperature'] = 273.0
    d['maxmolrot'] = 0.005
    d['equilibration'] = 100000
    d['print'] = 1000
    #d['distewald'] = ""
    d['acceptmolmoveupdate'] =  200        # Period (in moves) at which the maximum move size is recalculated
    d['acceptmolrotupdate'] =  200
    d['stack'] = 100

    main = dlmonte.dlcontrol.MainBlock(d)

    #the movers are the MC moves
    movers = []
    mover = dlmonte.dlmove.parse_molecule("co2")
    movers.append(mover) 
    mmove = dlmonte.dlmove.MoleculeMove(20, movers)
    rmove = dlmonte.dlmove.RotateMoleculeMove(20, movers)

    gcmovers = []
    gcmover = dlmonte.dlmove.parse_molecule_gcmc("co2 0.0001")
    gcmovers.append(gcmover)
    gmove = dlmonte.dlmove.InsertMoleculeMove(60, 0.5, gcmovers)
    main.moves.append(mmove)
    main.moves.append(rmove)
    main.moves.append(gmove)

    #print("fabricated control")

    #create the instance of the control file
    cntrl = dlmonte.dlcontrol.CONTROL(title, use, main)

    #control file to stdout
    #print(cntrl)

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
cntrl.to_file()


#this follows the document doc/tutorial/util-dlmonte.html
#set the path to the DL_MONTE executable
DL_MONTE_HOME = "/home/jap93/DLMONTE3/DL_MONTE-2/bin/"
input_dir = "/home/jap93/DLMONTE3/dlmontepython_course/dlmontepython/examples/htk/co2_zeolite"


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

