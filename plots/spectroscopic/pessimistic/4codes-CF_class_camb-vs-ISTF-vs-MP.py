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
    '../../../results/cosmicfish_internal/spectroscopic/pessimistic/CosmicFish_v0.9_w0wa_internal_class-Pessimistic-own_GCsp_fishermatrix.txt',
    '../../../results/cosmicfish_internal/spectroscopic/pessimistic/CosmicFish_v0.9_w0wa_internal_camb-Pessimistic-own_GCsp_fishermatrix.txt',
    '../../../results/montepython_fisher/spectroscopic/pessimistic/fisher.mat'
     ,
      '../../../external_fishers/soapfish/km025/SOAPFish_C2-NL2-km025-w0wa-flat-full-1p0E-02-last.dat'
              ]
    
labels=  [
         r'CF_int_class',
         r'CF_int_camb',
          r'MP'
          ,
          r'SOAPFish'
          ]

cutnames=['Omegam', 'Omegab','ns', 'h','sigma8', 'w0', 'wa',  'lnbgs8_1', 'lnbgs8_2', 'lnbgs8_3', 'lnbgs8_4', 'Ps_1', 'Ps_2', 'Ps_3', 'Ps_4']

transf_labels={'\\ln(b_g \\sigma_8)_1': r'b_{g1}',
               '\\ln(b_g \\sigma_8)_2': r'b_{g2}', 
               '\\ln(b_g \\sigma_8)_3': r'b_{g3}', 
                '\\ln(b_g \\sigma_8)_4': r'b_{g4}'
               }

compare_errors_dict={'ncol_legend':4, 'legend_title':'GCsp pess', 'xticksrotation':45, 'transform_latex_dict': transf_labels}# 'legend_title_fontsize':16} 
plotter(fish_files=fish_files,labels=labels,pars=cutnames,error_only=error_only, compare_errors_dict=compare_errors_dict)
