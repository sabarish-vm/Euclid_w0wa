import os, sys, argparse

os.chdir(os.path.dirname(os.path.realpath(__file__)))
sys.path.append('../../')

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('--error-only',action='store_true',dest='error_only',
                    help='    Plot error comparions plots only',
                    default=False)
args = parser.parse_args()
error_only = args.error_only

from plot_master import plotter

fish_files =  [
    '../../../results/cosmicfish_external/photometric/optimistic/CosmicFish_v0.9_w0wa_external_class-Optimistic-3PT_DP_WLGCph_fishermatrix.txt',
    '../../../results/cosmicfish_external/photometric/optimistic/CosmicFish_v0.9_w0wa_external_class-Optimistic-3PT_HP_WLGCph_fishermatrix.txt'
              ]

labels=  [r'${\tt CF/ext/CLASS}$ DP',
          r'${\tt CF/ext/CLASS}$ HP']

cutnames=['Omegam', 'Omegab', 'ns', 'h','sigma8','w0', 'wa', 'b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8', 'b9', 'b10','AIA', 'etaIA']

plotter(fish_files=fish_files,labels=labels,pars=cutnames,error_only=error_only)
