import numpy as np
import matplotlib.colors as col
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.cm as cm
import matplotlib.ticker as ticker
import pdb
import time
import progressbar
import include.simulations.useQuasi3D as sim

def getFieldArrays():

    xiaxis_1, xi2, raxis_1, r2 = sim.axes()
    xiiter = len(xiaxis_1)
    riter = len(raxis_1)

    print(f"Number of xiiter = {xiiter}")
    print(f"Number of riter = {riter}")
    
    Ex = np.zeros((riter,xiiter),dtype=float)
    Ey = np.zeros((riter,xiiter),dtype=float)
    Ez = np.zeros((riter,xiiter),dtype=float)
    Bx = np.zeros((riter,xiiter),dtype=float)
    By = np.zeros((riter,xiiter),dtype=float)
    Bz = np.zeros((riter,xiiter),dtype=float)

    for ir in progressbar.progressbar(range(riter), redirect_stout=True):
        for ixi in range(xiiter):
            #pdb.set_trace()
            Ex[ir, ixi] = sim.EField(2, raxis_1[ir], 0, xiaxis_1[ixi], raxis_1[ir])
            Ey[ir, ixi] = sim.EField(3, 0, raxis_1[ir], xiaxis_1[ixi], raxis_1[ir])
            Ez[ir, ixi] = sim.EField(1, raxis_1[ir], 0, xiaxis_1[ixi], raxis_1[ir])
            Bx[ir, ixi] = sim.BField(2, raxis_1[ir], 0, xiaxis_1[ixi], raxis_1[ir])
            By[ir, ixi] = sim.BField(3, 0, raxis_1[ir], xiaxis_1[ixi], raxis_1[ir])
            Bz[ir, ixi] = sim.BField(1, raxis_1[ir], 0, xiaxis_1[ixi], raxis_1[ir])

    return xiaxis_1, raxis_1, Ex, Ey, Ez, Bx, By, Bz

def main():

    start_time = time.time()
    t0 = sim.getTime()

    xiaxis, raxis, Ex, Ey, Ez, Bx, By, Bz = getFieldArrays()
    zaxis = [xi + t0 for xi in xiaxis]

    fig, axs = plt.subplots(2, 3)
    plt.subplots_adjust(left=0.05, bottom=0.1, right=0.8, top=0.9)
    fig.suptitle("OSIRIS Transverse ($\\phi = 0$) Electromagnetic Fields")

    axs[0, 0].set_title('$E_x$')
    axs[0, 1].set_title('$E_y$')
    axs[0, 2].set_title('$E_z$')
    axs[1, 0].set_title('$B_x$')
    axs[1, 1].set_title('$B_y$')
    axs[1, 2].set_title('$B_z$')

    for ax in axs.flat:
        ax.set(xlabel = 'Z ($c/\omega_p$)', ylabel = 'R ($c/\omega_p$)')
    for ax in axs.flat:
        ax.label_outer()

    Ex = axs[0, 0].pcolormesh(zaxis, raxis, Ex, norm=col.SymLogNorm(linthresh=0.03,linscale=0.03,vmin=-50,vmax=50),cmap="RdBu_r")
    Ey = axs[0, 1].pcolormesh(zaxis, raxis, Ey, norm=col.SymLogNorm(linthresh=0.03,linscale=0.03,vmin=-50,vmax=50),cmap="RdBu_r")
    Ez = axs[0, 2].pcolormesh(zaxis, raxis, Ez, norm=col.SymLogNorm(linthresh=0.03,linscale=0.03,vmin=-50,vmax=50),cmap="RdBu_r")
    Bx = axs[1, 0].pcolormesh(zaxis, raxis, Bx, norm=col.SymLogNorm(linthresh=0.03,linscale=0.03,vmin=-50,vmax=50),cmap="RdBu_r")
    By = axs[1, 1].pcolormesh(zaxis, raxis, By, norm=col.SymLogNorm(linthresh=0.03,linscale=0.03,vmin=-50,vmax=50),cmap="RdBu_r")
    Bz = axs[1, 2].pcolormesh(zaxis, raxis, Bz, norm=col.SymLogNorm(linthresh=0.03,linscale=0.03,vmin=-50,vmax=50),cmap="RdBu_r")

    axs[0,0].set_ylim(0,1.6)
    axs[0,1].set_ylim(0,1.6)
    axs[0,2].set_ylim(0,1.6)
    axs[1,0].set_ylim(0,1.6)
    axs[1,1].set_ylim(0,1.6)
    axs[1,2].set_ylim(0,1.6)

    tick_locations=[x*0.01 for x in range(2,10)]+ [x*0.01 for x in range(-10,-1)] + [x*0.1 for x in range(-10,10)] +[ x for x in range(-10,10)]
    cbar_ax = fig.add_axes([0.83, 0.05, 0.03, 0.9])
    cbar = fig.colorbar(Ex, cax=cbar_ax, ticks=tick_locations, format=ticker.LogFormatterMathtext())

    cbar.set_label('Electric ($m_e c \omega_p / e$) or Magnetic ($m_e \omega_p / e$) Field')

    print((time.time() - start_time)/60, " min")

    plt.savefig("fields.png",dpi=600,transparent=True)
    #plt.show()
    input()

main()
