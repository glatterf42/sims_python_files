# -*- coding: utf-8 -*-
"""
Created on Tue Jul 20 15:03:28 2021

@author: Ben Melville
"""


import h5py
from pathlib import Path
#import matplotlib.pyplot as plt
from scipy.spatial import KDTree #for nearest neighbour search
import numpy as np
import numba


def determine_desired_range(offset, minimum, upper_limit_bottom, lower_limit_top, maximum):
    a = minimum
    b = maximum
    
    if offset < 0:
        a = lower_limit_top
    elif offset > 0:
        b = upper_limit_bottom
    
    return a,b
        

@numba.njit()
def find_coordinates_to_move(minimum, maximum, ratio, x_offset, y_offset, z_offset, move_candidates):
    coordinates_to_move = []
    x_start, x_end = determine_desired_range(x_offset, minimum, upper_limit_bottom, lower_limit_top, maximum)
    y_start, y_end = determine_desired_range(y_offset, minimum, upper_limit_bottom, lower_limit_top, maximum)
    z_start, z_end = determine_desired_range(z_offset, minimum, upper_limit_bottom, lower_limit_top, maximum)
    
    for point in move_candidates:
        if x_start <= point[0] <= x_end and y_start <= point[1] <= y_end and z_start <= point[2] <= z_end:
            coordinates_to_move.append(point)
    
    return coordinates_to_move


directory = Path(r".\256_pbh_fast_10sigma")
# total_mass = 232209.09 #retrieved from visualisation.py
# #Choose one of the following Nres values:
# Nres = 64 
# #Nres = 128
# mass_per_particle = total_mass / (Nres**3)


# file = h5py.File(directory / "fof_subhalo_tab_038.hdf5", "r") #for whole duration
# file = h5py.File(directory / "fof_subhalo_tab_018.hdf5", "r") #for small boxes
file = h5py.File(directory / "fof_subhalo_tab_016.hdf5", "r") #for e5 boxes 256

# for key in file.keys():
#     print(key)


configuration   = file["Config"]  #appears to be empty
header          = file["Header"]         #appears to be empty
ids             = file["IDs"]               #appears to be empty
parameters      = file["Parameters"] #appears to be empty
group           = file["Group"]           #contains ['GroupAscale', 'GroupFirstSub', 'GroupLen', 'GroupLenType', 'GroupMass', 'GroupMassType', 'GroupNsubs', 'GroupOffsetType', 'GroupPos', 'GroupVel', 'Group_M_Crit200', 'Group_M_Crit500', 'Group_M_Mean200', 'Group_M_TopHat200', 'Group_R_Crit200', 'Group_R_Crit500', 'Group_R_Mean200', 'Group_R_TopHat200']
subhalo         = file["Subhalo"]       #contains ['SubhaloCM', 'SubhaloGroupNr', 'SubhaloHalfmassRad', 'SubhaloHalfmassRadType', 'SubhaloIDMostbound', 'SubhaloLen', 'SubhaloLenType', 'SubhaloMass', 'SubhaloMassType', 'SubhaloOffsetType', 'SubhaloParentRank', 'SubhaloPos', 'SubhaloRankInGr', 'SubhaloSpin', 'SubhaloVel', 'SubhaloVelDisp', 'SubhaloVmax', 'SubhaloVmaxRad']

# file = h5py.File(str(directory)+r"\subhalo_snapshot_038.hdf5", "r")

# configuration = file["Config"]  #appears to be empty
# header = file["Header"]         #appears to be empty
# parameters = file["Parameters"] #appears to be empty
# parttype1 = file["PartType1"]   #contains ['Coordinates', 'ParticleIDs', 'SubfindDensity', 'SubfindHsml', 'SubfindVelDisp', 'Velocities']

group_positions = group["GroupPos"][:]
group_radii     = group["Group_R_Crit200"][:]
group_masses    = group["Group_M_Crit200"][:]

# file = h5py.File(directory / "subhalo_snapshot_038.hdf5", "r") #for whole duration
# file = h5py.File(directory / "snapshot_018.hdf5", "r") #for small boxes
file = h5py.File(directory / "snapshot_016.hdf5", "r") #for e5 boxes 256

# parttype1             = file["PartType1"]   #contains ['Coordinates', 'ParticleIDs', 'SubfindDensity', 'SubfindHsml', 'SubfindVelDisp', 'Velocities']
# original_coordinates    = file["PartType1"]["Coordinates"][:] #for cdm particles

parttype1               = file["PartType0"]   #contains ['Coordinates', 'ParticleIDs', 'SubfindDensity', 'SubfindHsml', 'SubfindVelDisp', 'Velocities']
original_coordinates    = file["PartType0"]["Coordinates"][:] #for pbh particles


# boundaries = [30., 30., 30.] #BoxLength in MonofonIC is 30.
# boundaries = [2.77048, 2.77048, 2.77048] #BoxLength for small boxes depends on Nres, 2.77048 for 64, 5.54096 for 128.
boundaries = [2.36438, 2.36438, 2.36438] #BoxLength for e5 boxes depends on Nres, 2.36438 for 256, 4.72876 for 512.


offsets = [-1, 0, 1]
coordinates = original_coordinates[:]
number_of_time_that_points_have_been_found = 0

#assumes cube form and 0.1 as desired ratio to move
minimum = 0.0
maximum = max(boundaries)
ratio = 0.1
box_length = maximum - minimum  
range_to_move = 0.1 * box_length
upper_limit_bottom = minimum + range_to_move
lower_limit_top = maximum - range_to_move

print("Find candidates to move...")

@numba.njit()
def find_move_candidates():
    move_candidates = []
    for point in original_coordinates:
        if{
                minimum <= point[0] <= upper_limit_bottom or 
                lower_limit_top <= point[0] <= maximum or 
                minimum <= point[1] <= upper_limit_bottom or 
                lower_limit_top <= point[1] <= maximum or 
                minimum <= point[2] <= upper_limit_bottom or 
                lower_limit_top <= point[2] <= maximum
            }:
            move_candidates.append(point)
    return move_candidates
    
move_candidates = find_move_candidates()
print("...done.")

for x in offsets:
    for y in offsets:
        for z in offsets:
            if (x, y, z) == (0, 0, 0):
                continue
            moved_coordinates = find_coordinates_to_move(minimum, maximum, ratio, x, y, z, move_candidates) 
            moved_coordinates += np.array([x * boundaries[0], y * boundaries[1], z * boundaries[2]])
            coordinates = np.vstack((coordinates, moved_coordinates))
            number_of_time_that_points_have_been_found += 1
            print("Points found: " + str(number_of_time_that_points_have_been_found) + "/26...")
                    
# assert coordinates.shape[0] == original_coordinates.shape[0] * 3 ** 3 #check that the new space has the shape we want it to have
                    
print("Building 3d-Tree for all particles...")
tree = KDTree(coordinates)
print("...done.")

print("Searching group members...")
group_member_indices = tree.query_ball_point(group_positions, group_radii, workers=6)
assert len(group_member_indices) == len(group_positions)
print("...found.")

print("Calculating radial bins and saving data...")
for i in range(len(group_positions)):
    group_center = group_positions[i]
    group_radius = group_radii[i]
    group_mass   = group_masses[i]
    if group_radius == 0 or group_mass == 0:
        continue                #Not quite sure how this can happen, but apparently there are groups with a radius or mass of zero (and they are not necessarily the same).
    radial_bins = np.arange(0, group_radius + group_radius/10, group_radius/10)
    members = [coordinates[j] for j in group_member_indices[i]]
    members_in_bins = [] #should better be called distances now
    
    for member in members:
        distance = np.linalg.norm(group_center - member)
        members_in_bins.append(distance)
        #The following already sorts into bins, but that's not ideal for changing bins to e.g. logarithmic values.
        # for r in range(len(radial_bins)-1): #-1 because no value is going to be above radial_bins[10] anyway
        #     if radial_bins[r] <= distance < radial_bins[r + 1]:
        #         members_in_bins.append(radial_bins[r] + group_radius/20)
    assert len(members) == len(members_in_bins)
    
    group_ID            = [i+1] * len(members)
    group_radius_list   = [group_radius] * len(members)
    group_mass_list     = [group_mass] * len(members)
    
    all_data = np.column_stack((group_ID, group_radius_list, group_mass_list, members_in_bins))
    np.savetxt(directory/"density_profiles_16"/f"group{i+1}.csv", all_data, delimiter=",", fmt="%.3f", header="ID,R200,M200,Bin")
print("...done.")
                
    
    


    
    
    
    




