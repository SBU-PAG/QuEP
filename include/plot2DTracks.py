# Script for generating 2D plots of electron trajectories with option for plotting force

import numpy as np
import matplotlib.colors as col
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.cm as cm
import matplotlib.ticker as ticker
from mpl_toolkits.mplot3d import Axes3D
import pdb

from numpy.core.fromnumeric import size
plt.rcParams.update({'font.size': 16})

plotYForce = True # Plot transverse force with trajectories, not useful for many trajectories
plotZForce = True # Plot force along WF propagation

#large_size = 12

#plt.rc('ytick', labelsize=large_size)
#plt.rc('axes', labelsize=large_size)

def make_patch_spines_invisible(ax):
    ax.set_frame_on(True)
    ax.patch.set_visible(False)
    for sp in ax.spines.values():
        sp.set_visible(False)

def plot(x_dat,y_dat,z_dat,xi_dat,Fx_dat,Fy_dat,Fz_dat,px_dat,py_dat,sim_name,shape_name,s1,s2,noElec,fname):

# 2D: Z-X, constrained to blowout regime
    fig1 = plt.figure(1)
    ax1 = plt.axes()
    ax1.set_xlabel("X ($c/\omega_p$)")
    ax1.set_ylabel("Z ($c/\omega_p$)")
    ax1.set_xlim(-3,3)
    ax1.tick_params(axis='y', labelcolor='k')
    ax1.set_title("Electron Trajectories through Blowout Regime")

    for i in range(0, noElec):
        ax1.plot(x_dat[i,:], z_dat[i,:], 'k', label='$Z-X Trajectory') # Want vertical axis as y

    if (plotZForce):
        ax1_f = ax1.twinx()
        ax1_f.set_ylabel("$F_z$ ($m_e c \omega_p$)")
        ax1_f.yaxis.label.set_color('C0')
        ax1_f.tick_params(axis='y', labelcolor='C0', colors='C0')

        for i in range(0, noElec):
            ax1_f.plot(x_dat[i,:], Fz_dat[i,:], 'C0', label='Z Force')

        fig1.legend(bbox_to_anchor=(0.88, 0.94), bbox_transform=plt.gcf().transFigure)

# 2D: Y-X
    fig2, ax2 = plt.subplots(1,figsize=(15,10),dpi=300)
    fig2.subplots_adjust(right=0.75)

    for i in range(0, noElec):
        #y_dat[i,:] = [y/0.65 for y in y_dat[i,:]]
        ax2.plot(x_dat[i,:], y_dat[i,:], 'k', label='Y-X Electron Trajectory') # Want vertical axis as y
        ax2.set_xlim(-3,3)
    ax2.set_xlabel("X ($c/\omega_p$)")
    ax2.set_ylabel("Y/$R_b$ ($c/\omega_p$)")
    ax2.set_title("Electron Trajectory through Blowout Regime")

    if (plotYForce):
        Fy_ax = ax2.twinx()
        px_ax = ax2.twinx()
        py_ax = ax2.twinx()

        px_ax.spines["right"].set_position(("axes",1.15))
        make_patch_spines_invisible(px_ax)
        px_ax.spines["right"].set_visible(True)
        py_ax.spines["right"].set_position(("axes",1.3))
        make_patch_spines_invisible(py_ax)
        py_ax.spines["right"].set_visible(True)

        for i in range(0, noElec):
            Fy_ax.plot(x_dat[i,:], Fy_dat[i,:], 'C0', label='Transverse Electric Force, $F_y$')
            px_ax.plot(x_dat[i,:], px_dat[i,:], 'C1', label='Momentum in X')
            py_ax.plot(x_dat[i,:], py_dat[i,:], 'C2', label='Momentum in Y')
        Fy_ax.set_ylabel("$F_y$ ($m_e c \omega_p$)")
        px_ax.set_ylabel("$p_x (m_e c)$")
        py_ax.set_ylabel("$p_y (m_e c)$")

        Fy_ax.yaxis.label.set_color('C0')
        px_ax.yaxis.label.set_color('C1')
        py_ax.yaxis.label.set_color('C2')

        tkw = dict(size=4, width=1.5)
        ax2.tick_params(axis='y', colors='k', **tkw)
        Fy_ax.tick_params(axis='y', colors='C0', **tkw)
        px_ax.tick_params(axis='y', colors='C1', **tkw)
        py_ax.tick_params(axis='y', colors='C2', **tkw)
        ax2.tick_params(axis='x', **tkw)

        fig2.legend(bbox_to_anchor=(0.3, 0.8), bbox_transform=plt.gcf().transFigure)

    fig1.tight_layout()
    #fig1.show()
    fig2.tight_layout()
    fig2.savefig(f"eProbe-Trajectories_{fname}.png",transparent=False)
