#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 11:16:06 2022

@author: ben
"""

import h5py
from pathlib import Path
import numpy as np

directory = Path(r"/home/ben/sims/swiftsim/examples/agora/")
# directory = Path(r"/home/ben/Pictures/Gadget4/vsc4_256/")
# directory = Path(r'/home/ben/sims/music-panphasia/test/')


# ics = h5py.File(directory / "agora_128.hdf5", "r") 
file = h5py.File(directory / "output_0001.hdf5", "r") 
# file_2 = h5py.File(directory / 'output_0001.hdf5', 'r')

# file = h5py.File(directory / "cosmo_ics_gadget_256_pbh_vsc.hdf5", "r") 

# for key in file.keys():
#     print(key) #for finding all header entries, which are:
        

Header = file["Header"]
#ICs_parameters = file["ICs_parameters"]
PartType1 = file["PartType1"]
Units = file["Units"]
# PartType2 = file['PartType2']

# print(list(Header.attrs.items()))
# print(list(ics['Header'].attrs.items()))
print(Header.attrs['Scale-factor'])


# print(PartType1.keys())
# # print(PartType2.keys())
# print(PartType1['Masses'][0:10])

# print(PartType1['Velocities'][0:10])

# ic_ids = ics['PartType1']['ParticleIDs'][:]
# ic_velocities = ics['PartType1']['Velocities'][:]
# ic_absolute_vel = np.sqrt(np.sum(ic_velocities ** 2, axis=1))
# ic_data = np.vstack([ic_ids, ic_absolute_vel]).T
# ic_positions = ics['PartType1']['Coordinates'][:]
# ic_distances = np.sqrt(np.sum(ic_positions ** 2, axis=1))
# ic_data = np.vstack([ic_ids, ic_distances]).T

# snap_ids = PartType1['ParticleIDs'][:]
# snap_velocities = PartType1['Velocities'][:]
# snap_absolute_vel = np.sqrt(np.sum(snap_velocities ** 2, axis=1))
# snap_data = np.vstack([snap_ids, snap_absolute_vel]).T
# snap_data_sorted = snap_data[snap_data[:, 0].argsort()]
# snap_positions = PartType1['Coordinates'][:]
# snap_distances = np.sqrt(np.sum(snap_positions ** 2, axis=1))
# snap_data = np.vstack([snap_ids, snap_distances]).T
# snap_data_sorted = snap_data[snap_data[:, 0].argsort()]

# snap_2_ids = file_2['PartType1']['ParticleIDs'][:]
# snap_2_velocities = file_2['PartType1']['Velocities'][:]
# snap_2_absolute_vel = np.sqrt(np.sum(snap_2_velocities ** 2, axis=1))
# snap_2_data = np.vstack([snap_2_ids, snap_2_absolute_vel]).T
# snap_2_data_sorted = snap_2_data[snap_2_data[:, 0].argsort()]
# snap_2_positions = file_2['PartType1']['Coordinates'][:]
# snap_2_distances = np.sqrt(np.sum(snap_2_positions ** 2, axis=1))
# snap_2_data = np.vstack([snap_2_ids, snap_2_distances]).T
# snap_2_data_sorted = snap_2_data[snap_2_data[:, 0].argsort()]

# velocity_difference = np.abs(ic_data[:, 1] - snap_data_sorted[:, 1])
# mean_velocity_difference = np.mean(velocity_difference)

# velocity_difference_2 = np.abs(snap_data_sorted[:, 1] - snap_2_data_sorted[:, 1])
# mean_2_velocity_difference = np.mean(velocity_difference_2)

# print(mean_velocity_difference, mean_2_velocity_difference)
# print(np.min(velocity_difference), np.max(velocity_difference))
# print(np.min(velocity_difference_2), np.max(velocity_difference_2))

# distance_difference = np.abs(ic_data[:, 1] - snap_data_sorted[:, 1])
# mean_distance_difference = np.mean(distance_difference)

# distance_difference_2 = np.abs(snap_data_sorted[:, 1] - snap_2_data_sorted[:, 1])
# mean_2_distance_difference = np.mean(distance_difference_2)

# print(mean_distance_difference, mean_2_distance_difference)
# print(np.min(ic_distances), np.max(ic_distances))
# print(np.min(snap_distances), np.max(snap_distances))



# print(PartType2['Masses'][0:10])
# print(list(Units.attrs.items()))

# use list(Header.attr.keys()) to list all attributes contained in the Header and .attr.values() to see their values
# even otherwise empty things like ICs_parameters can contain such attributes
