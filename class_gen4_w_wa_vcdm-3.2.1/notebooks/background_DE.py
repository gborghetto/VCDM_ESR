# import necessary modules
from classy import Class
from math import pi
import matplotlib.pyplot as plt
import numpy as np

#############################################
#
# Cosmological parameters and other CLASS parameters
#
w0 = -0.6
wa = -1.0
# Using the exact parameter names as provided in the original script
common_settings = {# LambdaCDM parameters
                   'h':0.67810,
                   'omega_b':0.02238280,
                   'omega_cdm':0.1201075,
                   'A_s':2.100549e-09,
                   'n_s':0.9660499,
                   'tau_reio':0.05430842 ,
                   # output and precision parameters
                   'output':'tCl,pCl,lCl',
                   'lensing':'yes',
                   'l_max_scalars':5000,
                   # Using the user-specified names for the modified CLASS version
                   'w_0_VCDM': w0,
                   'w_a_VCDM': wa,
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
# Note the redshift array from CLASS is ordered from high z to low z
zs_class = background['z']
rho_lambda_class = background['(.)rho_lambda']
H_class = background['H [1/Mpc]']

# Normalize the CLASS rho_lambda result to get rho(z)/rho(0)
# The background array is ordered with z descending, so the last element is at z=0.
rho_lambda_norm_class = rho_lambda_class / rho_lambda_class[-1]


#############################################
#
# Manual Calculations
#
#############################################

# Define a redshift array for the manual calculations
z_manual = np.linspace(0, 5, 200)
a_manual = 1 / (1 + z_manual)

# 1) Manual calculation for Dark Energy Density
# The analytical solution for rho_DE(z)/rho_DE(0) in a CPL model
rho_lambda_ratio_manual = (a_manual**(-3 * (1 + w0 + wa))) * np.exp(3 * wa * (a_manual - 1))

# 2) Manual calculation for Hubble Parameter H(z)
# We will use the Friedmann equation: H(z)^2 = H0^2 * E(z)^2
# E(z)^2 = Omega_r*(1+z)^4 + Omega_m*(1+z)^3 + Omega_k*(1+z)^2 + Omega_de*f(z)
# where f(z) = rho_de(z)/rho_de(0)

# Get z=0 values from CLASS output to ensure consistency
H0 = H_class[-1]
rho_crit0 = background['(.)rho_crit'][-1]
# It is most accurate to get the Omega values directly from CLASS's computed background
Omega_m0 = (background['(.)rho_b'][-1] + background['(.)rho_cdm'][-1]) / rho_crit0
Omega_r0 = (background['(.)rho_g'][-1] + background['(.)rho_ur'][-1]) / rho_crit0
Omega_de0 = rho_lambda_class[-1] / rho_crit0
# Assume Omega_k=0 as it's the CLASS default if not specified
Omega_k0 = 1 - (Omega_m0 + Omega_r0 + Omega_de0)

print(f"\nDerived Omega values at z=0:")
print(f"Omega_m0 = {Omega_m0:.5f}")
print(f"Omega_r0 = {Omega_r0:.5f}")
print(f"Omega_de0 = {Omega_de0:.5f}")
print(f"Omega_k0 = {Omega_k0:.5f}")
print(f"Sum = {Omega_m0+Omega_r0+Omega_de0+Omega_k0:.5f}")

# Calculate H(z) using the derived parameters and the manual DE evolution
E_z_squared = (Omega_r0 * (1 + z_manual)**4 +
               Omega_m0 * (1 + z_manual)**3 +
               Omega_k0 * (1 + z_manual)**2 +
               Omega_de0 * rho_lambda_ratio_manual)
H_manual = H0 * np.sqrt(E_z_squared)


#############################################
#
# Plotting
#
#############################################

fig, ax = plt.subplots(1, 2, figsize=(16, 6))

# --- Plot 1: Dark Energy Density ---
ax[0].plot(z_manual, rho_lambda_ratio_manual, color='C0', linestyle='-', lw=2, label='Manual Calculation (Analytical)')
ax[0].plot(zs_class, rho_lambda_norm_class, color='C1', linestyle='--', lw=3, label='CLASS Result')
ax[0].set_xlabel(r'$z$', fontsize=16)
ax[0].set_ylabel(r'$\rho_\Lambda(z) / \rho_\Lambda(0)$', fontsize=16)
ax[0].set_title('Dark Energy Density Evolution', fontsize=16)
ax[0].grid(True)
ax[0].legend(fontsize=12)
ax[0].set_xlim(0, 5)

# --- Plot 2: Hubble Parameter ---
ax[1].plot(z_manual, H_manual, color='C0', linestyle='-', lw=2, label='Manual Calculation')
ax[1].plot(zs_class, H_class, color='C1', linestyle='--', lw=3, label='CLASS Result')
ax[1].set_xlabel(r'$z$', fontsize=16)
ax[1].set_ylabel(r'$H(z) \ [\mathrm{Mpc}^{-1}]$', fontsize=16)
ax[1].set_title('Hubble Parameter Evolution', fontsize=16)
ax[1].grid(True)
ax[1].legend(fontsize=12)
ax[1].set_yscale('log')
ax[1].set_xlim(0, 5)
ax[1].set_ylim(1e-4, 1e-2)


plt.tight_layout()
plt.show()

M.empty()