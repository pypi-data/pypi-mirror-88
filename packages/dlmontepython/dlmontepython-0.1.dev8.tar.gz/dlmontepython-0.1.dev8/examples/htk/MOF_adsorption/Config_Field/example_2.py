from ase import Atoms
from math import ceil
import numpy as np
from dlmontepython.examples.htk.MOF_adsorption.Config_Field import config_setup as cfg
import argparse

framework='IRMOF1'
inputfile = '{0}.gen'.format(framework)
indirectory = './JoesCharges/{0}/'.format(framework)
outdirectory= './example_outputs/{0}/'.format(framework)
cfg.directorymaker(outdirectory)


structure = cfg.read_framework(inputfile, indirectory)


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

MOF_LJ = {
    'Zn_S': [62.4, 2.46],
    'O_Zn': [30.19, 3.12],
    'O_S': [48.16, 3.03],
    'C_S': [47.86, 3.47],
    'H_S': [7.65, 2.85],
    'N_S': [38.95, 3.26],
    'Br_S': [186.19, 3.52]
}


#Defining some usful parameters for later on, which will help us make the simulation better
experiment_name = 'DL_MONTE autogenerate test'
cutoff = 12

indices = cfg.make_framework_indices(structure)

O_not_C, O_C = cfg.classify_elements_by_distance(structure,indices[8]['idx_mask'],1.5,indices[6]['idx_mask'])
indices[8]['moieties'] = {}
indices[8]['moieties']['O_Zn'] = O_not_C
indices[8]['moieties']['O_S'] = O_C

print('Number of moiety 1 atoms:',len(np.where(indices[8]['moieties']['O_Zn'])[0]))
print('Number of moiety 2 atoms:',len(np.where(indices[8]['moieties']['O_S'])[0]))


tag_dict, tags = cfg.assign_all_framework_tags(structure,indices)
print(structure[tags ==0])
for i in tag_dict.keys():
    print(i, structure[tags == i])

structure.set_tags(tags)



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
superstructure = structure * (supercell[0],supercell[1],supercell[2])

##################################################################################################
# Section 2: preparing the dlconfig object for an empty framework molecule
##################################################################################################


config = cfg.make_config_empty_framework(superstructure, tag_dict, framework)

with open('{0}ex2_CONFIG'.format(outdirectory), 'w') as f:
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

MOF_LJ_by_tag = {}
print(tag_dict)
for key, value in tag_dict.items():
    split_char = '_'
    LJ_key = split_char.join(value.split(split_char)[:2])
    MOF_LJ_by_tag[key] = MOF_LJ[LJ_key]
print(MOF_LJ_by_tag)


frame_dict = {	'name': framework,
				'molecule': superstructure,
				'tags': tag_dict,
				'LJ_by_tag': MOF_LJ_by_tag}

sim_field = cfg.make_field(frame_dict, [N2], cutoff=cutoff)
with open('{0}ex2_{1}.FIELD'.format(outdirectory,N2['name']), 'w') as f:
    f.write(str(sim_field))
