#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 22 17:25:58 2022

@author: ben
"""

import shutil
from pathlib import Path
from sys import argv

def rename_and_move_ics(n_tasks: int, source_dir: Path, dest_dir: Path, waveform: str, Nres: int, Lbox: float):
    for i in range(n_tasks):
        source_file = source_dir / f"ics_{waveform}_{Nres}_{Lbox:.0f}.hdf5"
        dest_file = dest_dir / f"ics_{waveform}_{Nres}_{Lbox:.0f}.hdf5"
        shutil.move(source_file, dest_file)
        

if __name__ == "__main__":
    rename_and_move_ics(
        n_tasks = int(argv[1]),
        source_dir = Path(argv[2]),
        dest_dir = Path(argv[3]),
        waveform = str(argv[4]),
        Nres = int(argv[5]),
        Lbox = float(argv[6])
        )
