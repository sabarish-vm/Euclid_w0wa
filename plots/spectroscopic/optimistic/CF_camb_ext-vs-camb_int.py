import os, sys, argparse

os.chdir(os.path.dirname(os.path.realpath(__file__)))
sys.path.append('../../')
from plot_master import *

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('--error-only',action='store_true',dest='error_only',
                    help='    Plot error comparions plots only',
                    default=False)
args = parser.parse_args()
error_only = args.error_only

fish_files =  [
    '../../../results/cosmicfish_external/spectroscopic/optimistic/CosmicFish_v0.9_w0wa_external_camb-Optimistic-own_P3_GCsp_fishermatrix.txt',
    '../../../results/cosmicfish_internal/spectroscopic/optimistic/CosmicFish_v0.9_w0wa_internal_camb-Optimistic-own_GCsp_fishermatrix.txt'
              ]

labels=  [r'${\tt CF/ext/CAMB}$',
          r'${\tt CF/int/CAMB}$']

cutnames=['Omegam', 'Omegab','ns', 'h','sigma8', 'w0', 'wa','lnbgs8_1', 'lnbgs8_2', 'lnbgs8_3', 'lnbgs8_4', 'Ps_1', 'Ps_2', 'Ps_3', 'Ps_4']

compare_errors_dict={'legend_title':'GCsp opt'}
plotter(fish_files=fish_files,labels=labels,pars=cutnames,
        error_only=error_only, compare_errors_dict=compare_errors_dict)
