#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 22 16:14:20 2022

@author: ben

Currently for 256 particles
"""

from pathlib import Path
from sys import argv
from directories import swift_basedir, swift_output_basedir, swift_mon_test_basedir, swift_tool_basedir, python_base

n_tasks = 48 # used 8 for 128, use 48 for 256.

def write_job_script(Nres: int, Lbox: float, waveform: str, output_dir: Path):
    output_dir_string = str(output_dir)
    
# replaced line #SBATCH --mem={2 * n_tasks}G with --exclusive for now to get all the memory
# deleted --ntasks-per-core=1
    script = f"""#!/bin/bash
#SBATCH --mail-type=ALL
#SBATCH --mail-user=a01611430@unet.univie.ac.at
#SBATCH --time=04:00:00
#SBATCH --nodes=1 #equal to -N 1
#SBATCH --ntasks-per-node={n_tasks}
#SBATCH --exclusive
#SBATCH --job-name MON_{Nres}
#SBATCH -o mon_{waveform}_{Nres}.out
 
module load gcc/9.1.0-gcc-4.8.5-mj7s6dg
module load openmpi/3.1.4-gcc-9.1.0-fdssbx5
module load gsl/2.5-gcc-9.1.0-ucmpak4
module load fftw/3.3.8-gcc-9.1.0-2kyouz7
module load libtool/2.4.6-gcc-9.1.0-vkpnfol
module load hdf5/1.10.5-gcc-9.1.0-rolgskh
module load metis/5.1.0-gcc-9.1.0-gvmpssi
module load python/3.9.4-gcc-9.1.0-l7amfu6

source {python_base}/swift_venv/bin/activate
    
cd $DATA/monofonic_exp_{waveform}/build
mpiexec -np 2 ./monofonIC ../swift_{waveform}_{Nres}_{Lbox:.0f}.conf
  
python3 {python_base}/rename_and_move_ics_swift.py 1 $DATA/monofonic_exp_{waveform}/build {output_dir_string} {waveform} {Nres} {Lbox}

cd $DATA/swiftsim/monofonic_tests/output/{waveform}_{Nres}_{Lbox:.0f}    
{swift_basedir}/examples/swift --cosmology --self-gravity --fof --threads=$SLURM_NPROCS {output_dir}/{waveform}_{Nres}_{Lbox:.0f}_param.yml
    """
    
    with (output_dir / "job.sh").open("w") as f:
        f.write(script)

    
if __name__ == "__main__": 
    write_job_script(
        Nres = int(argv[1]),
        Lbox = float(argv[2]),
        output_dir = swift_output_basedir / f"{argv[3]}_{argv[1]}_{argv[2]}"
        )
    
#shouldn't be necessary anymore:    
# python3 {swift_tool_basedir}/combine_ics.py {output_dir}/ics_{waveform}_{Nres}_{Lbox:.0f}.0.hdf5 {output_dir}/ics_{waveform}_{Nres}_{Lbox:.0f}.hdf5 4

    