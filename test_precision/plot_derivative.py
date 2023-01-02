import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

# this function takes:
# - the name of a code with given precision settings (in the input_4_cast respitory)
# - the name of the parameter to be plotted (input_4_cast name)
# - the stepsize (input_4_cast syntax)
# it returns:
# - the vector of k values
# - the vector of d ln P_L (k) / d param
# - the vector of d ln P_NL(k) / d param

def derivative(case,param,step):
    kk_plus = np.loadtxt('../../input_4_cast/output/%s/%s_pl_eps_1p0E-02/k_values_list.txt'%(case,param))
    pl_plus = np.loadtxt('../../input_4_cast/output/%s/%s_pl_eps_1p0E-02/Plin-zk.txt'%(case,param))
    pn_plus = np.loadtxt('../../input_4_cast/output/%s/%s_pl_eps_1p0E-02/Pnonlin-zk.txt'%(case,param))
    kk_minus = np.loadtxt('../../input_4_cast/output/%s/%s_mn_eps_1p0E-02/k_values_list.txt'%(case,param))
    pl_minus = np.loadtxt('../../input_4_cast/output/%s/%s_mn_eps_1p0E-02/Plin-zk.txt'%(case,param))
    pn_minus = np.loadtxt('../../input_4_cast/output/%s/%s_mn_eps_1p0E-02/Pnonlin-zk.txt'%(case,param))
    kk_fid = np.loadtxt('../../input_4_cast/output/%s/fiducial_eps_0/k_values_list.txt'%(case))
    pl_fid = np.loadtxt('../../input_4_cast/output/%s/fiducial_eps_0/Plin-zk.txt'%(case))
    pn_fid = np.loadtxt('../../input_4_cast/output/%s/fiducial_eps_0/Pnonlin-zk.txt'%(case))
    der_pl = (pl_plus-pl_minus)/2./step/pl_fid
    der_pn = (pn_plus-pn_minus)/2./step/pn_fid
    if kk_plus[0] != kk_minus[0] or kk_plus[0] != kk_fid[0]:
        print ("problem with k sampling! Don't trust results! Interpolation needed!")
    if kk_plus[-1] != kk_minus[-1] or kk_plus[-1] != kk_fid[-1]:
        print ("problem with k sampling! Don't trust results! Interpolation needed!")
    if len(kk_plus) != len(kk_minus) or len(kk_plus) != len(kk_fid):
        print ("problem with k sampling! Don't trust results! Interpolation needed!")
    return kk_fid,der_pl,der_pn

#########

params = ['Ob','Om','h','ns','s8','w0','wa']
latex_names = ['$\Omega_{\mathrm{b},0}$','$\Omega_{\mathrm{m},0}$','$h$','$n_\mathrm{s}$','$\sigma_8$','$w_0$','$w_a$']

param_num = len(params)

# index of wanted redshift in z array (iz=0 gives z=0)
iz = 0

fig, axs = plt.subplots(param_num,2,figsize=(9,10),sharex=True)

logscale = False

for i, param in enumerate(params):

    if i == 0:
        axs[i,0].set_title(r'$\partial_\alpha \ln P_\mathrm{L}(k,z=0)$')
        axs[i,1].set_title(r'$\partial_\alpha \ln P_\mathrm{NL}(k,z=0)$')
    if i == param_num-1:
        axs[i,0].set_xlabel(r'$k$   (1/Mpc)')
        axs[i,1].set_xlabel(r'$k$   (1/Mpc)')

    axs[i,0].set_ylabel(latex_names[i])

    axs[i,0].set_xlim(1.e-4,50.)
    axs[i,1].set_xlim(1.e-4,50.)

    axs[i,0].axhline(0,1.e-4,50.,color='k',linestyle='--',linewidth=0.5)
    axs[i,1].axhline(0,1.e-4,50.,color='k',linestyle='--',linewidth=0.5)

    if param == 'w0':
        axs[i,0].set_ylim(-0.3,0.05)
        axs[i,1].set_ylim(-0.3,0.05)
    elif param == 'wa':
        axs[i,0].set_ylim(-0.01,0.1)
        axs[i,1].set_ylim(-0.01,0.1)
    elif param == 's8':
        axs[i,0].set_ylim(-0.3,3.5)
        axs[i,1].set_ylim(-0.3,3.5)
    elif param == 'ns':
        axs[i,0].set_ylim(-7.,7.)
        axs[i,1].set_ylim(-7.,7.)
    elif param == 'h':
        axs[i,0].set_ylim(-2.8,1.5)
        axs[i,1].set_ylim(-2.8,1.5)
    elif param == 'Om':
        axs[i,0].set_ylim(-3.5,1.8)
        axs[i,1].set_ylim(-3.5,1.8)
    elif param == 'Ob':
        axs[i,0].set_ylim(-0.5,0.8)
        axs[i,1].set_ylim(-0.5,0.8)
    #else:
    #else:
    #    axs[i,0].set_ylim(-60000,60000)
    #    axs[i,1].set_ylim(-60000,60000)

    #factor=1
    #if

    #axs[i,0].set_title(str(latex_names[i]),pad=-0.1)
    #axs[i,1].set_title(str(latex_names[i]),pad=-0.1)

    kk,dl,dn = derivative('class_w0wa_DP',param,0.01)
    if logscale == False:
        axs[i,0].semilogx(kk[:],dl[iz,:],'k-',label='CLASS DP',linewidth=2)
        axs[i,1].semilogx(kk[:],dn[iz,:],'k-',linewidth=2)
    else:
        axs[i,0].loglog(kk[:],dl[iz,:],'k-',label='CLASS DP',linewidth=2)
        axs[i,1].loglog(kk[:],dn[iz,:],'k-',linewidth=2)
        axs[i,0].loglog(kk[:],-dl[iz,:],'k--',linewidth=2)
        axs[i,1].loglog(kk[:],-dn[iz,:],'k--',linewidth=2)

    kk,dl,dn = derivative('class_w0wa_HP',param,0.01)
    if logscale == False:
        axs[i,0].semilogx(kk[:],dl[iz,:],'g-',label='CLASS HP',linewidth=0.9)
        axs[i,1].semilogx(kk[:],dn[iz,:],'g-',linewidth=0.9)
    else:
        axs[i,0].loglog(kk[:],dl[iz,:],'g-',label='CLASS HP',linewidth=0.9)
        axs[i,1].loglog(kk[:],dn[iz,:],'g-',linewidth=0.9)
        axs[i,0].loglog(kk[:],-dl[iz,:],'g--',linewidth=0.9)
        axs[i,1].loglog(kk[:],-dn[iz,:],'g--',linewidth=0.9)

    kk,dl,dn = derivative('camb_w0wa_P1',param,0.01)
    if logscale == False:
        axs[i,0].semilogx(kk[:],dl[iz,:],'c-',label='CAMB P1',linewidth=0.9)
        axs[i,1].semilogx(kk[:],dn[iz,:],'c-',linewidth=0.9)
    else:
        axs[i,0].loglog(kk[:],dl[iz,:],'c-',label='CAMB P1',linewidth=0.9)
        axs[i,1].loglog(kk[:],dn[iz,:],'c-',linewidth=0.9)
        axs[i,0].loglog(kk[:],-dl[iz,:],'c--',linewidth=0.9)
        axs[i,1].loglog(kk[:],-dn[iz,:],'c--',linewidth=0.9)

    kk,dl,dn = derivative('camb_w0wa_P2',param,0.01)
    if logscale == False:
        axs[i,0].semilogx(kk[:],dl[iz,:],'b-',label='CAMB P2',linewidth=0.9)
        axs[i,1].semilogx(kk[:],dn[iz,:],'b-',linewidth=0.9)
    else:
        axs[i,0].loglog(kk[:],dl[iz,:],'b-',label='CAMB P2',linewidth=0.9)
        axs[i,1].loglog(kk[:],dn[iz,:],'b-',linewidth=0.9)
        axs[i,0].loglog(kk[:],-dl[iz,:],'b--',linewidth=0.9)
        axs[i,1].loglog(kk[:],-dn[iz,:],'b--',linewidth=0.9)

    kk,dl,dn = derivative('camb_w0wa_P3',param,0.01)
    if logscale == False:
        axs[i,0].semilogx(kk[:],dl[iz,:],'r-',label='CAMB P3',linewidth=0.9)
        axs[i,1].semilogx(kk[:],dn[iz,:],'r-',linewidth=0.9)
    else:
        axs[i,0].loglog(kk[:],dl[iz,:],'r-',label='CAMB P3',linewidth=0.9)
        axs[i,1].loglog(kk[:],dn[iz,:],'r-',linewidth=0.9)
        axs[i,0].loglog(kk[:],-dl[iz,:],'r--',linewidth=0.9)
        axs[i,1].loglog(kk[:],-dn[iz,:],'r--',linewidth=0.9)

    if param == 's8':
        axs[i,0].legend(loc='upper left')

#plt.show()
plt.savefig('derivatives.pdf')

fig, axs = plt.subplots(param_num,2,figsize=(9,10),sharex=True)

logscale = False

for i, param in enumerate(params):

    if i == 0:
        axs[i,0].set_title(r'$\Delta [\partial_\alpha \ln P_\mathrm{L}(k,z=0)]$')
        axs[i,1].set_title(r'$\Delta [\partial_\alpha \ln P_\mathrm{NL}(k,z=0)]$')
    if i == param_num-1:
        axs[i,0].set_xlabel(r'$k$   (1/Mpc)')
        axs[i,1].set_xlabel(r'$k$   (1/Mpc)')

    axs[i,0].set_ylabel(latex_names[i])

    axs[i,0].set_xlim(2.e-4,50.)
    axs[i,1].set_xlim(2.e-4,50.)

    axs[i,0].axhline(0,1.e-4,50.,color='k',linestyle='--',linewidth=0.5)
    axs[i,1].axhline(0,1.e-4,50.,color='k',linestyle='--',linewidth=0.5)

    if param == 'Ob':
        axs[i,0].set_ylim(-0.003,0.003)
        axs[i,1].set_ylim(-0.003,0.003)
    elif param == 'Om':
        axs[i,0].set_ylim(-0.007,0.007)
        axs[i,1].set_ylim(-0.007,0.007)
    elif param == 'h':
        axs[i,0].set_ylim(-0.15,0.15)
        axs[i,1].set_ylim(-0.15,0.15)
    elif param == 'ns':
        axs[i,0].set_ylim(-0.002,0.002)
        axs[i,1].set_ylim(-0.002,0.002)
    elif param == 's8':
        axs[i,0].set_ylim(-0.007,0.007)
        axs[i,1].set_ylim(-0.007,0.007)
    elif param == 'w0':
        axs[i,0].set_ylim(-0.0012,0.0012)
        axs[i,1].set_ylim(-0.0012,0.0012)
    elif param == 'wa':
        axs[i,0].set_ylim(-0.0006,0.0006)
        axs[i,1].set_ylim(-0.0006,0.0006)


    #factor=1
    #if

    #axs[i,0].set_title(str(latex_names[i]),pad=-0.1)
    #axs[i,1].set_title(str(latex_names[i]),pad=-0.1)

    kk_ref,dl_ref,dn_ref = derivative('class_w0wa_HP',param,0.01)

    kk,dl,dn = derivative('class_w0wa_DP',param,0.01)
    if logscale == False:
        axs[i,0].semilogx(kk_ref[:],interp1d(kk,dl[iz,:],fill_value="extrapolate")(kk_ref[:])-dl_ref[iz,:],'k-',label='CLASS DP - CLASS HP',linewidth=2)
        axs[i,1].semilogx(kk_ref[:],interp1d(kk,dn[iz,:],fill_value="extrapolate")(kk_ref[:])-dn_ref[iz,:],'k-',linewidth=2)
    else:
        axs[i,0].loglog(kk_ref[:],abs(interp1d(kk,dl[iz,:],fill_value="extrapolate")(kk_ref[:])/dl_ref[iz,:]),'k-',label='CLASS DP - CLASS HP',linewidth=2)
        axs[i,1].loglog(kk_ref[:],abs(interp1d(kk,dn[iz,:],fill_value="extrapolate")(kk_ref[:])/dn_ref[iz,:]),'k-',linewidth=2)

    kk,dl,dn = derivative('camb_w0wa_P1',param,0.01)
    if logscale == False:
        axs[i,0].semilogx(kk_ref[:],interp1d(kk,dl[iz,:],fill_value="extrapolate")(kk_ref[:])-dl_ref[iz,:],'c-',label='CAMB P1 - CLASS HP',linewidth=0.9)
        axs[i,1].semilogx(kk_ref[:],interp1d(kk,dn[iz,:],fill_value="extrapolate")(kk_ref[:])-dn_ref[iz,:],'c-',linewidth=0.9)
    else:
        axs[i,0].loglog(kk_ref[:],abs(interp1d(kk,dl[iz,:],fill_value="extrapolate")(kk_ref[:])/dl_ref[iz,:]),'c-',label='CAMB P1 - CLASS HP',linewidth=0.9)
        axs[i,1].loglog(kk_ref[:],abs(interp1d(kk,dn[iz,:],fill_value="extrapolate")(kk_ref[:])/dn_ref[iz,:]),'c-',linewidth=0.9)

    kk,dl,dn = derivative('camb_w0wa_P2',param,0.01)
    if logscale == False:
        axs[i,0].semilogx(kk_ref[:],interp1d(kk,dl[iz,:],fill_value="extrapolate")(kk_ref[:])-dl_ref[iz,:],'b-',label='CAMB P2 - CLASS HP',linewidth=0.9)
        axs[i,1].semilogx(kk_ref[:],interp1d(kk,dn[iz,:],fill_value="extrapolate")(kk_ref[:])-dn_ref[iz,:],'b-',linewidth=0.9)
    else:
        axs[i,0].loglog(kk_ref[:],abs(interp1d(kk,dl[iz,:],fill_value="extrapolate")(kk_ref[:])/dl_ref[iz,:]),'b-',label='CAMB P2 - CLASS HP',linewidth=0.9)
        axs[i,1].loglog(kk_ref[:],abs(interp1d(kk,dn[iz,:],fill_value="extrapolate")(kk_ref[:])/dn_ref[iz,:]),'b-',linewidth=0.9)

    kk,dl,dn = derivative('camb_w0wa_P3',param,0.01)
    if logscale == False:
        axs[i,0].semilogx(kk_ref[:],interp1d(kk,dl[iz,:],fill_value="extrapolate")(kk_ref[:])-dl_ref[iz,:],'r-',label='CAMB P3 - CLASS HP',linewidth=0.9)
        axs[i,1].semilogx(kk_ref[:],interp1d(kk,dn[iz,:],fill_value="extrapolate")(kk_ref[:])-dn_ref[iz,:],'r-',linewidth=0.9)
    else:
        axs[i,0].loglog(kk_ref[:],abs(interp1d(kk,dl[iz,:],fill_value="extrapolate")(kk_ref[:])/dl_ref[iz,:]),'r-',label='CAMB P3 - CLASS HP',linewidth=0.9)
        axs[i,1].loglog(kk_ref[:],abs(interp1d(kk,dn[iz,:],fill_value="extrapolate")(kk_ref[:])/dn_ref[iz,:]),'r-',linewidth=0.9)

    if param == 'ns':
        axs[i,0].legend(loc='upper left')

#plt.show()
plt.savefig('derivative_errors.pdf')
