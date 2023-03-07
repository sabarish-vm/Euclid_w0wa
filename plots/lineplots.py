# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.14.5
#   kernelspec:
#     display_name: cosmicfish
#     language: python
#     name: python3
# ---

# +
import matplotlib.pyplot   as plt
import matplotlib.gridspec as gridspec
import matplotlib.lines    as mlines
import matplotlib.ticker   as ticker
import matplotlib.patches  as mpatches
from matplotlib.lines import Line2D
from mpl_toolkits import axes_grid1

import numpy as np
import argparse
import math
import sys
import os
import copy
import itertools as it
import glob
import scipy
# -

sys.path.append('../../cosmicfish_reloaded/')
from cosmicfishpie.analysis import fisher_plot_analysis as cfa
from cosmicfishpie.analysis import fisher_plotting as cfp
from cosmicfishpie.analysis import fisher_matrix as cfm
from cosmicfishpie.analysis import fisher_operations as cfo



# +
obses = ["photometric", "spectroscopic"]
cases = ['optimistic', "pessimistic"]

for obse in obses[:]:
    for case in cases[:]:

        load_dir = '../results/cosmicfish_external/{:s}/{:s}/'.format(obse, case)
        namext = 'CosmicFish*.txt'
        print(load_dir+namext)

        first_mat = glob.glob(load_dir+namext)[0]
        print(first_mat)

        plot_dir = './{:s}/{:s}/'.format(obse, case)
        print(plot_dir)
        print(obse)
        if obse=="photometric":
            cutnames=['Omegam', 'Omegab', 'ns', 'h','sigma8','w0', 'wa', 'b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8', 'b9', 'b10','AIA', 'etaIA']
            fishmat = cfm.fisher_matrix(file_name=first_mat)
            fishmat = cfo.reshuffle(fishmat, cutnames)
            param_names = fishmat.get_param_names_latex()
            print("Param names: ", param_names)
            parsnames_latex=["$"+pp+"$" for pp in param_names if pp != '\\beta_{IA}']
        elif obse=="spectroscopic":
            print("Enter spectro")
            cutnames=['Omegam', 'Omegab','ns', 'h','sigma8', 'w0', 'wa',  'lnbgs8_1', 'lnbgs8_2', 'lnbgs8_3', 'lnbgs8_4', 'Ps_1', 'Ps_2', 'Ps_3', 'Ps_4']
            fishmat = cfm.fisher_matrix(file_name=first_mat)
            fishmat = cfo.reshuffle(fishmat, cutnames)
            param_names = fishmat.get_param_names_latex()
            transf_labels={'\\ln(b_g \\sigma_8)_1': r'\ln(b \sigma_8)_1',
                    '\\ln(b_g \\sigma_8)_2': r'\ln(b \sigma_8)_2',
                    '\\ln(b_g \\sigma_8)_3': r'\ln(b \sigma_8)_3',
                    '\\ln(b_g \\sigma_8)_4': r'\ln(b \sigma_8)_4'
                    }
            parsnames_latex = ["$"+transf_labels.get(pp, pp)+"$" for pp in param_names]
        
        #parsnames_latex=["$"+pp+"$" for pp in parsnames_latex]

        print("Param names Latex: ", parsnames_latex)
        print(len(parsnames_latex))


        fig, axs = plt.subplots(4, 1, sharey=True, figsize=(18,9),

                                    facecolor='white', sharex=True, 
                                    gridspec_kw = {'wspace':0., 'hspace':0.})
        fig.subplots_adjust(wspace=0., hspace=0.)
        eUnMa = {}
        eUnMa[0] = np.loadtxt(plot_dir+"CF_camb_ext-vs-camb_int_cosmo_and_nuisance_error_comparison.txt")
        eUnMa[1] = np.loadtxt(plot_dir+"CF_class_ext-vs-class_int_cosmo_and_nuisance_error_comparison.txt")
        eUnMa[2] = np.loadtxt(plot_dir+"CF_class_int-vs-camb_int_cosmo_and_nuisance_error_comparison.txt")
        eUnMa[3] = np.loadtxt(plot_dir+"CF_class_int-vs-MP_cosmo_and_nuisance_error_comparison.txt")
        labdic={}
        labdic[0] = r'${\tt CF/ext/CAMB}$ vs. ${\tt CF/int/CAMB}$'
        labdic[1] = r'${\tt CF/ext/CLASS}$ vs. ${\tt CF/int/CLASS}$'
        labdic[2] = r'${\tt CF/int/CLASS}$ vs. ${\tt CF/int/CAMB}$'
        labdic[3] = r'${\tt CF/int/CLASS}$ vs. ${\tt MP/Fisher}$'

        print("Data shape: ", eUnMa[0].shape)
        
        n_pars=len(parsnames_latex)
        x_pars = np.arange(1, n_pars+1)
        print("x pars: ", x_pars)
        collight = 'lightgrey'
        coldark = 'darkgrey'
        warmcol='darkorange'
        coldcol='darkblue'
        light_hatch='/'
        alpha = 0.6
        legfonts = 22
        lightpatch = mpatches.Patch(color=collight, alpha=alpha)
        darkpatch = mpatches.Patch(color=coldark, alpha=alpha)#, hatch=light_hatch)
        patchlist=[lightpatch, darkpatch]
        lines = []
        line1 = Line2D([0], [0], color=coldark, linewidth=20, linestyle='-', marker='o', ms=10, markerfacecolor=warmcol, 
                fillstyle='full', markeredgecolor=warmcol, alpha=alpha+0.1)
        line2 = Line2D([0], [0], color=collight, linewidth=20, linestyle='-', marker='o', ms=10, markerfacecolor=coldcol, 
                fillstyle='none', markeredgecolor=coldcol, markeredgewidth=3, alpha=alpha+0.1)
        legpatch=["marg.", "unmarg."]
        lines = [line2, line1]
        leg2=axs[0].legend(lines,legpatch, loc="upper left",ncol=2, fontsize=legfonts, facecolor=None, frameon=False)
        ymaxes=[]
        ymins=[]
        for ind, ax in enumerate(axs):
            unmargy = np.abs(eUnMa[ind][0,:])
            margy = np.abs(eUnMa[ind][2,:])
            print("margy: ", len(margy))
            ax.bar(x_pars, margy, color=collight, width=0.8, alpha=0.9, zorder=1)
            ax.bar(x_pars, unmargy, color=coldark, width=0.5, alpha=0.95, zorder=2)
            ax.plot(x_pars, unmargy, 'o', c=warmcol, alpha=0.7, ms=1*12, zorder=4)
            ax.scatter(x_pars, margy, s=100, lw=3, alpha=1.0, facecolors='none', edgecolors=coldcol, label=labdic[ind], zorder=3)
            #ax.fill_between(x_pars, margy, np.zeros(len(x_pars)), interpolate=False, facecolor=collight, edgecolor=collight, alpha=alpha+0.1, linewidth=0.01)
            #ax.fill_between(x_pars, unmargy, np.zeros(len(x_pars)), interpolate=False, facecolor=coldark, edgecolor=coldark, alpha=alpha+0.1, linewidth=0.01)
            #ax.plot(x_pars, eUnMa_rel[1,:])
            #ax.plot(x_pars, eUnMa_rel[3,:])
            ax.set_ylim(-0.5,5)
            ax.set_xlim(1.-0.1,n_pars+0.1)
            ax.legend(loc='upper right', fontsize=legfonts, ncol=1, facecolor=None, 
                                        scatterpoints=0, handlelength=0, handletextpad=0)
            ax.set_xticks(x_pars)
            ax.tick_params(axis='x', direction='in', pad=10, labelsize=28)
            ax.tick_params(axis='y', direction='in', pad=10, labelsize=22)
            ax.set_xticklabels(parsnames_latex, fontsize=28, rotation=45)
            ax.yaxis.tick_left()
            #ax.yaxis.tick_both()
            ax.hlines(y=0., xmin=0, xmax=20, ls=':', colors='k', lw=1.5)
            ax.yaxis.set_ticks_position('both')
            ax.xaxis.tick_bottom()
            ax.xaxis.set_ticks_position('both')
            locaty = 2.0
            majorLocator = ticker.MultipleLocator(locaty)
            minorLocator = ticker.MultipleLocator(locaty)
            majorFormatter = ticker.FormatStrFormatter('%.1f')
            ax.yaxis.set_major_locator(majorLocator)
            ax.yaxis.set_major_formatter(majorFormatter)
            ax.yaxis.set_minor_locator(minorLocator)
            print(ax.get_position(original=True).ymin)
            ymins.append(ax.get_position(original=True).ymin)
            ymaxes.append(ax.get_position(original=True).ymax)
        print(ymins)
        print(ymaxes)
        ymm = np.mean([np.max(ymaxes), np.min(ymins)])
        print(ymm)
        axs[0].add_artist(leg2)
        fig.supylabel(r'% discrepancy on $\sigma_i$ w.r.t. median', fontsize=28, x=0.009, y=0.545, va="center")
        #axs[0].set_ylabel(r'% discrepancy on $\sigma$ w.r.t. median', fontsize=28)#, x=0.009, y=0.5, va="center")
        fig.tight_layout()
        filename=("../plots/{a:s}/{b:s}/DotPlot-PairComparison-{a:s}_{b:s}.png".format(a=obse, b=case))
        filenamepdf=("../plots/{a:s}/{b:s}/DotPlot-PairComparison-{a:s}_{b:s}.png".format(a=obse, b=case))
        print(filename)
        fig.savefig(filename, bbox_inches='tight', dpi=150)
        fig.savefig(filenamepdf, bbox_inches='tight', dpi=50)

# +
obses = ["photometric", "spectroscopic"]
cases = ['optimistic']

for obse in obses[:]:
    for case in cases[:1]:

        load_dir = '../results/cosmicfish_external/{:s}/{:s}/'.format(obse, case)
        namext = 'CosmicFish*.txt'
        print(load_dir+namext)

        first_mat = glob.glob(load_dir+namext)[0]
        print(first_mat)

        plot_dir = './{:s}/{:s}/'.format(obse, case)
        print(plot_dir)
        print(obse)
        if obse=="photometric":
            cutnames=['Omegam', 'Omegab', 'ns', 'h','sigma8','w0', 'wa', 'b1', 'b2', 'b3', 'b4', 'b5', 'b6', 'b7', 'b8', 'b9', 'b10','AIA', 'etaIA']
            fishmat = cfm.fisher_matrix(file_name=first_mat)
            fishmat = cfo.reshuffle(fishmat, cutnames)
            param_names = fishmat.get_param_names_latex()
            print("Param names: ", param_names)
            parsnames_latex=["$"+pp+"$" for pp in param_names if pp != '\\beta_{IA}']
        elif obse=="spectroscopic":
            print("Enter spectro")
            cutnames=['Omegam', 'Omegab','ns', 'h','sigma8', 'w0', 'wa',  'lnbgs8_1', 'lnbgs8_2', 'lnbgs8_3', 'lnbgs8_4', 'Ps_1', 'Ps_2', 'Ps_3', 'Ps_4']
            fishmat = cfm.fisher_matrix(file_name=first_mat)
            fishmat = cfo.reshuffle(fishmat, cutnames)
            param_names = fishmat.get_param_names_latex()
            transf_labels={'\\ln(b_g \\sigma_8)_1': r'\ln(b \sigma_8)_1',
                    '\\ln(b_g \\sigma_8)_2': r'\ln(b \sigma_8)_2',
                    '\\ln(b_g \\sigma_8)_3': r'\ln(b \sigma_8)_3',
                    '\\ln(b_g \\sigma_8)_4': r'\ln(b \sigma_8)_4'
                    }
            parsnames_latex = ["$"+transf_labels.get(pp, pp)+"$" for pp in param_names]
        
        #parsnames_latex=["$"+pp+"$" for pp in parsnames_latex]

        print("Param names Latex: ", parsnames_latex)
        print(len(parsnames_latex))


        fig, axs = plt.subplots(2, 1, sharey=True, figsize=(18,9),

                                    facecolor='white', sharex=True, 
                                    gridspec_kw = {'wspace':0., 'hspace':0.})
        fig.subplots_adjust(wspace=0., hspace=0.)
        eUnMa = {}
        eUnMa[0] = np.loadtxt(plot_dir+"CF_camb_ext_P2-vs-P3_cosmo_and_nuisance_error_comparison.txt")
        eUnMa[1] = np.loadtxt(plot_dir+"CF_class_ext_DP-vs-HP_cosmo_and_nuisance_error_comparison.txt")
        labdic={}
        labdic[0] = r'${\tt CF/ext/CAMB}$ P2 vs. ${\tt CF/ext/CAMB}$ P3'
        labdic[1] = r'${\tt CF/ext/CLASS}$ DP vs. ${\tt CF/ext/CLASS}$ HP'

        print("Data shape: ", eUnMa[0].shape)
        
        n_pars=len(parsnames_latex)
        x_pars = np.arange(1, n_pars+1)
        print("x pars: ", x_pars)
        collight = 'lightgrey'
        coldark = 'darkgrey'
        warmcol='darkorange'
        coldcol='darkblue'
        light_hatch='/'
        alpha = 0.6
        legfonts = 22
        lightpatch = mpatches.Patch(color=collight, alpha=alpha)
        darkpatch = mpatches.Patch(color=coldark, alpha=alpha)#, hatch=light_hatch)
        patchlist=[lightpatch, darkpatch]
        lines = []
        line1 = Line2D([0], [0], color=coldark, linewidth=20, linestyle='-', marker='o', ms=10, markerfacecolor=warmcol, 
                fillstyle='full', markeredgecolor=warmcol, alpha=alpha+0.1)
        line2 = Line2D([0], [0], color=collight, linewidth=20, linestyle='-', marker='o', ms=10, markerfacecolor=coldcol, 
                fillstyle='none', markeredgecolor=coldcol, markeredgewidth=3, alpha=alpha+0.1)
        legpatch=["unmarg.", "marg."]
        lines = [line1, line2]
        leg2=axs[0].legend(lines,legpatch, loc="upper left",ncol=2, fontsize=legfonts, facecolor=None, frameon=False)
        ymaxes=[]
        ymins=[]
        for ind, ax in enumerate(axs):
            unmargy = np.abs(eUnMa[ind][0,:])
            margy = np.abs(eUnMa[ind][2,:])
            print("margy: ", len(margy))
            ax.bar(x_pars, margy, color=collight, width=0.8, alpha=0.9, zorder=1)
            ax.bar(x_pars, unmargy, color=coldark, width=0.5, alpha=0.95, zorder=2)
            ax.plot(x_pars, unmargy, 'o', c=warmcol, alpha=0.7, ms=1*12, zorder=4)
            ax.scatter(x_pars, margy, s=100, lw=3, alpha=1.0, facecolors='none', edgecolors=coldcol, label=labdic[ind], zorder=3)
            #ax.plot(x_pars, eUnMa_rel[1,:])
            #ax.plot(x_pars, eUnMa_rel[3,:])
            ax.set_ylim(-0.5,5)
            ax.set_xlim(1.-0.1,n_pars+0.1)
            ax.legend(loc='upper right', fontsize=legfonts, ncol=1, facecolor=None, 
                                        scatterpoints=0, handlelength=0, handletextpad=0)
            ax.set_xticks(x_pars)
            ax.tick_params(axis='x', direction='in', pad=10, labelsize=28)
            ax.tick_params(axis='y', direction='in', pad=10, labelsize=22)
            ax.set_xticklabels(parsnames_latex, fontsize=28, rotation=45)
            ax.yaxis.tick_left()
            #ax.yaxis.tick_both()
            ax.hlines(y=0., xmin=0, xmax=20, ls=':', colors='k', lw=1.5)
            ax.yaxis.set_ticks_position('both')
            ax.xaxis.tick_bottom()
            ax.xaxis.set_ticks_position('both')
            locaty = 2.0
            majorLocator = ticker.MultipleLocator(locaty)
            minorLocator = ticker.MultipleLocator(locaty)
            majorFormatter = ticker.FormatStrFormatter('%.1f')
            ax.yaxis.set_major_locator(majorLocator)
            ax.yaxis.set_major_formatter(majorFormatter)
            ax.yaxis.set_minor_locator(minorLocator)
            print(ax.get_position(original=True).ymin)
            ymins.append(ax.get_position(original=True).ymin)
            ymaxes.append(ax.get_position(original=True).ymax)
        print(ymins)
        print(ymaxes)
        ymm = np.mean([np.max(ymaxes), np.min(ymins)])
        print(ymm)
        axs[0].add_artist(leg2)
        fig.supylabel(r'% discrepancy on $\sigma_i$ w.r.t. median', fontsize=28, x=0.009, y=0.545, va="center")
        #axs[0].set_ylabel(r'% discrepancy on $\sigma$ w.r.t. median', fontsize=28)#, x=0.009, y=0.5, va="center")
        fig.tight_layout()
        filename=("../plots/{a:s}/{b:s}/DotPlot-PairComparison-DP-HP-{a:s}_{b:s}.png".format(a=obse, b=case))
        print(filename)
        fig.savefig(filename, bbox_inches='tight', dpi=150)
# -


