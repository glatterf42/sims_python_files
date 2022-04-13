#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 24 10:29:11 2022

@author: ben
"""

from configparser import ConfigParser
from pathlib import Path
from sys import argv

template_file = Path("/gpfs/data/fs71636/fglatter/monofonic/monofonic/example.conf")


def generate_config(Nres: int, Lbox: float, outputdir: Path, waveform: str, print_config=False):
    config = ConfigParser(inline_comment_prefixes="#")
    config.optionxform = str
    with template_file.open() as f:
        config.read_file(f)
    config.set("setup", "GridRes", str(Nres))
    config.set("setup", "BoxLength", f"{Lbox * 0.67742}")
    config.set("setup", "zstart", str(49.0))
    config.set("output", "format", "SWIFT")
    config.set("output", "filename", f"ics_{waveform}_{Nres}_{Lbox:.0f}.hdf5")
    config.set("output", "UseLongids", "true")
    config.set("random", "generator", "MUSIC2")
    config.set('execution', 'NumThreads', str(24))
    with (outputdir / f"swift_{waveform}_{Nres}_{Lbox:.0f}.conf").open("w") as outputfile:
        config.write(outputfile)
    # just for also printing the output
    if print_config:
        with (outputdir / f"swift_{waveform}_{Nres}_{Lbox:.0f}.conf").open("r") as outputfile:
            print(outputfile.read())


if __name__ == '__main__':
    generate_config(
        Nres=int(argv[1]),
        Lbox=float(argv[2]),
        outputdir=Path(f"/gpfs/data/fs71636/fglatter/monofonic_exp_{argv[3]}/"),
        waveform=argv[3],
        print_config=True
    )