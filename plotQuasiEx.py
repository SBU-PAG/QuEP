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

    Ex = np.empty((riter,xiiter),dtype=float)

    for ir in progressbar.progressbar(range(riter), redirect_stout=True):
        #print(f"{ir} of {riter}")
        for ixi in range(xiiter):
            #pdb.set_trace()
            Ex[ir, ixi] = sim.EField(2, raxis_1[ir], 0, xiaxis_1[ixi], raxis_1[ir],mode=0)

    return xiaxis_1, raxis_1, Ex

def main():

    start_time = time.time()

    xiaxis, raxis, Ex = getFieldArrays()

    fig, ax = plt.subplots()
    plt.subplots_adjust(left=0.05, bottom=0.1, right=0.8, top=0.9)
    fig.suptitle("Quasi3D Ex Field for $\\phi = 0$")

    ax.set(xlabel = '$\\xi$ ($c/\omega_p$)', ylabel = 'x ($c/\omega_p$)')

    Ex = ax.pcolormesh(xiaxis, raxis, Ex, norm=col.SymLogNorm(linthresh=0.03,linscale=0.03,vmin=-1,vmax=1),cmap="RdBu_r")
    ax.set_ylim(0,1.6)
    
    tick_locations=[x*0.01 for x in range(2,10)]+ [x*0.01 for x in range(-10,-1)] + [x*0.1 for x in range(-10,10)] +[ x for x in range(-10,10)]
    cbar_ax = fig.add_axes([0.83, 0.05, 0.03, 0.9])
    cbar = fig.colorbar(Ex, cax=cbar_ax, ticks=tick_locations, format=ticker.LogFormatterMathtext())
    cbar.set_label('Electric Field ($m_e c \omega_p / e$)')

    print((time.time() - start_time)/60, " min")
    
    fig.savefig("Ex-fields.png",transparent=False)
    #plt.show()
    input()

main()
