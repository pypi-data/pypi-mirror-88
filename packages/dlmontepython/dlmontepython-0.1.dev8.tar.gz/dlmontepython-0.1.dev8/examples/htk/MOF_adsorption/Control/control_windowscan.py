# This is Joe Manning's experiment setup file, which is a bit messy and complicated
#  Exemplar files are elsewhere in this directory, which will explain better what's going on

# TODO: full summary of what I'm doing here
# TODO: better comments of what's going on at the right time
# TODO: more happily organised functions and variables

import numpy as np
from dlmontepython.examples.htk.MOF_adsorption.Control import control_setup as cs
import shutil


#Key of N2 temps, pressures, and fugacities:
#77: 0.001 katm, 0.973 bar = 0.96e-3 katm
#87: 0.002701 katm, 2.519 bar = 2.49e-3 katm
#97: 0.00617 katm, 5.319 bar = 5.249e-3 katm
#107: 0.0122, 9.783 bar = 9.656e-3 katm
#117: 0.0214, 15.51 bar = 15.3e-3 katm
#127: 0.03456, 22.343 bar = 22.14e-3 katm

species = 'meoh'
path = './{0}/9000Pa'.format(species)
cs.directorymaker(path)
cs.directorymaker('{0}/finalcombine'.format(path))
xmin = 0
xmax = 1300 

general_main_statement_dictionary = {'Temperature': 298}
general_molecules_info = {'id': 'MeOH', 'molpot': 900e-7}
general_fed_options = {'xmax':xmax+0.5, 'xmin': xmin-0.5}

windowspan_1 = max(6, int(np.ceil(xmax/40)))
stride_1 =  min(windowspan_1-1, 10)
windowspan_2 = max(10, int(np.ceil(xmax/10)))
stride_2 = min(windowspan_2-1,20)
exploit_length=3e7
###########################################################################################
#loop one : small windows
scan_name_1 = 'scan1'
#windowspan_1 = 12
iterations_loop_1 = 1e6
fed_options_loop_1 = {'nout' : iterations_loop_1, 'win': True, 'tri': 1}
main_options_loop_1 = {'print': iterations_loop_1}
controldict_1 = {}
scan1names=[]
for count,i in enumerate(range(xmin, xmax-windowspan_1+1, stride_1), 1):
    name = '{0}_{1}'.format(scan_name_1, count)
    print('Creating object {0}'.format(name))
    fed_options_per_run = {'winmax': i + windowspan_1+0.5, 'winmin': i-0.5}
    placeholder = cs.make_control_file(title='First scan - {}'.format(count),
                                    fed='tmatrix',
                                    fed_options={**general_fed_options, **fed_options_loop_1, **fed_options_per_run},
                                    molecules=general_molecules_info,
                                    main_statement_options= {**general_main_statement_dictionary, **main_options_loop_1},
                                    iterations=iterations_loop_1)
    controldict_1[name]=placeholder
    scan1names.append(name)
print(len(controldict_1))
with open('{0}/taskfarm.{1}'.format(path, scan_name_1), 'w') as f:
    f.write('#!/bin/bash\n')

for i in scan1names:
    cs.setup(i, controldict_1, path,'./templates/', species)
    with open('{0}/taskfarm.{1}'.format(path, scan_name_1), 'a+') as f:
        f.write('bash dlmonte.sh {0}\n'.format(i))

##########################################################################################
#loop two : medium windows
scan_name_2 = 'scan2'
#windowspan_2 = 40
iterations_loop_2 = 1e7
fed_options_loop_2 = {'nout' : iterations_loop_2, 'win': True, 'mode' : 'res', 'tri': 1}
main_options_loop_2 = {'print': iterations_loop_2}
controldict_2 = {}
scan2names=[]
for count,i in enumerate(range(xmin, xmax-windowspan_2+1, stride_2), 1):
    name = '{0}_{1}'.format(scan_name_2, count)
    print('Creating object {0}'.format(name))
    fed_options_per_run_2 = {'winmax': i + windowspan_2+0.5, 'winmin': i-0.5}
    placeholder = cs.make_control_file(title='Second scan - {}'.format(count),
                                    fed='tmatrix',
                                    fed_options={**general_fed_options, **fed_options_loop_2, **fed_options_per_run_2},
                                    molecules=general_molecules_info,
                                    main_statement_options={**general_main_statement_dictionary,**main_options_loop_2},
                                    iterations=iterations_loop_2)
    controldict_2[name]=placeholder
    scan2names.append(name)
print(len(controldict_2))

with open('{0}/taskfarm.{1}'.format(path, scan_name_2), 'w') as f:
    f.write('#!/bin/bash\n')

for i in scan2names:
    cs.setup(i, controldict_2, path,'./templates/', species)
    with open('{0}/taskfarm.{1}'.format(path, scan_name_2), 'a+') as f:
        f.write('bash dlmonte.sh {0}\n'.format(i))
#########################################################################################
#loop three : no windows
iterations_loop_3 = exploit_length
scan_name_3 = 'exploit'
fed_options_loop_3 = {'nout' : int(iterations_loop_3/100), 'win': None, 'mode': 'res'}
main_options_loop_3 = {'print': iterations_loop_3}
controldict_3 = {}
scan3names=[]
for count,i in enumerate(range(1,17), 1):
    fed_options_per_run_3 = {}
    name = '{0}_{1}'.format(scan_name_3, count)
    print('Creating object {0}'.format(name))
    placeholder = cs.make_control_file(title='Third scan - {}'.format(count),
                                    fed = 'tmatrix',
                                    fed_options={**general_fed_options, **fed_options_loop_3, **fed_options_per_run_3},
                                    molecules=general_molecules_info,
                                    main_statement_options= {**general_main_statement_dictionary,**main_options_loop_3},
                                    iterations=iterations_loop_3)
    controldict_3[name]=placeholder
    scan3names.append(name)
print(len(controldict_3))
with open('{0}/taskfarm.{1}'.format(path, scan_name_3), 'w') as f:
    f.write('#!/bin/bash\n')

for i in scan3names:
    cs.setup(i, controldict_3, path,'./templates/', species)
    with open('{0}/taskfarm.{1}'.format(path, scan_name_3), 'a+') as f:
        f.write('bash dlmonte.sh {0}\n'.format(i))

#######################################################################

cs.directorymaker('{0}/finalcombine'.format(path))
iterations_final = 1e4
fed_final = {'nout' : int(iterations_final), 'win': None, 'mode': 'res'}
final_scan = cs.make_control_file(title='Final simulation',
                                    fed = 'tmatrix',
                                    fed_options={**general_fed_options, **fed_final},
                                    molecules=general_molecules_info,
                                    main_statement_options=general_main_statement_dictionary,
                                    iterations=iterations_final)
placeholder_dict = {'finalcombine':final_scan}
cs.setup('finalcombine', placeholder_dict, path,'./templates/', species)


with open('{0}/tm_combine_1.sh'.format(path), 'w') as f:
    f.write('#!/bin/bash\n')
    f.write('python tmatrix_combine.py -i ' + '/TMATRX '.join(scan1names) + '/TMATRX -o ' + '/ '.join(scan2names) + '/ -f TM_1.dat')

with open('{0}/tm_combine_2.sh'.format(path), 'w') as f:
    f.write('#!/bin/bash\n')
    f.write('python tmatrix_combine.py -i ' + '/TMATRX '.join(scan2names) + '/TMATRX -o ' + '/ '.join(scan3names) + '/ -f TM_2.dat')

with open('{0}/tm_combine_3.sh'.format(path), 'w') as f:
    f.write('#!/bin/bash\n')
    f.write('python tmatrix_combine.py -i ' + '/TMATRX '.join(scan3names) + '/TMATRX -o finalcombine/ -f TM_final.dat')


shutil.copy('{0}/dlmonte.sh'.format('templates'), '{0}/dlmonte.sh'.format(path))
shutil.copy('{0}/run.taskfarmer'.format('templates'), '{0}/run.taskfarmer'.format(path))
shutil.copy('{0}/tmatrix_combine.py'.format('templates'), '{0}/tmatrix_combine.py'.format(path))
shutil.copy('{0}/DLMONTE-SRL.X'.format('templates'), '{0}/DLMONTE-SRL.X'.format(path))
