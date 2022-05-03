from itertools import product

import numpy as np


def original_position(Nres: int, particle_ID: int):
    particle_k = particle_ID % Nres
    particle_j = ((particle_ID - particle_k) // Nres) % Nres
    particle_i = ((particle_ID - particle_k) // Nres - particle_j) // Nres
    return np.array([particle_i, particle_j, particle_k])


def upscale_IDs(particle_ID: int, Nres_min: int, Nres_max: int):
    assert Nres_max % Nres_min == 0
    N = Nres_max // Nres_min

    orig = original_position(Nres_min, particle_ID)
    mult = orig * N
    for shift in product(range(N), repeat=3):
        variant = mult + np.array(shift)
        yield ((variant[0] * Nres_max) + variant[1]) * Nres_max + variant[2]


def downscale_IDs(particle_ID: int, Nres_max: int, Nres_min: int):
    assert Nres_max % Nres_min == 0
    N = Nres_max // Nres_min

    orig = original_position(Nres_max, particle_ID)
    mult = np.floor_divide(orig, N)
    return ((mult[0] * Nres_min) + mult[1]) * Nres_min + mult[2]


if __name__ == "__main__":
    test_particle = np.array([0, 0, 127])
    # maximum_test = np.array([127, 127, 127]) #this works, Nres - 1 is the maximum for (i,j,k)

    Nres_1 = 128
    Nres_2 = 256

    test_particle_id = ((test_particle[0] * Nres_1) + test_particle[1]) * Nres_1 + test_particle[2]
    print(test_particle_id)

    particle_ID_1_converted = upscale_IDs(test_particle_id, Nres_1, Nres_2)

    for id in particle_ID_1_converted:
        reverse = downscale_IDs(id, Nres_2, Nres_1)
        print(id, reverse)
        assert reverse == test_particle_id
