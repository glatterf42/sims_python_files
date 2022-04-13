#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 24 10:54:50 2022

@author: ben
"""

from pathlib import Path
from directories import g4_output_basedir
from sys import argv


def create_dir_and_write_params_g4(Nres: int, Lbox: float, waveform: str, output_basedir: Path):
    # create directory if it doesn't exist already
    outputdir = output_basedir / f"{waveform}_{Nres}_{Lbox:.0f}"
    if outputdir.exists():
        print(outputdir, "already exists. Skipping...")
    else:
        print("creating", outputdir)
        outputdir.mkdir()
    
    # write param file there:
    param_script = f"""
%---- Relevant files
    
InitCondFile \t \t /gpfs/data/fs71636/fglatter/PBH_EFD/monofonic_tests/output/{waveform}_{Nres}_{Lbox:.0f}/ics_{waveform}_{Nres}_{Lbox:.0f} 
    
OutputDir \t \t /gpfs/data/fs71636/fglatter/PBH_EFD/monofonic_tests/output/{waveform}_{Nres}_{Lbox:.0f}
    
SnapshotFileBase \t snapshot
    
OutputListFilename \t /gpfs/data/fs71636/fglatter/PBH_EFD/monofonic_tests/outputs.txt
    
    
%---- File formats
    
ICFormat \t 3
    
SnapFormat \t 3
    
    
%---- CPU-time limits
    
TimeLimitCPU \t \t 86400 \t % 24h, in seconds
    
CpuTimeBetRestartFile \t 7200 \t % 2h, in seconds
    
    
%---- Memory allocation
    
MaxMemSize \t 1800 \t % in MByte
    
    
%---- Characteristics of run
    
TimeBegin \t 0.02 \t % Begin of the simulation, z=49
    
TimeMax \t 1.0 \t % End of the simulation, z=0
    
    
%---- Basic code options that set the type of simulation
    
ComovingIntegrationOn \t 1
    
    
%---- Cosmological parameters #update according to monofonic output
    
Omega0 \t \t \t \t 0.3099
   
OmegaLambda \t \t \t \t 0.690021
    
OmegaBaryon \t \t \t \t 0.0488911
    
HubbleParam \t \t \t \t 0.67742
    
Hubble \t \t \t \t 100.0
    
BoxSize \t \t \t \t {Lbox}
# 
# MeanPBHScatteringCrossSection \t 1.73189e-13
# 
# AveragePBHMass \t \t \t 3.086978e-10
# 
# SigmaOverM \t \t \t \t 5.6103e-4
    
    
%---- Output frequency and output parameters
    
OutputListOn \t \t \t 1
    
TimeBetSnapshot \t \t \t 0.0
    
TimeOfFirstSnapshot \t \t 0.0
    
TimeBetStatistics \t \t 0.01
    
NumFilesPerSnapshot \t \t 1
    
MaxFilesWithConcurrentIO \t 1
    
    
%---- Accuracy of time integration
    
ErrTolIntAccuracy \t \t 0.025
    
CourantFac \t \t \t 0.7
    
MaxSizeTimestep \t \t 0.025
    
MinSizeTimestep \t \t 0.0
    
   
%---- Tree algorithm, force accuracy, domain update frequency    
    
TypeOfOpeningCriterion \t \t 1
    
ErrTolTheta \t \t \t \t 0.5
    
ErrTolThetaMax \t \t \t 1.0
    
ErrTolForceAcc \t \t \t 0.002
    
TopNodeFactor \t \t \t \t 3.0
    
ActivePartFracForNewDomainDecomp \t 0.01
    
ActivePartFracForPMinsteadOfEwald \t 0.05
    
    
%---- Initial density estimate
    
DesNumNgb \t \t 64
    
MaxNumNgbDeviation \t 1
    
    
%---- Subfind parameters
    
DesLinkNgb \t \t 20
   
    
%---- System of units
    
UnitLength_in_cm \t \t 3.086578e24 \t ; Mpc/h
    
UnitMass_in_g \t \t \t 1.989e43 \t ; 1.0e10 Msun/h
    
UnitVelocity_in_cm_per_s \t 1e5 \t ; 1km/s
    
GravityConstantInternal \t 0
    
    
%---- Gravitational softening length
    
SofteningComovingClass0 \t {Lbox / Nres / 30}
    
SofteningMaxPhysClass0 \t {Lbox / Nres / 30}
    
SofteningClassOfPartType0 \t 0
    
SofteningClassOfPartType1 \t 0
    
SofteningClassOfPartType2 \t 0
    
SofteningClassOfPartType3 \t 0
    
SofteningClassOfPartType4 \t 0
    
SofteningClassOfPartType5 \t 0
    
    
%---- SPH
    
ArtBulkViscConst \t 1.0
    
MinEgySpec \t \t 0
    
InitGasTemp \t \t 10
    """
    
    with (outputdir / f"{waveform}_{Nres}_{Lbox:.0f}_param.txt").open("w") as f:
        f.write(param_script)
    
            
if __name__ == "__main__":
    create_dir_and_write_params_g4(
        Nres=int(argv[1]),
        Lbox=float(argv[2]),
        waveform=argv[3],
        output_basedir=g4_output_basedir
        )