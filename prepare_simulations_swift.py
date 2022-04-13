#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 22 16:59:03 2022

@author: ben
"""

from sys import argv
from write_monofonic_conf import generate_config
from pathlib import Path
from create_dir_and_write_params_swift import create_dir_and_write_params_swift
from directories import swift_output_basedir
from write_job_script_swift import write_job_script


def main(Nres: int, Lbox: float, waveforms: list):
    for form in waveforms:
        #write monofonic conf from template file
        generate_config(
            Nres = Nres,
            Lbox = Lbox,
            outputdir = Path(f"/gpfs/data/fs71636/fglatter/monofonic_exp_{form}/"),
            waveform = form
            )
        
        #create directory in swift_output_basedir and write param file for swift there
        create_dir_and_write_params_swift(
            Nres = Nres,
            Lbox = Lbox,
            waveform = form,
            output_basedir = swift_output_basedir
            )
        
        #write job scripts
        write_job_script(
            Nres = Nres,
            Lbox = Lbox,
            waveform = form,
            output_dir = swift_output_basedir / f"{form}_{Nres}_{Lbox:.0f}"
            )


if __name__ == "__main__":
    if argv[3] == "all":
        waveforms = ["DB2", "DB4", "DB6", "DB8", "DB10", "shannon"]
    else:
        waveforms = argv[3:len(argv)]
        
    assert len(waveforms) <= 6
    
    Nres = int(argv[1])
    Lbox = float(argv[2])
    
    main(
        Nres=Nres,
        Lbox=Lbox,
        waveforms=waveforms
        )
    
