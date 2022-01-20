# Transverse Electron Probe of Laser Wakefield Tracking Script
# Author: Marisa Petrusky - marisa.petrusky@stonybrook.edu
#   This script is designed to take the Lorentz fields of a simulated laser wakefield
#   and obtain the trajectory of an electron probe through a first order Runge Kutta

#   Implemented Simulations:
#   - Quasi3D

#   Instructions on how to add more simulations can be found in the README

#   Derived from Audrey Farrell's electron tracking script: eTracks.py

# Coordinate System
#   z   - Direction of laser propagation (longitudinal)
#   xi  - Position along z relative to wavefront (unnecessary?)
#   r   - Cylindrical coordinate around z
#   phi - Cylindrical coordinate around z, define phi = 0 along x
#   x   - Direction of transverse probe
#   y   - Direction perpendicular to transverse probe

# Python Imports
import sys
import math
import numpy as np
import h5py as h5
import importlib
import pdb
import time
import pickle
import multiprocessing as mp
from DebugObjectModule import DebugObject

# Include file imports
import eProbe

# Definition of Constants
M_E = 9.109e-31                      # Electron rest mass in kg
EC = 1.60217662e-19                  # Electron charge in C
EP_0 = 8.854187817e-12               # Vacuum permittivity in C/(V m)
C = 299892458                        # Speed of light in vacuum in m/s


if __name__ == '__main__':
    # Start of main()
    # Initialize multiprocessing.Pool()
    pool = mp.Pool(mp.cpu_count())

    start_time = time.time()
    t = time.localtime()
    curr_time = time.strftime("%H:%M:%S", t)
    print("Start Time: ", curr_time)

    if (len(sys.argv) == 2):
    # Initialize probe
        input_fname = str(sys.argv[1])
        print("Using initial conditions from ", input_fname)
        init = importlib.import_module(input_fname)
        sim_name = init.simulation_name
        shape_name = init.shape
        xden = init.xdensity
        yden = init.ydensity
        xiden = init.xidensity
        res = init.resolution
        iter = init.iterations
        mode = init.mode
        fname = init.fname
        debugmode = init.debugmode
        x_c = init.x_c
        y_c = init.y_c
        xi_c = init.xi_c
        px_0 = init.px_0
        py_0 = init.py_0
        pz_0 = init.pz_0
        x_s = init.x_s
        s1 = init.s1
        s2 = init.s2

        if (sim_name.upper() == 'OSIRIS_CYLINSYMM'):
            import include.simulations.useOsiCylin as sim
        elif (sim_name.upper() == 'QUASI3D'):
            import include.simulations.useQuasi3D as sim
        else:
            print("Simulation name unrecognized. Quitting...")
            exit()

        t0 = sim.getTime()
        plasma_bnds = sim.getBoundCond()

        if (shape_name.upper() == 'CIRCLE'):
            import include.shapes.circle as shape
        elif (shape_name.upper() == 'DISC'):
            import include.shapes.disc as shape
        elif (shape_name.upper() == 'RECTANGLE'):
            import include.shapes.rectangle as shape
        elif (shape_name.upper() == 'VLINE'):
            import include.shapes.vline as shape
        elif (shape_name.upper() == 'HLINE'):
            import include.shapes.hline as shape
        elif (shape_name.upper() == 'SINGLE'):
            import include.shapes.single as shape
        elif (shape_name.upper() == 'RPRISM'):
            import include.shapes.rprism as shape
        elif (shape_name.upper() == 'RPRISM_WEIGHTED_AFTER'):
            import include.shapes.rprism_weighted_after as shape
        else:
            print("Electron probe shape unrecognized. Quitting...")
            exit()

    # Get arrays of initial coordinates in shape of probe
        x_0, y_0, xi_0, z_0 = shape.initProbe(x_c, y_c, xi_c, t0, s1, s2, xden, yden, xiden, res)

        print("Probe initialized...")
        noObj = len(x_0) # Number of electrons/particles to track
        print("Number of objects:",noObj)

        if debugmode == True:
            assert shape_name == 'single', "Debug mode can only be used with shape 'single'"
        x_f, y_f, xi_f, z_f, px_f, py_f, pz_f, Debug = zip(*pool.starmap(eProbe.getTrajectory, [(x_0[i], y_0[i], xi_0[i], px_0, py_0, pz_0, t0, iter, plasma_bnds, mode, sim_name, debugmode, x_s) for i in range(0,noObj)]))

        pool.close()

        tf = time.localtime()
        curr_time_f = time.strftime("%H:%M:%S", tf)
        print("End Time: ", curr_time_f)
        print("Duration: ", (time.time() - start_time)/60, " min")

        np.savez(fname, x_init=x_0, y_init=y_0, xi_init=xi_0, z_init=z_0, x_dat=x_f, y_dat=y_f, xi_dat=xi_f, z_dat=z_f, px_dat=px_f, py_dat=py_f, pz_dat=pz_f, t_dat=t0)
        
        if debugmode == True:
            debugname = fname[:-4]+"-DEBUG.obj"
            filehandler = open(debugname, 'wb')
            pickle.dump(Debug,filehandler)
            print(f"Debug object saved to {debugname}")



    else:
        print("Improper number of arguments. Expected 'python3 main.py <fname>'")
        exit()
