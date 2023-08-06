# A set of factory functions for producing DL_MONTE 2.07 CONTROL files.
# The intended application of these functions is for adsorption in frameworks
# Each function has default settings to show Nitrogen adsorption at 77K
# TODO: proper docstrings for the functions
# TODO: umbrella and wanglandau FED method functions
# TODO: uncomment the sampling statements function, put in better defaults
# TODO: refactor all the dictionary things to make a but more sense (maybe?)
import errno
import random
from collections import OrderedDict
import dlmontepython.htk.sources.dlcontrol as control
import dlmontepython.htk.sources.dlfedmethod as fedmethod
import dlmontepython.htk.sources.dlfedorder as fedorder
import dlmontepython.htk.sources.dlfedflavour as fedflavour
import dlmontepython.htk.sources.dlmove as movetypes
import pathlib
import shutil
import os


def directorymaker(dxout="./"):
    '''
    A simple function for making new directories to write files into.
    This is probably superseded by pathlib.Path.mkdir(parents=True, exist_ok=True)
    :param dxout: (str) The path to the directory that you're aiming towards
    :return: Nothing
    '''
    filename = "{0}/test.txt".format(dxout)
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    with open(filename, "w") as f:
        f.write("FOOBAR")
    print("Directory written!")


def parameter_dict_update(dictionary, options):
    '''
    A function to update dlcontrol and related object parameters.
    These parameters are input as dictionaries of type {'variable': value}
    :param dictionary: (dict) default values from the factory function
    :param options: (dict) modified values included when invoking the functions
    :return dict: (dict) an updated input dictionary with new or changed {'variable': value} pairs
    '''
    for key, value in options.items():
        if key in dictionary.keys():
            print("Updating parameter {0} from {1} to {2}.".format(key, dictionary[key], value))
        else:
            print('Adding new parameter {0} with value {1}'.format(key, value))
        placeholder = {key: value}
        dictionary.update(placeholder)
    return dictionary


def setup(name, dictionary, directory='./', filesource='./templates/', species=None):
    '''
    This function sets up a DL_MONTE experiment in 'directory', using a dlcontrol object from a dictionary,
    and template FIELD/ CONFIG files from the directory filesource.
    This is useful when batch preparing multiple DL_MONTE simulations at once e.g. isotherm experiments,
    or FED-based experiments using windows.
    :param name: (str) They key of the dictionary containing your dlconfig item
    :param dictionary: (dict) the dictionary containing your dlconfig items
    :param directory: (str) the target directory for running your DL_MONTE experiment in
    :param filesource: (str) the directory to pull your template files from
    :param species: (str) an optional prefix to your template FIELD files, e.g. if you have one per sorbate in a library
    :return: nothing
    '''
    p = pathlib.Path('{0}/{1}'.format(directory, name))
    p.mkdir(parents=True, exist_ok=True)
    archive_p = pathlib.Path('{0}/{1}/archive'.format(directory, name))
    archive_p.mkdir(parents=True, exist_ok=True)
    move_files(filesource, p, species)
    tofile(name, dictionary, p)


def tofile(name, dictionary, todirectory):
    '''
    This function prints a DL_MONTE CONTROL file from a dlcontrol object, in the directory 'todirectory'.
     The dlcontrol obect is found inside a dictionary, to suit batch processing of multiple CONTROL files at once.
    :param name: (str) the key for your dlcontrol object dictionary
    :param dictionary: (dict) the dlcontrol object dictionary
    :param todirectory: (str) the path to the directory you're aiming to put the CONTROL file into.
    :return: nothing
    '''
    string = str(dictionary[name])
    with open('{0}/CONTROL'.format(todirectory), 'w') as f:
        f.write(string)


def move_files(origin, destination, species=None):
    '''
    This function moves template files from the directory 'origin' to directory 'destination'.
    There is an option for the prefix 'species' on the FIELD file, if yuo have a library of sorbate.FIELD files
    TODO: prefixes for CONFIG files?
    :param origin: (str) the directory your template files are stored in
    :param destination: (str) the directory your simulation will take place in
    :param species: (str) an optional prefix for FIELD files
    :return: nothing
    '''
    if species is not None:
        shutil.copy('{0}/{1}FIELD'.format(origin, species + '.'), '{0}/FIELD'.format(destination))
    else:
        shutil.copy('{0}/FIELD'.format(origin), '{0}/FIELD'.format(destination))
    shutil.copy('{0}/CONFIG'.format(origin), '{0}/CONFIG'.format(destination))


def make_tmatrix_block(**kwargs):
    """
    A factory function which produces a dlcontrol FEDBlock object from a dictionary of defaults and kwargs.
    To do this, dlfedorder, dlfedmethod, and dlfedflavour objects are all invoked according to the input dictionary
    For the kwargs, a dictionary of type {'variable': value} is expected
    :param kwargs: (dict) a dictionary of keywords and their values
    :return fed: (dlcontrol FEDBlock) an object to be used during initiation of a dlcontrol.USEBlock object
    """
    parameters = {'nout': 1e6,
                  'n_upd': 1e3,
                  'mode': 'new',
                  'name': 'nmols',
                  'xmin': -0.5,
                  'xmax': 10.5,
                  'npow': None,
                  'win': None,
                  'winmax': 0,
                  'winmin': -0.5,
                  'tri': True
                  }
    parameter_dict_update(parameters, kwargs)

    flavour = fedflavour.Generic()
    transmatrix = fedmethod.TransitionMatrix(parameters['nout'],
                                             parameters['n_upd'],
                                             parameters['mode'],
                                             parameters['tri']
                                             )
    orderparam = fedorder.FEDOrderParameter(parameters['name'],
                                            (parameters['xmax'] - parameters['xmin']),
                                            parameters['xmin'],
                                            parameters['xmax'],
                                            parameters['npow'],
                                            parameters['win'],
                                            parameters['winmin'],
                                            parameters['winmax']
                                            )
    fed = control.FEDBlock(flavour=flavour, method=transmatrix, orderparam=orderparam)
    return fed


def make_use_block(fed=None, **kwargs):
    """
    A factory function for creating a use block for input into a dlcontrol.CONTROL object
    For the kwargs, a dictionary of type {'variable': value} is expected
    TODO: reduce/remove defaults?
    :param kwargs: (dict) a dictionary of keywords and their values
    :param fed: (dlcontrol FEDBlock) a FED Block object made using a separate factory function
    :return Use: (dlcontrol USEBlock) a filled dlcontrol UseBlock object for use in a dlcontrol.CONTROL object
    """
    use_statements = OrderedDict()
    use_statements['gaspressure'] = None
    use_statements['ortho'] = None
    parameter_dict_update(use_statements, kwargs)
    Use = control.UseBlock(use_statements=use_statements, fed_block=fed)
    return Use


def make_main_statements(iterations=1e6, **kwargs):
    """
    This function arranges the 'main block statements', which are needed to initialise a dlcontrol.MainBlock object.
    It includes a number of defaults which relate simulation length to output printing, for convenience.
    For the kwargs, a dictionary of type {'variable': value} is expected
    :param iterations: (int) an integer number of iterations to be used
    :param kwargs: (dict) a dictionary of keywords and their values
    :return main_statements: (OrderedDict) an OrderedDict which feeds directly into the dlmonte MainBlock object
    """

    main_statements = OrderedDict()
    main_statements['seeds'] = '{0} {1} {2} {3}'.format(random.randint(1, 99),
                                                        random.randint(1, 99),
                                                        random.randint(1, 99),
                                                        random.randint(1, 99))
    main_statements['Temperature'] = 77
    main_statements['equilibration'] = 0
    main_statements["steps"] = iterations
    main_statements['check'] = int(min(iterations, max(iterations / 1000, 1000)))  # this feels messy
    main_statements["print"] = int(min(iterations, max(iterations / 1000, 1000)))
    main_statements["stack"] = int(min(iterations, max(iterations / 1000, 1000)))
    main_statements["yamldata"] = int(min(iterations, max(iterations / 1000, 1000)))
    main_statements['ewald prec'] = 1e-6
    main_statements['archiveformat'] = 'dlpoly4'
    main_statements["acceptatmmoveupdate"] = 200
    main_statements["acceptmolrotupdate"] = 200
    # should I be able to add ('archiveformat', 'dlpoly4') to this dictionary?

    parameter_dict_update(main_statements, kwargs)

    return main_statements


def make_sample_statements(iterations=1e6, species='Nitrogen', **kwargs):
    '''
    This function arranges the coordinate sampling statements, needed to initialise a dlcontrol.MainBlock object.
    Defaults are currently set to no sampling, with example values included but commented out.
    This is to prevent accidental creation of large trajectory files when none are required.
    Iterations is taken as an input, to relate simulation length to output printing for convenience.
    For the kwargs, a dictionary of type {'variable': value} is expected
    :param species:
    :param iterations: (int) an integer number of iterations to be used
    :param kwargs: (dict) a dictionary of keywords and their values
    :return samples: (OrderedDict) an OrderedDict which feeds directly into the dlmonte MainBlock object
    '''
    samples = OrderedDict()
    # samples['coords'] = {0: int(min(iterations, max(iterations / 100, 100))), 1: 'only {0}}'.format(species)}
    # samples['energies'] = {0: int(min(iterations, max(iterations / 100, 100)))}
    parameter_dict_update(samples, kwargs)
    return samples


def make_movers(molecules=None, **kwargs):
    """
    This is a function to produce a list of movetype objects for your simulation.
    Currently this is limited to rigid molecule GCMC - insert, translate, and rotate moves.
    It first prepares a list of molecule dictionaries and their potentials.
    Then, a 'moves' dictionary is generated with each movetype listed in.
    Finally, for each move, a corresponding movetypes object is made and appended to the output list.
    TODO: rewrite to make a bit more pythonic and cut out unnecessary intermediate steps
    TODO: Add in functionality for further MC move types (atom translate/rotate, id flips)
    :param molecules: (dict or list) sorbate molecules & chemical potential in the form [{'id': 'name', 'molpot' : mu}]
    :param kwargs: (dict) updates made to the default moves dictionary
    :return output: a list of movetypes objects, for use making a main block
    """
    output = []

    molecules_default = [{"id": 'Nitrogen', "molpot": 0.001}]
    if molecules is None:
        molecules = molecules_default
    elif isinstance(molecules, dict):
        molecules = [molecules]
    print('molecules list:',molecules)

    moves = {'insert': {'pfreq': 50, 'rmin': 0.7, 'movers': molecules},
             'move': {'pfreq': 25, 'movers': molecules},
             'rotate': {'pfreq': 25, 'movers': molecules}}
    parameter_dict_update(moves, kwargs)


    if moves['insert'] is not None:
        output.append(movetypes.InsertMoleculeMove(pfreq=moves['insert']['pfreq'],
                                                   rmin=moves['insert']['rmin'],
                                                   movers=moves['insert']['movers']))
    if moves['move'] is not None:
        output.append(movetypes.MoleculeMove(pfreq=moves['move']['pfreq'],
                                             movers=moves['move']['movers']))

    if moves['rotate'] is not None:
        output.append(movetypes.RotateMoleculeMove(pfreq=moves['rotate']['pfreq'],
                                                   movers=moves['rotate']['movers']))
    return output


def make_main_block(statements, moves, samples):
    """
    This is a simple function to make a dlcontol.MainBlock object, given 3 input OrderedDicts for the 3 sections
    :param samples: (OrderedDict) sampling keywords and their values (e.g. {'energies': 1e6})
    :param moves: (list) MC moves to simulate, each of which is a movetype object (e.g. movetypes.InsertMoleculeMove)
    :param statements: (orderedDict) main statement keywords and their values (e.g. {'iterations': 1.e6})
    :return: a dlmonte MainBlock object
    """
    return control.MainBlock(statements=statements, moves=moves, samples=samples)


def make_control_file(title = 'Test title',
                      fed = '',
                      molecules = 'Nitrogen',
                      use_options = None,
                      iterations=1e6,
                      main_statement_options = None,
                      main_moves_options = None,
                      main_samples_options = None,
                      fed_options = None):
    '''
    This function makes a complete dlcontrol.CONTROL objectready to be printed to file.
    The object preparation splits into 3 parts: FED, USE, and MAIN.
    For FED, a keyword is first read in, then the appropriate object is made using the factory function and fed_options.
    For USE, a dlcontrol.UseBlock is made with use_options for non-default settings.
    for MAIN, a dlcontrol.MainBlock is made with main_statement_options, main_moves_options, and main_samples_options.
    :param title: (str) The title to be written at the start of your control file
    :param fed: (str) a keyword for which free-energy difference method you plan to use
    :param molecules: (dict or list) sorbate molecules & chemical potential in the form [{'id': 'name', 'molpot' : mu}]
    :param use_options: (dict) a dictionary of keywords and their values for the use block
    :param iterations: (int) the number of iterations in your simulation
    :param main_statement_options: (dict) a dictionary of keywords and their values for the main statements
    :param main_moves_options: (dict) a dictionary of keywords and their values for the MC move statements
    :param main_samples_options: (dict) a dictionary of keywords and their values for the sampling statements
    :param fed_options: (dict) a dictionary of keywords and their values for the free-energy difference method (if used)
    :return: a dlcontrol.CONTROL object, which can be directly printed to file.
    '''
    if fed_options is None:
        fed_options = {}

    FED = None

    if fed is None:
        pass
    elif 'tmatrix' in fed:
        FED = make_tmatrix_block(**(fed_options or {}))
    elif 'umbrella' in fed:
        raise NotImplementedError
    elif 'wanglandau' in fed:
        raise NotImplementedError
    else:
        raise NotImplementedError

    USE = make_use_block(FED, **(use_options or {}))

    statements = make_main_statements(iterations, **(main_statement_options or {}))
    moves = make_movers(molecules, **(main_moves_options or {}))
    samples = make_sample_statements(iterations,molecules, **(main_samples_options or {}))
    MAIN = make_main_block(statements, moves, samples)

    return control.CONTROL(title=title, use_block=USE, main_block=MAIN)
