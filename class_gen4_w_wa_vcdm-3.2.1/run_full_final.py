#!/usr/bin/env python3

"""
Python script to run Cobaya minimization for multiple VCDM w(a) functions.

This script iterates through different w(a) parametrizations stored in 
generated_functions.c, automatically detects how many parameters each function needs,
runs CLASS with each function, and saves results.

TWO-STAGE OPTIMIZATION:
1. Quick MCMC (500 samples) to find viable parameter region
2. Minimize from best MCMC point for precise fit

Usage:
    python vcdm_multi_function_run_local.py [--resume] [--test] [--force] [--debug]
"""

from cobaya.run import run
import argparse
import os
import re
import numpy as np

def get_function_expression(generated_functions_file, function_index):
    """
    Extract the mathematical expression for a function from generated_functions.c
    
    Returns:
    --------
    str: The function expression as a string, or "Unknown" if not found
    """
    try:
        with open(generated_functions_file, 'r') as f:
            content = f.read()
        
        # Look for the comment that contains the original expression
        # Format: "// Expression N (original line M): <expression>"
        pattern = rf'// Expression {function_index}[^\n]*:\s*(.+?)$'
        match = re.search(pattern, content, re.MULTILINE)
        
        if match:
            return match.group(1).strip()
        
        # If not found in comment, try to extract from function body
        # This is harder but we can try
        pattern = rf'double func_{function_index}\s*\([^)]+\)\s*\{{[^}}]*return\s+([^;]+);'
        match = re.search(pattern, content, re.DOTALL)
        
        if match:
            expr = match.group(1).strip()
            # Clean up the expression a bit
            expr = expr.replace('(void)a0;', '').replace('(void)a1;', '')
            expr = expr.strip()
            return expr
        
        return "Unknown"
        
    except Exception as e:
        return f"Error: {e}"

def parse_function_signature(generated_functions_file, function_index):
    """
    Parse generated_functions.c to determine how many parameters a function ACTUALLY uses.
    
    Checks for (void)a0 and (void)a1 markers to detect unused parameters.
    
    Returns:
    --------
    dict with:
        'num_params': int (number of parameters actually used)
        'param_names': list of parameter names that are used
        'valid': bool (whether function was found and parsed)
    """
    try:
        with open(generated_functions_file, 'r') as f:
            content = f.read()
        
        # Find the function definition
        # Match from function start to its closing brace
        pattern = rf'double\s+func_{function_index}\s*\((.*?)\)\s*\{{(.*?)\n\}}'
        match = re.search(pattern, content, re.DOTALL)
        
        if not match:
            print(f"Warning: Could not find func_{function_index} in generated_functions.c")
            return {'num_params': 0, 'param_names': [], 'valid': False}
        
        # Extract parameter list and function body
        param_string = match.group(1)
        function_body = match.group(2)
        
        # Get all declared parameters (excluding 'x')
        params = [p.strip() for p in param_string.split(',')]
        declared_params = []
        for param in params:
            parts = param.split()
            if len(parts) == 2:
                param_type, param_name = parts
                if param_name != 'x':
                    declared_params.append(param_name)
        
        # Check which parameters are actually used
        # Parameters marked with (void)param_name are unused
        used_params = []
        for param_name in declared_params:
            void_marker = f"(void){param_name}"
            if void_marker not in function_body:
                # Parameter is NOT voided out, so it's used
                used_params.append(param_name)
        
        return {
            'num_params': len(used_params),
            'param_names': used_params,
            'valid': True,
            'declared_params': declared_params  # For debugging
        }
        
    except Exception as e:
        print(f"Error parsing function {function_index}: {e}")
        import traceback
        traceback.print_exc()
        return {'num_params': 0, 'param_names': [], 'valid': False}

def create_cobaya_info_dict(class_path, w_function_index, output_base_path, 
                            param_info):
    """
    Create the Cobaya info dictionary for a specific w(a) function.
    
    Parameters:
    -----------
    class_path : str
        Path to your modified CLASS installation
    w_function_index : int
        Index of the w(a) function to use from generated_functions.c
    output_base_path : str
        Base directory for output chains
    param_info : dict
        Information about function parameters from parse_function_signature
    """
    
    # Output path for this specific function
    output_path = os.path.join(output_base_path, f"{w_function_index:03d}/{w_function_index:03d}")
    
    info = {
        # Theory code
        "debug": True,
        "theory": {
            "classy": {
                "path": class_path,
                "stop_at_error": False,
                "extra_args": {
                    "output": "tCl,pCl,lCl",
                    "lensing": "yes",
                    "gauge": "newtonian",
#                    "N_ncdm": 1,          # 1 massive neutrino species
#                    "m_ncdm": 0.06 ,          # Mass in eV
#                    "N_ur": 2.0308   ,        # Remaining massless neutrinos
#                    "T_ncdm": 0.71611,
                    'tol_background_integration': 1e-10,
                    'tol_perturbations_integration': 1e-9,
                    "w_function_index": w_function_index,
                    # "input_verbose": 3,
                    # "background_verbose": 3,
                    # "output_verbose": 3,
                    #"l_max_scalars": 2508,
                    #"a_ini_over_a_today_default": 1e-21,
                }
            }
        },

        # Likelihoods - Planck lite (local machine)
        "likelihood": {
            "planck_2018_lowl.TT": None,
            "planck_2018_lowl.EE": None,
            "planck_2018_highl_plik.TTTEEE_lite_native": None,
            "planck_2018_lensing.native": None,
            #"cmb_lite_3d": {"thetastar_name": "theta_s_100", "ombh2_name": "omega_b", "omch2_name": "omega_cdm"},
            "bao.desi_dr2.desi_bao_all": None,
#            "sn.union3": None,
        },

        # Parameters
        "params": {
            # Standard cosmological parameters
            "omega_b": {
                "latex": r"\omega_b",
                "prior": {"min": 0.021, "max": 0.023},  # ← Match test.yaml
                "ref": {"dist": "norm", "loc": 0.022633, "scale": 0.001},  # ← Match test.yaml
                "proposal": 0.0001  # ← Match test.yaml
            },
            "omega_cdm": {
                "latex": r"\omega_{cdm}",
                "prior": {"min": 0.11, "max": 0.13},  # ← Match test.yaml
                "ref": {"dist": "norm", "loc": 0.1184, "scale": 0.01},  # ← Match test.yaml
                "proposal": 0.0001  # ← Match test.yaml
            },
            "logA": {
                "prior": {"min": 2.98, "max": 3.1},
                "ref": {"dist": "norm", "loc": 3.040776555, "scale": 0.001},
                "proposal": 0.001,
                "latex": r'\log(10^{10} A_\mathrm{s})',
                "drop": True
            },
            "A_s": {
                "value": 'lambda logA: 1e-10*np.exp(logA)',
                "latex": r'A_\mathrm{s}'
            },
            "n_s": {
                "latex": r"n_s",
                "prior": {"min": 0.94, "max": 0.99},
                "ref": {"dist": "norm", "loc": 0.965, "scale": 0.002},
                "proposal": 0.002
            },
            "tau_reio": {
                "latex": r"\tau",
                "prior": {"min": 0.01, "max": 0.15},
                "ref": {"dist": "norm", "loc": 0.0555, "scale": 0.003},
                "proposal": 0.003
            },
            "H0": {
                "latex": r"H_0",
                "prior": {"min": 60, "max": 72},
                "ref": {"dist": "norm", "loc": 66, "scale": 1.0},
                "proposal": 0.5
            },
            # "A_planck": {
            #     "latex": r"A_{\rm planck}",
            #     "prior": {"min": 0.9, "max": 1.1},
            #     "ref": 1.0,
            #     "proposal": 0.0025
            # },

            #Derived parameters
            "omega_m":{
                "latex": r"\Omega_\mathrm{m}",
                "derived": "lambda omega_cdm, omega_b, H0: (omega_cdm + omega_b) / (H0 / 100.0)**2"
            },
            "rdrag": {
                "latex": r"\mathrm{drag}",
                "derived": True
            },
            "hrd": {
                "latex": r'hr_d',
                "derived": 'lambda H0, rdrag: H0/100 * rdrag'
            },
            "sigma8": {
                "latex": r"\sigma_8",
                "derived": True
            },
            
            # 100 θ_s = 1.04189 ± 0.00028 → best-fit: 1.04191
            # This is automatically computed by CLASS
            "theta_s_100": {
                "latex": r"100\theta_s",
                "derived": True
            },
            
            "chi2__CMB": {
                "latex": r"\chi^2_{\rm CMB}",
                "derived": True
            },

             "chi2__BAO": {
                "latex": r"\chi^2_{\rm BAO}",
                "derived": True
            },

#             "chi2__SN": {
#                "latex": r"\chi^2_{\rm SN}",
#                "derived": True
#           },
            
            "chi2_total": {
                "latex": r"\chi^2_{\rm total}",
                "derived": "lambda chi2__CMB, chi2__BAO: chi2__CMB + chi2__BAO"
            },
        },
        
        # Output settings
        "output": output_path,
    }
    
    # Add VCDM parameters based on function signature
    # Map C parameter names (a0, a1, ...) to our naming (c0_esr, c1_esr, ...)
    """
Replace the VCDM parameter addition section in run_full.py (lines ~223-252)
This handles functions with 0, 1, or 2 parameters
"""

# Add VCDM parameters based on function signature
# Map C parameter names (a0, a1, ...) to our naming (c0_esr, c1_esr, ...)
    param_name_map = {
        'a0': 'c0_esr',
        'a1': 'c1_esr',
    }

    if param_info['valid']:
        num_params = param_info['num_params']
        
        if num_params == 0:
            # Function has no free parameters - fix c0 and c1 to safe defaults
            info['params']['c0_esr'] = 0.0  # Fixed, not sampled
            info['params']['c1_esr'] = 0.0   # Fixed, not sampled
            print(f"  Function {w_function_index} has no free parameters")
            print(f"  Fixed: c0_esr = 0.0, c1_esr = 0.0")
            
        elif num_params == 1:
            # Function has 1 parameter
            c_param_name = param_info['param_names'][0]
            
            if c_param_name == 'a0':
                info['params']['c0_esr'] = {
                    "latex": "w_0",
                    "prior": {"min": -10.0, "max": 10.0},
                    "ref": {"dist": "norm", "loc": -0.5, "scale": 0.3},
                    "proposal": 0.05
                }
                info['params']['c1_esr'] = 0.0  # Fixed
                print(f"  Function {w_function_index} has 1 parameter: c0_esr (free), c1_esr = 0 (fixed)")
                
            elif c_param_name == 'a1':
                info['params']['c0_esr'] = 0.0  # Fixed
                info['params']['c1_esr'] = {
                    "latex": "w_a",
                    "prior": {"min": -10.0, "max": 10.0},
                    "ref": {"dist": "norm", "loc": -0.5, "scale": 0.3},
                    "proposal": 0.05
                }
                print(f"  Function {w_function_index} has 1 parameter: c0_esr = 0 (fixed), c1_esr (free)")
            else:
                print(f"  Warning: Unknown single parameter '{c_param_name}' in function {w_function_index}")
                
        elif num_params == 2:
            # Function has 2 parameters - add both as free parameters
            for c_param_name in param_info['param_names']:
                if c_param_name in param_name_map:
                    cobaya_param_name = param_name_map[c_param_name]
                    
                    # Use test.yaml values (dark energy region)
                    if cobaya_param_name == 'c0_esr':
                        prior_min, prior_max = -10.0, 10.0
                        ref_loc = -0.5      # Dark energy region
                        ref_scale = 0.2
                        latex_name = "w_0"
                    elif cobaya_param_name == 'c1_esr':
                        prior_min, prior_max = -10.0, 10.0
                        ref_loc = -1.0      # Quintessence-like
                        ref_scale = 0.5
                        latex_name = "w_a"
                    else:
                        prior_min, prior_max = -10.0, 10.0
                        ref_loc = -0.5
                        ref_scale = 0.5
                        param_num = c_param_name[1]
                        latex_name = f"w_{param_num}"
                    
                    info['params'][cobaya_param_name] = {
                        "latex": latex_name,
                        "prior": {"min": prior_min, "max": prior_max},
                        "ref": {"dist": "norm", "loc": ref_loc, "scale": ref_scale},
                        "proposal": 0.05
                    }
                else:
                    print(f"  Warning: Unknown parameter name '{c_param_name}' in function {w_function_index}")
            
            print(f"  Function {w_function_index} has 2 parameters: c0_esr (free), c1_esr (free)")
        
        else:
            # More than 2 parameters - future extension
            print(f"  Warning: Function {w_function_index} has {num_params} parameters")
            print(f"  Current implementation only supports 0, 1, or 2 parameters")
            # Add all parameters generically
            for c_param_name in param_info['param_names']:
                if c_param_name in param_name_map:
                    cobaya_param_name = param_name_map[c_param_name]
                    param_num = c_param_name[1]
                    
                    info['params'][cobaya_param_name] = {
                        "latex": f"w_{param_num}",
                        "prior": {"min": -10.0, "max": 10.0},
                        "ref": {"dist": "norm", "loc": 0.01, "scale": 0.5},
                        "proposal": 0.05
                    }

    return info


def read_function_count(generated_functions_file):
    """
    Read the number of functions defined in generated_functions.c
    
    Returns the value of 'function_count' from the file.
    """
    try:
        with open(generated_functions_file, 'r') as f:
            content = f.read()
            # Look for line like: const int function_count = 1;
            for line in content.split('\n'):
                if 'function_count' in line and '=' in line:
                    # Extract the number
                    count_str = line.split('=')[1].split(';')[0].strip()
                    return int(count_str)
        print("Warning: Could not find function_count in generated_functions.c")
        return None
    except Exception as e:
        print(f"Error reading function count: {e}")
        return None


def run_single_function(class_path, w_function_index, output_base_path,
                       generated_functions_file, resume, test, force, debug):
    """
    Run TWO-STAGE optimization for a single w(a) function:
    1. Quick MCMC (500 samples) to explore and find viable region
    2. Minimize from best MCMC point for precise fit
    
    This approach is much more robust than direct minimization with random starts.
    """
    
    print(f"\n{'='*70}")
    print(f"Processing function index: {w_function_index}")
    func_expr = get_function_expression(generated_functions_file, w_function_index)
    print(f"Function expression: w(a) = {func_expr}")
    print(f"{'='*70}\n")
    
    # Parse function signature to determine parameters
    param_info = parse_function_signature(generated_functions_file, w_function_index)
    
    if not param_info['valid']:
        print(f"✗ Could not parse function {w_function_index}. Skipping.")
        return False
    
    print(f"Function {w_function_index} has {param_info['num_params']} parameter(s): {param_info['param_names']}")
    
    # Create info dictionary for this function
    info = create_cobaya_info_dict(class_path, w_function_index, output_base_path, param_info)
    
    # Output paths
    #output_path = info['output']
    #mcmc_output = os.path.join(output_path, 'mcmc_exploration')
    #minimize_output = os.path.join(output_path, 'minimize')
    output_path = os.path.join(output_base_path, f"{w_function_index:03d}", f"{w_function_index:03d}")
    
    # Check if we should skip (already done and not forcing)
    #min_file = os.path.join(minimize_output, os.path.basename(minimize_output) + '.minimum.txt')
    print(f"Output will be saved to: {output_path}")

    # if os.path.exists(min_file) and not force and not resume:
    #     print(f"✓ Function {w_function_index} already completed. Skipping...")
    #     print(f"  (Use --force to overwrite or --resume to continue)")
    #     return True
    # Create info dictionary
    #info = create_cobaya_info_dict(class_path, w_function_index, output_base_path, param_info)
    
    # Set the SAME output path for both stages
    info['output'] = output_path
    
    # ========================================================================
    # STAGE 1: Quick MCMC to find viable region
    # ========================================================================
    print(f"\nSTAGE 1: Quick MCMC exploration")
    print("-" * 70)

     # Configure MCMC
    info['sampler'] = {
        'mcmc': {
            'drag': False,
            'oversample_power': 0.4,
            'proposal_scale': 1.9,
            'Rminus1_stop': 0.1,
            'Rminus1_cl_stop': 0.2,
            'max_tries': 100,
            'max_samples': 500,  # Quick exploration
        }
    }
    
    # Check if MCMC already done
    mcmc_chain_file = f"{output_path}.1.txt"
    if os.path.exists(mcmc_chain_file) and not force:
        print(f"✓ MCMC chain already exists: {mcmc_chain_file}")
        print(f"  Skipping MCMC stage (use --force to rerun)")
        mcmc_success = True
    else:
        try:
            print(f"Starting MCMC exploration...")
            updated_info, sampler = run(info, resume=resume, test=test, force=force, debug=debug)
            print(f"✓ MCMC exploration completed")
            mcmc_success = True
        except Exception as e:
            print(f"⚠ MCMC exploration failed: {e}")
            print(f"  Will use default starting points for minimization")
            mcmc_success = False
    
    # mcmc_info = info.copy()
    # mcmc_info['output'] = mcmc_output
    # mcmc_info['sampler'] = {
    #     'mcmc': {
    #         'max_samples': 500,           # Quick exploration
    #         'Rminus1_stop': 0.3,          # Loose convergence (just need viability)
    #         'Rminus1_cl_stop': 0.5,
    #         'learn_proposal': True,       # Adapt to find good regions
    #         'drag': False,                # Faster
    #         'oversample_power': 0.2,
    #     }
    # }
    
    # best_point = None
    # mcmc_success = False
    
    # try:
    #     print("Starting quick MCMC (max 500 samples)...")
    #     print("  This explores parameter space to find regions where CLASS works")
        
    #     updated_mcmc, sampler_mcmc = run(mcmc_info, force=True)
        
    #     # Try to load samples and find best point
    #     try:
    #         from getdist.mcsamples import loadMCSamples
    #         mcmc_samples = loadMCSamples(mcmc_output)
            
    #         # Find best likelihood point
    #         loglikes = mcmc_samples.loglikes
    #         if len(loglikes) > 0:
    #             best_idx = np.argmax(loglikes)
    #             best_loglike = loglikes[best_idx]
                
    #             # Get parameter names (only sampled ones)
    #             sampled_params = [p for p in info['params'].keys() 
    #                              if isinstance(info['params'][p], dict) and 
    #                              'prior' in info['params'][p]]
                
    #             # Extract best point
    #             best_point = {}
    #             for i, param in enumerate(sampled_params):
    #                 best_point[param] = mcmc_samples.samples[best_idx, i]
                
    #             print(f"\n✓ MCMC exploration successful!")
    #             print(f"  Found {len(loglikes)} viable samples")
    #             print(f"  Best log-likelihood: {best_loglike:.2f}")
    #             print(f"  Best point parameters:")
    #             for param, value in best_point.items():
    #                 if 'c0_esr' in param or 'c1_esr' in param:
    #                     print(f"    {param:15s} = {value:10.6f}")
                
    #             mcmc_success = True
    #         else:
    #             print(f"⚠ MCMC produced no valid samples")
    #             print(f"  Will use default starting points for minimization")
        
    #     except Exception as e:
    #         print(f"⚠ Could not load MCMC samples: {e}")
    #         print(f"  Will use default starting points for minimization")
    
    # except Exception as e:
    #     print(f"⚠ MCMC exploration failed: {e}")
    #     print(f"  Will use default starting points for minimization")
    
    # ========================================================================
    # STAGE 2: Minimize from best point (or default)
    # ========================================================================
    print(f"\nSTAGE 2: Minimization")
    print("-" * 70)
    
    #minimize_info = info.copy()
    #minimize_info['output'] = minimize_output
    
    # Update starting point if MCMC found a good region
    # if best_point is not None and mcmc_success:
    #     print("Starting minimization from best MCMC point:")
    #     for param, value in best_point.items():
    #         if param in minimize_info['params'] and isinstance(minimize_info['params'][param], dict):
    #             minimize_info['params'][param]['ref'] = value
    #             if 'c0_esr' in param or 'c1_esr' in param:
    #                 print(f"  {param:15s} starting at {value:10.6f}")
    # else:
    #     print("Starting minimization from default reference points")
    #     print("  (MCMC did not find a better starting region)")
    
    # Configure minimizer
    info['sampler'] = {
        'minimize': {
            'method': 'bobyqa',
            'ignore_prior': False,
            'max_evals': 1e6,
            'best_of': 16,
        }
    }

    # Check if minimization already done
    min_file = f"{output_path}.minimum.txt"
    if os.path.exists(min_file) and not force:
        print(f"✓ Minimization already complete: {min_file}")
        print(f"  Skipping minimization (use --force to rerun)")
        return True
    
    # Run minimization - with resume=True, Cobaya auto-uses MCMC results
    try:
        print(f"Starting minimization...")
        if mcmc_success:
            print(f"  Will start from best MCMC point (resume=True)")
        else:
            print(f"  Will start from default reference points")
        
        updated_info, sampler = run(info, resume=True, test=test, force=force, debug=debug)
        
        print(f"\n{'='*70}")
        print(f"✓ Successfully completed function {w_function_index}")
        print(f"{'='*70}")
        print(f"  Output: {output_path}")
        print(f"  Files:")
        print(f"    - MCMC chain: {output_path}.1.txt")
        print(f"    - Minimum: {output_path}.minimum.txt")
        
        return True
        
    except Exception as e:
        print(f"\n{'='*70}")
        print(f"✗ Minimization failed for function {w_function_index}")
        print(f"{'='*70}")
        print(f"  Error: {e}")
        
        error_file = f"{output_path}.error.log"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)  # Create directory
        with open(error_file, 'w') as f:  # Write to the error file
            f.write(f"Error for function {w_function_index}:\n{e}\n")
        
        return False
    
    # # Run minimization
    # try:
    #     print(f"\nStarting minimization (best_of={minimize_info['sampler']['minimize']['best_of']})...")
    #     updated_info, sampler = run(minimize_info, resume=True, test=test, force=True, debug=debug)
        
    #     print(f"\n{'='*70}")
    #     print(f"✓ Successfully completed function {w_function_index}")
    #     print(f"{'='*70}")
    #     print(f"  MCMC exploration: {mcmc_output}")
    #     print(f"  Final results:    {minimize_output}")
        
    #     return True
        
    # except Exception as e:
    #     print(f"\n{'='*70}")
    #     print(f"✗ Minimization failed for function {w_function_index}")
    #     print(f"{'='*70}")
    #     print(f"  Error: {e}")
        
    #     # Save error log
    #     error_file = os.path.join(output_path, 'error.log')
    #     os.makedirs(output_path, exist_ok=True)
    #     with open(error_file, 'w') as f:
    #         f.write(f"Error for function {w_function_index}:\n")
    #         f.write(f"MCMC success: {mcmc_success}\n")
    #         if best_point:
    #             f.write(f"Best MCMC point: {best_point}\n")
    #         f.write(f"\nMinimization error:\n{e}\n")
        
    #     print(f"  Error log saved to: {error_file}")
    #     return False


def main():
    """
    Main execution: iterate through all functions and run minimization.
    """
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Run CLASS minimization for multiple w(a) functions"
    )
    parser.add_argument(
        "--resume", action="store_true", 
        help="Resume from previous run", 
        default=False
    )
    parser.add_argument(
        "--test", action="store_true", 
        help="Test run (quick, doesn't save)", 
        default=False
    )
    parser.add_argument(
        "--force", action="store_true", 
        help="Force overwrite of existing results", 
        default=False
    )
    parser.add_argument(
        "--debug", action="store_true", 
        help="Debug mode (more verbose output)", 
        default=False
    )
    parser.add_argument(
        "--functions", type=str,
        help="Function indices to run (e.g., '0-5' or '0,2,4')",
        default=None
    )
    
    args = parser.parse_args()
    
    # Configuration (local machine)
    class_path = "/scratch/s.2362709/VCDM/class_gen4_w_wa_vcdm-3.2.1" #"/Users/giuliaborghetto/OneDriveSwanseaUniversity/VCDM/class_gen4_w_wa_vcdm-3.2.1" 
    output_base = "/scratch/s.2362709/VCDM/class_gen4_w_wa_vcdm-3.2.1/chains_noSN"  #"/Users/giuliaborghetto/OneDriveSwanseaUniversity/VCDM/chains" 
    generated_functions_file = os.path.join(class_path, "source/generated_functions.c")
    
    # Read number of functions
    num_functions = read_function_count(generated_functions_file)
    
    if num_functions is None:
        print("ERROR: Could not determine number of functions.")
        print("Please check generated_functions.c contains 'const int function_count = N;'")
        return
    
    print(f"\n{'='*70}")
    print(f"VCDM Multi-Function Analysis")
    print(f"{'='*70}")
    print(f"CLASS path: {class_path}")
    print(f"Output base: {output_base}")
    print(f"Number of functions: {num_functions}")
    #print(f"Likelihood: Planck Lite + DESI BAO")
    print(f"{'='*70}\n")
    
    # Determine which functions to run
    if args.functions:
        # Parse function specification
        if '-' in args.functions:
            # Range: "0-5"
            start, end = map(int, args.functions.split('-'))
            function_indices = range(start, end + 1)
        elif ',' in args.functions:
            # List: "0,2,4,6"
            function_indices = [int(x.strip()) for x in args.functions.split(',')]
        else:
            # Single: "3"
            function_indices = [int(args.functions)]
    else:
        # Run all functions
        function_indices = range(num_functions)
    
    print(f"Will process {len(list(function_indices))} function(s)\n")
    
    # Track results
    successful = []
    failed = []
    
    # Iterate through functions
    for idx in function_indices:
        if idx >= num_functions:
            print(f"Warning: Function index {idx} >= {num_functions}. Skipping.")
            continue
            
        success = run_single_function(
            class_path=class_path,
            w_function_index=idx,
            output_base_path=output_base,
            generated_functions_file=generated_functions_file,
            resume=args.resume,
            test=args.test,
            force=args.force,
            debug=args.debug
        )
        
        if success:
            successful.append(idx)
        else:
            failed.append(idx)
    
   # Summary
    print(f"\n{'='*70}")
    print(f"SUMMARY")
    print(f"{'='*70}")
    print(f"Successful: {len(successful)}/{len(list(function_indices))}")
    if successful:
        print(f"  Functions: {successful}")
    if failed:
        print(f"Failed: {len(failed)}")
        print(f"  Functions: {failed}")
    print(f"{'='*70}\n")
    
    # Save summary file with unique name based on function range
    first_func = min(function_indices) if function_indices else 0
    last_func = max(function_indices) if function_indices else 0
    summary_file = os.path.join(output_base, f'run_summary_{first_func:03d}-{last_func:03d}.txt')
    os.makedirs(output_base, exist_ok=True)
    with open(summary_file, 'w') as f:
        f.write(f"VCDM Multi-Function Analysis Summary\n")
        f.write(f"{'='*70}\n\n")
        f.write(f"Function range: {first_func}-{last_func}\n")
        f.write(f"Total functions in system: {num_functions}\n")
        f.write(f"Processed in this run: {len(list(function_indices))}\n")
        f.write(f"Successful: {len(successful)}\n")
        f.write(f"Failed: {len(failed)}\n\n")
        f.write(f"Successful functions: {successful}\n")
        f.write(f"Failed functions: {failed}\n")
    
    print(f"Summary saved to: {summary_file}")


if __name__ == "__main__":
    main()
