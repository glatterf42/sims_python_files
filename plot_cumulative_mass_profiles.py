#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 10:50:06 2022

@author: ben
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

directories = [(Path(r'/home/ben/sims/swiftsim/examples/zoom_tests/auriga6_halo7_8_9'), 'Levelmax 9'), 
                (Path(r'/home/ben/sims/swiftsim/examples/zoom_tests/auriga6_halo7_8_10'), 'Levelmax 10'),
                (Path(r'/home/ben/sims/swiftsim/examples/zoom_tests/auriga6_halo_arj'), 'ARJ')]

for (directory, label) in directories:
    filename = directory / 'cumulative_mass_profile.csv'
    radii, masses = np.loadtxt(filename, dtype=float, delimiter=',', skiprows=1, unpack=True) # unpack seems to deal with formatting of input file
    plt.loglog(radii, masses, label=label)

# # This could be evolved to plot some resolution indicator for the different sims, but I need to save/read in the group_radius somehow.
# Nres = [128, 128, 233.45]
# Lbox = [100, 100, 100]
# group_radius = []

# for i in range(len(Nres)):
#     softening = Lbox[i] / Nres[i] / 30
#     plt.axvline(4 * softening / group_radius, linestyle='--', color='grey')

plt.xlabel(r'R / R$_\mathrm{group}$')
plt.ylabel(r'M [$10^{10} \mathrm{M}_\odot$]')
plt.title('Cumulative Mass Profile Auriga 6')
plt.legend()
plt.show()