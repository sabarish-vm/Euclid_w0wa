import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d


matplotlib.rcParams.update({'font.size': 12})
matplotlib.rcParams.update({'font.family' : 'cm'})
params = {'mathtext.fontset': 'cm',
          'mathtext.rm': 'serif',
          'mathtext.bf': 'serif:bold',
          'mathtext.it': 'serif:italic',
          'mathtext.sf': 'sans\\-serif',
          'text.usetex': False,
          'font.family': 'serif',
          'font.weight': 'normal',
          'font.serif': 'Computer Modern'}

matplotlib.rcParams.update(params)
matplotlib.rcParams['text.usetex']

def fiducial(case):
    kk_fid = np.loadtxt('output/%s/fiducial_eps_0/k_values_list.txt'%(case))
    pl_fid = np.loadtxt('output/%s/fiducial_eps_0/Plin-zk.txt'%(case))
    pn_fid = np.loadtxt('output/%s/fiducial_eps_0/Pnonlin-zk.txt'%(case))
    return kk_fid,pl_fid,pn_fid

#########

fig, axs = plt.subplots(2,2,figsize=(9,7),sharex=True)

kk_class_HP,pl_class_HP,pn_class_HP = fiducial('class_w0wa_HP')

kk_class_DP,pl_class_raw,pn_class_raw = fiducial('class_w0wa_DP')
pl_class_DP = interp1d(kk_class_DP[:],pl_class_raw[:,:],bounds_error=False,fill_value='extrapolate',kind='quadratic')(kk_class_HP[:])
pn_class_DP = interp1d(kk_class_DP[:],pn_class_raw[:,:],bounds_error=False,fill_value='extrapolate',kind='quadratic')(kk_class_HP[:])

kk_camb,pl_camb_raw,pn_camb_raw = fiducial('camb_w0wa_P1')
pl_camb_P1 = interp1d(kk_camb[:],pl_camb_raw[:,:],bounds_error=False,fill_value='extrapolate',kind='quadratic')(kk_class_HP[:])
pn_camb_P1 = interp1d(kk_camb[:],pn_camb_raw[:,:],bounds_error=False,fill_value='extrapolate',kind='quadratic')(kk_class_HP[:])

kk_camb,pl_camb_raw,pn_camb_raw = fiducial('camb_w0wa_P2')
pl_camb_P2 = interp1d(kk_camb[:],pl_camb_raw[:,:],bounds_error=False,fill_value='extrapolate',kind='quadratic')(kk_class_HP[:])
pn_camb_P2 = interp1d(kk_camb[:],pn_camb_raw[:,:],bounds_error=False,fill_value='extrapolate',kind='quadratic')(kk_class_HP[:])

kk_camb,pl_camb_raw,pn_camb_raw = fiducial('camb_w0wa_P3')
pl_camb_P3 = interp1d(kk_camb[:],pl_camb_raw[:,:],bounds_error=False,fill_value='extrapolate',kind='quadratic')(kk_class_HP[:])
pn_camb_P3 = interp1d(kk_camb[:],pn_camb_raw[:,:],bounds_error=False,fill_value='extrapolate',kind='quadratic')(kk_class_HP[:])

axs[0,0].tick_params(axis="both",which="both",direction="in",left="on",right="on",top="on",bottom="on")
axs[0,0].set_title(r'$P_\mathrm{L}(k,z=0)$',y=1.0,pad=-16)
axs[0,0].set_ylabel(r'diff. w.r.t ${\tt CLASS}$ HP (%)')
axs[0,0].set_xlim(2.e-4,50.)
axs[0,0].set_ylim(2.e-6,0.8)
axs[0,0].loglog(kk_class_HP[:],abs(pl_class_DP[0,:]/pl_class_HP[0,:]-1.)*100.,'k-')
axs[0,0].loglog(kk_class_HP[:],abs(pl_camb_P1[0,:]/pl_class_HP[0,:]-1.)*100.,'c-')
axs[0,0].loglog(kk_class_HP[:],abs(pl_camb_P2[0,:]/pl_class_HP[0,:]-1.)*100.,'b-')
axs[0,0].loglog(kk_class_HP[:],abs(pl_camb_P3[0,:]/pl_class_HP[0,:]-1.)*100.,'r-')

axs[0,1].tick_params(axis="both",which="both",direction="in",left="on",right="on",top="on",bottom="on")
axs[0,1].tick_params(labelleft=False)
axs[0,1].set_title(r'$P_\mathrm{NL}(k,z=0)$',y=1.0,pad=-16)
axs[0,1].set_xlim(2.e-4,50.)
axs[0,1].set_ylim(2.e-6,0.8)
axs[0,1].loglog(kk_class_HP[:],abs(pn_class_DP[0,:]/pn_class_HP[0,:]-1.)*100.,'k-',label=r'${\tt CLASS}$ DP')
axs[0,1].loglog(kk_class_HP[:],abs(pn_camb_P1[0,:]/pn_class_HP[0,:]-1.)*100.,'c-',label=r'${\tt CAMB}$ P1')
axs[0,1].loglog(kk_class_HP[:],abs(pn_camb_P2[0,:]/pn_class_HP[0,:]-1.)*100.,'b-',label=r'${\tt CAMB}$ P2')
axs[0,1].loglog(kk_class_HP[:],abs(pn_camb_P3[0,:]/pn_class_HP[0,:]-1.)*100.,'r-',label=r'${\tt CAMB}$ P3')
axs[0,1].legend(loc='lower left')

axs[1,0].tick_params(axis="both",which="both",direction="in",left="on",right="on",top="on",bottom="on")
axs[1,0].set_title(r'$P_\mathrm{L}(k,z=2)$',y=1.0,pad=-16)
axs[1,0].set_xlabel(r'$k$   (1/Mpc)')
axs[1,0].set_ylabel(r'diff. w.r.t ${\tt CLASS}$ HP (%)')
axs[1,0].set_xlim(2.e-4,50.)
axs[1,0].set_ylim(2.e-6,0.8)
axs[1,0].loglog(kk_class_HP[:],abs(pl_class_DP[-1,:]/pl_class_HP[-1,:]-1.)*100.,'k-')
axs[1,0].loglog(kk_class_HP[:],abs(pl_camb_P1[-1,:]/pl_class_HP[-1,:]-1.)*100.,'c-')
axs[1,0].loglog(kk_class_HP[:],abs(pl_camb_P2[-1,:]/pl_class_HP[-1,:]-1.)*100.,'b-')
axs[1,0].loglog(kk_class_HP[:],abs(pl_camb_P3[-1,:]/pl_class_HP[-1,:]-1.)*100.,'r-')

axs[1,1].tick_params(axis="both",which="both",direction="in",left="on",right="on",top="on",bottom="on")
axs[1,1].tick_params(labelleft=False)
axs[1,1].set_title(r'$P_\mathrm{NL}(k,z=2)$',y=1.0,pad=-16)
axs[1,1].set_xlabel(r'$k$   (1/Mpc)')
axs[1,1].set_xlim(2.e-4,50.)
axs[1,1].set_ylim(2.e-6,0.8)
axs[1,1].loglog(kk_class_HP[:],abs(pn_class_DP[-1,:]/pn_class_HP[-1,:]-1.)*100.,'k-')
axs[1,1].loglog(kk_class_HP[:],abs(pn_camb_P1[-1,:]/pn_class_HP[-1,:]-1.)*100.,'c-')
axs[1,1].loglog(kk_class_HP[:],abs(pn_camb_P2[-1,:]/pn_class_HP[-1,:]-1.)*100.,'b-')
axs[1,1].loglog(kk_class_HP[:],abs(pn_camb_P3[-1,:]/pn_class_HP[-1,:]-1.)*100.,'r-')

#plt.show()
plt.subplots_adjust(wspace=0, hspace=0)
plt.savefig('fiducial_ratios.pdf')
