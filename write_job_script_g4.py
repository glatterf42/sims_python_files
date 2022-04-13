#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 22 16:14:20 2022

@author: ben

Currently for 256 particles
"""

from pathlib import Path
from sys import argv
from directories import g4_basedir, g4_output_basedir, python_base

n_tasks = 48 # used 8 for 128, use 48 for 256.

def write_job_script(Nres: int, Lbox: float, waveform: str, output_dir: Path):
    output_dir_string = str(output_dir)
    
# replaced line #SBATCH --mem={2 * n_tasks}G with --exclusive for now to get all the memory
# deleted --ntasks-per-node={n_tasks} and --ntasks-per-core=1
    script = f"""#!/bin/bash
#SBATCH --mail-type=ALL
#SBATCH --mail-user=a01611430@unet.univie.ac.at
#SBATCH --time=24:00:00
#SBATCH --nodes=1 #equal to -N 1
#SBATCH --exclusive
#SBATCH --job-name MON_{Nres}
#SBATCH -o mon_{waveform}_{Nres}.out
 
module load gcc/9.1.0-gcc-4.8.5-mj7s6dg 
module load openmpi/3.1.4-gcc-9.1.0-fdssbx5 
module load hdf5/1.10.5-gcc-9.1.0-rolgskh 
module load fftw/3.3.8-gcc-9.1.0-2kyouz7 
module load gsl/2.5-gcc-9.1.0-ucmpak4 
module load cmake/3.17.3-gcc-9.1.0-tsjr5x6 
module load python/3.9.4-gcc-9.1.0-l7amfu6
    
cd $DATA/monofonic_exp_{waveform}/build
mpiexec -np {n_tasks} ./monofonIC ../g4_{waveform}_{Nres}_{Lbox:.0f}.conf
  
python3 {python_base}/rename_and_move_ics.py {n_tasks} $DATA/monofonic_exp_{waveform}/build {output_dir_string} {waveform} {Nres} {Lbox}
    
mpiexec -np {n_tasks} {g4_basedir}/Gadget4 {output_dir}/{waveform}_{Nres}_{Lbox:.0f}_param.txt
    """
    
    with (output_dir / "job.sh").open("w") as f:
        f.write(script)

    
if __name__ == "__main__": 
    write_job_script(
        Nres = int(argv[1]),
        Lbox = float(argv[2]),
        output_dir = g4_output_basedir / f"{argv[3]}_{argv[1]}_{argv[2]}"
        )
    
    