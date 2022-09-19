PYTHON=python3

# placeholder for running optionally input_4_cast

echo "Shall we rerun the photometric pessimsitic case ? (y/n)"
read answer
if [ ! "$answer" = "y" ] ; then

# run CosmicFish
$PYTHON input/cosmicfish/photometric/pessimistic/class_external.py
$PYTHON input/cosmicfish/photometric/pessimistic/camb_external.py
$PYTHON input/cosmicfish/photometric/pessimistic/class_internal.py
$PYTHON input/cosmicfish/photometric/pessimistic/camb_internal.py

# run MP
cd ../montepython
cp montepython/likelihoods/euclid_photometric_z/euclid_photometric_z.data.pessimsitic montepython/likelihoods/euclid_photometric_z/euclid_photometric_z.data

rm data/euclid_xc_fiducial.dat
rm -rf ../Euclid_w0wa/results/montepython_fisher/photometric/pessimistic
$PYTHON montepython/MontePython.py run -p ../Euclid_w0wa/input/montepython_fisher/photometric/pessimistic/photometric_pess.param -o ../Euclid_w0wa/results/montepython_fisher/photometric/pessimistic -f 0
$PYTHON montepython/MontePython.py run -o ../Euclid_w0wa/results/montepython_fisher/photometric/pessimistic --fisher --fisher-step-it 1 --fisher-tol 10000
cd ../Euclid_w0wa
$PYTHON input/montepython_fisher/paramnames_for_cosmicfish.py results/montepython_fisher/photometric/pessimistic

# TBD: run MCMC

# plot error comparisons
cd plots/photometric/pessimistic
$PYTHON CF_camb_ext-vs-MP.py --error-only
$PYTHON CF_camb_int-vs-MP.py --error-only
$PYTHON CF_class_ext-vs-camb_ext.py --error-only
$PYTHON CF_class_ext-vs-class_int.py --error-only
$PYTHON CF_class_int-vs-camb_ext.py --error-only
$PYTHON CF_camb_ext-vs-camb_int.py --error-only
$PYTHON CF_class_ext-vs-MP.py --error-only
$PYTHON CF_class_ext-vs-camb_int.py --error-only
$PYTHON CF_class_int-vs-MP.py --error-only
$PYTHON CF_class_int-vs-camb_int.py --error-only
cd ../../..

# run comparison table
cd results/comparison_table
$PYTHON table-to-pdf.py
cd ../..

# run getdist
cd getdist
$PYTHON photo_pess.py

fi

# run absolute error script
results/absolute_sigmas
$PYTHON all_sigmas.py
