import numpy as np
import matplotlib.pyplot as plt
import re
import glob
from runinfo import *

RADIATION  = True
ISOTHERMAL = True

filename = '../data/id0/isoSelfG.hst'
outFile = glob.glob('../*.out')[0] # look in the .out file for this run
with open(outFile) as o:
    data = o.readlines()
o.close()

pattern = re.compile('units.g')
for line in data:
    if re.match(pattern, line):
        a = line.split()
        runGrams = float(a[2]) #obtain grams unit to scale mass history
print runGrams
# History file columns
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
# FX     = 10 + Eoff
# FY     = 11 + Eoff
# FZ     = 12 + Eoff
# FOUT   = 13 + Eoff
# MOUT   = 14 + Eoff
# FRADZ  = 15 + Eoff
# FGRAVZ = 16 + Eoff
# TAUZ   = 17 + Eoff
# FZC    = 18 + Eoff

# Problem parameters
#fEdd_star = 0.02
#tau_star  = 10.0
#Lx        = 64.0
# fEdd_star = 1.00
# tau_star  = 3.0


# Problem constants
g         = 1.0
cstar     = 1.0
Sigma     = 1.0

with open(filename,'r') as f:
    data = np.loadtxt(f)

t = data[:,TIME]
M = data[:,MASS]
M /= runGrams
M /= 2e33
fgravz = data[:,FGRAVZ]
print M
if RADIATION:
    fradz  = data[:,FRADZ]
    #tauz_V = data[:,TAUZ]
    #Fzc    = data[:,FZC]
    fEdd   = fradz/fgravz
    print fEdd
    #tauz_F = fradz/Fzc
#    ftrap  = fEdd*tau_star/fEdd_star - 1.0  # def. from KT12
    #ftrap  = tauz_F - 1.0  # def. from D14
vx = data[:,MOMX]/M
vz = data[:,MOMZ]/M
kinx = data[:,KINX]
kinz = data[:,KINZ]
sigmax = np.sqrt(2.0*kinx/M - vx**2)/cstar
sigmaz = np.sqrt(2.0*kinz/M - vz**2)/cstar
sigma = np.sqrt(sigmax**2 + sigmaz**2)/cstar

# Plot mass history
plt.figure()
plt.plot(t,M)
plt.xlabel(r'$t/t_{\mathrm{ff}}$')
plt.ylabel(r'$M / M_{\odot}$')
plt.ylim(0, 100)
plt.title(r'$\epsilon = {}$, $\kappa = {} $, $\Sigma = {}$'.format(eps, kap, sig))
plt.savefig('isoSelfG_'+run+'_mass.png')
plt.savefig('isoSelfG_{:s}_mass.eps'.format(run))

if RADIATION:
    # Plot <f_Edd> and f_trap
    fEddGuess = 0.08 * kap * eps
    plt.figure()
    fig1, ax1 = plt.subplots()
    #plt.semilogy(t,fEdd,t,fEddGuess*np.ones(t.shape),'r--')
    plt.plot(t,fEdd,t,fEddGuess*np.ones(t.shape),'r--')
    plt.xlabel(r'$t/t_{\mathrm{ff}}$')
    plt.ylabel(r'$\langle f_\mathrm{Edd} \rangle$')
    plt.title(r'$\epsilon = {}$, $\kappa = {} $, $\Sigma = {}$'.format(eps, kap, sig))
    # ax2 = ax1.twinx()  # Create a separate axis on right for ftrap
    # ax2.set_ylabel(r'$f_\mathrm{trap}$')
    # a,b = ax1.get_ylim()
    # #print a,b
    # a *= tau_star/fEdd_star
    # b *= tau_star/fEdd_star
    # #print a,b
    # ax2.set_ylim(a,b)
    #ax2.set_yscale('log')
    ax1.set_ylim(0,2)
    plt.savefig('isoSelfG_{:s}_fEdd.png'.format(run))

    # # Plot tau_z history
    # plt.figure()
    # plt.plot(t,tauz_V)
    # plt.xlabel(r'$t$')
    # plt.ylabel(r'$\tau_V$')
    # plt.ylim(0,15)
    # plt.savefig('radplanesrc_kt12_{:s}_tauz.eps'.format(run))

    # # Plot tauz_F/tauz_V history (flux-density correlation)
    # plt.figure()
    # plt.plot(t,tauz_F/tauz_V)
    # plt.xlabel(r'$t$')
    # plt.ylabel(r'$\tau_F/\tau_V$')
    # plt.ylim(0,1)
    # plt.savefig('radplanesrc_kt12_{:s}_tauz_FV.eps'.format(run))


# # Plot \sigma
# fig2 = plt.figure()
# plt.plot(t,sigmax,'b--',label=r'$\sigma_x/c_\mathrm{s,*}$')
# plt.plot(t,sigmaz,'r-.',label=r'$\sigma_z/c_\mathrm{s,*}$')
# plt.plot(t,sigma,'k-',label=r'$\sigma/c_\mathrm{s,*}$')
# #plt.plot(t,sigmax,'b--',t,sigmaz,'r-.',t,sigma,'k-')
# plt.ylim(0.01,25)
# plt.xlabel(r'$t/t_*$')
# #plt.ylabel(r'$\sigma/c_\mathrm{s,*}$')
# plt.legend(loc='best')
# plt.savefig('radplanesrc_kt12_{:s}_sigma.eps'.format(run))

# # Plot <v_z>
# fig3 = plt.figure()
# plt.plot(t,vz,t,np.zeros(vz.shape),'r--')
# plt.xlabel(r'$t/t_*$')
# plt.ylabel(r'$\langle v_z \rangle/c_\mathrm{s,*}$')
# plt.savefig('isoSelfG_{:s}_vz.eps'.format(run))


#with open(filename2,'r') as f:
#    data = np.loadtxt(f)
#
#t = data[:,TIME]
#M = data[:,MASS]
#fgrav = g*M/128.0
#if RADIATION:
#    fradz = data[:,FRADZ]
##    fEdd = fradz/(M*g)
##    fEdd = fradz/(Sigma*g)  # Definition from KT12
#    fEdd = fradz/fgrav  # Seems like a better definition
#    ftrap = fEdd*tau_star/fEdd_star - 1.0
#vx = data[:,MOMX]/M
#vz = data[:,MOMZ]/M
#kinx = data[:,KINX]
#kinz = data[:,KINZ]
#sigmax = np.sqrt(2.0*kinx/M - vx**2)/cstar
#sigmaz = np.sqrt(2.0*kinz/M - vz**2)/cstar
#sigma = np.sqrt(sigmax**2 + sigmaz**2)/cstar
#
## Plot \sigma
#plt.figure(fig2.number)
#plt.semilogy(t,sigmax,'b--',t,sigmaz,'r-.',t,sigma,'k-')
##plt.plot(t,sigmax,'b--',t,sigmaz,'r-.',t,sigma,'k-')
#plt.ylim(0.01,10)
#plt.xlabel(r'$t/t_*$')
##plt.ylabel(r'$\sigma/c_\mathrm{s,*}$')
#plt.legend([r'$\sigma_x/c_\mathrm{s,*}$',r'$\sigma_z/c_\mathrm{s,*}$',r'$\sigma/c_\mathrm{s,*}$'],
#            loc='upper left')
#
## Plot <v_z>
#plt.figure(fig3.number)
#plt.plot(t,vz)
#plt.xlabel(r'$t/t_*$')
#plt.ylabel(r'$\langle v_z \rangle/c_\mathrm{s,*}$')

print 'done'
#plt.show()
