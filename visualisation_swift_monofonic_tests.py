#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import vtk
import sys
import time
from pathlib import Path
from sys import getsizeof

import h5py
import numba
import numpy as np
import scipy.spatial


@numba.njit()
def determine_desired_range(offset, minimum, upper_limit_bottom, lower_limit_top, maximum):
    a = minimum
    b = maximum

    if offset < 0:
        a = lower_limit_top
    elif offset > 0:
        b = upper_limit_bottom

    return a, b


@numba.njit()
def find_coordinates_to_move(minimum, maximum, x_offset, y_offset, z_offset, move_candidates):
    coordinates_to_move = []
    x_start, x_end = determine_desired_range(x_offset, minimum, upper_limit_bottom, lower_limit_top, maximum)
    y_start, y_end = determine_desired_range(y_offset, minimum, upper_limit_bottom, lower_limit_top, maximum)
    z_start, z_end = determine_desired_range(z_offset, minimum, upper_limit_bottom, lower_limit_top, maximum)

    for particle in move_candidates:
        point = particle[0:3]
        if x_start <= point[0] <= x_end and y_start <= point[1] <= y_end and z_start <= point[2] <= z_end:
            coordinates_to_move.append(particle)

    return coordinates_to_move


directory = Path(r"/home/ben/sims/data_swift/monofonic_tests/shannon_256_100/")

for filename in sorted(directory.glob("output_0004.hdf5")):
    print(filename)
    file = h5py.File(str(filename), "r")
    Header = file['Header']

    original_coordinates = file["PartType1"]["Coordinates"][:]  # for cdm particles
    names = file["PartType1"]["ParticleIDs"][:]
    velocities = file["PartType1"]["Velocities"][:]
    masses = file['PartType1']['Masses'][:]
    group_ids = file['PartType1']['FOFGroupIDs'][:]
    absolute_velo = np.sqrt(np.sum(velocities ** 2, axis=1))

    original_data = np.vstack([
        original_coordinates[::, 0],
        original_coordinates[::, 1],
        original_coordinates[::, 2],
        names,
        velocities[::, 0],
        velocities[::, 1],
        velocities[::, 2],
        masses,
        group_ids,
        absolute_velo,
    ]).T
    print(original_data.shape)
    assert (original_coordinates == original_data[::, 0:3]).all()

    boundaries = Header.attrs['BoxSize']  # BoxLength for e5 boxes depends on Nres, 2.36438 for 256, 4.72876 for 512.
    print(boundaries, len(names))
    if not boundaries.shape:
        boundaries = np.array([boundaries] * 3)
    offsets = [-1, 0, 1]
    transformed_data = original_data[:]
    number_of_time_that_points_have_been_found = 0

    # assumes cube form and 0.1 as desired ratio to move
    minimum = 0.0
    maximum = max(boundaries)
    box_length = maximum - minimum
    # magic number: mean particle separation * 15 in units of box_length
    range_to_move = 0.0586 * box_length  # mean particle separation: 0.78125 Mpc for 128, 0.390625 Mpc for 256, etc
    upper_limit_bottom = minimum + range_to_move
    lower_limit_top = maximum - range_to_move

    print("Find candidates to move...")


    @numba.njit()
    def find_move_candidates():
        move_candidates = []
        print("finding move candidates")
        for particle in original_data:
            point = particle[0:3]
            if (
                    minimum <= point[0] <= upper_limit_bottom or
                    lower_limit_top <= point[0] <= maximum or
                    minimum <= point[1] <= upper_limit_bottom or
                    lower_limit_top <= point[1] <= maximum or
                    minimum <= point[2] <= upper_limit_bottom or
                    lower_limit_top <= point[2] <= maximum
            ):
                move_candidates.append(particle)
                # print(point)
        return move_candidates


    move_candidates = find_move_candidates()
    move_candidates = np.array(move_candidates)

    print("...done.")
    for x in offsets:
        for y in offsets:
            for z in offsets:
                if (x, y, z) == (0, 0, 0):
                    continue
                moved_coordinates = find_coordinates_to_move(minimum, maximum, x, y, z, move_candidates)
                # print(moved_coordinates)
                moved_coordinates = np.array(moved_coordinates)
                # if not moved_coordinates.all():
                #     print(f"nothing moved in {(x,y,z)}")
                #     continue
                moved_coordinates[::, 0] += x * boundaries[0]
                moved_coordinates[::, 1] += y * boundaries[1]
                moved_coordinates[::, 2] += z * boundaries[2]
                transformed_data = np.vstack((transformed_data, moved_coordinates))
                number_of_time_that_points_have_been_found += 1
                print(f"Points found: {number_of_time_that_points_have_been_found}/26...")

    # assert coordinates.shape[0] == original_coordinates.shape[0] * 3 ** 3 #check that the new space has the shape we want it to have

    num_nearest_neighbors = 40
    print("Building 3d-Tree for all particles...")
    coordinates = transformed_data[::, 0:3]
    print(coordinates.shape)
    tree = scipy.spatial.KDTree(coordinates)
    print(getsizeof(tree) / 1024, "KB")
    print("...done.")
    print("Searching neighbours...")
    a = time.perf_counter_ns()
    distances, indices = tree.query([coordinates], k=num_nearest_neighbors, workers=6)
    # shape of closest_neighbours: (1, xxxx, 40)
    b = time.perf_counter_ns()
    print("...found neighbours.")
    print(f"took {(b - a) / 1000 / 1000:.2f} ms")
    distances = distances[0]  # to (xxxx, 40)
    indices = indices[0]  # to (xxxx, 40)
    print(distances.shape)
    print(indices.shape)
    print(indices)
    mass_array = []
    print("fetching masses")
    for subindices in indices:  # subindices is (40)
        # can maybe be optimized to remove loop
        masses = transformed_data[subindices, 7]
        mass_array.append(masses)
    mass_array = np.array(mass_array)
    print("finished fetching masses")
    # print(closest_neighbours, indices)
    # print(indices)

    # densities = num_nearest_neighbors * mass_per_particle / np.mean(closest_neighbours, axis=1) ** 3
    total_masses = np.sum(mass_array, axis=1)
    densities = total_masses / np.mean(distances, axis=1) ** 3
    alt_densities = total_masses / np.max(distances, axis=1) ** 3

    # print(closest_neighbours.shape)

    # print(densities)
    # print(densities.shape)
    all_data = np.column_stack([list(range(densities.shape[0])), transformed_data, densities, alt_densities])
    # print(all_data.shape)
    # print(original_data.shape[0])
    export_data = all_data[:original_data.shape[0]]
    # print(export_data.shape)

    # all_data = np.append(coordinates, velocities, axis=1)
    # all_data = np.column_stack((all_data, absolute_velo, names, densities))
    # sorted_index = np.argsort(all_data[::, 7], kind="stable")
    # all_data = all_data[sorted_index, :]

    #    np.savetxt("out_"+filename.with_suffix(".csv").name, all_data[indices], delimiter=",", fmt="%.3f", header="x,y,z,vx,vy,vz,v,name") #if indices are needed
    np.savetxt(directory / f"visualisation_{filename.with_suffix('.csv').name}",
               export_data,
               delimiter=",",
               fmt="%.3f",
               header="num,x,y,z,name,vx,vy,vz,masse,groupid,v,density,density_alt")
    file.close()
