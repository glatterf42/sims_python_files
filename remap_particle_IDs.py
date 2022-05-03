import numpy as np


def convert_ID_between_resolutions(particle_ID: int, Nres_from: int, Nres_to: int):
    particle_k = particle_ID % Nres_from
    particle_j = ((particle_ID - particle_k) // Nres_from) % Nres_from
    particle_i = ((particle_ID - particle_k) // Nres_from - particle_j) // Nres_from
    lowres_ID = ((particle_i * Nres_to) + particle_j) * Nres_to + particle_k
    return lowres_ID


if __name__ == "__main__":
    test_particle = np.array([0, 127, 127])
    # maximum_test = np.array([127, 127, 127]) #this works, Nres - 1 is the maximum for (i,j,k)

    Nres_1 = 128
    Nres_2 = 256

    particle_ID_1 = ((test_particle[0] * Nres_1) + test_particle[1]) * Nres_1 + test_particle[2]
    particle_ID_2 = ((test_particle[0] * Nres_2) + test_particle[1]) * Nres_2 + test_particle[2]

    print(particle_ID_1, particle_ID_2)

    particle_ID_1_converted = convert_ID_between_resolutions(particle_ID_1, Nres_1, Nres_2)
    particle_ID_1_converted_converted = convert_ID_between_resolutions(particle_ID_1_converted, Nres_2, Nres_1)

    print(particle_ID_1, particle_ID_1_converted, particle_ID_1_converted_converted)
