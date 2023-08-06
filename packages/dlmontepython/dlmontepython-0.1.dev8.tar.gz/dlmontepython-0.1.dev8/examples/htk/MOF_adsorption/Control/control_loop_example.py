#  This is a barebones script to exemplify the control_setup module for creating a series of DL_MONTE CONTROL files.
#  This is useful, for instance, for running free-energy difference experiments over a sequence of windows
#  In the cirrent example, transition matrix methods are used, where each experiment partially fills in one such matrix
#
#  After running a loop such as this, we need to recombine the
# TODO: full summary of what I'm doing here
# TODO: better comments of what's going on at the right time
# TODO: more happily organised functions and variables

import numpy as np
from dlmontepython.examples.htk.MOF_adsorption.Control import control_setup as cs
import shutil

#  First,some initial parameters common to each simulation are defined, and directories made
GCMC_species_name = 'Nitrogen'
fugacity = 100e3  # Pa

path = './{0}/{1}Pa'.format(GCMC_species_name, fugacity)
cs.directorymaker(path)

minimum_guest_molecules = 0
maximum_guest_molecules = 1300

#  General dictionaries for each simulation file component are then written
dl_fugacity = fugacity * 1e-8  # kilobar, approx equals kilo atmosphere
general_main_statement_dictionary = {'Temperature': 298}
general_molecules_info = {'id': GCMC_species_name, 'molpot': dl_fugacity}
general_fed_options = {'xmax': maximum_guest_molecules + 0.5, 'xmin': minimum_guest_molecules - 0.5}

##########################################
#  Now we start to look at simulation specifics for the window-scanning simulations
scan_name = 'scan'  # part of the simulation title
windowspan = max(6, int(np.ceil(maximum_guest_molecules / 40)))  # The sizes of each individual window
stride = min(windowspan - 1, 10)  # The change in minimum_guest_molecule per window
scan_iterations = 1e6

#  Scan-specific dictionaries for each simulation file component are then written
scan_fed_options_loop = {'nout': scan_iterations, 'win': True, 'tri': 1}
scan_main_options_loop = {'print': scan_iterations}

#  Now we begin to generate the control file options across our scan
control_file_dictionary = {}

for count, i in enumerate(range(minimum_guest_molecules, maximum_guest_molecules - windowspan + 1, stride), 1):
    name = '{0}_{1}'.format(scan_name, count)
    print('Creating object {0}'.format(name))
    fed_options_per_run = {'winmax': i + windowspan + 0.5, 'winmin': i - 0.5}
    placeholder = cs.make_control_file(title='First scan - {}'.format(count),
                                       fed='tmatrix',
                                       fed_options={**general_fed_options, **scan_fed_options_loop,
                                                    **fed_options_per_run},
                                       molecules=general_molecules_info,
                                       main_statement_options={**general_main_statement_dictionary,
                                                               **scan_main_options_loop},
                                       iterations=scan_iterations)
    control_file_dictionary[name] = placeholder

print(len(control_file_dictionary))

#  We now create a taskfarm file, which will eventaully contain a list of our required simulations for the experiment
with open('{0}/taskfarm.{1}'.format(path, scan_name), 'w') as f:
    f.write('#!/bin/bash\n')

for name in control_file_dictionary.keys():
    cs.setup(name, control_file_dictionary, path, './templates/', GCMC_species_name)
    with open('{0}/taskfarm.{1}'.format(path, name), 'a+') as f:
        f.write('bash dlmonte.sh {0}\n'.format(name))

##########################################################################################
#  Next we start to look at simulation specifics for the window-combining simulation

cs.directorymaker('{0}/finalcombine'.format(path))
iterations_final = 1e4
fed_final = {'nout': int(iterations_final), 'win': None, 'mode': 'res'}

#  The control object is made, and put into a placegholder dictionary for use in cs.setup
final_scan = cs.make_control_file(title='Final simulation',
                                  fed='tmatrix',
                                  fed_options={**general_fed_options, **fed_final},
                                  molecules=general_molecules_info,
                                  main_statement_options=general_main_statement_dictionary,
                                  iterations=iterations_final)
placeholder_dict = {'finalcombine': final_scan}
cs.setup('finalcombine', placeholder_dict, path, './templates/', GCMC_species_name)

#########################################################
#  Finally, some cleanup steps are performed

#  A python file for combining tmatrix files together is moved into the experiment directory, and a runscript written
shutil.copy('{0}/tmatrix_combine.py'.format('templates'), '{0}/tmatrix_combine.py'.format(path))
with open('{0}/tm_combine.sh'.format(path), 'w') as f:
    f.write('#!/bin/bash\n')
    f.write('python tmatrix_combine.py -i ' +
            '/TMATRX '.join([i for i in control_file_dictionary.keys()]) +
            '/TMATRX -o finalcombine/ -f TM_final.dat')


#  Also, further batch runscripts are copied into the experiment directory
shutil.copy('{0}/dlmonte.sh'.format('templates'), '{0}/dlmonte.sh'.format(path))
shutil.copy('{0}/run.taskfarmer'.format('templates'), '{0}/run.taskfarmer'.format(path))
