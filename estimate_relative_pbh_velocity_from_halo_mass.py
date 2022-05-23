import numpy as np

G = 42.981 #everything here is in Gadget-units

def v_halo_from_mass(m_halo:int, L_box: float, N_res:int, m_particle:float):

    m_box = N_res**3 * m_particle 

    rho_mean = m_box / (L_box ** 3)
    rho_halo = 200 * rho_mean

    r_halo = (3 * m_halo / (4 * np.pi * rho_halo)) ** (1/3)

    v_halo = np.sqrt(G * m_halo / r_halo)

    return v_halo

v_result = v_halo_from_mass(m_halo=0.000067742, L_box=30.0, N_res=128, m_particle=0.1107263)

print(v_result)


# #Results:
# 11.75 for 0.067742 * 10^10 / h
# 6.21 for 0.01 ...
# 2.88 for 0.001 ...
# 1.17 for 0.000067742 ... (i.e. 10^6 M_sun halos, i.e. three orders of magnitude smaller than the 10^9 we started with)

