# This is a barebones script to exemplify the control_setup module for creating DL_MONTE CONTROL files.
# It mostly uses the defaults in control_setup, for the time being, and creates a working CONTROL file int he target dir

from dlmontepython.examples.htk.MOF_adsorption.Control import control_setup as cs

# First, we prepare the directory to be made, according tot he species being simulated and fugacity
GCMC_species_name = 'nitrogen'
fugacity = 100e3  # Pa
experiment_directory = './test/{0}/{1}Pa'.format(GCMC_species_name, fugacity)
cs.directorymaker(experiment_directory)

# Then, we define some of the main simulation parameters used in all simulations
title = 'Test nitrogen simulation'
iterations = 1e6
dl_fugacity = fugacity * 1e-8  # kilobar, approx equals kilo atmosphere

# After this, we throw in some non-default simulation options
# TODO: show further options available, to exemplify what can be changed
main_statement_dictionary = {'Temperature': 77, 'noewald': 'all'}
molecules_info = {'id': 'Nitrogen', 'molpot': dl_fugacity}

# Finally, a dlcontrol.CONTROL object is made with all of the options from above, and printed to file.
experiment = cs.make_control_file(title=title,
                                  fed=None,
                                  fed_options={},
                                  molecules=molecules_info,
                                  main_statement_options=main_statement_dictionary,
                                  iterations=iterations)

with open('{0}/CONTROL'.format(experiment_directory), 'w') as f:
    f.write(str(experiment))
