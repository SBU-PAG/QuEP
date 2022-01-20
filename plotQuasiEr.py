import numpy as np
import matplotlib.colors as col
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 15})
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

    Er_full = np.empty((riter,xiiter),dtype=float)
    Er_m0 = np.empty((riter,xiiter),dtype=float)
    Er_m1 = np.empty((riter,xiiter),dtype=float)

    for ir in progressbar.progressbar(range(riter), redirect_stout=True):
        #print(f"{ir} of {riter}")
        for ixi in range(xiiter):
            #pdb.set_trace()
            #Er_full[ir, ixi] = sim.EField(2, raxis_1[ir], 0, xiaxis_1[ixi], raxis_1[ir], mode=-1)
            Er_m0[ir, ixi] = sim.EField(2, raxis_1[ir], 0, xiaxis_1[ixi], raxis_1[ir], mode=0)
            #Er_m1[ir, ixi] = sim.EField(2, raxis_1[ir], 0, xiaxis_1[ixi], raxis_1[ir], mode=1)

    return xiaxis_1, raxis_1, Er_full, Er_m0, Er_m1

def main():

    start_time = time.time()
    t0 = sim.getTime()

    xiaxis, raxis, Er_full, Er_m0, Er_m1 = getFieldArrays()

    # Save data for future plotting
    fname = "Er-plot-data.npz"
    np.savez(fname,xiaxis, raxis, Er_full, Er_m0, Er_m1)
    print(f"Data for plot saved to {fname}")

    zaxis = [xi + t0 for xi in xiaxis]

    fig1, ax1 = plt.subplots(figsize=(10,8))
    fig2, ax2 = plt.subplots(figsize=(10,8))
    fig3, ax3 = plt.subplots(figsize=(10,8))

    fig1.subplots_adjust(left=0.1, bottom=0.1, right=0.8, top=0.9)
    fig2.subplots_adjust(left=0.05, bottom=0.1, right=0.8, top=0.9)
    fig3.subplots_adjust(left=0.05, bottom=0.1, right=0.8, top=0.9)

    #fig.suptitle("Quasi3D Ex Field for $\\phi = 0$")

    #ax.set(xlabel = '$\\xi$ ($c/\omega_p$)', ylabel = 'x ($c/\omega_p$)')

    Er_m0 = ax1.pcolormesh(zaxis, raxis, Er_m0, norm=col.SymLogNorm(linthresh=0.03,linscale=0.03,vmin=-50,vmax=50),cmap="RdBu_r")
    Er_m1 = ax2.pcolormesh(zaxis, raxis, Er_m1, norm=col.SymLogNorm(linthresh=0.03,linscale=0.03,vmin=-1000,vmax=1000),cmap="RdBu_r")
    Er_full = ax3.pcolormesh(zaxis, raxis, Er_full, norm=col.SymLogNorm(linthresh=0.03,linscale=0.03,vmin=-50,vmax=50),cmap="RdBu_r")
    ax1.set_ylim(0,7)
    ax2.set_ylim(0,1.6)
    ax3.set_ylim(0,1.6)

    ax1.set(xlabel = 'Z ($c/\omega_p$)', ylabel = 'X ($c/\omega_p$)')
    ax2.set(xlabel = 'Z ($c/\omega_p$)', ylabel = 'X ($c/\omega_p$)')
    ax3.set(xlabel = 'Z ($c/\omega_p$)', ylabel = 'X ($c/\omega_p$)')
    ax1.set_title('Transverse ($\phi = 0$) Electric Field in X, M0 Only')
    ax2.set_title('Transverse ($\phi = 0$) Electric Field in X, M1 Only')
    ax3.set_title('Transverse ($\phi = 0$) Electric Field in X, M0 + M1')

    tick_locations=[x*0.01 for x in range(2,10)]+ [x*0.01 for x in range(-10,-1)] + [x*0.1 for x in range(-10,10)] +[ x for x in range(-10,10)]
    cbar_ax1 = fig1.add_axes([0.83, 0.05, 0.03, 0.9])
    cbar_ax2 = fig2.add_axes([0.83, 0.05, 0.03, 0.9])
    cbar_ax3 = fig3.add_axes([0.83, 0.05, 0.03, 0.9])

    cbar1 = fig1.colorbar(Er_m0, cax=cbar_ax1, ticks=tick_locations, format=ticker.LogFormatterMathtext())
    cbar2 = fig2.colorbar(Er_m1, cax=cbar_ax2)#, ticks=tick_locations, format=ticker.LogFormatterMathtext())
    cbar3 = fig3.colorbar(Er_full, cax=cbar_ax3, ticks=tick_locations, format=ticker.LogFormatterMathtext())

    cbar1.set_label('Electric Field ($m_e c \omega_p / e$)')
    cbar2.set_label('Electric Field ($m_e c \omega_p / e$)')
    cbar3.set_label('Electric Field ($m_e c \omega_p / e$)')

    print((time.time() - start_time)/60, " min")

    #plt.savefig("fields.png",transparent=True)
    fig1.savefig("Er-M0-fields.png",dpi=600,transparent=True)
    
    #fig1.show()
    #fig2.show()
    #fig3.show()
    input()

main()
