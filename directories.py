#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 22 16:08:54 2022

@author: ben
"""

from pathlib import Path

g4_basedir = Path("/gpfs/data/fs71636/fglatter/PBH_EFD/monofonic_tests/")
g4_output_basedir = Path("/gpfs/data/fs71636/fglatter/PBH_EFD/monofonic_tests/output/")

swift_basedir = Path("/gpfs/data/fs71636/fglatter/swiftsim/")
swift_mon_test_basedir = Path("/gpfs/data/fs71636/fglatter/swiftsim/monofonic_tests/")
swift_output_basedir = Path("/gpfs/data/fs71636/fglatter/swiftsim/monofonic_tests/output/")
swift_tool_basedir = Path("/gpfs/data/fs71636/fglatter/swiftsim/tools/")

python_base = Path("/gpfs/data/fs71636/fglatter/python_files/")

monofonic_dir = Path("/gpfs/data/fs71636/fglatter/monofonic-experimental")
template_file = monofonic_dir / "example.conf"
# monofonic_binary = monofonic_dir / "build" / "monofonIC"
