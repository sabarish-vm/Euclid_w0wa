PYTHON=python3

PROBE=photometric
PROBE_SHORT=photo
LKL=euclid_photometric_z
#CASE=pessimistic
#CASE_SHORT=pess
CASE=optimistic
CASE_SHORT=opt

# placeholder for running optionally input_4_cast

echo "Shall we rerun the $PROBE $CASE case ? (y/n)"
read answer
if [ "$answer" = "y" ] ; then

    # run CosmicFish

    echo "Shall we rerun CosmicFish CLASS external ? (y/n)"
    read answer
    if [ "$answer" = "y" ] ; then
        $PYTHON input/cosmicfish/$PROBE/$CASE/class_external.py
    fi

    echo "Shall we rerun CosmicFish CAMB external ? (y/n)"
    read answer
    if [ "$answer" = "y" ] ; then
        $PYTHON input/cosmicfish/$PROBE/$CASE/camb_external.py
    fi

    echo "Shall we rerun CosmicFish CLASS internal ? (y/n)"
    read answer
    if [ "$answer" = "y" ] ; then
        $PYTHON input/cosmicfish/$PROBE/$CASE/class_internal.py
    fi

    echo "Shall we rerun CosmicFish CAMB internal ? (y/n)"
    read answer
    if [ "$answer" = "y" ] ; then
        $PYTHON input/cosmicfish/$PROBE/$CASE/camb_internal.py
    fi

    # run MP

    echo "Shall we rerun MontePython Fisher ? (y/n)"
    read answer
    if [ "$answer" = "y" ] ; then
        cd ../montepython
        cp montepython/likelihoods/$LKL/$LKL.data.pessimsitic montepython/likelihoods/$LKL/$LKL.data
        rm data/euclid_xc_fiducial.dat
        rm -rf ../Euclid_w0wa/results/montepython_fisher/$PROBE/$CASE
        $PYTHON montepython/MontePython.py run -p ../Euclid_w0wa/input/montepython_fisher/$PROBE/$CASE/$PROBE_$CASE_SHORT.param -o ../Euclid_w0wa/results/montepython_fisher/$PROBE/$CASE -f 0
        $PYTHON montepython/MontePython.py run -o ../Euclid_w0wa/results/montepython_fisher/$PROBE/$CASE --fisher --fisher-step-it 1 --fisher-tol 10000
        cd ../Euclid_w0wa
        $PYTHON input/montepython_fisher/paramnames_for_cosmicfish.py results/montepython_fisher/$PROBE/$CASE
    fi

    # TBD: run MCMC
    echo "Shall we rerun MontePython MCMC ? (y/n)"
    read answer
    if [ "$answer" = "y" ] ; then
        echo "script not written yet"
    fi

    # plot error comparisons
    cd plots/$PROBE/$CASE
    #
    $PYTHON CF_camb_ext-vs-MP.py --error-only
    rm CF_camb_ext-vs-MP_cosmo_and_nuisance_error_comparison.pdf
    rm CF_camb_ext-vs-MP_cosmo_and_nuisance_matrix_ratio.pdf
    #
    $PYTHON CF_camb_ext-vs-camb_int.py --error-only
    # keep error comparison plot for the paper
    rm CF_camb_ext-vs-camb_int_cosmo_and_nuisance_matrix_ratio.pdf
    #
    $PYTHON CF_camb_int-vs-MP.py --error-only
    rm CF_camb_int-vs-MP_cosmo_and_nuisance_error_comparison.pdf
    rm CF_camb_int-vs-MP_cosmo_and_nuisance_matrix_ratio.pdf
    #
    $PYTHON CF_class_ext-vs-MP.py --error-only
    rm CF_class_ext-vs-MP_cosmo_and_nuisance_error_comparison.pdf
    rm CF_class_ext-vs-MP_cosmo_and_nuisance_matrix_ratio.pdf
    #
    $PYTHON CF_class_ext-vs-camb_ext.py --error-only
    rm CF_class_ext-vs-camb_ext_cosmo_and_nuisance_error_comparison.pdf
    rm CF_class_ext-vs-camb_ext_cosmo_and_nuisance_matrix_ratio.pdf
    #
    $PYTHON CF_class_ext-vs-camb_int.py --error-only
    rm CF_class_ext-vs-camb_int_cosmo_and_nuisance_error_comparison.pdf
    rm CF_class_ext-vs-camb_int_cosmo_and_nuisance_matrix_ratio.pdf
    #
    $PYTHON CF_class_ext-vs-class_int.py --error-only
    # keep error comparison plot for the paper
    rm CF_class_ext-vs-class_int_cosmo_and_nuisance_matrix_ratio.pdf
    #
    $PYTHON CF_class_int-vs-MP.py --error-only
    # keep error comparison plot for the paper
    rm CF_class_int-vs-MP_cosmo_and_nuisance_matrix_ratio.pdf
    #
    $PYTHON CF_class_int-vs-camb_ext.py --error-only
    rm CF_class_int-vs-camb_ext_cosmo_and_nuisance_error_comparison.pdf
    rm CF_class_int-vs-camb_ext_cosmo_and_nuisance_matrix_ratio.pdf
    #
    $PYTHON CF_class_int-vs-camb_int.py --error-only
    # keep error comparison plot for the paper
    rm CF_class_int-vs-camb_int_cosmo_and_nuisance_matrix_ratio.pdf
    #
    # run comparison plot between various pipelines
    $PYTHON 4codes-CF_class_camb-vs-ISTF-vs-MP.py --error-only
    #
    cd ../../..

    # run comparison table
    cd results/comparison_table
    $PYTHON table-$PROBE_SHORT-$CASE_SHORT.py
    cd ../..

    # run getdist
    cd getdist
    $PYTHON $PROBE_SHORT_$CASE_SHORT.py
    cd ..

    # run absolute error script
    cd results/absolute_sigmas
    $PYTHON $PROBE_SHORT-$CASE_SHORT-sigmas.py
    cd ../..

fi
