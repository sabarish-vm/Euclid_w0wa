import glob
import sys
import os

path_to_change = sys.argv[1]
dirname = os.path.realpath(path_to_change)
print(dirname)
os.chdir(dirname)

pars_old=['aIA', 'bIA', 'eIA']
pars_new=['AIA', 'betaIA', 'etaIA']


for f in glob.glob("*.paramnames"):
    print(f)
    with open(f, "r") as inputfile:
        newText = inputfile.read()
        for po, pn in zip(pars_old, pars_new):
    	    newText = newText.replace(po, pn)
        newText = newText.replace('betAIA','betaIA') # this lines is used when the script is run more than once, to avoid bIA -> betaIA -> betAIA
        newText = newText.replace('b10    b10   1.743', 'b10    b10    1.743')
    print(newText)
    with open(f, "w") as outputfile:
        outputfile.write(newText)

print("***Finished replacing strings***")
