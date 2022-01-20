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

Quasi_ID = '000067' #'000067' is for a0 = 4 matched density data
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

def getPlasDensity(): 
    if (Quasi_ID == '000130'):
        return 1e21
    elif (Quasi_ID == '000067'):
        return 1.1e16
    else:
        return 3e23

def getPropagationSpeed(): 
    if (Quasi_ID == '000130'):
        return 0.95 #THIS IS INCORRECT, JUST FOR TESTING
    elif (Quasi_ID == '000067'):
        return 0.9958959
    else:
        return 1

def getPlasFreq(): 
    N_0 = getPlasDensity()
    return math.sqrt(EC**2 * N_0 / (M_E * EP_0))

def axes(): 
# Retrieve axes boundaries under staggered mesh
    f = h5.File('data/OSIRIS/Quasi3D/b1_cyl_m-0-re-'+ Quasi_ID + '.h5',"r")
    datasetNames = [n for n in f.keys()] # Three Datasets: AXIS, SIMULATION, Field data
    field = datasetNames[-1]
    Field_dat = f[field][:].astype(float)
    a1_bounds = f['AXIS']['AXIS1'] # zmin and zmax
    a2_bounds = f['AXIS']['AXIS2'] # rmin and rmax - dr/2
    dz = 9.908e-4 # Width of each cell
    dr = 6.59e-3
# Account for specific definitions of bottom-left values for each field component
    z_bounds_1 = [a1_bounds[0], a1_bounds[1]] # Used for E1, B1
    z_bounds_2 = [a1_bounds[0] - dz/2, a1_bounds[1] + dz/2] # Used for E2, E3, B2, B3
    r_bounds_1 = [a2_bounds[0], a2_bounds[1] + dr/2] # Used for E2, B2
    r_bounds_2 = [a2_bounds[0] - dr/2, a2_bounds[1] + dr] # Used for E1, E3, B1, B3
    t0 = getTime()#f.attrs['TIME']

# Field Shape is (433, 25231), where data is written as E(r,z)
    xiaxis_1 = np.linspace(z_bounds_1[0] - t0, z_bounds_1[1] - t0, len(Field_dat[0]))
    xiaxis_2 = np.linspace(z_bounds_2[0] - t0, z_bounds_2[1] - t0, len(Field_dat[0]))
    raxis_1 = np.linspace(r_bounds_1[0], r_bounds_2[1], len(Field_dat))
    raxis_2 = np.linspace(r_bounds_2[0], r_bounds_2[1], len(Field_dat))

    return xiaxis_1, xiaxis_2, raxis_1, raxis_2

xiaxis_1, xiaxis_2, raxis_1, raxis_2 = axes() # Evenly spaced axes data

def getBoundCond(): # ***
# Define when the electron leaves the plasma cell
    f = h5.File('data/OSIRIS/Quasi3D/b1_cyl_m-0-re-'+ Quasi_ID + '.h5',"r")
    datasetNames = [n for n in f.keys()] # Three Datasets: AXIS, SIMULATION, Field data
    field = datasetNames[-1]
    Field_dat = f[field][:].astype(float)
    a1_bounds = f['AXIS']['AXIS1'] # ximin and ximax
    a2_bounds = f['AXIS']['AXIS2'] # rmin and rmax - dr/2
    dr = 6.59e-3
    t0 = getTime()
    return [a1_bounds[0] - t0, a1_bounds[1] - t0, a2_bounds[1] + dr/2] # zmin, zmax, rmax

# Return cylindrical Electric field components
# E1 - z
# E2 - r
# E3 - phi

def getE1_M0():
    return getField('data/OSIRIS/Quasi3D/e1_cyl_m-0-re-'+ Quasi_ID + '.h5')

def getE2_M0():
    return getField('data/OSIRIS/Quasi3D/e2_cyl_m-0-re-'+ Quasi_ID + '.h5')

def getE3_M0():
    return getField('data/OSIRIS/Quasi3D/e3_cyl_m-0-re-'+ Quasi_ID + '.h5')

def getE1_M1_Re():
    return getField('data/OSIRIS/Quasi3D/e1_cyl_m-1-re-'+ Quasi_ID + '.h5')

def getE2_M1_Re():
    return getField('data/OSIRIS/Quasi3D/e2_cyl_m-1-re-'+ Quasi_ID + '.h5')

def getE3_M1_Re():
    return getField('data/OSIRIS/Quasi3D/e3_cyl_m-1-re-'+ Quasi_ID + '.h5')

def getE1_M1_Im():
    return getField('data/OSIRIS/Quasi3D/e1_cyl_m-1-im-'+ Quasi_ID + '.h5')

def getE2_M1_Im():
    return getField('data/OSIRIS/Quasi3D/e2_cyl_m-1-im-'+ Quasi_ID + '.h5')

def getE3_M1_Im():
    return getField('data/OSIRIS/Quasi3D/e3_cyl_m-1-im-'+ Quasi_ID + '.h5')

# Return Magnetic Field components
# B1 - z
# B2 - r
# B3 - phi

def getB1_M0():
    return getField('data/OSIRIS/Quasi3D/b1_cyl_m-0-re-'+ Quasi_ID + '.h5')

def getB2_M0():
    return getField('data/OSIRIS/Quasi3D/b2_cyl_m-0-re-'+ Quasi_ID + '.h5')

def getB3_M0():
    return getField('data/OSIRIS/Quasi3D/b3_cyl_m-0-re-'+ Quasi_ID + '.h5')

def getB1_M1_Re():
    return getField('data/OSIRIS/Quasi3D/b1_cyl_m-1-re-'+ Quasi_ID + '.h5')

def getB2_M1_Re():
    return getField('data/OSIRIS/Quasi3D/b2_cyl_m-1-re-'+ Quasi_ID + '.h5')

def getB3_M1_Re():
    return getField('data/OSIRIS/Quasi3D/b3_cyl_m-1-re-'+ Quasi_ID + '.h5')

def getB1_M1_Im():
    return getField('data/OSIRIS/Quasi3D/b1_cyl_m-1-im-'+ Quasi_ID + '.h5')

def getB2_M1_Im():
    return getField('data/OSIRIS/Quasi3D/b2_cyl_m-1-im-'+ Quasi_ID + '.h5')

def getB3_M1_Im():
    return getField('data/OSIRIS/Quasi3D/b3_cyl_m-1-im-'+ Quasi_ID + '.h5')

E1_M0 = getE1_M0()
E2_M0 = getE2_M0()
E3_M0 = getE3_M0()
E1_M1_Re = getE1_M1_Re()
E2_M1_Re = getE2_M1_Re()
E3_M1_Re = getE3_M1_Re()
E1_M1_Im = getE1_M1_Im()
E2_M1_Im = getE2_M1_Im()
E3_M1_Im = getE3_M1_Im()
B1_M0 = getB1_M0()
B2_M0 = getB2_M0()
B3_M0 = getB3_M0()
B1_M1_Re = getB1_M1_Re()
B2_M1_Re = getB2_M1_Re()
B3_M1_Re = getB3_M1_Re()
B1_M1_Im = getB1_M1_Im()
B2_M1_Im = getB2_M1_Im()
B3_M1_Im = getB3_M1_Im()

def getPhi(x,y):
    return math.atan2(y,x) # From -pi to pi

def find_nearest_index(array,value):
    idx = np.searchsorted(array, value, side="right")
    if idx > 0 and (idx == len(array) or math.fabs(value - array[idx-1]) < math.fabs(value - array[idx])):
        return idx-1
    else:
        return idx

def EField(axis,x,y,xi,r,vx=-1,vy=-1,vz=-1,vr=-1,vphi=-1,mode=-1): # ***
# axis = 1 refers to z-axis field
# axis = 2 refers to x-axis field
# axis = 3 refers to y-axis field
# mode = 0 refers to LWF effects only
# mode = 1 refers to laser effects only
# mode = any other integer uses LWF + laser effects
    phi = getPhi(x,y)
    cos = math.cos(phi)
    sin = math.sin(phi)
    xiDex1 = find_nearest_index(xiaxis_1, xi)
    xiDex2 = find_nearest_index(xiaxis_2, xi)
    rDex1 = find_nearest_index(raxis_1, r)
    rDex2 = find_nearest_index(raxis_2, r)
    # Return expanded EFields
    if (mode == 0):
        if (axis == 1):
            return E1_M0[rDex2, xiDex1]
        elif (axis == 2):
            return E2_M0[rDex1, xiDex2]*cos - E3_M0[rDex2, xiDex2]*sin
        elif (axis == 3):
            return E3_M0[rDex2, xiDex2]*cos + E2_M0[rDex1, xiDex2]*sin
    elif (mode == 1):
        if (axis == 1):
            return E1_M1_Re[rDex2, xiDex1]*cos + E1_M1_Im[rDex2, xiDex1]*sin
        elif (axis == 2):
            return E2_M1_Re[rDex1, xiDex2]*cos**2 - E3_M1_Re[rDex2, xiDex2]*cos*sin + E2_M1_Im[rDex1, xiDex2]*cos*sin - E3_M1_Im[rDex2, xiDex2]*sin**2
        elif (axis == 3):
            return E3_M1_Re[rDex2, xiDex2]*cos**2 + E2_M1_Re[rDex1, xiDex2]*cos*sin + E3_M1_Im[rDex2, xiDex2]*cos*sin + E2_M1_Im[rDex1, xiDex2]*sin**2
    else:
        if (axis == 1):
            return E1_M0[rDex2, xiDex1] + E1_M1_Re[rDex2, xiDex1]*cos + E1_M1_Im[rDex2, xiDex1]*sin
        elif (axis == 2):
            return E2_M0[rDex1, xiDex2]*cos - E3_M0[rDex2, xiDex2]*sin + E2_M1_Re[rDex1, xiDex2]*cos**2 - E3_M1_Re[rDex2, xiDex2]*cos*sin + E2_M1_Im[rDex1, xiDex2]*cos*sin - E3_M1_Im[rDex2, xiDex2]*sin**2
        elif (axis == 3):
            return E3_M0[rDex2, xiDex2]*cos + E2_M0[rDex1, xiDex2]*sin + E3_M1_Re[rDex2, xiDex2]*cos**2 + E2_M1_Re[rDex1, xiDex2]*cos*sin + E3_M1_Im[rDex2, xiDex2]*cos*sin + E2_M1_Im[rDex1, xiDex2]*sin**2

def BForce(axis,x,y,xi,r,vx=-1,vy=-1,vz=-1,vr=-1,vphi=-1,mode=-1): # ***
# axis = 1 refers to z-axis field
# axis = 2 refers to x-axis field
# axis = 3 refers to y-axis field
    phi = getPhi(x,y)
    cos = math.cos(phi)
    sin = math.sin(phi)
    xiDex1 = find_nearest_index(xiaxis_1, xi)
    xiDex2 = find_nearest_index(xiaxis_2, xi)
    rDex1 = find_nearest_index(raxis_1, r)
    rDex2 = find_nearest_index(raxis_2, r)
    # Calculate expanded BFields
    if (mode == 0):
        Bz = B1_M0[rDex2, xiDex1]
        Bx = B2_M0[rDex1, xiDex2]*cos - B3_M0[rDex2, xiDex2]*sin
        By = B3_M0[rDex2, xiDex2]*cos + B2_M0[rDex1, xiDex2]*sin
    elif (mode == 1):
        Bz = B1_M1_Re[rDex2, xiDex1]*cos + B1_M1_Im[rDex2, xiDex1]*sin
        Bx = B2_M1_Re[rDex1, xiDex2]*cos**2 - B3_M1_Re[rDex2, xiDex2]*cos*sin + B2_M1_Im[rDex1, xiDex2]*cos*sin - B3_M1_Im[rDex2, xiDex2]*sin**2
        By = B3_M1_Re[rDex2, xiDex2]*cos**2 + B2_M1_Re[rDex1, xiDex2]*cos*sin + B3_M1_Im[rDex2, xiDex2]*cos*sin + B2_M1_Im[rDex1, xiDex2]*sin**2
    else:
        Bz = B1_M0[rDex2, xiDex1] + B1_M1_Re[rDex2, xiDex1]*cos + B1_M1_Im[rDex2, xiDex1]*sin
        Bx = B2_M0[rDex1, xiDex2]*cos - B3_M0[rDex2, xiDex2]*sin + B2_M1_Re[rDex1, xiDex2]*cos**2 - B3_M1_Re[rDex2, xiDex2]*cos*sin + B2_M1_Im[rDex1, xiDex2]*cos*sin - B3_M1_Im[rDex2, xiDex2]*sin**2
        By = B3_M0[rDex2, xiDex2]*cos + B2_M0[rDex1, xiDex2]*sin + B3_M1_Re[rDex2, xiDex2]*cos**2 + B2_M1_Re[rDex1, xiDex2]*cos*sin + B3_M1_Im[rDex2, xiDex2]*cos*sin + B2_M1_Im[rDex1, xiDex2]*sin**2
    # Cross-product velocities with BFields and return the BForce
    if axis == 1:
        return vx * By - vy * Bx
    elif axis == 2:
        return vy * Bz - vz * By
    elif axis == 3:
        return -1.0 * (vx * Bz - vz * Bx)

def BField(axis,x,y,xi,r,vx=-1,vy=-1,vz=-1,vr=-1,vphi=-1,mode=-1):
# Return BField
    phi = getPhi(x,y)
    cos = math.cos(phi)
    sin = math.sin(phi)
    xiDex1 = find_nearest_index(xiaxis_1, xi)
    xiDex2 = find_nearest_index(xiaxis_2, xi)
    rDex1 = find_nearest_index(raxis_1, r)
    rDex2 = find_nearest_index(raxis_2, r)
# Calculate expanded BFields
    if (mode == 0):
        if (axis == 1):
            return B1_M0[rDex2, xiDex1]
        elif (axis == 2):
            return B2_M0[rDex1, xiDex2]*cos - B3_M0[rDex2, xiDex2]*sin
        elif (axis == 3):
            return B3_M0[rDex2, xiDex2]*cos + B2_M0[rDex1, xiDex2]*sin
    elif (mode == 1):
        if (axis == 1):
            return B1_M1_Re[rDex2, xiDex1]*cos + B1_M1_Im[rDex2, xiDex1]*sin
        elif (axis == 2):
            return B2_M1_Re[rDex1, xiDex2]*cos**2 - B3_M1_Re[rDex2, xiDex2]*cos*sin + B2_M1_Im[rDex1, xiDex2]*cos*sin - B3_M1_Im[rDex2, xiDex2]*sin**2
        elif (axis == 3):
            return B3_M1_Re[rDex2, xiDex2]*cos**2 + B2_M1_Re[rDex1, xiDex2]*cos*sin + B3_M1_Im[rDex2, xiDex2]*cos*sin + B2_M1_Im[rDex1, xiDex2]*sin**2
    else:
        if (axis == 1):
            return B1_M0[rDex2, xiDex1] + B1_M1_Re[rDex2, xiDex1]*cos + B1_M1_Im[rDex2, xiDex1]*sin
        elif (axis == 2):
            return B2_M0[rDex1, xiDex2]*cos - B3_M0[rDex2, xiDex2]*sin + B2_M1_Re[rDex1, xiDex2]*cos**2 - B3_M1_Re[rDex2, xiDex2]*cos*sin + B2_M1_Im[rDex1, xiDex2]*cos*sin - B3_M1_Im[rDex2, xiDex2]*sin**2
        elif (axis == 3):
            return B3_M0[rDex2, xiDex2]*cos + B2_M0[rDex1, xiDex2]*sin + B3_M1_Re[rDex2, xiDex2]*cos**2 + B2_M1_Re[rDex1, xiDex2]*cos*sin + B3_M1_Im[rDex2, xiDex2]*cos*sin + B2_M1_Im[rDex1, xiDex2]*sin**2
