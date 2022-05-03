#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  27 11:55:06 2022

@author: ben
"""

import h5py
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

directory = Path(r"/home/ben/sims/swiftsim/examples/zoom_tests/auriga6_halo7_8_10")
Nres = 128 # 233.45 #for arj
Lbox = 100

snap_number = 7 # 7 for our tests, 0 for arj

fof_file = h5py.File(directory / f"fof_output_000{snap_number}.hdf5", "r") 
file = h5py.File(directory / f'output_000{snap_number}.hdf5', 'r')

PartType1 = file["PartType1"]
highres_groupids = PartType1['FOFGroupIDs'][:]
highres_coordinates = np.array(PartType1['Coordinates'][:])
highres_masses = PartType1['Masses'][:]

total_highres_particles = len(highres_groupids)
unique_groups, particle_count = np.unique(highres_groupids, return_counts=True)
# print(f'Group IDs: {unique_groups}, Number in them: {particle_count}')

# all particles belonging to no group have group id 2147483647

highres_x, highres_y, highres_z = highres_coordinates[:, 0], highres_coordinates[:, 1], highres_coordinates[:, 2]

groups = fof_file['Groups']

# for key in groups.keys():
#     print(key)

centres = groups['Centres'][:]
groupids = groups['GroupIDs'][:]
masses = groups['Masses'][:]
number_of_members = groups['Sizes'][:]

# table_width = 4

# separate_unique_counter = 0
# # for i in range(len(groupids)-1):
# for i in range(11):
#     if np.isin(groupids[i], unique_groups):
#         highres_members = particle_count[separate_unique_counter]
#         contamination = (1 - highres_members / number_of_members[i]) 
#         print(f'Group: {groupids[i]:{table_width}} | Mass: {masses[i]:{table_width + 1}.{table_width}} | Highres Members: {highres_members:{table_width + 1}} | Total Members: {number_of_members[i]:{table_width}} | Contamination: {contamination * 100:.{table_width}}%\n')
#         separate_unique_counter += 1

main_group_origin = centres[np.min(unique_groups) - 1]
main_group_mass = masses[np.min(unique_groups) - 1]
origin_x, origin_y, origin_z = main_group_origin[0], main_group_origin[1], main_group_origin[2]
print(np.mean(highres_masses))

plt.title('Histogram of Auriga 6 Centre Levelmax 10')
plt.xlabel('x [Mpc]')
plt.ylabel('y [Mpc]')
i = np.logical_and( highres_z>origin_z-0.5, highres_z<origin_z+0.5 )
plt.hist2d(x=highres_x[i], y=highres_y[i], bins=256, range=[[origin_x - 0.5, origin_x + 0.5], [origin_y - 0.5, origin_y + 0.5]], weights=highres_masses[i], norm=LogNorm())
plt.colorbar()
plt.show()