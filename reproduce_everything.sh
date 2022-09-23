PYTHON=python3

# NOTE: the IST:Fisher matrix located in the ../fisher_for_public directory
# can only be handled after a renaming of the parameters, performed by running
# once the script:
# python3 external_fisher/replace_paramnames.py

# Select here the probe (photometric/spectroscopic)
#
#PROBE=photometric
#PROBE_SHORT=photo
#LKL=euclid_photometric_z
#
PROBE=spectroscopic
PROBE_SHORT=spec
LKL=euclid_spectroscopic

# Select here the case (pessimistic/optimistic)
#
CASE=pessimistic
CASE_SHORT=pess
#
#CASE=optimistic
#CASE_SHORT=opt

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
        cp montepython/likelihoods/$LKL/$LKL.data.$CASE montepython/likelihoods/$LKL/$LKL.data
        if [ "$PROBE" = "photometric" ] ; then
            rm data/euclid_xc_fiducial.dat
        fi
        if [ "$PROBE" = "spectroscopic" ] ; then
            rm data/euclid_pk_fiducial.dat
        fi
        rm -rf ../Euclid_w0wa/results/montepython_fisher/$PROBE/$CASE
        $PYTHON montepython/MontePython.py run -p ../Euclid_w0wa/input/montepython_fisher/$PROBE/$CASE/($PROBE)_$CASE_SHORT.param -o ../Euclid_w0wa/results/montepython_fisher/$PROBE/$CASE -f 0
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

    echo "Shall we recompute error ratios and redo error plots ? (y/n)"
    echo "(this step is necessary to update the main comparison table)"
    read answer
    if [ "$answer" = "y" ] ; then

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
    fi

    echo "Shall we replot main the comparison table ? (y/n)"
    read answer
    if [ "$answer" = "y" ] ; then

        # run comparison table
        cd results/comparison_table
        $PYTHON table-$PROBE_SHORT-$CASE_SHORT.py
        cd ../..
    fi

    echo "Shall we replot main the contours with getdist ? (y/n)"
    read answer
    if [ "$answer" = "y" ] ; then

        # run getdist
        cd getdist
        $PYTHON ($PROBE_SHORT)_$CASE_SHORT.py
        cd ..
    fi

    echo "Shall we redo the LaTeX table with absolute errors ? (y/n)"
    read answer
    if [ "$answer" = "y" ] ; then

        if [ "$PROBE" = "photometric" ] ; then
           echo "setting the parameter names in fisher_for_public"
           python3 external_fishers/replace_paramnames.py ../fisher_for_public/All_Results/$CASE/flat/
        fi

        # run absolute error script
        cd results/absolute_sigmas
        $PYTHON $PROBE_SHORT-$CASE_SHORT-sigmas.py
        cd ../..
    fi

fi
