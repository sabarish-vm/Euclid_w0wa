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

cf1_path = '../results/cosmicfish_internal/photometric/pessimistic/CosmicFish_v0.9_w0wa_internal_class-Pessimistic-3PT_WLGCph_fishermatrix.txt'
cf2_path = '../results/cosmicfish_internal/spectroscopic/pessimistic/CosmicFish_v0.9_w0wa_internal_class-Pessimistic-own_GCsp_fishermatrix.txt'
cf3_path = '../results/cosmicfish_internal/combined/pess_pess/CosmicFish_v0.9_w0wa_internal_class-combined-pess-pess_fishermatrix.txt'

cf1 = cfm.fisher_matrix(file_name=cf1_path)
cf2 = cfm.fisher_matrix(file_name=cf2_path)
cf3 = cf1+cf2

## cfm.save(cf3,file_name=cf3_path)
