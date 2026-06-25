# Script for showing quick evolution of probe at user inputted locations outside plasma

import numpy as np
import matplotlib.colors as col
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.cm as cm
import matplotlib.ticker as ticker
import pdb
import math
# import include.simulations.useQuasi3D as sim
plt.rcParams.update({'font.size': 15 })
mpl.use('Agg')

# Definition of Constants
M_E = 9.109e-31                      # Electron rest mass in kg
EC = 1.60217662e-19                  # Electron charge in C
EP_0 = 8.854187817e-12               # Vacuum permittivity in C/(V m)
C = 299892458                        # Speed of light in vacuum in m/s

def Gamma(p):
    return math.sqrt(1.0 + p**2)

def Velocity(px,ptot):
# Returns relativistic velocity from momentum
    return px / Gamma(ptot)

def getBallisticTraj(x_0,y_0,xi_0,z_0,px,py,pz,x_s):
# Use ballistic matrix to find positions on screens
    dx = x_s - x_0
    y_f = y_0 + dx * (py/px)
    z_f = z_0 + dx * (pz/px)

# Find time traveled to get proper xi
    p = math.sqrt(px**2 + py**2 + pz**2)
    vx = Velocity(px, p)
    vy = Velocity(py, p)
    vz = Velocity(pz, p)
    vtot = math.sqrt(vx**2 + vy**2 + vz**2)
    dtot = math.sqrt((x_s - x_0)**2 + (y_f - y_0)**2 + (z_f - z_0)**2)
    t = dtot/vtot

    xi_f = xi_0 + dx * (pz/px) + t

    return y_f, xi_f, z_f

# t0 = sim.getTime()

def returnXi(z,t0):
    return z - C * t0

def returnZ(xi,t0):
    return xi + C * t0

def plot(x_f,y_f,xi_f,z_f,px_f,py_f,pz_f,sim_name,shape_name,x_s,noElec,iter):
# Plot evolution of probe after leaving plasma
    if (sim_name.upper() == 'OSIRIS_CYLINSYMM'):
        import include.simulations.useOsiCylin as sim
    elif (sim_name.upper() == 'QUASI3D'):
        import include.simulations.useQuasi3D as sim
    else:
        print("Simulation name unrecognized. Quitting...")
        exit()

    W_P = sim.getPlasFreq()
    shape_name = shape_name.capitalize()
    slices = len(x_s)
    xs_norm = []
    xs_norm.append(x_f[0])
    for i in range(0,slices):
        print("xs = ", x_s[i])
        xs_norm.append(x_s[i] * W_P * 10**(-3) / C) # Convert screen distances

# Generate arrays of coordinates at origin + each screen
    yslice = np.empty([slices+1, noElec])
    xislice = np.empty([slices+1, noElec])
    zslice = np.empty([slices+1, noElec])
# Fill first position with initial probe shape
    for i in range(0, noElec):
        yslice[0, i] = y_f[i]
        xislice[0, i] = xi_f[i]
        zslice[0, i] = z_f[i]
# Project positions at distances in x_s
    for i in range(1,slices+1):
        for j in range(0,noElec):
            yslice[i, j], xislice[i, j], zslice[i, j] = getBallisticTraj(x_f[j], y_f[j], xi_f[j], z_f[j], px_f[j], py_f[j], pz_f[j], xs_norm[i])

    x_s = [x_f[0] * C * 10**3 / W_P] + x_s

# Plot slices
    fig5, axs = plt.subplots(3, sharex=True, sharey=True, figsize=(8, 10), dpi=80)
    fig5.suptitle("Progression of " + shape_name + " EProbe")

    for i in range(0, 3):
        axs[i].set_title("Low Density Probe, X = " + str(x_s[i]) + " mm")
        #axs[i].hist2d(xislice[i,:], yslice[i,:], bins=(50,50), cmap=plt.cm.jet)
        axs[i].scatter(xislice[i,:], yslice[i,:], c='C0', zorder=1)
        axs[i].set_xlim(27,52)
        axs[i].set_ylim(-12,12)
    #for ax in axs.flat:
        #ax.set(xlabel = '$\\xi$ ($c/\omega_p$)', ylabel = 'Y ($c/\omega_p$)')
        #ax.label_outer()
        axs[2].set(xlabel = '$\\xi$ ($c/\omega_p$)', ylabel = 'Y ($c/\omega_p$)')

    fig6, axs2 = plt.subplots(3, sharey=True, figsize=(8, 10), dpi=80)
    fig6.suptitle("Progression of " + shape_name + " EProbe")

    for i in range(0, 3):
        axs2[i].set_title("Low Density Probe, X = " + str(x_s[i+3]) + " mm")
        #axs2[i].hist2d(xislice[i+3,:], yslice[i+3,:], bins=(50,50), cmap=plt.cm.jet)
        axs2[i].scatter(xislice[i+3,:], yslice[i+3,:], c='C0', zorder=1)
        #axs2[i].set_ylim(-2,2)
    #for ax in axs2.flat:
        #ax.set(xlabel = '$\\xi$ ($c/\omega_p$)', ylabel = 'Y ($c/\omega_p$)')
        #ax.label_outer()
        axs2[2].set(xlabel = '$\\xi$ ($c/\omega_p$)', ylabel = 'Y ($c/\omega_p$)')

    fig7, axs3 = plt.subplots(3, sharex=True, sharey=True, figsize=(8, 10), dpi=80)
    fig7.suptitle("Progression of " + shape_name + " EProbe")

    for i in range(0, 3):
        axs3[i].set_title("Low Density Probe, X = " + str(x_s[i]) + " mm")
        axs3[i].scatter(zslice[i,:], yslice[i,:], zorder=2)
        #axs3[i].set_ylim(-1,1)
        #axs3[i].set_xlim(35,40)
    axs3[2].set(xlabel = 'Z ($c/\omega_p$)', ylabel = 'Y ($c/\omega_p$)')

    #####################################################################################
    fig8, axs4 = plt.subplots(3, sharex=True, sharey=True, figsize=(8, 10), dpi=80)
    fig8.suptitle("Progression of " + shape_name + " EProbe")

    for i in range(0, 3):
        axs4[i].set_title("Low Density Probe, X = " + str(x_s[i+3]) + " mm")
        axs4[i].scatter(zslice[i+3,:], yslice[i+3,:])

    secax = axs4[2].secondary_xaxis('top', functions= (returnXi, returnZ))
    secax.set(xlabel= '$\\xi$ ($c/\omega_p$)')
    #axs4[i].set_ylim(-30,1) #commented out before was -1 to 1
    #axs4[i].set_xlim(0,2000)  #commented out before was 35 to 40 before
    axs4[2].set(xlabel = 'Z ($c/\omega_p$)', ylabel = 'Y ($c/\omega_p$)')
    ######################################################################################

    fig9, axs5 = plt.subplots(constrained_layout=True, figsize=(10,5))
    axs5.set_title("Low Density Probe, X = " + str(x_s[5]) + " mm")
    axs5.scatter(zslice[5], yslice[5])
    axs5.set(xlabel = 'Z ($c/\omega_p$)', ylabel = 'Y ($c/\omega_p$)')
    secax = axs5.secondary_xaxis('top', functions= (returnXi, returnZ))
    secax.set(xlabel= '$\\xi$ ($c/\omega_p$)')

    #fig9.show()
    #fig5.show()
    #fig.tight_layout()
    #fig6.show()
    #fig7.show()
    fig8.savefig('quickevolutions.png')

    input()
