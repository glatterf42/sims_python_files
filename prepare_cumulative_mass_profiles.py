#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 11:16:06 2022

@author: ben
"""

import h5py
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

def V(r):
    return 4 * np.pi * r**3 / 3

directory = Path(r"/home/ben/sims/swiftsim/examples/zoom_tests/auriga6_halo7_8_9")
Nres = 128 # 233.45 #for arj
Lbox = 100

snap_number = 7 # 7 for our tests, 0 for arj

fof_file = h5py.File(directory / f"fof_output_000{snap_number}.hdf5", "r") 
file = h5py.File(directory / f'output_000{snap_number}.hdf5', 'r')

PartType1 = file["PartType1"]
highres_groupids = PartType1['FOFGroupIDs'][:]
highres_coordinates = PartType1['Coordinates'][:]
highres_masses = PartType1['Masses'][:]

total_highres_particles = len(highres_groupids)
unique_groups, particle_count = np.unique(highres_groupids, return_counts=True)
print(f'Group IDs: {unique_groups}, Number in them: {particle_count}')

# all particles belonging to no group have group id 2147483647


# for key in fof_file.keys():
#     print(key) #for finding all header entries, which are:
        
groups = fof_file['Groups']

# for key in groups.keys():
#     print(key)

centres = groups['Centres'][:]
groupids = groups['GroupIDs'][:]
masses = groups['Masses'][:]
number_of_members = groups['Sizes'][:]

table_width = 4

separate_unique_counter = 0
# for i in range(len(groupids)-1):
for i in range(11):
    if np.isin(groupids[i], unique_groups):
        highres_members = particle_count[separate_unique_counter]
        contamination = (1 - highres_members / number_of_members[i]) 
        print(f'Group: {groupids[i]:{table_width}} | Mass: {masses[i]:{table_width + 1}.{table_width}} | Highres Members: {highres_members:{table_width + 1}} | Total Members: {number_of_members[i]:{table_width}} | Contamination: {contamination * 100:.{table_width}}%\n')
        separate_unique_counter += 1


main_group_origin = centres[np.min(unique_groups) - 1]
main_group_mass = masses[np.min(unique_groups) - 1]
distances = []
# masses = []

for j in range(len(highres_groupids)):
    if highres_groupids[j] == np.min(unique_groups):
        distance = np.linalg.norm(main_group_origin - highres_coordinates[j])
        # mass = highres_masses[j]
        distances.append(distance)
        # masses.append(mass)

group_radius = np.max(np.array(distances))
normalised_distances = np.array(distances) / group_radius

num_bins = 30
log_radial_bins = np.geomspace(0.01, 2, num_bins)

particle_mass = highres_masses[0] # Careful: this assumes that all highres particles have the same mass and that it's exclusively them in the main group,
                                  # so keep an eye on its contamination and adjust accordingly!

counts_in_radial_bins = []
for k in range(len(log_radial_bins) - 1):
    count = 0
    for member_distance in normalised_distances:
        if log_radial_bins[k] <= member_distance < log_radial_bins[k + 1]:
            count += 1
    # volume = V(log_radial_bins[k + 1] * group_radius) - V(log_radial_bins[k] * group_radius)
    # count /= volume
    counts_in_radial_bins.append(count)

plot_log_radial_bins = log_radial_bins[0:len(log_radial_bins) - 1] # there is one fewer bin then there are bin borders
masses_in_radial_bins = np.array(counts_in_radial_bins) * particle_mass

cumulative_mass_profile = np.cumsum(masses_in_radial_bins)

softening = Lbox / Nres / 30
# plt.axvline(4 * softening / group_radius, linestyle='--', color='grey')


save_data = np.column_stack((plot_log_radial_bins, cumulative_mass_profile))
np.savetxt(directory/'cumulative_mass_profile.csv', save_data, delimiter=',', fmt='%.3f', header='Radii[R/R_group],Masses[1e10Msun]')


# kumulatives Dichteprofil -> sollte bei grossen Massen praktisch gleich sein, am besten direkt uebereinander plotten. 
# plt.hist2D mit x und y, jeweils Zentrum der Gruppe +- 0.5 Mpc anschauen, alles andere wegwerfen, sollte direkt Struktur erkennen koennen, ob sie gleich ist. Muss noch durch Masse teilen (nur Teilchen zaehlen?)





# for i in range(10):
#     print(f'Group: {groupids[i]} | Mass: {masses[i]} | Size: {sizes[i]} | Centre: {centres[i]}\n')
    


# print(list(parameters.attrs.items()))


# use list(Header.attr.keys()) to list all attributes contained in the Header and .attr.values() to see their values
# even otherwise empty things like ICs_parameters can contain such attributes
