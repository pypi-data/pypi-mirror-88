'''
A python script for producing dl_monte monte carlo simulations inside a framework.
Using ASE, it starts by reading in a file (e.g. a .cif for a dftb .gen file).
Then, it creates a supercell according to the minimum image convention.
Using a predefined dictionary of atom name tags, it assigns types consistent with a FIELD file.
It spits out the maxatom value for a FIELD file, then writes a CONFIG object from dlmonte
'''

from ase import Atoms
from math import ceil
import numpy as np
from dlmontepython.examples.htk.MOF_adsorption.Config_Field import config_setup as cfg
import argparse

# TODO: function docstrings
# DONE: tag assignment functions - by charge and distance criteria (and working together!)
# TODO: god functions for uncharged/singly charged framework, multiply charged framework (with/out automatic charge assignment)
# DONE: make dlconfig objects
# DONE: make dlfield objects
# TODO: fix the funcitons defining the LJ_interactions - tags by ase atomtypes?
# TODO: I could totally work that out somehow, but with a catch fro the number = 8 and tag include Zn

##################################################################################################
# Section 1: making some simple definitions of things you need to carry out the rest of the script
# TODO: Argparsing
##################################################################################################
# Defining the MOF and its charges
#parser = argparse.ArgumentParser()
#parser.add_argument('framework', help='the name of the framework you\'re using')
#args = parser.parse_args()
#framework = args.framework

framework='FJI1'
inputfile = '{0}.gen'.format(framework)
indirectory = './JoesCharges/{0}/'.format(framework)
outdirectory= './structures/{0}/'.format(framework)
cfg.directorymaker(outdirectory)

structure = cfg.read_framework(inputfile, indirectory)
charge_list= cfg.read_charges_from_dftb('detailed.out',indirectory)
charged_structure = cfg.framework_charges(structure,charge_list)

#view(charged_structure)

# Defining the possible sets of guest molecules, as well as MOF forcefield params
N2 = {'name': 'Nitrogen',
        'molecule': Atoms('NXN', positions=[
          (0,0,0),
          (0,0,0.55),
          (0,0,1.1)],
          tags = [0,1,0]),
        'tags': {0:'N', 1:'COM'},
        'LJ_by_tag': {
            0: [36, 3.31, -0.482],
            1: [0,0,0.964]} #eps, sigma, q
        } #TRAPPE

MeOH = {'name': 'MeOH', 'molecule': Atoms('HOX', positions=[(-1.430,0.000,0.000), (0,0,0), (0.300,0.896,0.000)], tags=[0,1,2]),
       'tags': {0:'H', 1:'O', 2:'Me'},
'LJ_by_tag': {
    0: [0,0,0.435],
    1: [93,3.02,-0.7],
    2: [98, 3.75, 0.265]
          } #eps, sigma, q
} #TRAPPE

DMF = { 'name': 'DMF',
    'molecule': Atoms('HCONXX', positions = [
    (1.594,1.019,0.000), #H
    (1.130,0.000,0.000), #C
    (1.732,-0.945,0.000), #O
    (0,0,0), #N
    (-0.720,1.247,0.000), #Me
    (-0.698,-1.259,0.000) #Me
    ],tags= [0,1,2,3,4,4]),
    'tags':  {0:'H', 1:'C', 2:'O', 3:'N', 4:'Me'},
    'LJ_by_tag': {
    0: [7.18, 2.2, 0.06],
    1: [47.3, 3.7, 0.45],
    2: [226, 2.96, -0.5],
    3: [144, 3.2, -0.57],
    4: [69, 3.8, 0.28]
}
} #TRAPPE

Ace = {'name': 'Acetone',
       'molecule': Atoms('XCOX', positions= [
            (-0.792, 1.297, 0.000),
            (0.000, 0.000, 0.000),
            (1.229, 0.000, 0.000),
            (-0.792, -1.297, 0.000)],
            tags = [0,1,2,0]),
       'tags': {0: 'Me', 1: 'C', 2:'O'},
       'LJ_by_tag': {
           0: [98, 3.75, 0],
           1: [40, 3.82, 0.424],
           2: [79, 3.05, -0.424]}
       } #TRAPPE

EtOH = {'name': 'EtOH',
        'molecule': Atoms('HOCC',positions=[
            (0.300, 0.896, 0.000),
            (0,0,0),
            (-1.430, 0.000, 0.000),
            (-1.944, -1.452, 0.000)],
            tags=[0,1,2,3]),
        'tags': {0:'H', 1:'O',2:'CH2', 3:'Me'},
        'LJ_by_tag': {
            0: [0,0,0.435],
            1: [93,3.02,-0.7],
            2: [46, 3.95, 0.265],
            3:[98,3.75,0]} #eps, sigma, q
        } #TRAPPE

Dioxane = {'name' : 'Dioxane',
        'molecule': Atoms('OCCOCC',
            positions=[(1.320, 0.000, 0.596),
            (0.780, 1.194, 0.000),
            (-0.780, 1.194, 0.000),
            (0.780, -1.194, 0.000),
            (-0.780, -1.194, 0.000),
            (-1.320, 0.000, -0.596)],
            tags=[0,1,1,0,1,1]),
        'tags': {0:'O', 1:'CH2'},
        'LJ_by_tag':{
            0:[155,2.39,-0.38],
            1:[52.5,3.91,0.19]}
        } #TRAPPE

ACN = {'name':'Acetonitrile',
       'molecule': Atoms('NCX', positions=[
            (1.157,0,0),
            (0,0,0),
            (-1.54,0,0)],
            tags=[0,1,2]),
       'tags': {0: 'N', 1: 'C', 2: 'Me'},
       'LJ_by_tag': {
           0: [98,3.75,0.269],
           1: [60,3.55,0.129],
           2: [60,2.95,-0.398]}
       } #TRAPPE

Chloroform = {'name':'Chloroform',
       'molecule': Atoms('HCCl3', positions=[
            (-0.39735, -0.26191, 1.13681),
            (-0.03496, 0.00302, 0.12229),
            (1.74297, -0.00071, 0.10829),
            (-0.63937, -1.18691, -1.05244),
            (-0.62768, 1.62127, -0.31495)],
            tags=[0,1,2,2,2]),
       'tags':{0: 'H', 1: 'C', 2: 'Cl'},
       'LJ_by_tag':{
           0: [10.06,2.81,0.355],
           1: [138.58,3.41,-0.235],
           2: [68.94,3.45,-0.04]}
        } #after 10.1021/jp0535238

CCl4 = {'name':'CCl4',
       'molecule': Atoms('CCl4', positions=[
            (0,0,0),
            (1.18,1.18,1.18),
            (-1.18,-1.18,1.18),
            (-1.18,1.18,-1.18),
            (1.18,-1.18,-1.18)],
            tags=[0,1,1,1,1]),
       'tags':{0: 'C', 1: 'Cl'},
       'LJ_by_tag':{
           0:[12.37,2.81,-0.362],
           1:[212.6,3.25,-0.235]}
        } #after 10.1063/1.4943395

CH2Cl2 = {'name': 'Dichloromethane',
        'molecule':  Atoms('XCl2', positions=[
            (0.000000, 0.762012, 0.000016),
            (-1.474470, -0.215523, 0.000013),
            (1.474468, -0.215525, 0.000014)],
            tags=[0,1,1]),
        'tags': {0: 'CH2', 1: 'Cl'},
        'LJ_by_tag': {
            0: [123.34,3.60,0.4044],
            1: [123.34,3.42,-0.2022]}
        } #intermolecular interactions after 10.1021/ct500853, positions by Mat Tolladay

MOF_LJ = {
    'Zn_S': [62.4, 2.46],
    'O_Zn': [30.19, 3.12],
    'O_S': [48.16, 3.03],
    'C_S': [47.86, 3.47],
    'H_S': [7.65, 2.85],
    'N_S': [38.95, 3.26],
    'Br_S': [186.19, 3.52]
}

sorbates = [N2, MeOH, DMF, Ace, EtOH, Dioxane, ACN, Chloroform, CCl4, CH2Cl2] # The sorbate molecules you're going to be simulating


#Defining some usful parameters for later on, which will help us make the simulation better
experiment_name = 'DL_MONTE autogenerate test'
cutoff = 12

##################################################################################################
# Section 2: preparing the MOf from an ase object into something understandable by dlfield
##################################################################################################
# Making a dictionary of atomtypes by index in thr ase object, which makes for handier manipulation
indices = cfg.make_framework_indices(structure)

# Distabnce-based separation of Zn4O Oxygens from COO oxygens
# This is essential for the mixed DREIDING/UFF forcefield method that I use, but probbaly not too useful otherwise

O_not_C, O_C = cfg.classify_elements_by_distance(charged_structure,indices[8]['idx_mask'],1.5,indices[6]['idx_mask'])
indices[8]['moieties'] = {}
indices[8]['moieties']['O_Zn']=O_not_C
indices[8]['moieties']['O_S']=O_C

#Now we condense down the number of unique charges in the MOF, to make the eventual FIELD more readable

newcharges = np.zeros_like(structure)
for i in indices.keys():
    print('element: ', i)
    if 'moieties' not in indices[i].keys():
        print('element {0} has only 1 chemical moiety'.format(i))
        newcharges += cfg.condense_similar_charges(charged_structure, indices[i]['idx_mask'])
    else:
        for j in indices[i]['moieties'].keys():
            if len(indices[i]['moieties'][j]) == 0:
                print('Nothing here guv!')
            else:
                print(i,j)
                newcharges += cfg.condense_similar_charges(charged_structure, indices[i]['moieties'][j])
charged_structure_2 = cfg.framework_charges(structure,newcharges)


# And now we assign a set of tags to the ASE object corresponding to a specific framework atom/charge type
# After this, I'm getting an np.ndarray of int tag numbers and a dictionary of tag labels corresponding to those numbers
# so at the lowest level I want to take a moiety and provide subtags by unique charges
# one level above, I want to do this by element

tag_dict, tags = cfg.assign_all_framework_tags(charged_structure_2,indices)

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

print('Net charge on structure: ', round(sum(charged_structure_2.get_initial_charges()),4))

#Finally, we make a supercell of the MOF to ensure we're not breaking the periodic boundary conditions
supercell = []
for i in range(3):
    dim = np.linalg.norm(structure.cell[i])
    if dim<cutoff*2:
        print('oh no! my x value is too small! ({0})'.format(dim))
        supercell.append(ceil((cutoff*2)/dim))
    else:
        supercell.append(1)
print(supercell)
assert len(supercell) == 3
superstructure = charged_structure_2 * (supercell[0],supercell[1],supercell[2])

##################################################################################################
# Section 2: preparing the dlconfig object for an empty framework molecule
##################################################################################################


config = cfg.make_config_empty_framework(superstructure, tag_dict, framework)

with open('{0}CONFIG'.format(outdirectory), 'w') as f:
    f.write(str(config))

##################################################################################################
# Section 3: preparing the dlfield object for an n-molecule simulation
##################################################################################################
#I'm going to need to handle sorbates and sorbents separately here
#1. make a function to handle atomtypes
#2. make a function to handle moltypes
#3. make a function which handles atoms, and one which appends them into a molecule object
#4. make a funciton to handle VdW interactions
#5. Leave a TODO for nonrigid molecules
#6. Make a dlfield object for pure MOF, then think about adding a sorbents in - as files ot be read in?

frame_dict = {'name': framework,
    'molecule': superstructure,
              'tags': tag_dict,
              'LJ_by_tag': MOF_LJ_by_tag}


print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
for i in sorbates:
    sim_field = cfg.make_field(frame_dict, [i], cutoff=cutoff)
    with open('{0}{1}.FIELD'.format(outdirectory,i['name']), 'w') as f:
        f.write(str(sim_field))

