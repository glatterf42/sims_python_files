# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 19:11:42 2021

@author: Ben Melville
"""
import time
from pathlib import Path
from sys import getsizeof

import h5py
import numpy as np
import scipy.spatial

"""
Use this section to find out how many particles there are. The second part retrieves the total mass of cdm or pbh particles, which is all we need because we only have one type of particle in every simulation.
"""

# paths = [Path(r"C:\Users\Ben Melville\Documents\Studium\MSc Thesis\cosmo_sims\64_cdm"), Path(r"C:\Users\Ben Melville\Documents\Studium\MSc Thesis\cosmo_sims\64_pbh"), Path(r"C:\Users\Ben Melville\Documents\Studium\MSc Thesis\cosmo_sims\128_cdm"), Path(r"C:\Users\Ben Melville\Documents\Studium\MSc Thesis\cosmo_sims\128_pbh")]
cdm_paths = [Path(r"C:\Users\Ben Melville\Documents\Studium\MSc Thesis\cosmo_sims\64_cdm"), Path(r"C:\Users\Ben Melville\Documents\Studium\MSc Thesis\cosmo_sims\128_cdm")]
pbh_paths = [Path(r"C:\Users\Ben Melville\Documents\Studium\MSc Thesis\cosmo_sims\64_pbh"), Path(r"C:\Users\Ben Melville\Documents\Studium\MSc Thesis\cosmo_sims\128_pbh")]


# for path in pbh_paths:
#     file = h5py.File(str(path)+"\snapshot_000.hdf5", "r")
#     names = file["PartType0"]["ParticleIDs"][:]
#     print("There are "+str(len(names))+" particles.")

# for path in cdm_paths:
#     file = h5py.File(str(path)+"\snapshot_000.hdf5", "r")
#     names = file["PartType1"]["ParticleIDs"][:]
#     print("There are "+str(len(names))+" particles.")

# for path in pbh_paths:
#     filename = str(path)+"\energy.txt"
#     file = np.loadtxt(filename)
#     print("File: "+filename+" Total mass: "+str(file[0][22])+"\n")

# for path in cdm_paths:
#     filename = str(path)+"\energy.txt"
#     file = np.loadtxt(filename)
#     print("File: "+filename+" Total mass: "+str(file[0][23])+"\n")

#For Standard DM-L50-N128, there are 2097152 particles, i.e for Nres=128. For Nres=64, there are 262144 particles.
#For our cosmos-sims, the total amount of mass is always the same: 232209.09 (units unclear!)

"""
Use this section to extract the desired data from every snapshot. Start with
a random selection of particles to enable faster testing with ParaView. Raw 
String needed to read spaces; filename.with_suffix(".csv").name works thanks to 
Lukas.
"""


#indices = np.random.choice(np.arange(2097152), 100000, replace=False) #for Nres=128
#indices = np.random.choice(np.arange(262144), 100000, replace=False) #for Nres=64

# directory = Path(r"C:\Users\Ben Melville\Documents\Studium\MSc Thesis\cosmo_sims\64_cdm")
directory = Path(".")
total_mass = 232209.09 #retrieved from above
Nres = 64 #choose one of this or the following:
#Nres = 128
mass_per_particle = total_mass / (Nres**3)

for filename in sorted(directory.glob("snapshot_*.hdf5")):
    print(filename)
    file = h5py.File(str(filename), "r")

    coordinates = file["PartType1"]["Coordinates"][:] #for cdm particles
    names = file["PartType1"]["ParticleIDs"][:]
    velocities = file["PartType1"]["Velocities"][:]

    print("building 3d-Tree")
    tree = scipy.spatial.KDTree(coordinates)
    print(getsizeof(tree)/1024,"KB")
    print("tree built")

    # coordinates = file["PartType0"]["Coordinates"][:] #for pbh particles
    # names = file["PartType0"]["ParticleIDs"][:]
    # velocities = file["PartType0"]["Velocities"][:]

    absolute_velo = np.sqrt(np.sum(velocities**2, axis=1))
    print(len(names))

    print("searching neighbours")
    a = time.perf_counter_ns()
    closest_neighbours, indices = tree.query([coordinates], k=40, workers=6)
    # shape of closest_neighbours: (1, 262144, 40)
    b = time.perf_counter_ns()
    print("found neighbours")
    print(f"took {(b - a) / 1000 / 1000:.2f} ms")
    closest_neighbours = closest_neighbours[0]  # to (262144, 40)
    densities = 40 * mass_per_particle / np.mean(closest_neighbours, axis=1) ** 3

    print(closest_neighbours.shape)
    print(densities)
    print(densities.shape)
    all_data = np.append(coordinates, velocities, axis=1)
    all_data = np.column_stack((all_data, absolute_velo, names, densities))
    sorted_index = np.argsort(all_data[::,7], kind="stable")
    all_data = all_data[sorted_index, :]

#    np.savetxt("out_"+filename.with_suffix(".csv").name, all_data[indices], delimiter=",", fmt="%.3f", header="x,y,z,vx,vy,vz,v,name") #if indices are needed
    np.savetxt(directory/f"out_{filename.stem}.csv", all_data, delimiter=",", fmt="%.3f", header="x,y,z,vx,vy,vz,v,name,density")
    print(all_data.shape)


"""
This section is the old version of reading in just one file. It shows some 
underlying structure and gives the option of using all data.
"""


# file = h5py.File("snapshot_000.hdf5", "r")

# configuration = file["Config"]
# header = file["Header"]
# parameters = file["Parameters"]
# data_b = file["PartType0"] #according to Oliver's program, Type_0 are the baryons and Type_1 the cdms
# coordinates_b = data_b["Coordinates"][:]
# names_b = data_b["ParticleIDs"][:]
# velocities_b = data_b["Velocities"][:]

# data_c = file["PartType1"] #all keys used here: ['Coordinates', 'ParticleIDs', 'Velocities']
# coordinates_c = data_c["Coordinates"][:]
# names_c = data_c["ParticleIDs"][:]
# velocities_c = data_c["Velocities"][:]



#print(configuration)
#print("------------")
#print(header)
#print("------------")
#print(parameters)
#print("------------")
#print(data_b) #keys contained in data_b: ['Coordinates', 'Density', 'InternalEnergy', 'ParticleIDs', 'SmoothingLength', 'Velocities']



"""
absolute_velo = np.sqrt(np.sum(velocities**2, axis=1))

all_data = np.append(coordinates, velocities, axis=1)
all_data = np.column_stack((all_data, absolute_velo, names))
sorted_index = np.argsort(all_data[::, 7], kind="stable")
all_data = all_data[sorted_index, :]

np.savetxt("out.csv", all_data[indices], delimiter=",", fmt="%.3f", header="x,y,z,vx,vy,vz,v,name")
#np.savetxt("out_all.csv", all_data, delimiter=",", fmt="%.3f", header="x,y,z,vx,vy,vz,v,name")
print(all_data.shape)
"""

"""
For the plane wave test, we don't need 3-D plots, we just want to plot z-coordinates as x vs z-velocities as y.
Output times: [0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1]
"""

"""
file = h5py.File("snapshot_000.hdf5", "r")

data_b = file["PartType0"]                  #according to Oliver's program, Type_0 are the baryons and Type_1 the cdms
z_b = data_b["Coordinates"][:,2]
names_b = data_b["ParticleIDs"][:]
vz_b = data_b["Velocities"][:,2]

data_c = file["PartType1"] 
z_c = data_c["Coordinates"][:,2]
names_c = data_c["ParticleIDs"][:]
vz_c = data_c["Velocities"][:,2]

plt.figure()
plt.plot( z_b, vz_b, '.', label='type b' )
plt.plot( z_c, vz_c, '.', label='type c' )
plt.legend()
plt.show()
"""
