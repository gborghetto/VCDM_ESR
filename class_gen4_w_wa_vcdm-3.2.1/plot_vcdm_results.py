#!/usr/bin/env python3
"""
Analyze and plot VCDM function results from minimization chains.

This script:
1. Scans the chains directory for successful functions (those with .minimum.txt files)
2. Extracts best-fit parameters (c0_esr, c1_esr) and chi-squared values
3. Reads analytical expressions from generated_functions.c
4. Evaluates w(z) for each function using the analytical expression
5. Plots w(z) for each successful function with chi-squared in the legend
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['text.usetex'] = True
matplotlib.rcParams['font.family'] = 'serif'
import os
import re
from pathlib import Path
import pandas as pd

def expr_to_latex(expr):
    """
    Convert a raw expression string from generated_functions.c to a LaTeX string.
    Handles: x→a, a0/a1→parameter names, Python operators→LaTeX, functions→LaTeX.
    """
    import re

    s = expr.strip()

    # Replace x (scale factor) with a
    s = re.sub(r'\bx\b', 'a', s)

    # Replace parameter names
    s = re.sub(r'\ba0\b', 'w_0', s)
    s = re.sub(r'\ba1\b', 'w_a', s)

    # Replace Python power operator ** with LaTeX ^{...}
    def replace_power(m):
        base = m.group(1)
        exp  = m.group(2)
        if any(c in base for c in ('+', '-', '*', '/', '(')):
            base = r'\left(' + base + r'\right)'
        return f'{base}^{{{exp}}}'

    s = re.sub(r'(\w+(?:\.\w+)?)\*\*(-?[\d.]+(?:/[\d.]+)?)', replace_power, s)
    s = re.sub(r'\*\*', '^', s)

    # Replace sqrt(expr) → \sqrt{expr}
    s = re.sub(r'sqrt\(([^)]+)\)', lambda m: r'\sqrt{' + m.group(1) + r'}', s)

    # Replace exp(expr) → e^{expr}
    s = re.sub(r'exp\(([^)]+)\)', lambda m: r'e^{' + m.group(1) + r'}', s)

    # Replace log(expr) → \ln(expr)
    s = re.sub(r'\blog\b\(', r'\\ln(', s)

    # Replace Abs(expr) or abs(expr) → \left|expr\right|
    s = re.sub(r'[Aa]bs\(([^)]+)\)', lambda m: r'\left|' + m.group(1) + r'\right|', s)

    # Replace * → \, (implicit multiplication)
    s = s.replace('*', r'\,')

    # Replace a/b → \frac{a}{b}
    s = re.sub(r'([a-zA-Z0-9_{}\\ ]+)\s*/\s*([a-zA-Z0-9_{}\\ ]+)',
               lambda m: r'\frac{' + m.group(1).strip() + r'}{' + m.group(2).strip() + r'}', s)

    return s


def load_minimum_file(min_file_path):
    """
    Load a .minimum.txt file (space-separated with header).
    
    Format:
    #  weight  minuslogpost  omega_b  omega_cdm  ...
       1       510.51998     0.0225   0.1177     ...
    """
    try:
        # Read with pandas
        # Read the file, treating # as comment for header, but keep the header
        with open(min_file_path, 'r') as f:
            header_line = f.readline().strip()
            # Remove leading # and split
            column_names = header_line.replace('#', '').strip().split()
        
        # Read data (single row)
        df = pd.read_csv(min_file_path, sep=r'\s+', comment='#', header=None, engine='python')
        df.columns = column_names
        
        # Convert to dict (first row only)
        min_data = df.iloc[0].to_dict()
        
        return min_data
        
    except Exception as e:
        print(f"Error loading {min_file_path}: {e}")
        import traceback
        traceback.print_exc()
        return None

def get_function_expression(generated_functions_file, function_index):
    """
    Extract the mathematical expression for a function from generated_functions.c
    
    Looks for comments like:
    // Expression N (original line M): <expression>
    
    Returns the expression string, e.g., "a0 + a1*(1-x)"
    """
    if generated_functions_file is None:
        return None
    
    try:
        with open(generated_functions_file, 'r') as f:
            content = f.read()
        
        # Look for the comment that contains the original expression
        # Format: "// Expression N (original line M): <expression>"
        pattern = rf'// Expression {function_index}[^\n]*:\s*(.+?)$'
        match = re.search(pattern, content, re.MULTILINE)
        
        if match:
            expr = match.group(1).strip()
            print(f"  Found expression: {expr}")
            return expr
        else:
            print(f"  Warning: No expression comment found for function {function_index}")
            # Try to extract from function body as fallback
            pattern = rf'double func_{function_index}\s*\([^)]+\)\s*\{{[^{{]*return\s+([^;]+);'
            match = re.search(pattern, content, re.DOTALL)
            if match:
                expr = match.group(1).strip()
                # Clean up
                expr = expr.replace('(void)a0;', '').replace('(void)a1;', '').strip()
                print(f"  Extracted from function body: {expr}")
                return expr
            
            return None
        
    except Exception as e:
        print(f"Warning: Could not read function expression: {e}")
        return None

def evaluate_w_from_expression(func_expr, c0, c1, z_array):
    """
    Evaluate w(z) from the analytical expression.
    
    The expression uses:
    - x = a = 1/(1+z)  (scale factor)
    - a0 = c0_esr (first parameter)
    - a1 = c1_esr (second parameter)
    
    Example expressions:
    - "a0 + a1*(1-x)" → CPL
    - "a0*x + a1*x**2" → polynomial in a
    - "a0*exp(a1*x)" → exponential
    """
    
    # if func_expr is None:
    #     print("  No expression available, using CPL as fallback")
    #     # Fallback to CPL
    #     a = 1.0 / (1.0 + z_array)
    #     return c0 + c1 * (1 - a)
    
    # Convert z to a (scale factor)
    a = 1.0 / (1.0 + z_array)
    
    # IMPORTANT: Replace parameter names CAREFULLY to avoid breaking function names
    # Use word boundaries or more specific patterns
    import re
    
    # Replace a0 and a1 with actual values using word boundaries
    expr = re.sub(r'\ba0\b', f'({c0})', func_expr)
    expr = re.sub(r'\ba1\b', f'({c1})', expr)
    
    # Replace x with a
    expr = re.sub(r'\bx\b', 'a', expr)
    
    # Fix capitalization issues (Abs → abs)
    expr = expr.replace('Abs', 'abs')
    
    print(f"  Evaluating: {expr}")
    
    try:
        # Create safe namespace with only numpy functions
        safe_dict = {
            "__builtins__": {},
            "a": a,
            "np": np,
            "exp": np.exp,
            "log": np.log,
            "sqrt": np.sqrt,
            "sin": np.sin,
            "cos": np.cos,
            "tan": np.tan,
            "abs": np.abs,
            "pow": np.power,
        }
        
        # Evaluate the expression
        w = eval(expr, safe_dict)
        
        return w
        
    except Exception as e:
        print(f"  ERROR evaluating expression '{expr}': {e}")
        #print(f"  Falling back to CPL with c0={c0}, c1={c1}")
        # Return CPL as fallback
        return None #c0 + c1 * (1 - a)

def scan_chains_directory(chains_dir):
    """
    Scan chains directory and return list of successful function indices.
    
    Returns:
    --------
    list of tuples: (function_index, minimum_file_path)
    """
    successful_functions = []
    
    # Look for directories named with 3-digit numbers (000, 001, etc.)
    for item in sorted(os.listdir(chains_dir)):
        item_path = os.path.join(chains_dir, item)
        
        # Check if it's a directory and matches pattern
        if os.path.isdir(item_path) and re.match(r'^\d{3}$', item):
            function_idx = int(item)
            
            # Look for .minimum.txt file
            minimum_file = os.path.join(item_path, f"{item}.minimum.txt")
            
            if os.path.exists(minimum_file):
                successful_functions.append((function_idx, minimum_file))
            else:
                print(f"Skipping function {function_idx}: no .minimum.txt file")
    
    return successful_functions

def plot_w_functions(chains_dir, class_path, generated_functions_file=None, 
                    cpl_bounds_file=None, cpl_minimum_file=None, lcdm_minimum_file=None,
                    output_file='w_functions_comparison.pdf', function_indices=None):
    """
    Main plotting function: scan directory, load results, and plot w(z) curves + H(z).
    """
    
    print(f"\n{'='*70}")
    print(f"Analyzing VCDM Function Results")
    print(f"{'='*70}")
    print(f"Chains directory: {chains_dir}")
    print(f"CLASS path: {class_path}")
    if generated_functions_file:
        print(f"Functions file: {generated_functions_file}")
    if cpl_bounds_file:
        print(f"CPL bounds file: {cpl_bounds_file}")
    if cpl_minimum_file:
        print(f"CPL minimum file: {cpl_minimum_file}")
    if lcdm_minimum_file:
        print(f"ΛCDM minimum file: {lcdm_minimum_file}")
    print(f"{'='*70}\n")
    
    # Import classy
    import sys
    sys.path.insert(0, os.path.join(class_path, 'python/build'))
    from classy import Class
    
    # Scan for successful functions
    successful_functions = scan_chains_directory(chains_dir)
    
    if not successful_functions:
        print("No successful functions found!")
        return
    
    print(f"Found {len(successful_functions)} successful function(s) in chains directory")

    # Filter to requested indices if specified
    if function_indices is not None:
        successful_functions = [(idx, f) for idx, f in successful_functions if idx in function_indices]
        missing = set(function_indices) - {idx for idx, _ in successful_functions}
        if missing:
            print(f"Warning: requested functions not found or incomplete: {sorted(missing)}")

    if not successful_functions:
        print("No functions to plot after filtering!")
        return

    print(f"Plotting {len(successful_functions)} function(s)\n")
    
    # Create figure with 2 subplots (w(z) on top, H(z) on bottom)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 12))
    
    # Redshift range
    z = np.linspace(0, 3, 100)
    
    # Track statistics
    best_chi2 = float('inf')
    best_func = None
    all_chi2 = []
    plotted_count = 0
    
    # Colors for different functions
    colors = plt.cm.tab20(np.linspace(0, 1, len(successful_functions)))
    
    # =========================================================================
    # Load ΛCDM for H(z) normalization
    # =========================================================================
    H_lcdm = None
    if lcdm_minimum_file and os.path.exists(lcdm_minimum_file):
        print(f"Loading ΛCDM for normalization from {lcdm_minimum_file}")
        try:
            lcdm_data = load_minimum_file(lcdm_minimum_file)
            
            if lcdm_data is not None:
                M_lcdm = Class()
                
                omega_cdm = lcdm_data.get('omega_cdm', lcdm_data.get('omch2', 0.12))
                omega_b = lcdm_data.get('omega_b', lcdm_data.get('ombh2', 0.022))
                H0 = lcdm_data.get('H0', 67.0)
                
                M_lcdm.set({
                    # 'output': 'tCl,lCl,mPk',
                    # 'lensing': 'yes',
                    'Omega_cdm': omega_cdm / (H0/100)**2,
                    'Omega_b': omega_b / (H0/100)**2,
                    'h': H0 / 100,
                    'A_s': lcdm_data.get('A_s', 2.1e-9),
                    'n_s': lcdm_data.get('n_s', 0.96),
                    'tau_reio': lcdm_data.get('tau_reio', 0.055),
                    # 'N_ncdm': 1,
                    # 'm_ncdm': 0.06,
                    # 'N_ur': 2.0308,
                    # 'T_ncdm': 0.71611,
                    # 'l_max_scalars': 2400,
                })
                M_lcdm.compute()
                
                # Get H(z) - pass redshift z directly
                H_lcdm = np.array([M_lcdm.Hubble(zi) * 299792.458 for zi in z])
                
                M_lcdm.struct_cleanup()
                M_lcdm.empty()
                
                print(f"✓ Loaded ΛCDM H(z)")
        except Exception as e:
            print(f"Warning: Could not compute ΛCDM H(z): {e}")
            import traceback
            traceback.print_exc()
    
    # =========================================================================
    # Plot CPL uncertainty bands
    # =========================================================================
    if cpl_bounds_file and os.path.exists(cpl_bounds_file):
        print(f"Loading CPL uncertainty bands from {cpl_bounds_file}")
        try:
            cpl_df = pd.read_csv(cpl_bounds_file)
            z_cpl = cpl_df['z'].values
            w_lower = cpl_df['w_de_lower_95'].values
            w_upper = cpl_df['w_de_upper_95'].values
            
            ax1.fill_between(z_cpl, w_lower, w_upper, 
                           alpha=0.1, color='blue', 
                           label=r'CPL 95\% CI', zorder=1)
            
            # H(z) bounds if available
            # Around line 329 - H(z) bounds
            if 'hubble_lower_95' in cpl_df.columns and H_lcdm is not None:
                print(f"DEBUG: Attempting to plot H(z) uncertainty bands")
                
                # These are H(z)/H0_cpl from the CSV
                h_lower = cpl_df['hubble_lower_95'].values  
                h_upper = cpl_df['hubble_upper_95'].values
                
                # We need H0_cpl to convert to absolute H(z)
                # Get it from the CPL minimum file (should already be loaded)
                if cpl_minimum_file and os.path.exists(cpl_minimum_file):
                    cpl_data_temp = load_minimum_file(cpl_minimum_file)
                    if cpl_data_temp:
                        H0_cpl = cpl_data_temp.get('H0', 67.0)
                        print(f"  Using H0_cpl = {H0_cpl:.2f}")
                        
                        # Convert H(z)/H0_cpl to absolute H(z) in km/s/Mpc
                        h_lower_abs = h_lower * H0_cpl
                        h_upper_abs = h_upper * H0_cpl
                        
                        # Interpolate LCDM to CPL z grid
                        H_lcdm_interp = np.interp(z_cpl, z, H_lcdm)
                        
                        print(f"  h_lower_abs range: [{h_lower_abs.min():.2f}, {h_lower_abs.max():.2f}]")
                        print(f"  h_upper_abs range: [{h_upper_abs.min():.2f}, {h_upper_abs.max():.2f}]")
                        print(f"  H_lcdm_interp range: [{H_lcdm_interp.min():.2f}, {H_lcdm_interp.max():.2f}]")
                        print(f"  Ratio range: [{(h_lower_abs/H_lcdm_interp).min():.3f}, {(h_upper_abs/H_lcdm_interp).max():.3f}]")
                        
                        ax2.fill_between(z_cpl, h_lower_abs/H_lcdm_interp, h_upper_abs/H_lcdm_interp,
                                    alpha=0.1, color='blue', 
                                    label=r'CPL 95\% CI', zorder=1)
                        print(f"✓ Plotted CPL H(z) uncertainty bands")
            
            print(f"✓ Loaded CPL bounds")
            
        except Exception as e:
            print(f"Warning: Could not load CPL bounds: {e}")
    
    # =========================================================================
    # Plot CPL best-fit
    # =========================================================================
    if cpl_minimum_file and os.path.exists(cpl_minimum_file):
        print(f"Loading CPL best-fit from {cpl_minimum_file}")
        try:
            cpl_data = load_minimum_file(cpl_minimum_file)
            
            if cpl_data is not None:
                w0_cpl = cpl_data.get('c0_esr', -1.0)
                wa_cpl = cpl_data.get('c1_esr', 0.0)
                
                # Calculate CPL w(z)
                w_cpl = w0_cpl + wa_cpl * z / (1 + z)
                
                # ax1.plot(z, w_cpl, color='black', linestyle=':', linewidth=2.5, 
                #        label=f'CPL (w0={w0_cpl:.3f}, wa={wa_cpl:.3f})', 
                #        zorder=2)
                
                # Compute CPL H(z)
                try:
                    M_cpl = Class()
                    
                    omega_cdm = cpl_data.get('omega_cdm', cpl_data.get('omch2', 0.12))
                    omega_b = cpl_data.get('omega_b', cpl_data.get('ombh2', 0.022))
                    H0 = cpl_data.get('H0', 67.0)
                    
                    M_cpl.set({
                        # 'output': 'tCl,lCl,mPk',
                        # 'lensing': 'yes',
                        'Omega_cdm': omega_cdm / (H0/100)**2,
                        'Omega_b': omega_b / (H0/100)**2,
                        'h': H0 / 100,
                        'A_s': cpl_data.get('A_s', 2.1e-9),
                        'n_s': cpl_data.get('n_s', 0.96),
                        'tau_reio': cpl_data.get('tau_reio', 0.055),
                        'w_function_index': 0,
                        'c0_esr': w0_cpl,
                        'c1_esr': wa_cpl,
                        # 'N_ncdm': 1,
                        # 'm_ncdm': 0.06,
                        # 'N_ur': 2.0308,
                        # 'T_ncdm': 0.71611,
                        # 'l_max_scalars': 2400,
                    })
                    M_cpl.compute()
                    
                    H_cpl = np.array([M_cpl.Hubble(zi) * 299792.458 for zi in z])
                    
                    # if H_lcdm is not None:
                    #     ax2.plot(z, H_cpl/H_lcdm, color='black', linestyle=':', 
                    #             linewidth=2.5, label='CPL', zorder=200)
                    
                    M_cpl.struct_cleanup()
                    M_cpl.empty()
                    
                except Exception as e:
                    print(f"  Warning: Could not compute CPL H(z): {e}")
                
                print(f"✓ Loaded CPL best-fit")
            
        except Exception as e:
            print(f"Warning: Could not load CPL minimum file: {e}")
    
    # =========================================================================
    # Plot each VCDM function
    # =========================================================================
    for i, (func_idx, min_file) in enumerate(successful_functions):
        # Skip specific functions
        functions_to_exclude = []  # Add function numbers you want to skip
        if func_idx in functions_to_exclude:
            print(f"Skipping function {func_idx} (excluded by user)")
            continue
        print(f"\n{'='*70}")
        print(f"Processing Function {func_idx}")
        print(f"{'='*70}")
        
        min_data = load_minimum_file(min_file)
        
        if min_data is None:
            print(f"✗ Could not load function {func_idx}")
            continue
        
        c0 = min_data.get('c0_esr', 0.0)
        c1 = min_data.get('c1_esr', 0.0)
        chi2_total = min_data.get('chi2_total', None)
        
        if chi2_total is None:
            print(f"✗ Function {func_idx} has no chi2_total")
            continue
        
        func_expr = get_function_expression(generated_functions_file, func_idx)
        
        print(f"Parameters:")
        print(f"  c0_esr = {c0:.6f}")
        print(f"  c1_esr = {c1:.6f}")
        print(f"  χ² = {chi2_total:.2f}")
        
        all_chi2.append(chi2_total)
        if chi2_total < best_chi2:
            best_chi2 = chi2_total
            best_func = func_idx
        
        # Evaluate w(z)
        w_z = evaluate_w_from_expression(func_expr, c0, c1, z)
        
        print(f"  w(z=0) = {w_z[0]:.6f}")
        print(f"  w(z=1) = {w_z[50]:.6f}")
        print(f"  w(z=3) = {w_z[-1]:.6f}")
        
        # Compute H(z) using CLASS
        H_z = None
        try:
            M = Class()
            
            omega_cdm = min_data.get('omega_cdm', min_data.get('omch2', 0.12))
            omega_b = min_data.get('omega_b', min_data.get('ombh2', 0.022))
            H0 = min_data.get('H0', 67.0)
            
            M.set({
                # 'output': 'tCl,lCl,mPk',
                # 'lensing': 'yes',
                'Omega_cdm': omega_cdm / (H0/100)**2,
                'Omega_b': omega_b / (H0/100)**2,
                'h': H0 / 100,
                'A_s': min_data.get('A_s', 2.1e-9),
                'n_s': min_data.get('n_s', 0.96),
                'tau_reio': min_data.get('tau_reio', 0.055),
                'w_function_index': func_idx,
                'c0_esr': c0,
                'c1_esr': c1,
                # 'N_ncdm': 1,
                # 'm_ncdm': 0.06,
                # 'N_ur': 2.0308,
                # 'T_ncdm': 0.71611,
                # 'l_max_scalars': 2400,
                # 'a_ini_over_a_today_default': 1e-21,
            })
            M.compute()
            
            # Get H(z) - pass redshift z directly
            H_z = np.array([M.Hubble(zi) * 299792.458 for zi in z])
            
            print(f"  H(z=0) = {H_z[0]:.2f} km/s/Mpc")
            
            M.struct_cleanup()
            M.empty()
            
        except Exception as e:
            print(f"  Warning: Could not compute H(z): {e}")
        
        # Map standard parametrizations to their names
        named_parametrizations = {0: 'CPL', 1: 'BA', 2: 'JBP', 3: 'EXP', 4: 'LOG'}
        func_prefix = named_parametrizations.get(func_idx, f'F{func_idx}')

        # Manual w_0 best-fit values for specific functions (add values here)
        # w_0 = c_0 * exp(-1) for F83, w_0 = c_0 for F42
        manual_w0 = {
            42: -0.792,   # SR: w_0 = c_0 (best fit CMB+BAO+SN)
            83: -0.702,   # F83: w_0 = c_0 * exp(-1) (best fit CMB+BAO+SN)
        }

        # Custom expressions for specific functions
        custom_expressions = {
            83: r'w_0 e^{-a}',
        }

        # Create label with LaTeX expression
        if func_expr:
            if func_idx in custom_expressions:
                func_expr_latex = custom_expressions[func_idx]
            else:
                func_expr_latex = expr_to_latex(func_expr)
                if func_idx in named_parametrizations:
                    func_expr_latex = func_expr_latex.replace('w_0', 'w_0').replace('w_1', 'w_a')
            if len(func_expr_latex) > 40:
                func_expr_latex = func_expr_latex[:37] + r'\ldots'
            if func_idx in manual_w0:
                label = rf"{func_prefix}: $w={func_expr_latex}$, $\chi^2={chi2_total:.1f}$"
            else:
                label = rf"{func_prefix}: $w={func_expr_latex}$, $\chi^2={chi2_total:.1f}$"
        else:
            if func_idx in manual_w0:
                label = rf"{func_prefix}: $w_0={manual_w0[func_idx]:.3f}$, $\chi^2={chi2_total:.1f}$"
            else:
                label = rf"{func_prefix}: $w_0={c0:.3f}$, $w_1={c1:.3f}$, $\chi^2={chi2_total:.1f}$"
        
        # Plot w(z)
        ax1.plot(z, w_z, color=colors[i], linewidth=2.5, label=label, 
               alpha=0.8, zorder=3)
        
        # Plot H(z)/H_LCDM
        if H_z is not None and H_lcdm is not None:
            ax2.plot(z, H_z/H_lcdm, color=colors[i], linewidth=2.5, 
                   label=label, alpha=0.8, zorder=3)
        
        plotted_count += 1
        print(f"✓ Successfully plotted function {func_idx}")
    
    # =========================================================================
    # Add reference lines and formatting
    # =========================================================================
    
    # ΛCDM reference lines
    ax1.axhline(y=-1, color='black', linestyle='--', linewidth=2, 
               label=r'$\Lambda$CDM: $\chi^2=1053.2$', alpha=0.5, zorder=0)
    ax2.axhline(y=1, color='black', linestyle='--', linewidth=2, 
               label=r'$\Lambda$CDM', alpha=0.5, zorder=0)
    
    # w(z) plot formatting
    ax1.set_xlabel(r'$z$', fontsize=24)
    ax1.set_ylabel(r'$w(z)$', fontsize=24)
    ax1.tick_params(axis='both', which='major', labelsize=18)
    #ax1.set_title(f'Dark Energy Equation of State: {plotted_count} VCDM Functions', 
    #             fontsize=16, fontweight='bold')
   
    #ax1.grid(True, alpha=0.3)
    #ax1.set_title('CMB+BAO+SN', fontsize=16)
    ax1.set_xlim(0, 2.4)
    ax1.set_ylim(-2, -0.3)
    # ax1.legend(bbox_to_anchor=(1.05, 1), loc='center left', fontsize=14, 
    #           framealpha=0.9, edgecolor='black')
    
    # H(z) plot formatting
    ax2.set_xlabel(r'$z$', fontsize=24)
    ax2.tick_params(axis='both', which='major', labelsize=18)
    ax2.set_ylabel(r'$h(z)/h_{\Lambda\mathrm{CDM}}(z)$', fontsize=20)
    #ax2.set_title('Hubble Parameter Evolution', fontsize=16, fontweight='bold')
    #ax2.grid(True, alpha=0.3)
    ax2.set_xlim(0, 2.4)
    ax2.set_ylim(0.92, 1.05)
    # ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=14, 
    #           framealpha=0.9, edgecolor='black')
    
    # Best function annotation
    # if best_func is not None:
    #     ax1.text(0.02, 0.02, f'Best fit: Function {best_func}',#\nχ²={best_chi2:.1f}',
    #             transform=ax1.transAxes, fontsize=12, verticalalignment='bottom',)
    #             #bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    handles, labels = ax1.get_legend_handles_labels()

    fig.legend(handles, labels,
           loc='center left',
           bbox_to_anchor=(1.0, 0.5),  # x=left edge, y=vertical center of figure
           fontsize=20,
           framealpha=0.9,
           edgecolor='black')
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"\n{'='*70}")
    print(f"✓ Plot saved to: {output_file}")
    print(f"{'='*70}\n")
    
    # Summary statistics
    if all_chi2:
        print("\nSummary Statistics:")
        print(f"  Total successful functions: {len(successful_functions)}")
        print(f"  Successfully plotted: {plotted_count}")
        print(f"  Best function: {best_func} (χ² = {best_chi2:.2f})")
        print(f"  Mean χ²: {np.mean(all_chi2):.2f}")
        print(f"  Median χ²: {np.median(all_chi2):.2f}")
        print(f"  χ² range: [{np.min(all_chi2):.2f}, {np.max(all_chi2):.2f}]")
    
    
    #plt.show()

def create_comparison_table(chains_dir, generated_functions_file=None, output_csv='vcdm_results_table.csv'):
    """
    Create a CSV table with all results for easy analysis.
    """
    
    print(f"\n{'='*70}")
    print(f"Creating results table...")
    print(f"{'='*70}\n")
    
    # Scan for successful functions
    successful_functions = scan_chains_directory(chains_dir)
    
    if not successful_functions:
        print("No successful functions found!")
        return
    
    # Collect data
    results_list = []
    
    for func_idx, min_file in successful_functions:
        # Load minimum file
        min_data = load_minimum_file(min_file)
        
        if min_data is None:
            continue
        
        # Get function expression
        func_expr = get_function_expression(generated_functions_file, func_idx)
        
        # Extract key parameters
        result_dict = {
            'function_idx': func_idx,
            'expression': func_expr if func_expr else 'Unknown',
            'c0_esr': min_data.get('c0_esr', 0.0),
            'c1_esr': min_data.get('c1_esr', 0.0),
            'omega_b': min_data.get('omega_b', np.nan),
            'omega_cdm': min_data.get('omega_cdm', np.nan),
            'H0': min_data.get('H0', np.nan),
            'chi2_total': min_data.get('chi2_total', np.nan),
            'chi2_CMB': min_data.get('chi2__CMB', np.nan),
            'chi2_BAO': min_data.get('chi2__BAO', np.nan),
            'chi2_SN': min_data.get('chi2__SN', np.nan),
        }
        
        results_list.append(result_dict)
    
    # Create DataFrame
    df = pd.DataFrame(results_list)
    
    # Sort by chi2_total
    df = df.sort_values('chi2_total')
    
    # Save to CSV
    df.to_csv(output_csv, index=False, float_format='%.6f')
    
    print(f"✓ Results table saved to: {output_csv}")
    print(f"\nTop 10 functions by χ²:")
    print(df.head(10).to_string(index=False))

def main():
    """
    Main execution
    """
    import argparse
    
    parser = argparse.ArgumentParser(description="Analyze and plot VCDM function results")
    parser.add_argument(
        "--chains_dir", type=str,
        default="chains_SN",
        help="Path to chains directory"
    )
    parser.add_argument(
        "--functions_file", type=str,
        default='source/generated_functions.c',
        help="Path to generated_functions.c"
    )
    parser.add_argument(
        "--cpl_bounds", type=str,
        default='/Users/giuliaborghetto/OneDriveSwanseaUniversity/VCDM/class_gen4_w_wa_vcdm-3.2.1/cpl_w_hubble_bounds_PlanckDESIUnion.csv', #'/Users/giuliaborghetto/OneDriveSwanseaUniversity/Swansea/Project_Fernando/VExpansion/VExpansion_chains_local/cpl_w_hubble_bounds_Plancklite.csv',
        help="Path to CPL uncertainty bounds CSV file"
    )
    parser.add_argument(
        "--cpl_minimum", type=str,
        default=  '/Users/giuliaborghetto/OneDriveSwanseaUniversity/VCDM/class_gen4_w_wa_vcdm-3.2.1/chains_CPL_SN/chains_CPL.minimum.txt', #"/Users/giuliaborghetto/OneDriveSwanseaUniversity/Swansea/Project_Fernando/chains_CPL_Planck/CPL.minimum.txt", 
        help="Path to CPL .minimum.txt file for best-fit CPL"
    )
    parser.add_argument(
        "--output", type=str,
        default="best_w.pdf",
        help="Output plot filename"
    )

    parser.add_argument(
        "--class_path", type=str,
        default= '/Users/giuliaborghetto/OneDriveSwanseaUniversity/VCDM/class_gen4_w_wa_vcdm-3.2.1',
        help="Path to CLASS installation"
    )
    parser.add_argument(
        "--lcdm_minimum", type=str,
        default='/Users/giuliaborghetto/OneDriveSwanseaUniversity/VCDM/class_gen4_w_wa_vcdm-3.2.1/chains_LCDM/chains_LCDM.minimum.txt',
        help="Path to ΛCDM .minimum.txt file for H(z) normalization"
    )
    parser.add_argument(
        "--table", type=str,
        default="vcdm_results_table.csv",
        help="Output CSV table filename"
    )
    parser.add_argument(
        "--create_table", action="store_true",
        help="Also create a CSV table of results"
    )
    parser.add_argument(
        "--functions", type=str, default=None,
        help="Subset of function indices to plot, e.g. \'0-5\' or \'0,2,4\'. "
             "Ranges and comma lists can be mixed: \'1-3,7,10-12\'. "
             "If omitted, all successful functions are plotted."
    )

    args = parser.parse_args()

    # Parse --functions into a set of ints (or None = plot all)
    function_indices = None
    if args.functions:
        indices = []
        for part in args.functions.split(','):
            part = part.strip()
            if '-' in part:
                start, end = map(int, part.split('-'))
                indices.extend(range(start, end + 1))
            else:
                indices.append(int(part))
        function_indices = set(indices)

    # Check if paths exist
    if not os.path.exists(args.chains_dir):
        print(f"Error: Chains directory not found: {args.chains_dir}")
        return

    if args.functions_file and not os.path.exists(args.functions_file):
        print(f"Warning: Functions file not found: {args.functions_file}")
        print("  Will use generic labels and CPL fallback")
        args.functions_file = None

    # Plot results
    plot_w_functions(args.chains_dir, args.class_path, args.functions_file,
                    args.cpl_bounds, args.cpl_minimum, args.lcdm_minimum, args.output,
                    function_indices=function_indices)

    # Create table if requested
    if args.create_table:
        create_comparison_table(args.chains_dir, args.functions_file, args.table)
if __name__ == "__main__":
    main()