import numpy as np
import os
from getdist import paramnames
from getdist import loadMCSamples
from getdist import plots
import seaborn as sns
import sys
os.chdir(os.path.dirname(os.path.realpath(__file__)))
sys.path.append('../../cosmicfish_reloaded/')
from cosmicfishpie.analysis import fisher_matrix as cfm
from cosmicfishpie.analysis import fisher_operations as cfo


def combine(case1,case2):

    if case1 == 'pessimistic':
        case1_cap='Pessimistic'
        case1_short='pess'
    elif case1 == 'optimistic':
        case1_cap='Optimistic'
        case1_short='opt'

    if case2 == 'pessimistic':
        case2_cap='Pessimistic'
        case2_short='pess'
    elif case2 == 'optimistic':
        case2_cap='Optimistic'
        case2_short='opt'

    cf1_path = '../results/cosmicfish_internal/photometric/%s/CosmicFish_v0.9_w0wa_internal_class-%s-3PT_WLGCph_fishermatrix'%(case1,case1_cap)
    cf2_path = '../results/cosmicfish_internal/spectroscopic/%s/CosmicFish_v0.9_w0wa_internal_class-%s-own_GCsp_fishermatrix'%(case2,case2_cap)
    cf3_path = '../results/cosmicfish_internal/combined/%s_%s/CosmicFish_v0.9_w0wa_internal_class-combined-%s-%s_fishermatrix'%(case1_short,case2_short,case1_short,case2_short)

    # read fisher matrices for individual probes
    cf1 = cfm.fisher_matrix(file_name=cf1_path+'.txt')
    cf2 = cfm.fisher_matrix(file_name=cf2_path+'.txt')

    # sum up matrices
    cf3 = cf1+cf2

    # save fisher matrix as .txt
    cf3.save_to_file(file_name=cf3_path+'.txt')

    # save inverse matrix as .covmat with MontePython-style header
    header_covmat = str(cf3.param_names).translate({91: 35,39: 32, 44: 32,93: None})
    np.savetxt(cf3_path+'.covmat',cf3.inverse_fisher_matrix(),header=header_covmat)

    ###########

    mp1_path = '../results/montepython_fisher/photometric/%s_HP/fisher'%(case1)
    mp2_path = '../results/montepython_fisher/spectroscopic/%s_HP/fisher'%(case2)
    mp3_path = '../results/montepython_fisher/combined/%s_%s/fisher'%(case1_short,case2_short)

    # read fisher matrices for individual probes
    mp1 = cfm.fisher_matrix(file_name=mp1_path+'.mat')
    mp2 = cfm.fisher_matrix(file_name=mp2_path+'.mat')

    # sum up matrices
    mp3 = mp1+mp2

    # save fisher matrix as .txt
    mp3.save_to_file(file_name=mp3_path+'.mat')

    # save inverse matrix as .covmat with MontePython-style header
    header_covmat = str(mp3.param_names).translate({91: 35,39: 32, 44: 32,93: None})
    np.savetxt(mp3_path+'.covmat',mp3.inverse_fisher_matrix(),header=header_covmat)

    return


combine('pessimistic','pessimistic')
combine('pessimistic','optimistic')
combine('optimistic','pessimistic')
combine('optimistic','optimistic')
