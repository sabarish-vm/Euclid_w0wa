PYTHON=python

# NOTE: the IST:Fisher matrix located in the ../fisher_for_public directory
# can only be handled after a renaming of the parameters, performed by running
# once the commands:
# python external_fishers/replace_paramnames.py ../fisher_for_public/All_Results/pessimistic/flat/
# python external_fishers/replace_paramnames.py ../fisher_for_public/All_Results/optimistic/flat/

# Select here the probe (photometric/spectroscopic)
#
PROBE=photometric
PROBE_SHORT=photo
LKL=euclid_photometric_z
#
#PROBE=spectroscopic
#PROBE_SHORT=spec
#LKL=euclid_spectroscopic

# Select here the case (pessimistic/optimistic)
#
CASE=pessimistic
CASE_SHORT=pess
#
#CASE=optimistic
#CASE_SHORT=opt

# Select here the precision
CLASS_PREC=HP
CAMB_PREC=P3
argu=$1
# placeholder for running optionally input_4_cast

cd plots

$PYTHON lineplots.py

for PROBE in photometric spectroscopic
do
for CASE in pessimistic optimistic
do
echo "Shall we rerun the $PROBE $CASE case ? (y/n)"
read answer
if [ "$answer" = "y" ] ; then

    # run CosmicFish


        # plot error comparisons
        #
        # uncomment if you prefer old files to be removed rather than overwritten
        #rm $PROBE/$CASE/*.txt
        #rm $PROBE/$CASE*/.pdf
        #
        $PYTHON $PROBE/$CASE/CF_camb_ext-vs-MP.py --error-only
        rm $PROBE/$CASE/CF_camb_ext-vs-MP_cosmo_and_nuisance_error_comparison.pdf
        #
        $PYTHON $PROBE/$CASE/CF_camb_ext-vs-camb_int.py --error-only
        # keep error comparison plot for the paper
        #
        $PYTHON $PROBE/$CASE/CF_camb_int-vs-MP.py --error-only
        rm $PROBE/$CASE/CF_camb_int-vs-MP_cosmo_and_nuisance_error_comparison.pdf
        #
        $PYTHON $PROBE/$CASE/CF_class_ext-vs-MP.py --error-only
        rm $PROBE/$CASE/CF_class_ext-vs-MP_cosmo_and_nuisance_error_comparison.pdf
        #
        $PYTHON $PROBE/$CASE/CF_class_ext-vs-camb_ext.py --error-only
        rm $PROBE/$CASE/CF_class_ext-vs-camb_ext_cosmo_and_nuisance_error_comparison.pdf
        #
        $PYTHON $PROBE/$CASE/CF_class_ext-vs-camb_int.py --error-only
        rm $PROBE/$CASE/CF_class_ext-vs-camb_int_cosmo_and_nuisance_error_comparison.pdf
        #
        $PYTHON $PROBE/$CASE/CF_class_ext-vs-class_int.py --error-only
        # keep error comparison plot for the paper
        #
        $PYTHON $PROBE/$CASE/CF_class_int-vs-MP.py --error-only
        # keep error comparison plot for the paper
        #
        $PYTHON $PROBE/$CASE/CF_class_int-vs-camb_ext.py --error-only
        rm $PROBE/$CASE/CF_class_int-vs-camb_ext_cosmo_and_nuisance_error_comparison.pdf
        #
        $PYTHON $PROBE/$CASE/CF_class_int-vs-camb_int.py --error-only
        # keep error comparison plot for the paper
        #
        # run comparison plot between various pipelines
        $PYTHON $PROBE/$CASE/4codes-CF_class_camb-vs-ISTF-vs-MP.py --error-only
        # keep error comparison plot for the paper
        #
        $PYTHON $PROBE/$CASE/CF_class_ext_DP-vs-HP.py --error-only
        ##
        $PYTHON $PROBE/$CASE/CF_camb_ext_P2-vs-P3.py --error-only
        #
#        $PYTHON $PROBE/$CASE/CF_MP_DP-vs-HP.py --error-only
        #
        $PYTHON $PROBE/$CASE/CF_class_ext_DP-vs-HP.py --error-only
        #
        $PYTHON $PROBE/$CASE/CF_camb_ext_P2-vs-P3.py --error-only
        #
 #       $PYTHON $PROBE/$CASE/CF_MP_DP-vs-HP.py --error-only
        cd ..


fi
done
done
