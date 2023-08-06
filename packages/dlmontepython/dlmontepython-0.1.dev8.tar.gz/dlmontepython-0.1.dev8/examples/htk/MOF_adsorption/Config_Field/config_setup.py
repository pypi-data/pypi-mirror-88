''' A python script for producing dl_monte monte carlo simulations inside a framework.
Using ASE, it starts by reading in a file (e.g. a .cif for a dftb .gen file).
Then, it creates a supercell according to the minimum image convention.
Using a predefined dictionary of atom name tags, it assigns types consistent with a FIELD file.
It spits out the maxatom value for a FIELD file, then writes a CONFIG object from dlmonte
'''

import errno
from ase import Atoms
from ase.visualize import view
from math import sqrt, ceil
from ase.io import read
from itertools import combinations, combinations_with_replacement
import numpy as np
from sklearn.neighbors import KernelDensity
from scipy.signal import argrelextrema
from sys import exit
import dlmontepython.htk.sources.dlconfig as CONFIG
import dlmontepython.htk.sources.dlfield as FIELD
import dlmontepython.htk.sources.dlfieldspecies as FIELDSPECIES
import dlmontepython.htk.sources.dlinteraction as INT
import matplotlib.pyplot as plt
import os


# TODO: function docstrings
# DONE: tag assignment functions - by charge and distance criteria (and working together!)
# TODO: god functions for uncharged/singly charged framework, multiply charged framework (with/out automatic charge assignment)
# DONE: make dlconfig objects
# DONE: make dlfield objects
# TODO: fix the funcitons defining the LJ_interactions - tags by ase atomtypes?
# I could totally work that out somehow, but with a catch fro the number = 8 and tag include Zn
# In fact, I think it's done now? Needs tests...


def directorymaker(dxout="./"):
    """
    A simple function for making new directories to write files into.
    This is probably superseded by pathlib.Path.mkdir(parents=True, exist_ok=True)
    :param dxout: (str) The path to the directory that you're aiming towards
    :return: Nothing
    """
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

#######################################################################################################################
# The following functions all pertain to importing a framework file into ASE
# It then manipulates the charges and tags in such a way that the framework can be used by DL_Monte as a molecule
# Realistically, it's a very overcomplicated way of automatically splitting all atoms down into the following way:
# [Element]_[index of LJ parameters]_[index of charge state]
#######################################################################################################################


def read_framework(filename, directory='./', cell_params=None):
    '''
    This function reads in your framework from an ASE-compatible file format (.xyz, .cif, .gen, etc.)
    If the file has no unit cell information, there is an optional argument 'cell_params.'
    Cell parameters are needed for defining the simulation periodic boundaries, so if none are present the script exits.
    :param filename: (str) the name of the framework molecule file, including suffix
    :param directory: (str) the name of the directory in which your framework file is in, defaults to current directory
    :param cell_params: (numpy ndarray) 3-d unit cell vectors a, b, and c, in the format [[a],[b],[c]]
    :return struct: (ASE.Atoms) an object which contains all element types and positions, to manipulate into a CONFIG file
    '''
    struct = read('{0}{1}'.format(directory, filename))
    if not struct.cell:
        if cell_params == None:
            print('Uh-oh! There\'s no cell parameters we can use!'
                  'Please check the input file or define a list of cell perameters then try again')
            exit()
        else:
            struct.cell = cell_params
    return struct


def read_charges_from_dftb(filename, directory='./'):
    '''
    This function reads in charges from a dftb+ "detailed.out" file to a list.
    If you read in the dftb+ .gen file from the same source, the list and Atoms object have corresponding order.
    You can then use the Atoms.set_initial_charges(charges) method to install charges onto your framework.
    This allows dftb+ to be used to generate starting configuratinos and charges for a DL_MONTE simulation
    :param filename: (str) the name of the framework molecule file, including suffix
    :param directory: (str) the name of the directory in which your framework file is in, defaults to current directory
    :return charges: (list) a list of charge values for all of the atoms in the file, in original order
    '''
    alldata = []
    with open('{0}{1}'.format(directory, filename)) as f:
        for line in f.readlines()[14:]:
            alldata.append(line.split())
    charges = []
    line = 0
    while len(alldata[line]) > 0:
        charges.append(float(alldata[line][-1]))
        line += 1
    return charges


def make_framework_indices(struct):
    '''
    This function creates a dictionary of indices in your ASE.Atoms framework.
    For each element type in the framework, a key is made corresponding to the element number.
    This has values 'symbol' (the element symbol as a string), and 'idx_mask'
    idx_mask is an ndarray which is true when the Atoms index == your element, otherwise false
    :param struct: (ASE.Atoms) your framework as an ASE Atoms object
    :return structure_dictionary: (dict) a dictionary of element types, symbols, and their corresponding indices
    '''
    element_types = np.unique(struct.numbers)
    print('Element types detected:',element_types)
    structure_dictionary = {}
    for i in element_types:
        structure_dictionary[i] = {}
        idx_mask = struct.numbers == i
        assert len(idx_mask) == len(struct)
        structure_dictionary[i]['symbol'] = struct[np.where(idx_mask)[0][0]].symbol
        structure_dictionary[i]['idx_mask'] = idx_mask
    return structure_dictionary


def framework_charges(struct, charges=[], tol=None):
    '''
    This simple function takes in your structure as an ASE.Atoms object and list of charges.
    It optionally rounds all the items in the list of charges according to your tolerances
    Then, assuming the charges and structure have the same length, it applies the charges to the structure

    :param struct: (ASE.Atoms) your framework structure as an ASE.Atoms object
    :param charges: (list) a list of charges for each atom in your structure, in theh same order as struct
    :param tol: (int) the number of decimal places to round your charges to, defaults to non-rounded
    :return struct: (ASE.Atoms) the same structure as was input, but with atom charges according to the charges list
    '''
    if tol is not None:
        charges = [round(i, tol) for i in charges]
        assert len(struct) == len(charges)
    struct.set_initial_charges(charges)
    return struct


def assign_sub_tags_by_charge(struct, indices, element, name, tag_counter):
    '''
    This function assigns tags to your ase object, according to the number of unique charge states present.
    It takes the framework structure (struct), and first finds each unique charge in the index list.
    Then, for each unique charge state, it adds a new tag to the Atoms object.
    This tag then corresponds to a dictionary key, whose value is the string written to DL_MONTE as the atom type.

    Realistically, it's a very overcomplicated way of automatically splitting all atoms down into the following way:
    [Element]_[index of LJ parameters]_[index of charge state]

    :param struct: (ASE.Atoms) your framework structure as an ASE.Atoms object
    :param indices: (ndarray) ndarray which is true when the Atoms index == your element/moeity, otherwise false
    :param element: (int) the atomic number of your element/moiety of choice
    :param name: (str) the name of your element/moiety of choice e.g. O_COOH
    :param tag_counter: (int) a counter for the number of tags assigned already
    :return sub_tag_dict: (dict) a dictionary which connects ASE.Atoms tags of struct to a string for DL_Monte
    :return sub_tag_list: (ndarray) A list of the same length as struct, with the assigned tag values in it
    :return tag_counter: (int) a counter to make sure there's no duplication of ASE.Atoms.tag values between objects
    '''
    sub_tag_list = np.zeros_like(struct)
    sub_tag_dict = {}
    assert len(indices) == len(struct)
    charge_states = np.unique(struct[indices].get_initial_charges())
    for count, k in enumerate(charge_states):
        k_indices = (struct.get_initial_charges() == k) & (struct.numbers == element) & (indices == True)
        # NB this doesn't protect against 2 atom types having exactly the same charge. How do I do that?
        # But also, is it a problem if the same element has the same charge type? isn't that what I'm trying to do here?
        if len(charge_states) > 1:
            sub_tag_dict[tag_counter] = '{0}_{1}'.format(name, count)
        else:
            sub_tag_dict[tag_counter] = '{0}'.format(name)
        sub_tag_list[k_indices] = tag_counter
        tag_counter += 1
    return sub_tag_dict, sub_tag_list, tag_counter


def assign_all_framework_tags(struct, structure_dictionary, element_label_addition='S'):
    '''
    This parent function takes in an ASE.Atoms framework structure and assigns unique tags to each atom type
    Atom types are subdivided by Lennard Jones rules ('moieties') and coulombic point charges, and so are tags
    It takes in a structure, the structure dictionary (cf. make_framework_indices), and a string to signify it's a sorbent

    Based on the element and option moiety subdivision in the structure dictionary, tags are assigned to unique charges
    A list of unique tags is then made (tag_list) which can be applied directly on the to structure ASE.Atoms object
    This corresponds to keys in a dictionary (tag_dict), which can be read when writing a DL_MONTE FIELD and CONFIG file

    :param struct: (ASE.Atoms) your framework structure as an ASE.Atoms object
    :param structure_dictionary: (dict) a dictionary of element types, symbols, and their corresponding indices
    :return tag_dict: (dict) a dictionary which connects ASE.Atoms tags of struct to a string for DL_Monte
    :return tag_list: (ndarray) a list of the same length as struct, with the assigned tag values in it
    '''
    tag_list = np.zeros_like(struct)
    tag_dict = {}
    tag_counter = 1
    for element, element_dict in structure_dictionary.items():
        print('Making tags for element', element)
        if 'moieties' in element_dict.keys():
            print('Subdividing element {0} into {1} moieties'.format(element, len(element_dict['moieties'])))
            for moiety, indices in element_dict['moieties'].items():
                print('Making tags for element', moiety)
                print('Assigning tag', tag_counter)
                subtag_dict, subtag_list, tag_counter = assign_sub_tags_by_charge(struct, indices, element, moiety,
                                                                                  tag_counter)
                tag_dict = {**tag_dict, **subtag_dict}
                tag_list += subtag_list
        else:
            print('Assigning tag', tag_counter)
            indices = element_dict['idx_mask']
            moiety = '{0}_{1}'.format(element_dict['symbol'], element_label_addition)
            subtag_dict, subtag_list, tag_counter = assign_sub_tags_by_charge(struct, indices, element, moiety,
                                                                              tag_counter)
            tag_dict = {**tag_dict, **subtag_dict}
            tag_list += subtag_list
    print('Final tag assignments:',tag_dict)
    return tag_dict, tag_list


def classify_elements_by_distance(struct, test_index_list, threshold, compare_index_list=None):
    '''
    This function can be used to sort elements from a structure according to moiety types.
    It does this by distance-sorting all instances of an element to differentiate them.
    E.g. to separate O in Zn4O and COO oxygen in MOF-5, the distance from the closest C can be used to differentiate them

    To do this, first the ASE.Atoms struct object is read in. An ndarray of indices of the test elements is then read in
    A list of elements to compare with is then read, alternatively the test indices are compared against everything else
    Finally, it takes a threshold distance in, separating into lists of atoms whose distance is higher or lower

    :param struct: (ASE.Atoms) your framework structure as an ASE.Atoms object
    :param test_index_list: (ndarray) a list of the same length as struct, where the test atoms evaluate to True
    :param threshold: (float) the threshold distance for sorting, nominally in Angstrom
    :param compare_index_list: (ndarray) as test_index_list, but where only the comparison atoms evaluate to True
    :return higher: (ndarray) as test_index_list, where the test atoms further than threshhold value evaluate to True
    :return lower: (ndarray) as test_index_list, where the test atoms closwer than threshhold value evaluate to True
    '''

    higher_list = np.zeros_like(struct, dtype=bool)
    lower_list = np.zeros_like(struct, dtype=bool)

    test_positions = struct[test_index_list].positions
    if compare_index_list is None:
        compare_index_list = struct.numbers != struct[test_index_list][0].number
    compare_positions = struct[compare_index_list].positions
    print(len(test_positions))
    for i, pos_i in zip(np.where(test_index_list)[0], test_positions):
        distance = np.linalg.norm(pos_i - compare_positions, axis=1)
        #print(round(min(distance),2), threshold, min(distance) < threshold) # Sanity check
        if min(distance) < threshold:
            lower_list[i] = 1
        else:
            higher_list[i] = 1

    assert len(test_positions) == (len(np.where(higher_list)[0]) + len(np.where(lower_list)[0]))
    return higher_list, lower_list


def get_charge_modes(struct, test_indices):
    '''
    Raw outputs from ab initio calculations may show chemically equivalent atoms as having marginally different charges.
    The purpose of this function is to automagically identify those atoms, and group them together.
    It uses kernel density estimation and the Silverman rule of thumb for bandwidth selection (ISBN 978-0-412-24620-3)
    From this, a probability density function of charge states is estimated.
    Peaks correspond to modal charge values, and troughs to separations between charge modes
    Finally very similar minima and maxima are condensed, to stop functionally identical charges from being separated.

    :param struct: (ASE.Atoms) your framework structure as an ASE.Atoms object
    :param test_indices: (ndarray) a list of the same length as struct, where the test atoms evaluate to True
    :return mi: (list) a list of minima values from the kde probability density function
    :return ma: (list) a list of maxima values from the kde probability density function
    '''
    chg = [i for i in struct[test_indices].get_initial_charges()]

    if len(np.unique(chg)) == 1:
        return [], np.unique(chg)
    h = 0.9 * min(float(np.std(chg)),
                  float(np.percentile(chg, 75) - np.percentile(chg, 25)) / 1.34) * len(chg) ** -0.2
    if h <= 0:
        h = 1
    chg2 = np.array([i for i in chg]).reshape(-1, 1)
    kde = KernelDensity(kernel='gaussian', bandwidth=h).fit(chg2)
    s = np.linspace(min(chg), max(chg))
    e = kde.score_samples(s.reshape(-1, 1))

    minima, maxima = argrelextrema(e, np.less)[0], argrelextrema(e, np.greater)[0]
    for i in range(1, len(minima)):
        if minima[i] - minima[i - 1] < 0.005:
            np.delete(minima, i)
    for i in range(1, len(maxima)):
        if maxima[i] - maxima[i - 1] < 0.005:
            np.delete(maxima, i)


    mi = [i for i in s[minima]]
    ma = [i for i in s[maxima]]
    return mi, ma


def assign_charge_states(struct, test_indices, minima, maxima):
    '''
    This function takes in a probaility density function of charges on a structure, condenses them, then collates them.
    It starts by loading in a structure and a list of test atoms (i.e. all instances of an element).
    It then loads in the minima and maxima from get_charge_modes, cleans the lists, then sorts test atoms into intervals
    The charges on these atoms is then averages, and added to an ndarray of the new charges, for assinging to struct

    :param struct: (ASE.Atoms) your framework structure as an ASE.Atoms object
    :param test_indices: (ndarray) a list of the same length as struct, where the test atoms evaluate to True
    :param minima: (list) a list of minima values from the kde probability density function
    :param maxima: (list) a list of maxima values from the kde probability density function
    :return newcharges: (ndarray) a list of the same length as struct, with condensed charge values corr. atom index
    '''

    # Brief summary of cleaning the lists mi and ma:
    # number of target values  = number of minima +1
    # minima, maxima conditions:
    # len(maxima) == 1 and len(minima) == 0 -> single modal charge
    # len(maxima) < len(minima) -> include extreme charge values from struct
    # len(maxima) == len(minima) -> include one extreme charge value from struct (so mi has a larger range than ma)
    # len(maxima) > len(minima) -> working as intended (each interval 0...minima...max has 1 maximum)
    #
    # So the plan is: make a list of intervals (0... minima... max)
    # then modal charges are chg[maxima]
    # Find indices which fall in the interval using boolean logic
    # Assign modal charges to be the correct atoms.
    # This didn't conserve charge though, so we just average the charge of all atoms within an interval
    chg = struct[test_indices].get_initial_charges()
    print(len(chg))
    extreme1 = min(chg)
    extreme2 = max(chg)
    print(extreme1, extreme2)
    if len(minima) == 0 and len(maxima) == 0:
        newcharges = struct[test_indices].get_initial_charges()
        print(len(newcharges))
        return newcharges
    elif len(minima) == 0 and len(maxima) == 1:
        for i in struct[test_indices]:
            i.charge = float(maxima[0])
        print('Kernel density estimation found a monomodal distribution of charges. all charges set to {}'.format(
            round(float(maxima[0]), 3)))
        newcharges = np.zeros_like(struct)
        newcharges[test_indices] = maxima[0]
        return newcharges
    elif len(minima) > len(maxima):
        # both extreme charge values are needed to have enough modal values
        # Add extreme charge values to chg[maxima]
        modal_charges = sorted([*maxima, extreme1, extreme2])
    elif len(minima) == len(maxima):
        # one extreme charge value is needed to have enough modal values
        # use logic to work out if the missing modal charge is the biggest or smallest value in chg
        # then add chg.max or chg.min, depending
        if max(minima) > max(maxima):
            modal_charges = sorted([*maxima, extreme2])
        elif min(minima) < min(maxima):
            modal_charges = sorted([*maxima, extreme1])
        else:
            print(
                'Uh-oh! The author is bad at boolean logic and as a result something\
                 has gone horribly wrong in the automatic charge assignment functions!')
            newcharges = struct[test_indices].get_initial_charges()
            print(len(newcharges))
            return newcharges
    elif len(minima) < len(maxima):
        # Niether extreme value is needed to have enough modal values
        modal_charges = sorted(maxima)
    else:
        print(
            'Uh-oh! This condition wasn\'t meant to happen!\
             Something has gone horribly wrong in the automatic charge assignment functions!')

    # Now the minima and maxima lists have been cleaned, we can start to assign atom indices within those intervals
    interval_edges = sorted([extreme1, extreme2, *minima])
    print('interval edges: ', interval_edges)
    print('modal charges: ', modal_charges)
    modal_charges_2 = np.array(modal_charges)

    #Now we make our charge index list
    oldcharges = struct.get_initial_charges()
    newcharges = np.zeros_like(struct)
    for i in range(1, len(interval_edges)):
        atoms_in_interval = np.where(interval_edges[i - 1] <= oldcharges, True, False) &\
                            np.where(oldcharges <= interval_edges[i], True, False) &\
                            np.where(test_indices, True, False)
        print(len(np.where(atoms_in_interval)[0]))
        print('max charge:', max(oldcharges[atoms_in_interval]),\
              '; min charge:', min(oldcharges[atoms_in_interval]),\
              '; mean (assigned) charge:',np.mean(oldcharges[atoms_in_interval]))
        assigned_charge = np.mean(oldcharges[atoms_in_interval])
        newcharges[atoms_in_interval] = assigned_charge

    # Finally, we want to show charge is conserved
    print('change in overall charge: ', round(sum(newcharges) - sum(struct[test_indices].get_initial_charges()), 4))
    print('~~~~~~~~~~~')
    return newcharges


def condense_similar_charges(ase_molecule, index_list):
    '''
    This short function combines the actions of get_charge_modes and assign_charge_states.
    It takes in a structure with potential differences in charges of equivalent atoms (e.g. from ab initio simulations)
    Then it uses kernel density estimation in get_charge_states to identify modal charge values
    These are then assigned to an ndarray of charge values to be re-cast onto the structure ASE.Atoms object

    :param ase_molecule: (ASE.Atoms) an ASE.Atoms object for one of your simulation molecules
    :param index_list: (ndarray) a list of the same length as struct, where the test atoms evaluate to True
    :return output: (ndarray) a list of the same length as struct, with condensed charge values corr. atom index
    '''
    minima, maxima = get_charge_modes(ase_molecule, index_list)
    output = assign_charge_states(ase_molecule, index_list, minima, maxima)
    return output

######################################################################################################################
# The following functions all pertain to making DL_Monte Config file from a set of ASE.Atoms molecules
# They need the names of the molecules you're using as well as tag dictionaries for unique atomtypes
#######################################################################################################################

def config_atoms_stringify(ase_molecule, tag_dict):
    '''
    This short function makes an appropriate molecule string for a CONFIG.CONFIG object.
    For each atom in the molecule, the atom name and DL_MONTE tag 'core' is added on line 1
    On line 2, the cartesian coordinates of the atom is then printed.

    :param ase_molecule: (ASE.Atoms) an ASE.Atoms object for one of your simulation molecules
    :param tag_dict: (dict) a dictionary which connects ASE.Atoms tags of struct to a string for DL_Monte
    :return output: (str) a string of the molecule positions for a DL_monte CONFIG.CONFIG object
    '''
    output = []
    for i in ase_molecule:
        counter = i.tag
        output.append('{0} core\n {1} {2} {3} 0'.format(tag_dict[counter], i.position[0], i.position[1], i.position[2]))
    return output


def config_molecule_dict_maker(ase_molecule, tag_dict, molecule_name):
    '''
    This function creates a dictionary of all the information you need to write a molecule to a CONFIG.CONFIG object

    :param ase_molecule: (ASE.Atoms) an ASE.Atoms object for one of your simulation molecules
    :param tag_dict: (dict) a dictionary which connects ASE.Atoms tags of struct to a string for DL_Monte
    :param molecule_name: (str) the name of your molecule in the DL_Monte Field file
    :return output: (dict) a dictionary of all of the key information about your molecule to make a CONFIG.CONFIG object
    '''
    output = {}
    output['name'] = molecule_name
    output['natom'] = len(ase_molecule)
    output['atoms'] = config_atoms_stringify(ase_molecule, tag_dict)
    return output


def make_config_empty_framework(ase_molecule, tag_dict, name, max_molecules=[1000, 1000]):
    '''
    This function makes a CONFIG.CONFIG object for an empty framework, ready for adsorption simulation.
    NB this could be fairly easily extended to handle multiple starting molecules, but that's a job for another day

    :param ase_molecule: (ASE.Atoms) an ASE.Atoms object for one of your simulation molecules
    :param tag_dict: (dict) a dictionary which connects ASE.Atoms tags of struct to a string for DL_Monte
    :param name: (str) the name of your molecule in the DL_Monte Field file
    :param max_molecules: (list) max num. of each molecule type in your simulation. Default for single adsorption sims
    :return empty_box: (CONFIG.CONFIG) a DL_monte CONFIG.CONFIG object ready to print to a file
    '''
    molecules_list = [config_molecule_dict_maker(ase_molecule, tag_dict, name)]
    molecule_numbers = [len(molecules_list), *max_molecules]
    empty_box = CONFIG.CONFIG(name,
                              0,
                              1,
                              ase_molecule.cell,
                              molecule_numbers,
                              molecules_list)
    return empty_box


######################################################################################################################
# The following functions all pertain to making DL_Monte FIELD file from a set of ASE.Atoms molecules
# They need the names of the molecules you're using, tag dictionaries for unique atomtypes, and LJ interaciton params
# To simplify(?) things, it uses molecule dictionaries containing all of this information:
#       {'name': (str) the molecule name,
#       'molecule':(ASE.Atoms) the Atoms object for the molecule,
#        'tags': (dict) the tag_dict for the molecule,
#        'LJ_by_tag': (dict) a dict of {tag: [eps, sigma, q]...}}
#######################################################################################################################

def get_maxatom_moltype(name, ase_molecule):
    '''
    This function takes an ASE.Atoms object along with a name and makes a FIELDSPECIES.Moltype object for it
    The object suits a MAXATOM type molecule i.e. a rigid framework-style molecule with no self-interactions.

    :param name: (str) the name of your DL_Monte molecule, as written in the FIELD file
    :param ase_molecule: (ASE.Atoms) an ASE.Atoms object for one of your simulation molecules
    :return: (FIELDSPECIES.MolType) a MAXATOM molecule object ready to be put into a DL_Monte FIELD.FIELD object
    '''
    return FIELDSPECIES.MolType(name, len(ase_molecule))


def get_field_rigid_molecule(name, ase_molecule, tag_dict):
    '''
    This function takes in a molecule as an ASE.Atoms object and returns it as a rgid molecule for a FIELD.FIELD object

    :param name: (str) the name of your DL_Monte molecule, as written in the FIELD file
    :param ase_molecule: (ASE.Atoms) an ASE.Atoms object for one of your simulation molecules
    :param tag_dict: (dict) a dictionary which connects ASE.Atoms tags of struct to a string for DL_Monte
    :return output: (FIELDSPECIES.MolType) a molecule object ready to be put into a DL_Monte FIELD.FIELD object
    '''
    output = FIELDSPECIES.MolType(name, len(ase_molecule))
    output.rigid = True
    output.exc_coul_ints = True
    output.atoms = get_field_atoms(ase_molecule, tag_dict)
    return output


def get_field_atomtype(ase_molecule, tag, name):
    '''
    This function creates an Atomtype entry for an individual atom type from your simulation molecule ASE.Atoms objects
    For a given tag, it identifies from the ASE.Atoms object the atom mass and charge, then invokes an Atomtype object

    :param name: (str) the name of your DL_Monte atom, as written in tag_dict
    :param ase_molecule: (ASE.Atoms) an ASE.Atoms object for one of your simulation molecules
    :param tag_dict: (dict) a dictionary which connects ASE.Atoms tags of struct to a string for DL_Monte
    :return: (FIELDspecies.Atomtype) An atomtype object for puttin ginto the Atomtypes section of a FIELD.FIELD object
    '''
    tag_mask = ase_molecule.get_tags() == tag
    if np.any(tag_mask):
        test_atom = ase_molecule[tag_mask][0]
    else:
        print('Something weird has happened and you have a tag with no assigned atoms!')
        print('Better check your python script!')
        exit()
    return FIELDSPECIES.AtomType(name,
                          'core',
                          test_atom.mass,
                          round(test_atom.charge, 5))


def get_field_atomtypes(ase_molecule, tag_dict):
    '''
    This function creates a list of FIELDSPECIES.Atomtype objects for a whole molecule, covering each unique atom type

    :param ase_molecule: (ASE.Atoms) an ASE.Atoms object for one of your simulation molecules
    :param tag_dict: (dict) a dictionary which connects ASE.Atoms tags of struct to a string for DL_Monte
    :return output: (list) a list of FIELDSPECIES.Atomtype objects corresponding to the whole molecule
    '''
    output = []
    for tag, name in tag_dict.items():
        output.append(get_field_atomtype(ase_molecule, tag, name))
    return output


def get_field_atoms(ase_molecule, tag_dict):
    '''
    This function takes in the positions of each atom within one of your simulation molecules.
    It then returns a list of FIELDSPECIES.Atom objects, useful for making a FIELDSPECIES.Molecule object

    :param ase_molecule: (ASE.Atoms) an ASE.Atoms object for one of your simulation molecules
    :param tag_dict: (dict) a dictionary which connects ASE.Atoms tags of struct to a string for DL_Monte
    :return output: (list) a list of FIELDSPECIES.Atom objects which go into a FIELDSPECIES.Molecule object
    '''
    output = []
    site = None
    for i in ase_molecule:
        output.append(FIELDSPECIES.Atom(
            tag_dict[i.tag],
            'core',
            i.position[0],
            i.position[1],
            i.position[2],
            i.mass,
            i.charge,
            site
        ))
    return output


def get_field_molecule(name, ase_molecule, tag_dict):
    '''
    This function takes in an ASE.Atoms molecule object, its name, and a dictionary of the atom tags for DL_Monte
    It then creates a FIELDSPECIES.Molecule object defining the initial atom positions for your FIELD.FIELD object

    :param name: (str) the name of your DL_Monte molecule, as written in the FIELD file
    :param ase_molecule: (ASE.Atoms) an ASE.Atoms object for one of your simulation molecules
    :param tag_dict: (dict) a dictionary which connects ASE.Atoms tags of struct to a string for DL_Monte
    :return output: (FIELDSPECIES.Molecule) a FIELDSPECIES.Molecule object defining your molecule for the FIELD.FIELD object
    '''
    output = FIELDSPECIES.Molecule(name)
    atoms_list = get_field_atoms(ase_molecule, tag_dict)
    for i in atoms_list:
        output.add_atom(i)
    return output


def get_vdw_interactions(moldict_1, moldict_2=None, self_exclusion_moldict=None):
    '''
    This function creates a set of Van der Waals interactions for a FIELD.FIELD object.
    First, it takes in a moldict consisting of the following information:
        {'name': (str) the molecule name,
        'molecule' (ASE.Atoms) the Atoms object for the molecule,
        'tags': (dict) the tag_dict for the molecule,
        'LJ_by_tag': (dict) a dict of {tag: [eps, sigma, q]...}}

    It can optionally take in a moldict of a second species to get interaciton sof both species with one another
    Finally, it can take in a moldict for a molecule whose self LJ-interactions you want to exclude i.e. your framework

    Based on these moldicts, it creates a list of all atom pairs minus the self_exclusion atompairs
    It then calculates the Lorentz-Berthelot mixing interactions between these atom pairs.
    For each atompair, it creates an INT.InteractionLJPlus object followed by a FIELD.VDW object from this
    It finally returns a list of FIELD.VDW objects used to make a FIELD.FIELD file


    TODO: Split this up into smaller constituent functions, for better future flexibility
    TODO: instead of explicitly moldict_1 and moldict_2, make it a list to allow flexible numbers of molecules
    :param moldict_1: (dict) a dictionary containing all the key information about your simulaiton molecule
    :param moldict_2: (dict) as moldict_1, if you want multiples
    :param self_exclusion_moldict: (dict) as moldict_1, if you want to exclude self-interactions for a molecules
    :return output: (list) a list of FIELD.VDW objects used for making a FIELD.FIELD file
    '''
    output = []
    interactions_by_name = {}
    exclusion_interactions = {}
    for tag, name in moldict_1['tags'].items():
        interactions_by_name[name] = (
        (get_field_atomtype(moldict_1['molecule'], tag, name), moldict_1['LJ_by_tag'][tag]))

    if moldict_2 != None:
        for tag, name in moldict_2['tags'].items():
            interactions_by_name[name] = (
            (get_field_atomtype(moldict_2['molecule'], tag, name), moldict_2['LJ_by_tag'][tag]))

    if self_exclusion_moldict != None:
        for tag, name in self_exclusion_moldict['tags'].items():
            exclusion_interactions[name] = ((get_field_atomtype(self_exclusion_moldict['molecule'], tag, name),
                                             self_exclusion_moldict['LJ_by_tag'][tag]))


    atompairs = [i for i in combinations_with_replacement(interactions_by_name.keys(), 2)]
    atompair_set = set()
    for i in atompairs:
        atompair_set.add(i)
    exclusion_atompairs = [i for i in combinations_with_replacement(exclusion_interactions.keys(), 2)]
    tested_atompairs = list(atompair_set.difference(exclusion_atompairs))
    print(tested_atompairs)

    for i in tested_atompairs:
        name1 = interactions_by_name[i[0]][0]
        name2 = interactions_by_name[i[1]][0]
        sigma = round(0.5 * interactions_by_name[i[0]][1][1] + interactions_by_name[i[1]][1][1], 3)
        epsilon = round(sqrt(interactions_by_name[i[0]][1][0] * interactions_by_name[i[1]][1][0]), 3)
        output.append(FIELD.VDW(name1, name2, INT.InteractionLJPlus(epsilon, sigma)))

    return output


def make_field(framework_molecule_dict, sorbate_molecule_list=[], cutoff=12, sim_title='Test',
               sorbent_self_interactions=False):
    '''
    This function makes an entire FIELD.FIELD object for you.
    It pulls together a lot of functions to make a complete FIELD file for you.
    To do this, it needs a moelcule dictionary for the framework you're using as well as for each sorbate you're using.
    The molecule dictionary takes the following form:
        {'name': (str) the molecule name,
        'molecule' (ASE.Atoms) the Atoms object for the molecule,
        'tags': (dict) the tag_dict for the molecule,
        'LJ_by_tag': (dict) a dict of {tag: [eps, sigma, q]...}}

    First it creates a FIELD.FIELD object and fills in some universal parameters
    Then it creates atomtypes and moltypes for the framework molecule
    After this, it does the same for sorbate molecules
    Foially, it creates a list of VDW parameters for all of the molecules you're simulating

    :param framework_molecule_dict: (dict) a molecule dictionary of your framework
    :param sorbate_molecule_list: (list) a list of molecule dictionaries for all of your sorbates
    :param cutoff: (float) your simulation cutoff, in A
    :param sim_title: (str) the name of your simulation
    :param sorbent_self_interactions: (bool) True if you want to consider framework self-LJ interactions (untested)
    :return output: (FIELD.FIELD) a FIELD.FIELD object of your simulation parameters
    '''
    # Preamble
    output = FIELD.FIELD()
    output.description = sim_title
    output.cutoff = cutoff
    output.units = 'K'

    #Framework atomtypes and moltype
    for atomtype in get_field_atomtypes(framework_molecule_dict['molecule'], framework_molecule_dict['tags']):
        output.atomtypes.append(atomtype)
    output.moltypes.append(get_maxatom_moltype(framework_molecule_dict['name'], framework_molecule_dict['molecule']))

    # Sorbate atomtypes and moltypes
    for sorbate in sorbate_molecule_list:
        if len(sorbate['LJ_by_tag'][0]) > 2:
            for atom in sorbate['molecule']:
                atom.charge = (sorbate['LJ_by_tag'][atom.tag][2])

        for atomtype in get_field_atomtypes(sorbate['molecule'], sorbate['tags']):
            output.atomtypes.append(atomtype)
        output.moltypes.append(get_field_rigid_molecule(sorbate['name'], sorbate['molecule'], sorbate['tags']))

    # VDW interactions
    if len(sorbate_molecule_list) > 0:
        for i, j in combinations([framework_molecule_dict, *sorbate_molecule_list], 2):
            print('Interactions between', i['name'],'and', j['name'])
            for interaction in get_vdw_interactions(i, j, framework_molecule_dict):
                output.vdw.append(interaction)

    elif sorbent_self_interactions:
        for interaction in get_vdw_interactions(framework_molecule_dict):
            output.vdw.append(interaction)

    print('number of interactions: ', len(output.vdw), 'max:',
          int(0.5 * (len(output.atomtypes) * (len(output.atomtypes) + 1))))
    return output


######################################################################################################################
# The following script is my preparation for a lot of IRMOFs with Mulliken charges I got in DFTB+
# It's very complicated so there are simpler example script slocated in this directory.
######################################################################################################################

if __name__ == "__main__":
    ##################################################################################################
    # Section 1: making some simple definitions of things you need to carry out the rest of the script
    # TODO: Argparsing
    ##################################################################################################
    # Defining the MOF and its charges
    framework = 'UMCM1'
    inputfile = '{0}.gen'.format(framework)
    directory = './JoesCharges/{0}/'.format(framework)

    structure = read_framework(inputfile, directory)
    charge_list = read_charges_from_dftb('detailed.out', directory)
    charged_structure = framework_charges(structure, charge_list)

    view(charged_structure)

    # Defining the possible sets of guest molecules, as well as MOF forcefield params
    N2 = {'name': 'Nitrogen',
          'molecule': Atoms('NXN', positions=[(0, 0, 0), (0, 0, 0.55), (0, 0, 1.1)], tags=[0, 1, 0]),
          'tags': {0: 'N', 1: 'COM'},
          'LJ_by_tag': {0: [36, 3.31, -0.482],
                        1: [0, 0, 0.964]
                        }  # eps, sigma, q
          }

    MeOH = {'name': 'MeOH',
            'molecule': Atoms('HOX', positions=[(-1.430, 0.000, 0.000), (0, 0, 0), (0.300, 0.896, 0.000)],
                              tags=[0, 1, 2]),
            'tags': {0: 'H', 1: 'O', 2: 'Me'},
            'LJ_by_tag': {
                0: [0, 0, 0.435],
                1: [93, 3.02, -0.7],
                2: [98, 3.75, 0.265]
            }  # eps, sigma, q
            }

    DMF = {'name': 'DMF',
           'molecule': Atoms('HCONXX', positions=[
               (1.594, 1.019, 0.000),  # H
               (1.130, 0.000, 0.000),  # C
               (1.732, -0.945, 0.000),  # O
               (0, 0, 0),  # N
               (-0.720, 1.247, 0.000),  # Me
               (-0.698, -1.259, 0.000)  # Me
           ], tags=[0, 1, 2, 3, 4, 4]),
           'tags': {0: 'H', 1: 'C', 2: 'O', 3: 'N', 4: 'Me'},
           'LJ_by_tag': {
               0: [7.18, 2.2, 0.06],
               1: [47.3, 3.7, 0.45],
               2: [226, 2.96, -0.5],
               3: [144, 3.2, -0.57],
               4: [69, 3.8, 0.28]
           }
           }

    Ace = {'name': 'Acetone',
           'molecule': Atoms('XCOX', positions=[
               (-0.792, 1.297, 0.000),
               (0.000, 0.000, 0.000),
               (1.229, 0.000, 0.000),
               (-0.792, -1.297, 0.000)],
                             tags=[0, 1, 2, 0]),
           'tags': {0: 'Me', 1: 'C', 2: 'O'},
           'LJ_by_tag': {
               0: [98, 3.75, 0],
               1: [40, 3.82, 0.424],
               2: [79, 3.05, -0.424]}}

    EtOH = {'name': 'EtOH', 'molecule': Atoms('HOCC',
                                              positions=[
                                                  (0.300, 0.896, 0.000),
                                                  (0, 0, 0),
                                                  (-1.430, 0.000, 0.000),
                                                  (-1.944, -1.452, 0.000)], tags=[0, 1, 2, 3]),
            'tags': {0: 'H', 1: 'O', 2: 'CH2', 3: 'Me'},
            'LJ_by_tag': {
                0: [0, 0, 0.435],
                1: [93, 3.02, -0.7],
                2: [46, 3.95, 0.265],
                3: [98, 3.75, 0]}  # eps, sigma, q
            }

    Dioxane = {'name': 'Dioxane', 'molecule': Atoms('OCCOCC',
                                                    positions=[(1.320, 0.000, 0.596),
                                                               (0.780, 1.194, 0.000),
                                                               (-0.780, 1.194, 0.000),
                                                               (0.780, -1.194, 0.000),
                                                               (-0.780, -1.194, 0.000),
                                                               (-1.320, 0.000, -0.596)],
                                                    tags=[0, 1, 1, 0, 1, 1]),
               'tags': {0: 'O', 1: 'CH2'},
               'LJ_by_tag': {0: [155, 2.39, -0.38],
                             1: [52.5, 3.91, 0.19]}
               }

    ACN = {'name': 'Acetonitrile',
           'molecule': Atoms('NCX', positions=[
               (1.157, 0, 0),
               (0, 0, 0),
               (-1.54, 0, 0)],
                             tags=[0, 1, 2]),
           'tags': {0: 'N',
                    1: 'C',
                    2: 'Me'},
           'LJ_by_tag': {0: [98, 3.75, 0.269],
                         1: [60, 3.55, 0.129],
                         2: [60, 2.95, -0.398]}}

    MOF_LJ = {
        'Zn_S': [62.4, 2.46],
        'O_Zn': [30.19, 3.12],
        'O_S': [48.16, 3.03],
        'C_S': [47.86, 3.47],
        'H_S': [7.65, 2.85],
        'N_S': [38.95, 3.26],
        'Br_S': [186.19, 3.52]
    }

    sorbates = []  # The sorbate molecules you're going to be simulating

    # Defining some usful parameters for later on, which will help us make the simulation better
    experiment_name = 'DL_MONTE autogenerate test'
    cutoff = 12

    ##################################################################################################
    # Section 2: preparing the MOf from an ase object into something understandable by dlfield
    ##################################################################################################
    # Making a dictionary of atomtypes by index in thr ase object, which makes for handier manipulation
    indices = make_framework_indices(structure)

    # Distabnce-based separation of Zn4O Oxygens from COO oxygens
    # This is essential for the mixed DREIDING/UFF forcefield method that I use, but probbaly not too useful otherwise
    # It also breaks the script if you're not plannign to use moieties
    # TODO: make this optional!

    O_not_C, O_C = classify_elements_by_distance(charged_structure, indices[8]['idx_mask'], 1.5, indices[6]['idx_mask'])
    indices[8]['moieties'] = {}
    indices[8]['moieties']['O_Zn'] = O_not_C
    indices[8]['moieties']['O_S'] = O_C

    # Now we condense down the number of unique charges in the MOF, to make the eventual FIELD more readable

    newcharges = np.zeros_like(structure)
    for i in indices.keys():
        print('element: ', i)
        if 'moieties' not in indices[i].keys():
            print('element {0} has only 1 chemical moiety'.format(i))
            newcharges += condense_similar_charges(charged_structure, indices[i]['idx_mask'])
        else:
            for j in indices[i]['moieties'].keys():
                if len(indices[i]['moieties'][j]) == 0:
                    print('Nothing here guv!')
                else:
                    print(i, j)
                    newcharges += condense_similar_charges(charged_structure, indices[i]['moieties'][j])
    charged_structure_2 = framework_charges(structure, newcharges)

    # And now we assign a set of tags to the ASE object corresponding to a specific framework atom/charge type
    # After this, I'm getting an np.ndarray of int tag numbers and a dictionary of tag labels corresponding to those numbers
    # so at the lowest level I want to take a moiety and provide subtags by unique charges
    # one level above, I want to do this by element

    tag_dict, tags = assign_all_framework_tags(charged_structure_2, indices)

    charged_structure_2.set_tags(tags)

    # Using our tags, we now apply our MOF lennard hones interaction dictionary to the structure
    # Due to subtags because of multiple charge states, it's a bit messy, but there we go

    MOF_LJ_by_tag = {}
    print(tag_dict)
    for key, value in tag_dict.items():
        split_char = '_'
        LJ_key = split_char.join(value.split(split_char)[:2])
        MOF_LJ_by_tag[key] = MOF_LJ[LJ_key]
    print(MOF_LJ_by_tag)

    print('Net charge on structure: ', round(sum(charged_structure_2.get_initial_charges()), 4))

    # Finally, we make a supercell of the MOF to ensure we're not breaking the periodic boundary conditions
    supercell = []
    for i in range(3):
        dim = np.linalg.norm(structure.cell[i])
        if dim < cutoff * 2:
            print('oh no! my x value is too small! ({0})'.format(dim))
            supercell.append(ceil((cutoff * 2) / dim))
        else:
            supercell.append(1)
    print(supercell)
    assert len(supercell) == 3
    superstructure = charged_structure_2 * (supercell[0], supercell[1], supercell[2])

    ##################################################################################################
    # Section 2: preparing the dlconfig object for an empty framework molecule
    ##################################################################################################

    molecules_list = [config_molecule_dict_maker(superstructure, tag_dict, framework)]
    molecule_numbers = [len(molecules_list), 1000, 1000]
    empty_box = CONFIG.CONFIG(experiment_name,
                              0,
                              1,
                              superstructure.cell,
                              molecule_numbers,
                              molecules_list)

    ##################################################################################################
    # Section 3: preparing the dlfield object for an n-molecule simulation
    ##################################################################################################
    # I'm going to need to handle sorbates and sorbents separately here
    # 1. make a function to handle atomtypes
    # 2. make a function to handle moltypes
    # 3. make a function which handles atoms, and one which appends them into a molecule object
    # 4. make a funciton to handle VdW interactions
    # 5. Leave a TODO for nonrigid molecules
    # 6. Make a dlfield object for pure MOF, then think about adding a sorbents in - as files ot be read in?

    frame_dict = {'name': framework,
                  'molecule': superstructure,
                  'tags': tag_dict,
                  'LJ_by_tag': MOF_LJ_by_tag}

    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    sim_field = make_field(frame_dict, [N2], cutoff=cutoff)

    print(sim_field)
