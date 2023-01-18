#!/bin/bash
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

# placeholder for running optionally input_4_cast

    echo "Shall we replot the contours of the combined probes with getdist ? (y/n)"
    read answer
if [ "$answer" = "y" ] ; then

        echo "plotting getdist/combined_triangle.py"
start=$(date +%s.%N)

# Here you can place your function
$PYTHON getdist/combined_triangle.py

duration=$(echo "$(date +%s.%N) - $start" | bc)
execution_time=`printf "%.2f seconds" $duration`

echo "Script Execution Time: $execution_time"

fi
    echo "Shall we replot the contours of the individual probes with getdist ? (y/n)"
    read answer
if [ "$answer" = "y" ] ; then
for PROBE_SHORT in spec
do
for CASE_SHORT in opt pess
do
        # run getdist
        cd getdist
        echo "plotting ${PROBE_SHORT} ${CASE_SHORT}"
start=$(date +%s.%N)

# Here you can place your function
        $PYTHON ${PROBE_SHORT}_$CASE_SHORT.py

duration=$(echo "$(date +%s.%N) - $start" | bc)
execution_time=`printf "%.2f seconds" $duration`

echo "Script Execution Time: $execution_time"
        cd ..
  done
done    
fi


