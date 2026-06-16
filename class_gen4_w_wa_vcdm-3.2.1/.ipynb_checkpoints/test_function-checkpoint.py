#!/usr/bin/env python3
"""
Quick verification script for CLASS output with CPL parametrization
Compare your CLASS background.dat with expected CPL behavior

Usage: python3 verify_class_output.py <path_to_background.dat>
"""

import sys
import numpy as np
import matplotlib.pyplot as plt

def cpl_w(a, w0, wa):
    """CPL parametrization: w(a) = w0 + wa*(1-a)"""
    return w0 + wa * (1 - a)

def cpl_rho_ratio(a, w0, wa):
    """Analytical rho_lambda(a) / rho_lambda(1) for CPL"""
    integral = -3.0 * (1.0 + w0 + wa) * np.log(a) + 3.0 * wa * (a - 1.0)
    return np.exp(integral)

def main():
    # Parameters matching your test
    w0 = -0.68
    wa = -0.98
    
    if len(sys.argv) > 1:
        # User provided a background.dat file
        try:
            data = np.loadtxt(sys.argv[1], comments='#')
            print("Loaded CLASS output from:", sys.argv[1])
            print("Columns found:", data.shape[1])
            print("\nNote: You'll need to identify which columns are 'a', 'w', and 'rho_lambda'")
            print("Typical CLASS columns: z, a, H, H', rho_g, rho_b, rho_cdm, rho_lambda, ...")
        except Exception as e:
            print(f"Error loading file: {e}")
            print("Continuing with analytical predictions only...")
    
    # Generate expected values
    print("\n" + "="*70)
    print("EXPECTED VALUES FOR CPL MODEL")
    print("Parameters: w0 = {:.2f}, wa = {:.2f}".format(w0, wa))
    print("="*70)
    
    # Create table
    redshifts = [0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 5.0]
    
    print("\n{:>8s} {:>8s} {:>12s} {:>12s}".format("z", "a", "w(a)", "rho/rho_0"))
    print("-" * 45)
    
    for z in redshifts:
        a = 1.0 / (1.0 + z)
        w = cpl_w(a, w0, wa)
        rho_ratio = cpl_rho_ratio(a, w0, wa)
        print("{:8.2f} {:8.4f} {:12.6f} {:12.6f}".format(z, a, w, rho_ratio))
    
    print("\n" + "="*70)
    print("KEY EXPECTATIONS:")
    print("="*70)
    print("1. w(a) should become MORE NEGATIVE as z increases (a decreases)")
    print("   - Today (z=0, a=1.0): w = {:.3f}".format(cpl_w(1.0, w0, wa)))
    print("   - Past (z=1, a=0.5): w = {:.3f}".format(cpl_w(0.5, w0, wa)))
    print("   - Early (z=3, a=0.25): w = {:.3f}".format(cpl_w(0.25, w0, wa)))
    
    print("\n2. Dark energy density INCREASES going to past (for wa < 0, w0 > -1)")
    print("   - rho_lambda(a=0.5) / rho_lambda(a=1.0) = {:.3f}".format(
        cpl_rho_ratio(0.5, w0, wa)))
    
    print("\n3. w(a) crosses phantom divide (w = -1)?")
    # Find where w = -1
    a_phantom = wa / (w0 + wa + 1.0) if abs(w0 + wa + 1.0) > 1e-10 else None
    if a_phantom and 0 < a_phantom < 1:
        z_phantom = 1.0/a_phantom - 1.0
        print("   Yes! At a = {:.3f} (z = {:.2f})".format(a_phantom, z_phantom))
        print("   w < -1 for a < {:.3f} (phantom regime)".format(a_phantom))
        print("   w > -1 for a > {:.3f} (quintessence regime)".format(a_phantom))
    else:
        print("   No, this model stays {} -1".format("above" if w0 > -1 else "below"))
    
    print("\n" + "="*70)
    print("VERIFICATION CHECKLIST:")
    print("="*70)
    print("□ Run CLASS and check stderr for: DEBUG: w_function_index=0, c0_esr=-0.680000, c1_esr=-0.980000")
    print("□ Open background.dat and find columns for a, w, and rho_lambda")
    print("□ Verify w(a=1.0) ≈ {:.3f}".format(w0))
    print("□ Verify w(a=0.5) ≈ {:.3f}".format(cpl_w(0.5, w0, wa)))
    print("□ Check that rho_lambda evolves as shown above")
    print("□ Ensure H(z) is smooth with no discontinuities")
    print("□ Compare with CLASS built-in CPL if available")
    
    print("\n" + "="*70)
    print("COMMON ISSUES:")
    print("="*70)
    print("- If w(a) is constant: Check that c1_esr (wa) is being read correctly")
    print("- If w(a) has wrong sign: Check derivative implementation")
    print("- If rho grows exponentially: Check integration limits (should be 1.0 to a)")
    print("- If CLASS crashes: Check w_function_index is in valid range [0, {}]".format(0))
    
    # Create a simple plot
    print("\n" + "="*70)
    print("GENERATING PLOTS...")
    print("="*70)
    
    # Generate smooth curves
    a_vals = np.linspace(0.1, 1.0, 100)
    z_vals = 1.0/a_vals - 1.0
    w_vals = cpl_w(a_vals, w0, wa)
    rho_vals = cpl_rho_ratio(a_vals, w0, wa)
    
    # Create figure with 2 subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    
    # Plot 1: w(a) vs a
    ax1.plot(a_vals, w_vals, 'b-', linewidth=2, label='CPL: w(a) = w0 + wa(1-a)')
    ax1.axhline(-1, color='red', linestyle='--', alpha=0.5, label='w = -1 (ΛCDM)')
    ax1.axvline(1.0, color='gray', linestyle=':', alpha=0.5)
    ax1.set_xlabel('Scale factor a', fontsize=12)
    ax1.set_ylabel('w(a)', fontsize=12)
    ax1.set_title('Expected Equation of State Evolution', fontsize=14, fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.text(0.5, -0.9, 'Today', ha='right', va='bottom', fontsize=10, color='gray')
    
    # Plot 2: rho_lambda ratio vs z
    ax2.plot(z_vals, rho_vals, 'g-', linewidth=2, label='ρ_Λ(z) / ρ_Λ(0)')
    ax2.axhline(1.0, color='gray', linestyle=':', alpha=0.5)
    ax2.axvline(0.0, color='gray', linestyle=':', alpha=0.5)
    ax2.set_xlabel('Redshift z', fontsize=12)
    ax2.set_ylabel('ρ_Λ(z) / ρ_Λ(0)', fontsize=12)
    ax2.set_title('Expected Dark Energy Density Evolution', fontsize=14, fontweight='bold')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim([0, 5])
    
    plt.tight_layout()
    plt.savefig('/mnt/user-data/outputs/expected_cpl_behavior.png', dpi=150, bbox_inches='tight')
    print("✓ Saved plot to: expected_cpl_behavior.png")
    
    print("\n" + "="*70)
    print("NEXT STEPS:")
    print("="*70)
    print("1. Run CLASS with your parameters")
    print("2. Check that background.dat columns match the expected values above")
    print("3. Plot your CLASS output and compare with expected_cpl_behavior.png")
    print("4. If values match within ~0.01%, your integration is working correctly!")
    print("="*70)

if __name__ == "__main__":
    main()