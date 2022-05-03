import numpy as np

def get_highres_ID_from_lowres(particle_ID: int, Nres_low: int, Nres_high: int):
    particle_k = particle_ID % Nres_low
    particle_j = ((particle_ID - particle_k) // Nres_low) % Nres_low
    particle_i = ((particle_ID - particle_k) // Nres_low - particle_j) // Nres_low
    highres_ID = ((particle_i * Nres_high) + particle_j) * Nres_high + particle_k
    return highres_ID

def get_lowres_ID_from_highres(particle_ID: int, Nres_low: int, Nres_high: int):
    particle_k = particle_ID % Nres_high
    particle_j = ((particle_ID - particle_k) // Nres_high) % Nres_high
    particle_i = ((particle_ID - particle_k) // Nres_high - particle_j) // Nres_high
    lowres_ID = ((particle_i * Nres_low) + particle_j) * Nres_low + particle_k
    return lowres_ID

if __name__ == "__main__": 
    test_particle = np.array([0, 127, 127])
    # maximum_test = np.array([127, 127, 127]) #this works, Nres - 1 is the maximum for (i,j,k)

    Nres_1 = 128
    Nres_2 = 256

    particle_ID_1 = ((test_particle[0] * Nres_1) + test_particle[1]) * Nres_1 + test_particle[2]
    particle_ID_2 = ((test_particle[0] * Nres_2) + test_particle[1]) * Nres_2 + test_particle[2]

    print(particle_ID_1, particle_ID_2)

    particle_ID_1_converted = get_highres_ID_from_lowres(particle_ID_1, Nres_1, Nres_2)
    particle_ID_1_converted_converted = get_lowres_ID_from_highres(particle_ID_1_converted, Nres_1, Nres_2)

    print(particle_ID_1, particle_ID_1_converted, particle_ID_1_converted_converted)
