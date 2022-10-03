PYTHON=python3

# The tests below are performed using the spectra P_L, P_NL produced by input_4_cast for class/camb with different precision settings.

# First test: comparison of fiducial P_L and P_NL
# This test is not done with the output files located in
#
# Euclid_w0wa/input/input_4_cast
#
# Indeed, for this test, we need precisely the same value of A_s, and
# thus slightly different values of sigma_8.
# So we use here some customised input files with two different sigma_8
# giving the same A_s. However, we can do short runs because we only need
# the fiducial models, no parameter variations.
# Additionally, for this test, we use 'halofit_min_k_nonlinear=3.282e-3' in CLASS settings,
# to match the L/NL transition int he two codes. We do not do it elsewhere.

cd ../../input_4_cast
$PYTHON run.py ../Euclid_w0wa/test_precision/class_w0wa_DP.ini
$PYTHON run.py ../Euclid_w0wa/test_precision/class_w0wa_HP.ini
$PYTHON run.py ../Euclid_w0wa/test_precision/camb_w0wa_P1.ini
$PYTHON run.py ../Euclid_w0wa/test_precision/camb_w0wa_P2.ini
$PYTHON run.py ../Euclid_w0wa/test_precision/camb_w0wa_P3.ini
cd ../Euclid_w0wa/test_precision/
$PYTHON plot_fiducial_ratios.py

# Second test: comparison of first derivatives of P_L and P_NL w.r.t each parameter
# This test is done with the output files located in
#
# Euclid_w0wa/input/input_4_cast

#cd ../../input_4_cast
#$PYTHON run.py ../Euclid_w0wa/input/input_4_cast/class_w0wa_DP.ini
#$PYTHON run.py ../Euclid_w0wa/input/input_4_cast/class_w0wa_HP.ini
#$PYTHON run.py ../Euclid_w0wa/input/input_4_cast/camb_w0wa_P1.ini
#$PYTHON run.py ../Euclid_w0wa/input/input_4_cast/camb_w0wa_P2.ini
#$PYTHON run.py ../Euclid_w0wa/input/input_4_cast/camb_w0wa_P3.ini
#cd ../Euclid_w0wa/test_precision/
$PYTHON plot_derivative.py
