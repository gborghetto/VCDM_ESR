# import necessary modules
from classy import Class
from math import pi
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d
from scipy.integrate import cumulative_trapezoid
np.set_printoptions(precision=2, suppress=True)

#############################################
#
# Cosmological parameters and other CLASS parameters
#
N_nodes_VCDM = 10
w0 = -0.7
wa = -1.
z_arr = np.linspace(0., 5., N_nodes_VCDM)
a_arr = 1 / (1 + z_arr)
w_arr = w0 + wa * (1-a_arr)  # CPL formula for w(a)
z_nodes_VCDM = z_arr
a_nodes_VCDM = a_arr 
w_nodes_VCDM = w_arr

print("z_nodes_VCDM:\n", z_nodes_VCDM)
print("w_nodes_VCDM:\n", w_nodes_VCDM)

# Using the exact parameter names as provided in the original script
common_settings = {# LambdaCDM parameters
                   'h':0.67810,
                   'omega_b':0.02238280,
                   'omega_cdm':0.1201075,
                   'A_s':2.100549e-09,
                   'n_s':0.9660499,
                   'tau_reio':0.05430842 ,
                   # output and precision parameters
                #    'output':'tCl,pCl,lCl',
                #    'lensing':'yes',
                #    'l_max_scalars':5000,
                   # Using the user-specified names for the modified CLASS version
                   'N_nodes_VCDM': N_nodes_VCDM,
                   'w_nodes_VCDM': ','.join(map(str, w_nodes_VCDM)),
                   'a_nodes_VCDM': ','.join(map(str, a_nodes_VCDM)),
                   'input_verbose': 3,
                   'background_verbose': 3,
                   'output_verbose': 3,
               }
#
M = Class()
#
###############
#
# call CLASS
#
###############
#
M.set(common_settings)
M.compute(level=['background'])
background = M.get_background()
print("Available background quantities from CLASS:", background.keys())

# Extract results from CLASS
zs_class = background['z']
rho_lambda_class = background['(.)rho_lambda']
H_class = background['H [1/Mpc]']

# Normalize the CLASS rho_lambda result to get rho(z)/rho(0)
rho_lambda_norm_class = rho_lambda_class / rho_lambda_class[-1]


#############################################
#
# Manual Calculations
#
#############################################

# Define a redshift array for the manual calculations
z_manual = np.linspace(0, 5, 200)
a_manual = 1 / (1 + z_manual)

# --- Calculation 1: Analytical CPL Model (from before) ---
rho_lambda_ratio_analytical = (a_manual**(-3 * (1 + w0 + wa))) * np.exp(3 * wa * (a_manual - 1))

# --- Calculation 2: Spline w(a) Model ---
print("\nImplementing manual calculation with spline w(a)...")

# 2a. Define the spline for w(a) using the same nodes as CLASS
# Use the same a_arr that was computed from z_arr to ensure consistency
w_spline = interp1d(a_arr, w_arr, kind='linear', fill_value="extrapolate")

print(f"Spline nodes (a, w(a)):")
for i in range(N_nodes_VCDM):
    print(f"({a_arr[i]:.3f}, {w_arr[i]:.4f})")

# 2b. Calculate rho_DE(a) using the spline w(a)
# The CLASS implementation uses: rho(a) = rho_0 * exp(integrate_w_spline_trapezoidal(1.0, a, 300, ...))
# where integrate_w_spline_trapezoidal integrates y = -3 * (1 + w(a')) / a' from a_min to a_max
# So the integrand is already multiplied by -3, and we integrate from 1.0 to a

rho_lambda_ratio_spline = []

for a_val in a_manual:
    if a_val >= 1.0:
        # Present day: ratio = 1, integral = 0
        rho_lambda_ratio_spline.append(1.0)
    else:
        # Integrate from 1.0 to a_val (following CLASS implementation)
        # Use enough integration points for accuracy (CLASS uses 300)
        n_steps = 300
        a_integration = np.linspace(1.0, a_val, n_steps)
        # The integrand is -3 * (1 + w(a)) / a (following CLASS exactly)
        integrand = -3.0 * (1 + w_spline(a_integration)) / a_integration
        integral_val = np.trapz(integrand, a_integration)
        rho_ratio = np.exp(integral_val)
        rho_lambda_ratio_spline.append(rho_ratio)

rho_lambda_ratio_spline = np.array(rho_lambda_ratio_spline)

# --- Calculation 3: Hubble Parameter for both manual methods ---

# Get z=0 values from CLASS output for consistency
H0 = H_class[-1]
rho_crit0 = background['(.)rho_crit'][-1]
Omega_m0 = (background['(.)rho_b'][-1] + background['(.)rho_cdm'][-1]) / rho_crit0
Omega_r0 = (background['(.)rho_g'][-1] + background['(.)rho_ur'][-1]) / rho_crit0
Omega_de0 = rho_lambda_class[-1] / rho_crit0
print(f"Omega m = {Omega_m0}, Omega r = {Omega_r0}")
Omega_k0 = 1 - (Omega_m0 + Omega_r0 + Omega_de0)

# H(z) for the analytical CPL model
E_z_squared_analytical = (Omega_r0 * (1 + z_manual)**4 +
                          Omega_m0 * (1 + z_manual)**3 +
                          Omega_k0 * (1 + z_manual)**2 +
                          Omega_de0 * rho_lambda_ratio_analytical)
H_manual_analytical = H0 * np.sqrt(E_z_squared_analytical)

# H(z) for the spline w(a) model
E_z_squared_spline = (Omega_r0 * (1 + z_manual)**4 +
                      Omega_m0 * (1 + z_manual)**3 +
                      Omega_k0 * (1 + z_manual)**2 +
                      Omega_de0 * rho_lambda_ratio_spline)
H_manual_spline = H0 * np.sqrt(E_z_squared_spline)


#############################################
#
# Plotting
#
#############################################

fig, ax = plt.subplots(1, 2, figsize=(16, 6))

# --- Plot 1: Dark Energy Density ---
ax[0].plot(zs_class, rho_lambda_norm_class, color='k', linestyle='--', lw=3, label='CLASS Result')
ax[0].plot(z_manual, rho_lambda_ratio_analytical, color='C0', linestyle='-', lw=2, label='Manual (Analytical CPL)')
ax[0].plot(z_manual, rho_lambda_ratio_spline, color='C3', linestyle=':', lw=2, label=f'Manual (Spline w(a)), num_nodes={N_nodes_VCDM}')
ax[0].set_xlabel(r'$z$', fontsize=16)
ax[0].set_ylabel(r'$\rho_\Lambda(z) / \rho_\Lambda(0)$', fontsize=16)
ax[0].set_title('Dark Energy Density Evolution', fontsize=16)
ax[0].grid(True)
ax[0].legend(fontsize=12)
ax[0].set_xlim(0, 5)

# --- Plot 2: Hubble Parameter ---
ax[1].plot(zs_class, H_class, color='k', linestyle='--', lw=3, label='CLASS Result')
ax[1].plot(z_manual, H_manual_analytical, color='C0', linestyle='-', lw=2, label='Manual (Analytical CPL)')
ax[1].plot(z_manual, H_manual_spline, color='C3', linestyle=':', lw=2, label='Manual (Spline w(a))')
ax[1].set_xlabel(r'$z$', fontsize=16)
ax[1].set_ylabel(r'$H(z) \ [\mathrm{Mpc}^{-1}]$', fontsize=16)
ax[1].set_title('Hubble Parameter Evolution', fontsize=16)
ax[1].grid(True)
ax[1].legend(fontsize=12)
ax[1].set_xlim(0, 5)
ax[1].set_yscale('log')
ax[1].set_ylim(1e-4, 1e-2)

plt.tight_layout()
plt.show()

M.empty()