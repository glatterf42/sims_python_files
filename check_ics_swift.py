#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 11:16:06 2022

@author: ben
"""

import h5py
from pathlib import Path

# directory = Path(r"/home/ben/sims/swiftsim/examples/agora/")
# directory = Path(r"/home/ben/Pictures/Gadget4/vsc4_256/")
directory = Path(r'/home/ben/sims/music-panphasia/test/')


file = h5py.File(directory / "agora_128.hdf5", "r") 
# file = h5py.File(directory / "output_0001.hdf5", "r") 

# file = h5py.File(directory / "cosmo_ics_gadget_256_pbh_vsc.hdf5", "r") 

for key in file.keys():
    print(key) #for finding all header entries, which are:
        

Header = file["Header"]
#ICs_parameters = file["ICs_parameters"]
PartType1 = file["PartType1"]
Units = file["Units"]
# PartType2 = file['PartType2']

print(list(Header.attrs.items()))


print(PartType1.keys())
# print(PartType2.keys())
print(PartType1['Masses'][0:10])

print(PartType1['Velocities'][0:10])



# print(PartType2['Masses'][0:10])
# print(list(Units.attrs.items()))

# use list(Header.attr.keys()) to list all attributes contained in the Header and .attr.values() to see their values
# even otherwise empty things like ICs_parameters can contain such attributes
