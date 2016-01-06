#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
ISOTHERMAL = 1
#Problem parameters
c_s = 1.0

#Datafile

datapath = "../"

data_appends = ["e50k5s100", \
                "e50k10s100", \
                "e50k11s100-2", \
                "e50k12s100-2", \
                "e50k16s100" ]

filenames = [datapath + i + "/data/id0/isoSelfG.hst" for i in data_appends]
labels = [r'$\kappa = 5$', \
         r'$\kappa = 10$', \
         r'$\kappa = 11$', \
         r'$\kappa = 12$', \
         r'$\kappa = 16$' ]

print filenames
def times(filename):
    TIME   = 0

    with open(filename,'r') as f:
        hst = np.loadtxt(f)

        t = hst[:,TIME]

        f.close()

    return t

def mach_number(filename):
    #History file columns

    if ISOTHERMAL:
        Eoff = 0
    else:
        Eoff = 1
    TIME   = 0
    MASS   = 2
    MOMX   = 3 + Eoff
    MOMZ   = 4 + Eoff
    KINX   = 6 + Eoff
    KINZ   = 7 + Eoff
    EGRAV  = 9 + Eoff
    FX     = 11 + Eoff
    FY     = 12 + Eoff
    FZ     = 13 + Eoff
    JSRC   = 14 + Eoff
    INTER  = 15 + Eoff
    FOUT   = 16 + Eoff
    FRADZ  = 17 + Eoff
    FGRAVZ = 18 + Eoff


    with open(filename,'r') as f:
        hst = np.loadtxt(f)

        t = hst[:,TIME]
        M = hst[:,MASS]
        vx = hst[:,MOMX]/M
        vz = hst[:,MOMZ]/M
        Ekinx = hst[:,KINX]
        Ekinz = hst[:,KINZ]
        sigmax = np.sqrt(2.0*Ekinx/M - vx**2)
        sigmaz = np.sqrt(2.0*Ekinz/M - vz**2)
        Mach = np.sqrt(sigmax**2 + sigmaz**2)/c_s

        f.close()

    return Mach

def f_edd(filename):
    if ISOTHERMAL:
        Eoff = 0
    else:
        Eoff = 1
    TIME   = 0
    MASS   = 2
    MOMX   = 3 + Eoff
    MOMZ   = 4 + Eoff
    KINX   = 6 + Eoff
    KINZ   = 7 + Eoff
    EGRAV  = 9 + Eoff
    FX     = 11 + Eoff
    FY     = 12 + Eoff
    FZ     = 13 + Eoff
    JSRC   = 14 + Eoff
    INTER  = 15 + Eoff
    FOUT   = 16 + Eoff
    FRADZ  = 17 + Eoff
    FGRAVZ = 18 + Eoff

    with open(filename,'r') as f:
        hst = np.loadtxt(f)

        fradz  = hst[:,FRADZ]
        fgravz = hst[:,FGRAVZ]

        fedd = fradz/fgravz
    f.close()

    return fedd


def mass(filename):
    TIME   = 0
    MASS   = 2

    with open(filename,'r') as f:
        hst = np.loadtxt(f)

        mass = hst[:,MASS] / 5.875e-34 / 2e30
    return mass

plt.figure()
with plt.style.context("bmh"):
    for i in range(len(filenames)):
        t    = times(filenames[i])
        mach = mach_number(filenames[i])

        plt.plot(t,mach, label=labels[i])
    plt.title(r"Turbulent Velocity Distribution",size=18)
    plt.xlabel(r'$t/t_\mathrm{ff}$',size=18)
    plt.ylabel(r'$\mathrm{Mach}$ $\mathrm{Number}$',size=18)
    plt.axis([0,250,0,1])
    plt.legend(loc='upper right', shadow=True, prop={'size':12})
#plt.show()
plt.savefig('Vdist.png')

plt.figure()
with plt.style.context("bmh"):
    for i in range(len(filenames)):
        t    = times(filenames[i])
        edd = f_edd(filenames[i])
        plt.plot(t,edd,label=labels[i])

    plt.title("Effective Eddington Factor",size=18)
    plt.xlabel(r'$t/t_\mathrm{ff}$',size=18)
    plt.ylabel(r'$\langle f_\mathrm{Edd,eff} \rangle$',size=18)
    plt.axis([0,250,0,1])
    plt.legend(loc='upper right', shadow=True, prop={'size':12})

plt.savefig('fedd.png')
#plt.show()

plt.figure()
with plt.style.context("bmh"):
    for i in range(len(filenames)):
        t    = times(filenames[i])
        mej = mass(filenames[i])
        plt.plot(t,mej,label=labels[i])

    plt.title("Mass history",size=18)
    plt.xlabel(r'$t/t_\mathrm{ff}$',size=18)
    plt.ylabel(r'$\frac{M}{M_{\odot}}$',size=18)
    plt.axis([0,250,0,1])
    plt.legend(loc='upper right', shadow=True, prop={'size':12})
plt.savefig('mass.png')
