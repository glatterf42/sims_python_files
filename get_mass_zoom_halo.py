#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 11:16:06 2022

@author: ben
"""

import h5py
from pathlib import Path
import numpy as np

directory = Path(r"/home/ben/sims/swiftsim/examples/zoom_tests/")

snap_number = 7

fof_file = h5py.File(directory / f"fof_output_000{snap_number}.hdf5", "r") 
file = h5py.File(directory / f'output_000{snap_number}.hdf5', 'r')

PartType1 = file["PartType1"]
highres_groupids = PartType1['FOFGroupIDs'][:]

total_highres_particles = len(highres_groupids)
unique_groups, particle_count = np.unique(highres_groupids, return_counts=True)
print(f'Group IDs: {unique_groups}, Number in them: {particle_count}')

# all particles belonging to no group have group id 2147483647


# for key in fof_file.keys():
#     print(key) #for finding all header entries, which are:
        
groups = fof_file['Groups']

# for key in groups.keys():
#     print(key)


# centres = groups['Centres'][:]
groupids = groups['GroupIDs'][:]
masses = groups['Masses'][:]
number_of_members = groups['Sizes'][:]

table_width = 4

separate_unique_counter = 0
for i in range(len(groupids)-1):
    if np.isin(groupids[i], unique_groups):
        highres_members = particle_count[separate_unique_counter]
        contamination = (1 - highres_members / number_of_members[i]) 
        print(f'Group: {groupids[i]:{table_width}} | Mass: {masses[i]:{table_width + 1}.{table_width}} | Highres Members: {highres_members:{table_width}} | Total Members: {number_of_members[i]:{table_width}} | Contamination: {contamination * 100:.{table_width}}%\n')
        separate_unique_counter += 1


# for i in range(10):
#     print(f'Group: {groupids[i]} | Mass: {masses[i]} | Size: {sizes[i]} | Centre: {centres[i]}\n')
    


# print(list(parameters.attrs.items()))


# use list(Header.attr.keys()) to list all attributes contained in the Header and .attr.values() to see their values
# even otherwise empty things like ICs_parameters can contain such attributes
