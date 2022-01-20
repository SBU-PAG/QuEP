import math
import numpy as np

from DebugObjectModule import DebugObject

def Gamma(p):
        return math.sqrt(1.0 + p**2)

def Velocity(px,ptot):
    # Returns relativistic velocity from momentum
    return px / Gamma(ptot)

def sortVelocity(x,y,vx,vy,vr):
    # Obtain proper sign of velocity based on quadrant
    if (x >= 0 and y >= 0):                  # Quadrant 1
        if (vx >= 0 and vy >= 0):
            return vr
        elif (vx < 0 and vy < 0):
            return -1.0 * vr
        elif (abs(vx) > abs(vy)):
            if vx > 0:
                return vr
            else:
                return -1.0 * vr
        elif (abs(vy) > abs(vx)):
            if vy > 0:
                return vr
            else:
                return -1.0 * vr
    elif (x < 0 and y >= 0):                 # Quadrant 2
        if (vx <= 0 and vy >= 0):
                return vr
        elif (vx > 0 and vy < 0):
                return -1.0 * vr
        elif (abs(vx) > abs(vy)):
            if vx > 0:
                return -1.0 * vr
            else:
                return vr
        elif (abs(vy) > abs(vx)):
            if vy > 0:
                return vr
            else:
                return -1.0 * vr
    elif (x < 0 and y < 0):                   # Quadrant 3
        if (vx >= 0 and vy >= 0):
            return -1.0 * vr
        elif (vx < 0 and vy < 0):
            return vr
        elif (abs(vx) > abs(vy)):
            if vx > 0:
                return -1.0 * vr
            else:
                return vr
        elif (abs(vy) > abs(vx)):
            if vy > 0:
                return vr
            else:
                return -1.0 * vr
    elif (x >= 0 and y < 0):                 # Quadrant 4
        if (vx >= 0 and vy <= 0):
            return vr
        elif (vx < 0 and vy > 0):
            return -1.0 * vr
        elif (abs(vx) > abs(vy)):
            if vx > 0:
                return vr
            else:
                return -1.0 * vr
        elif (abs(vy) > abs(vx)):
            if vy > 0:
                return -1.0 * vr
            else:
                return vr

def Momentum(x,y,xi,dt,px,py,pz,mode,sim_name):
    if (sim_name.upper() == 'OSIRIS_CYLINSYMM'):
        import include.simulations.useOsiCylin as sim
    elif (sim_name.upper() == 'QUASI3D'):
        import include.simulations.useQuasi3D as sim
    else:
        print("Simulation name unrecognized. Quitting...")
        exit()
    
    # Returns the new momentum after dt, in units of c in the axis direction
    p = math.sqrt(px**2 + py**2 + pz**2)
    vx = Velocity(px, p)
    vy = Velocity(py, p)
    vz = Velocity(pz, p)
    r = math.sqrt(x**2 + y**2)
    vr = math.sqrt(vx**2 + vy**2)
    vr = sortVelocity(x, y, vx, vy, vr)
    if (r > 0):
        vphi = vr/r
    else:
        vphi = 0

    Fx = -1.0 * (sim.EField(2, x, y, xi, r, vx, vy, vz, vr, vphi, mode) + sim.BForce(2, x, y, xi, r, vx, vy, vz, vr, vphi, mode))
    Fy = -1.0 * (sim.EField(3, x, y, xi, r, vx, vy, vz, vr, vphi, mode) + sim.BForce(3, x, y, xi, r, vx, vy, vz, vr, vphi, mode))
    Fz = -1.0 * (sim.EField(1, x, y, xi, r, vx, vy, vz, vr, vphi, mode) + sim.BForce(1, x, y, xi, r, vx, vy, vz, vr, vphi, mode))

    px = px + Fx * dt
    py = py + Fy * dt
    pz = pz + Fz * dt
    p = math.sqrt(px**2 + py**2 + pz**2)
    gam = Gamma(p)
    return px, py, pz, p, gam, Fx, Fy, Fz

def getArrayForm(x_dat_, y_dat_, z_dat_, xi_dat_, Fx_dat_, Fy_dat_, Fz_dat_, px_dat_, py_dat_, iter):
    # Initialize whole trajectory arrays
    den = 1
    x_dat = np.empty([den, iter])
    y_dat = np.empty([den, iter])
    z_dat = np.empty([den, iter])
    xi_dat = np.empty([den, iter])
    Fx_dat = np.empty([den, iter])
    Fy_dat = np.empty([den, iter])
    Fz_dat = np.empty([den, iter])
    px_dat = np.empty([den, iter])
    py_dat = np.empty([den, iter])
    pz_dat = np.empty([den, iter])
    #Take data from debug mode and transform into 2D arrays to put into Debug object
    x_dat[0,:] = x_dat_
    y_dat[0,:] = y_dat_
    z_dat[0,:] = z_dat_
    xi_dat[0,:] = xi_dat_
    Fx_dat[0,:] = Fx_dat_
    Fy_dat[0,:] = Fy_dat_
    Fz_dat[0,:] = Fz_dat_
    px_dat[0,:] = px_dat_
    py_dat[0,:] = py_dat_
    return x_dat, y_dat, z_dat, xi_dat, Fx_dat, Fy_dat, Fz_dat, px_dat, py_dat

def getTrajectory(x_0,y_0,xi_0,px_0,py_0,pz_0,t0,iter,plasma_bnds,mode,sim_name,debugmode, x_s):
# Returns array of x, y, xi, z, and final x, y, xi, z, px, py, pz
    if (sim_name.upper() == 'OSIRIS_CYLINSYMM'):
        import include.simulations.useOsiCylin as sim
    elif (sim_name.upper() == 'QUASI3D'):
        import include.simulations.useQuasi3D as sim
    else:
        print("Simulation name unrecognized. Quitting...")
        exit()


    propspeed = sim.getPropagationSpeed()

    t = t0                       # Start time in 1/w_p
    dt = 0.005 #0.005            # Time step in 1/w_p
    xn = x_0                     # Positions in c/w_p
    yn = y_0
    xin = xi_0
    zn = xin + t0*propspeed # PLACE TO ADD MULTIPLIER TO t0 for group velocity
    rn = math.sqrt(xn**2 + yn**2)

    px = px_0                    # Momenta in m_e c
    py = py_0
    pz = pz_0

    ### DEBUGGING ###
    Debug = None # Create empty Debug object
    if debugmode == True: 
        print("Using Debug Mode...")
        x_f, y_f, xi_f, z_f, px_f, py_f, pz_f = [],[],[],[],[],[],[] # Final positions of electrons
        x_dat, y_dat, z_dat, xi_dat, Fx_dat, Fy_dat, Fz_dat, px_dat, py_dat = [],[],[],[],[],[],[],[],[]
    #################

    # Iterate through position and time using a linear approximation
    for i in range(0, iter):
        # Determine new momentum and velocity from this position
        px, py, pz, p, gam, Fx, Fy, Fz = Momentum(xn, yn, xin, dt, px, py, pz, mode, sim_name)

        vxn = Velocity(px, p)
        vyn = Velocity(py, p)
        vzn = Velocity(pz, p)

        if debugmode == True:
            x_dat.append(xn)
            y_dat.append(yn)
            z_dat.append(zn)
            xi_dat.append(xin)
            Fx_dat.append(Fx)
            Fy_dat.append(Fy)
            Fz_dat.append(Fz)
            px_dat.append(px)
            py_dat.append(py)

            if (abs(xn) > abs(x_s)):
                k = i + 1
                # Fill rest of array with the final position
                for k in range(k, iter):
                    x_dat.append(xn)
                    y_dat.append(yn)
                    z_dat.append(zn)
                    xi_dat.append(xin)
                    Fx_dat.append(Fx)
                    Fy_dat.append(Fy)
                    Fz_dat.append(Fz)
                    px_dat.append(px)
                    py_dat.append(py)
                x_dat, y_dat, z_dat, xi_dat, Fx_dat, Fy_dat, Fz_dat, px_dat, py_dat = getArrayForm(x_dat, y_dat, z_dat, xi_dat, Fx_dat, Fy_dat, Fz_dat, px_dat, py_dat, iter)
                Debug = DebugObject(x_dat, y_dat, z_dat, xi_dat, Fx_dat, Fy_dat, Fz_dat, px_dat, py_dat)
                return xn, yn, xin, zn, px, py, pz, Debug


            # If electron leaves cell, switch to ballistic trajectory
            if (xin < plasma_bnds[0] or xin > plasma_bnds[1] or rn > plasma_bnds[2]):
                j = i + 1
                j0 = j
                dt = 1
                for j in range(j, iter):
                    xn += vxn * dt
                    yn += vyn * dt
                    zn += vzn * dt
                    t += dt
                    xin = zn - t*propspeed
                    x_dat.append(xn)
                    y_dat.append(yn)
                    z_dat.append(zn)
                    xi_dat.append(xin)
                    Fx_dat.append(Fx)
                    Fy_dat.append(Fy)
                    Fz_dat.append(Fz)
                    px_dat.append(px)
                    py_dat.append(py)

                    # Stop when electron passes screen
                    if (abs(xn) > abs(x_s)):
                        k = j + 1
                        # Fill rest of array with the final position
                        for k in range(k, iter):
                            x_dat.append(xn)
                            y_dat.append(yn)
                            z_dat.append(zn)
                            xi_dat.append(xin)
                            Fx_dat.append(Fx)
                            Fy_dat.append(Fy)
                            Fz_dat.append(Fz)
                            px_dat.append(px)
                            py_dat.append(py)
                        x_dat, y_dat, z_dat, xi_dat, Fx_dat, Fy_dat, Fz_dat, px_dat, py_dat = getArrayForm(x_dat, y_dat, z_dat, xi_dat, Fx_dat, Fy_dat, Fz_dat, px_dat, py_dat, iter)
                        Debug = DebugObject(x_dat, y_dat, z_dat, xi_dat, Fx_dat, Fy_dat, Fz_dat, px_dat, py_dat)
                        return xn, yn, xin, zn, px, py, pz, Debug
                
                print("Tracking quit due to more than ", iter - j0, " iterations outside plasma")
                #print("xn = ", xn, " yn = ", yn, " zn = ", zn)
                x_dat, y_dat, z_dat, xi_dat, Fx_dat, Fy_dat, Fz_dat, px_dat, py_dat = getArrayForm(x_dat, y_dat, z_dat, xi_dat, Fx_dat, Fy_dat, Fz_dat, px_dat, py_dat, iter)
                Debug = DebugObject(x_dat, y_dat, z_dat, xi_dat, Fx_dat, Fy_dat, Fz_dat, px_dat, py_dat)
                return xn, yn, xin, zn, px, py, pz, Debug
        
        xn += vxn * dt
        yn += vyn * dt
        zn += vzn * dt
        rn = math.sqrt(xn**2 + yn**2)

        t += dt
        xin = zn - t*propspeed # PLACE TO ADD MULTIPLIER TO t for group velocity
        
        # If electron leaves cell, quit tracking
        if (xin < plasma_bnds[0] or xin > plasma_bnds[1] or rn > plasma_bnds[2]):
            if debugmode == True:
                j = i + 1
                j0 = j
                dt = 1
                for j in range(j, iter):
                    xn += vxn * dt
                    yn += vyn * dt
                    zn += vzn * dt
                    t += dt
                    xin = zn - t*propspeed
                    x_dat.append(xn)
                    y_dat.append(yn)
                    z_dat.append(zn)
                    xi_dat.append(xin)
                    Fx_dat.append(Fx)
                    Fy_dat.append(Fy)
                    Fz_dat.append(Fz)
                    px_dat.append(px)
                    py_dat.append(py)

                    # Stop when electron passes screen
                    if (abs(xn) > abs(x_s)):
                        k = j + 1
                        # Fill rest of array with the final position
                        for k in range(k, iter):
                            x_dat.append(xn)
                            y_dat.append(yn)
                            z_dat.append(zn)
                            xi_dat.append(xin)
                            Fx_dat.append(Fx)
                            Fy_dat.append(Fy)
                            Fz_dat.append(Fz)
                            px_dat.append(px)
                            py_dat.append(py)
                        x_dat, y_dat, z_dat, xi_dat, Fx_dat, Fy_dat, Fz_dat, px_dat, py_dat = getArrayForm(x_dat, y_dat, z_dat, xi_dat, Fx_dat, Fy_dat, Fz_dat, px_dat, py_dat, iter)
                        Debug = DebugObject(x_dat, y_dat, z_dat, xi_dat, Fx_dat, Fy_dat, Fz_dat, px_dat, py_dat)
                        return xn, yn, xin, zn, px, py, pz, Debug
                
                print("Tracking quit due to more than ", iter - j0, " iterations outside plasma")
                #print("xn = ", xn, " yn = ", yn, " zn = ", zn)
                x_dat, y_dat, z_dat, xi_dat, Fx_dat, Fy_dat, Fz_dat, px_dat, py_dat = getArrayForm(x_dat, y_dat, z_dat, xi_dat, Fx_dat, Fy_dat, Fz_dat, px_dat, py_dat, iter)
                Debug = DebugObject(x_dat, y_dat, z_dat, xi_dat, Fx_dat, Fy_dat, Fz_dat, px_dat, py_dat)
            return xn, yn, xin, zn, px, py, pz, Debug

    print("Tracking quit due to more than ", iter, " iterations in plasma")
    
    if debugmode == True:
        x_dat, y_dat, z_dat, xi_dat, Fx_dat, Fy_dat, Fz_dat, px_dat, py_dat = getArrayForm(x_dat, y_dat, z_dat, xi_dat, Fx_dat, Fy_dat, Fz_dat, px_dat, py_dat, iter)
        Debug = DebugObject(x_dat, y_dat, z_dat, xi_dat, Fx_dat, Fy_dat, Fz_dat, px_dat, py_dat)
        print("Debug object created...")

    return xn, yn, xin, zn, px, py, pz, Debug
