# This file retrieves the fields from OSIRIS Quasi3D data files stored within the data/ folder.
# Expresses EM fields in azimuthal harmonics up to the first order
# Functions that MUST be updated for any new simulation (i.e. Called in either main.py or eProbe.py) are designated with three asterisks ***
# All other functions are used for either reading out data or plotting results

import sys
import h5py as h5
import numpy as np
import math
import pdb

# Coordinate System
# z   - Direction of laser propagation (longitudinal)
# xi  - Position along z relative to wavefront
# r   - Cylindrical coordinate around z
# phi - Cylindrical coordinate around z, define phi = 0 along x
# x   - Direction of transverse probe
# y   - Direction perpendicular to transverse probe

# Modes
# mode = 0 refers to LWF effects only
# mode = 1 refers to laser effects only
# mode = any other integer uses LWF + laser effects

# Definition of Constants
M_E = 9.109e-31                       # Electron rest mass in kg
EC = 1.60217662e-19                   # Electron charge in C
EP_0 = 8.854187817e-12                # Vacuum permittivity in C/(V m)
C = 299892458                         # Speed of light in vacuum in m/s

Quasi_ID = '000130' #'000067' is for a0 = 4 matched density data
                    #'000130' is for 1e15 density data
                    #'000144' or '000232' are for 1e17 density data (at different times in run)

def getField(fpath): 
    f = h5.File(fpath,"r")
    datasetNames = [n for n in f.keys()]
    field = datasetNames[-1]
    Field_dat = f[field][:].astype(float)
    return Field_dat

def getTime(): # ***
    f = h5.File('data/OSIRIS/Quasi3D/b1_cyl_m-0-re-'+ Quasi_ID + '.h5',"r")
    t0 = f.attrs['TIME']
    t0 = t0[0]
    return t0

print(getTime())