#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  4 13:43:40 2022

@author: ben
"""

from pathlib import Path
from directories import swift_output_basedir, swift_mon_test_basedir
from sys import argv

def create_dir_and_write_params_swift(Nres: int, Lbox: float, waveform: str, output_basedir: Path):
    # create directory if it doesn't exist already
    outputdir = output_basedir / f"{waveform}_{Nres}_{Lbox:.0f}"
    if outputdir.exists():
        print(outputdir, "already exists. Skipping...")
    else:
        print("creating", outputdir)
        outputdir.mkdir()
    
    # write param file there:
    param_script = f"""
# Define some meta data about the simulation.
MetaData:
    run_name:   mon_test_{waveform}_{Nres}_{Lbox:.0f}

# Define the system of units to use internally.
InternalUnitSystem:
    UnitMass_in_cgs:     1.98848e43    # 10^10 M_sun in grams
    UnitLength_in_cgs:   3.08567758e24 # 1 Mpc in centimeters
    UnitVelocity_in_cgs: 1e5           # 1 km/s in centimeters per second
    UnitCurrent_in_cgs:  1             # 1 Ampere
    UnitTemp_in_cgs:     1             # 1 Kelvin


# Values of some physical constants
#PhysicalConstants:
#    G:            6.67408e-8 # (Optional) Overwrite the value of Newton's constant used internally by the code.

# Cosmological parameters # update according to monofonic output
Cosmology:
    h:              0.67742       # Reduced Hubble constant
    a_begin:        0.02          # Initial scale-factor of the simulation, z = 49
    a_end:          1.0           # Final scale factor of the simulation, z = 0
    Omega_cdm:      0.2610089     # CDM density parameter, new: Omega_m = _cdm + _b (w/o neutrinos)
    Omega_lambda:   0.690021      # Dark-energy density parameter
    Omega_b:        0.0488911     # Baryon density parameter

# Parameters for the self-gravity scheme
Gravity:
    mesh_side_length:              {Nres * 2}# Number of cells along each axis for the periodic gravity mesh (must be even).
    eta:                           0.025     # Constant dimensionless multiplier for time integration.
    MAC:                           adaptive  # Choice of mulitpole acceptance criterion: 'adaptive' OR 'geometric'.
    epsilon_fmm:                   0.001     # Tolerance parameter for the adaptive multipole acceptance criterion.
    theta_cr:                      0.7       # Opening angle for the purely gemoetric criterion.
    # use_tree_below_softening:      0         # (Optional) Can the gravity code use the multipole interactions below the softening scale?
    # allow_truncation_in_MAC:       0         # (Optional) Can the Multipole acceptance criterion use the truncated force estimator?
    comoving_DM_softening:         {Lbox / Nres / 30} # Comoving Plummer-equivalent softening length for DM particles (in internal units).
    max_physical_DM_softening:     {Lbox / Nres / 30} # Maximal Plummer-equivalent softening length in physical coordinates for DM particles (in internal units). #should work b/c Lbox is given in Mpc=internal unit
    rebuild_frequency:             0.01      # (Optional) Frequency of the gravity-tree rebuild in units of the number of g-particles (this is the default value).
    a_smooth:                      1.25      # (Optional) Smoothing scale in top-level cell sizes to smooth the long-range forces over (this is the default value).
    r_cut_max:                     4.5       # (Optional) Cut-off in number of top-level cells beyond which no FMM forces are computed (this is the default value).
    r_cut_min:                     0.1       # (Optional) Cut-off in number of top-level cells below which no truncation of FMM forces are performed (this is the default value).

# FOF group finding parameters
FOF:
    basename:                        fof_output  # Filename for the FOF outputs (Unused when FoF is only run to seed BHs).
    scale_factor_first:              0.91        # Scale-factor of first FoF black hole seeding calls (needed for cosmological runs).
    delta_time:                      1.005       # Time between consecutive FoF black hole seeding calls.
    min_group_size:                  256         # The minimum no. of particles required for a group.
    linking_length_ratio:            0.2         # Linking length in units of the main inter-particle separation.
    seed_black_holes_enabled:        0           # Enable (1) or disable (0) seeding of black holes in FoF groups
    dump_catalogue_when_seeding:     0           # Enable (1) or disable (0) dumping a group catalogue when runnning FOF for seeding purposes.
    absolute_linking_length:         -1.         # (Optional) Absolute linking length (in internal units). When not set to -1, this will overwrite the linking length computed from 'linking_length_ratio'.
    group_id_default:                2147483647  # (Optional) Sets the group ID of particles in groups below the minimum size. Defaults to 2^31 - 1 if unspecified. Has to be positive.
    group_id_offset:                 1           # (Optional) Sets the offset of group ID labeling. Defaults to 1 if unspecified.

# Parameters governing the time integration (Set dt_min and dt_max to the same value for a fixed time-step run.)
TimeIntegration:
    dt_min:              1e-6  # The minimal time-step size of the simulation (in internal units).
    dt_max:              0.025  # The maximal time-step size of the simulation (in internal units).

# Parameters governing the snapshots
Snapshots:
    basename:   output        # Common part of the name of output files.
    # subdir:     dir         # (Optional) Sub-directory in which to write the snapshots. Defaults to "" (i.e. the directory where SWIFT is run).
    scale_factor_first: 0.1   # (Optional) Scale-factor of the first snapshot if cosmological time-integration.
    delta_time: 0.01          # Time difference between consecutive outputs (in internal units)
    # invoke_stf: 0           # (Optional) Call VELOCIraptor every time a snapshot is written irrespective of the VELOCIraptor output strategy.
    invoke_fof: 1           # (Optional) Call FOF every time a snapshot is written
    # compression: 0          # (Optional) Set the level of GZIP compression of the HDF5 datasets [0-9]. 0 does no compression. The lossless compression is applied to *all* the fields.
    # distributed: 0          # (Optional) When running over MPI, should each rank write a partial snapshot or do we want a single file? 1 implies one file per MPI rank.
    # UnitMass_in_cgs:     1  # (Optional) Unit system for the outputs (Grams)
    # UnitLength_in_cgs:   1  # (Optional) Unit system for the outputs (Centimeters)
    # UnitVelocity_in_cgs: 1  # (Optional) Unit system for the outputs (Centimeters per second)
    # UnitCurrent_in_cgs:  1  # (Optional) Unit system for the outputs (Amperes)
    # UnitTemp_in_cgs:     1  # (Optional) Unit system for the outputs (Kelvin)
    output_list_on:        1  # (Optional) Enable the output list
    output_list: {swift_mon_test_basedir}/snap_times.txt # (Optional) File containing the output times (see documentation in "Parameter File" section)
    # select_output_on:    0  # (Optional) Enable the output selection behaviour
    # select_output:       selectoutput.yml # (Optional) File containing information to select outputs with (see documentation in the "Output Selection" section) 

# Parameters governing the conserved quantities statistics
Statistics:
    delta_time:           1.1        # Time between statistics output
    scale_factor_first:     0.1       # (Optional) Scale-factor of the first statistics dump if cosmological time-integration.
    energy_file_name:    statistics   # (Optional) File name for statistics output
    timestep_file_name:  timesteps    # (Optional) File name for timing information output. Note: No underscores "_" allowed in file name
    output_list_on:      1   	    # (Optional) Enable the output list
    output_list:         {swift_mon_test_basedir}/snap_times.txt # (Optional) File containing the output times (see documentation in "Parameter File" section)

# Parameters related to the initial conditions
InitialConditions:
    file_name:  {swift_output_basedir}/{waveform}_{Nres}_{Lbox:.0f}/ics_{waveform}_{Nres}_{Lbox:.0f}.hdf5 # The file to read
    periodic:                    1    # Are we running with periodic ICs?
    cleanup_h_factors:           0    # (Optional) Clean up the h-factors used in the ICs (e.g. in Gadget files).
    cleanup_velocity_factors:    0    # (Optional) Clean up the scale-factors used in the definition of the velocity variable in the ICs (e.g. in Gadget files).
    cleanup_smoothing_lengths:   0    # (Optional) Clean the values of the smoothing lengths that are read in to remove stupid values. Set to 1 to activate.
    smoothing_length_scaling:    1.   # (Optional) A scaling factor to apply to all smoothing lengths in the ICs.
    replicate:  1                     # (Optional) Replicate all particles along each axis a given integer number of times. Default 1.
    remap_ids:  0                     # (Optional) Remap all the particle IDs to the range [1, NumPart].
    metadata_group_name: ICs_parameters # (Optional) Copy this HDF5 group from the initial conditions file to all snapshots, if found

# Parameters controlling restarts
Restarts:
    enable:             1          # (Optional) whether to enable dumping restarts at fixed intervals.
    save:               0          # (Optional) whether to save copies of the previous set of restart files (named .prev)
    # onexit:             0          # (Optional) whether to dump restarts on exit (*needs enable*)
    subdir:             restart    # (Optional) name of subdirectory for restart files.
    basename:           restart      # (Optional) prefix used in naming restart files.
    delta_hours:        2.0        # (Optional) decimal hours between dumps of restart files.
    stop_steps:         100        # (Optional) how many steps to process before checking if the <subdir>/stop file exists. When present the application will attempt to exit early, dumping restart files first.
    max_run_time:       24.0       # (optional) Maximal wall-clock time in hours. The application will exit when this limit is reached.
    # resubmit_on_exit:   0          # (Optional) whether to run a command when exiting after the time limit has been reached.
    # resubmit_command:   ./resub.sh # (Optional) Command to run when time limit is reached. Compulsory if resubmit_on_exit is switched on. Note potentially unsafe.

# Parameters governing domain decomposition
# DomainDecomposition:
#     initial_type:     memory    # (Optional) The initial decomposition strategy: "grid",
#                                 #            "region", "memory", or "vectorized".
#     initial_grid: [10,10,10]    # (Optional) Grid sizes if the "grid" strategy is chosen.

#     synchronous:      0         # (Optional) Use synchronous MPI requests to redistribute, uses less system memory, but slower.
#     repartition_type: fullcosts # (Optional) The re-decomposition strategy, one of:
#                                 # "none", "fullcosts", "edgecosts", "memory" or
#                                 # "timecosts".
#     trigger:          0.05      # (Optional) Fractional (<1) CPU time difference between MPI ranks required to trigger a
#                                 # new decomposition, or number of steps (>1) between decompositions
#     minfrac:          0.9       # (Optional) Fractional of all particles that should be updated in previous step when
#                                 # using CPU time trigger
#     usemetis:         0         # Use serial METIS when ParMETIS is also available.
#     adaptive:         1         # Use adaptive repartition when ParMETIS is available, otherwise simple refinement.
#     itr:              100       # When adaptive defines the ratio of inter node communication time to data redistribution time, in the range 0.00001 to 10000000.0.
#                                 # Lower values give less data movement during redistributions, at the cost of global balance which may require more communication.
#     use_fixed_costs:  0         # If 1 then use any compiled in fixed costs for
#                                 # task weights in first repartition, if 0 only use task timings, if > 1 only use
#                                 # fixed costs, unless none are available
"""
    
    with (outputdir / f"{waveform}_{Nres}_{Lbox:.0f}_param.yml").open("w") as f:
        f.write(param_script)
    
            
if __name__ == "__main__":
    create_dir_and_write_params_swift(
        Nres=int(argv[1]),
        Lbox=float(argv[2]),
        waveform=argv[3],
        output_basedir=swift_output_basedir
        )
