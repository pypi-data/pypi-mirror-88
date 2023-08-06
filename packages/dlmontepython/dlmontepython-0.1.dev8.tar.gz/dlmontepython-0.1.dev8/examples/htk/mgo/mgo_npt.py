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

    #read the field file from a file
    filename = "FIELD.ORIGINAL"
    field = dlmonte.dlfield.from_file(filename)
    #print(repr(field1))

    return field


##############################################################################
# Produce the CONTROL file for the calculation
##############################################################################
def create_control_file():

    """ creates and writes out a control file for use in DL_MONTE using the HTK.
    The HTK defines the CONTROL as three parts: title, use_block and main_block
    The function niether takes input nor returns anything. TODO again put error checking in
    """

    #read the CONTROL file 
    filename = "CONTROL.ORIGINAL"
    ctrl = dlmonte.dlcontrol.from_file(filename)
    #print(dir(ctrl))

    return ctrl



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
cntrl.temperature = 700.0
#control file to stdout
temperature = cntrl.temperature
print(" I have updated temperature to ", temperature)
pressure = cntrl.pressure

if pressure is None:
    cntrl.pressure = 0.001
    pressure = cntrl.pressure

print(" I have an initial pressure of ", pressure)

cntrl.steps = 10000
cntrl.to_file()

#this follows the document doc/tutorial/util-dlmonte.html
#set the path to the DL_MONTE executable
DL_MONTE_HOME = "/home/jap93/DLMONTE3/DL_MONTE-2/bin/"
input_dir = "/home/jap93/DLMONTE3/dlmontepython/examples/htk/mgo"


#create the input
myinput = dlmonte.DLMonteInput.from_directory(input_dir)


dlx = os.path.join(DL_MONTE_HOME, "DLMONTE-SRL-VDW_dir-opt.X")

#starting pressure
press = 0.001

for i in range(10):                

    #create the control file with the desired pressure (in katms)
    pressuretag = {"pressure": press}
    myinput.control.pressure = press

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
