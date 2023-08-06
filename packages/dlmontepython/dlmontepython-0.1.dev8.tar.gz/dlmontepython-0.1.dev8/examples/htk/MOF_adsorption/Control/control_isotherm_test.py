# This is a barebones script to exemplify the control_setup module for creating an isotherm of DL_MONTE simulations
# It mostly uses the defaults in control_setup for the time being

from dlmontepython.examples.htk.MOF_adsorption.Control import control_setup as cs

# First,some initial parameters common to each simulation are defined, including the list of fugacities simulated.
GCMC_species_name = 'Nitrogen'
fugacities = [1000, 5000, 10000, 25000, 50000]  # Pa

iterations = 1e6
main_statement_dictionary = {'Temperature': 77, 'noewald': 'all'}

# Then, a dictionary is made, which we intend to populate with dlcontrol.CONTROL objects
isotherm_dict = {}

# After this, a loop is made across all fugacities considered
for fugacity in fugacities:
    title = 'Test nitrogen isotherm simulation at {0}Pa'.format(fugacity)

    dl_fugacity = fugacity * 1e-8  # kilobar, approx equals kilo atmosphere
    molecules_info = {'id': GCMC_species_name, 'molpot': dl_fugacity}

    experiment = cs.make_control_file(title=title,
                                      fed=None,
                                      fed_options={},
                                      molecules=molecules_info,
                                      main_statement_options=main_statement_dictionary,
                                      iterations=iterations)

    isotherm_dict[fugacity] = experiment

# Finally, a loop across the isotherm dictionary is used to print out files in the appropriate dictionaries.
for fugacity, control in isotherm_dict.items():
    experiment_directory = './testcontrol/{0}/{1}Pa'.format(GCMC_species_name, fugacity)
    cs.directorymaker(experiment_directory)

    with open('{0}/CONTROL'.format(experiment_directory), 'w') as f:
        f.write(str(control))
