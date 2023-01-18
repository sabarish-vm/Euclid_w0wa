import numpy as np
from matplotlib import cm,colors
from matplotlib.colors import ListedColormap
from matplotlib import pyplot as plt
from itertools import combinations as cb
import os
outpath = os.path.realpath(__file__)

types = ['All Pars', 'Cosmo with fixed Nuisance', 'Cosmo with marginalized Nuisance', 'Nuisance with fixed Nuisance']
codes = [r'\texttt{CLASS ext}', r'\texttt{CLASS int}', r'\texttt{MontePython}', r'\texttt{CAMB ext}' , r'\texttt{CAMB int}']
types_dict = {'All Pars':'cosmo_and_nuisance', 'Cosmo with fixed Nuisance' : 'cosmo_fix_nuisance',
'Cosmo with marginalized Nuisance' : 'cosmo_marg_nuisance', 'Nuisance with fixed Nuisance' :  'nuisance_fix_cosmo'  }
name_to_cell = {r'\texttt{CLASS ext}':'class_ext',
                r'\texttt{CLASS int}' : 'class_int', 
                r'\texttt{MontePython}':'MP', 
                r'\texttt{CAMB ext}' : 'camb_ext', 
                r'\texttt{CAMB int}' : 'camb_int'}
all_combinations = list(cb(codes,2))

greenmap = ListedColormap(cm.get_cmap('Greens')(np.linspace(0,1,500))[250:400])
norm_green = colors.Normalize(vmin=0., vmax=13., clip=True)
mapper_green = cm.ScalarMappable(norm=norm_green, cmap=greenmap)

def hexcolor(value,mapper):

    r,g,b,a = mapper.to_rgba(value)
    r = int(r*255)
    g = int(g*255)
    b = int(b*255)

    return "#%s%s%s" % tuple([hex(c)[2:].rjust(2, "0") for c in (r, g, b)])

def write_data(df,category,files) :
   for cell1,cell2 in all_combinations :
    name1 = name_to_cell[cell1]
    name2 = name_to_cell[cell2]
    for file in files :
        if name1 in file and name2 in file and category in file :
            contents = np.loadtxt(file)
            max_val = np.amax(np.abs(contents))
            df.at[cell1,cell2] = max_val
            df.at[cell2,cell1] = max_val

def save_table(df,filename,save=True) :
    vals = np.around(df.values,decimals=2)
    fig,ax = plt.subplots(figsize=(4,1))
    ax.axis('tight')
    ax.axis('off')
    cellcolors = np.vectorize(hexcolor)(np.copy(vals),mapper_green)
    rowlabs=[r'${\tt CF/ext/CLASS}$', r'${\tt CF/int/CLASS}$', r'${\tt MP/Fisher}$', r'${\tt CF/ext/CAMB}$' , r'${\tt CF/int/CAMB}$']
    the_table=ax.table(cellText=vals, rowLabels=rowlabs, colLabels=rowlabs,
                        loc='center',
                        cellColours=cellcolors
                        )
    the_table.auto_set_font_size(False)
    the_table.scale(2.2,2)
    the_table.set_fontsize(12)
    if save : fig.savefig('table_'+filename+'.pdf',bbox_inches = 'tight')
    return fig,ax
