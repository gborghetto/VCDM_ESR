import sympy
from sympy.printing.c import C99CodePrinter
# --- NEW IMPORTS ---
# We need a more powerful parser that can handle implicit multiplication
from sympy.parsing.sympy_parser import (
    parse_expr, 
    standard_transformations, 
    implicit_multiplication_application,
    implicit_multiplication
)

# --- Configuration ---
INPUT_FILE = 'expressions.txt'
H_FILE = 'generated_functions.h'
C_FILE = 'generated_functions.c'
# Fixed function pointer typedef syntax
TYPEDEF_NAME = "eos_function"
TYPEDEF_DERIV_NAME = "eos_function_deriv"
TABLE_NAME = "function_table"
DERIV_TABLE_NAME = "derivative_table"
COUNT_NAME = "function_count"
# ---------------------

# Define the symbols that are present in the expressions
x, a0, a1 = sympy.symbols('x a0 a1', real=True)
# Create a local dictionary for the parser
local_symbols = {'x': x, 'a0': a0, 'a1': a1}

# --- SETUP TRANSFORMATIONS ---
# This tells parse_expr to handle things like "2x" as "2*x" AND "a0x" as "a0*x"
all_transformations = standard_transformations + (
    implicit_multiplication_application, 
    implicit_multiplication # <--- ADDED THIS TRANSFORMATION
)

# Use SymPy's C code printer
# It correctly handles 'Abs' -> 'fabs', 'pow' -> 'pow', 'x**y' -> 'pow(x, y)'
printer = C99CodePrinter()

function_names = []
derivative_names = []
original_indices = []  # Track original line numbers for reference
skipped_functions = []  # Track which functions were skipped

try:
    with open(INPUT_FILE, 'r') as f_in, \
         open(H_FILE, 'w') as f_h, \
         open(C_FILE, 'w') as f_c:

        print(f"Reading from {INPUT_FILE}...")
        
        # --- Write Header File (.h) ---
        f_h.write("#ifndef GENERATED_FUNCTIONS_H\n")
        f_h.write("#define GENERATED_FUNCTIONS_H\n\n")
        f_h.write("#include <math.h> // For pow, fabs, etc.\n\n")
        f_h.write(f"// Define a function pointer type for our equation of state\n")
        f_h.write(f"typedef double (*{TYPEDEF_NAME})(double, double, double);\n\n")
        f_h.write(f"// Define a function pointer type for derivatives\n")
        f_h.write(f"typedef double (*{TYPEDEF_DERIV_NAME})(double, double, double);\n\n")
        f_h.write(f"// Declare the function table (array of function pointers)\n")
        f_h.write(f"extern {TYPEDEF_NAME} {TABLE_NAME}[];\n\n")
        f_h.write(f"// Declare the derivative table (array of function pointers)\n")
        f_h.write(f"extern {TYPEDEF_DERIV_NAME} {DERIV_TABLE_NAME}[];\n\n")
        f_h.write(f"// Declare the total number of functions\n")
        f_h.write(f"extern const int {COUNT_NAME};\n\n")
        f_h.write("#endif // GENERATED_FUNCTIONS_H\n")

        # --- Write C File (.c) ---
        f_c.write(f'#include "{H_FILE}"\n\n')
        f_c.write(f"// NOTE: Functions that don't depend on x (scale factor) have been excluded\n\n")
        
        lines = f_in.readlines()
        
        # First pass: parse all expressions and filter
        valid_expressions = []
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue

            # Add 'Abs' to our local_symbols dict so parser recognizes it
            local_symbols['Abs'] = sympy.Abs
            
            try:
                # Special case for "0"
                if line == "0":
                    expr = sympy.sympify(0)
                    used_symbols = set()
                else:
                    # Parse the expression
                    expr = parse_expr(
                        line, 
                        local_dict=local_symbols, 
                        transformations=all_transformations
                    )
                    used_symbols = expr.free_symbols
                
                # CHECK: Does this expression depend on x?
                if x in used_symbols:
                    valid_expressions.append((i, line, expr, used_symbols))
                    print(f"  ✓ Including function {len(valid_expressions)-1} (original line {i}): {line}")
                else:
                    skipped_functions.append((i, line))
                    print(f"  ✗ Skipping function (original line {i}) - no x dependence: {line}")
                    
            except Exception as e:
                print(f"  ✗ Error parsing line {i} ('{line}'): {e} - SKIPPED")
                skipped_functions.append((i, line))
        
        print(f"\n{'='*60}")
        print(f"Filtered {len(valid_expressions)} functions (out of {len(lines)} total)")
        print(f"Skipped {len(skipped_functions)} functions that don't depend on x")
        print(f"{'='*60}\n")
        
        # Second pass: generate code only for valid expressions
        for new_idx, (orig_idx, line, expr, used_symbols) in enumerate(valid_expressions):
            func_name = f"func_{new_idx}"
            deriv_name = f"func_{new_idx}_deriv"
            function_names.append(func_name)
            derivative_names.append(deriv_name)
            original_indices.append(orig_idx)
            
            # --- Generate original function ---
            f_c.write(f"// Expression {new_idx} (original line {orig_idx}): {line}\n")
            f_c.write(f"double {func_name}(double x, double a0, double a1) {{\n")
            
            try:
                # Convert to C code string
                expr_str = printer.doprint(expr)

                # --- Add (void) casts for unused parameters ---
                # Note: x will ALWAYS be used since we filtered for it
                if a0 not in used_symbols:
                    f_c.write("    (void)a0;\n")
                if a1 not in used_symbols:
                    f_c.write("    (void)a1;\n")
                
                f_c.write(f"    return {expr_str};\n")
                
            except Exception as e:
                print(f"Error generating code for line {orig_idx} ('{line}'): {e}")
                f_c.write(f"    // ERROR: Could not generate code: {line}\n")
                f_c.write("    return 0.0; // Default error value\n")
                
            f_c.write("}\n\n")
            
            # --- Generate derivative function ---
            f_c.write(f"// Derivative of expression {new_idx} with respect to x: d/dx({line})\n")
            f_c.write(f"double {deriv_name}(double x, double a0, double a1) {{\n")
            
            try:
                # Calculate derivative with respect to x
                deriv_expr = sympy.diff(expr, x)
                
                # Simplify the derivative
                deriv_expr = sympy.simplify(deriv_expr)
                
                # Convert to C code
                deriv_str = printer.doprint(deriv_expr)
                deriv_symbols = deriv_expr.free_symbols
                
                # Add (void) casts for unused parameters
                if x not in deriv_symbols:
                    f_c.write("    (void)x;\n")
                if a0 not in deriv_symbols:
                    f_c.write("    (void)a0;\n")
                if a1 not in deriv_symbols:
                    f_c.write("    (void)a1;\n")
                
                f_c.write(f"    return {deriv_str};\n")
                
            except Exception as e:
                print(f"Error computing derivative for line {orig_idx} ('{line}'): {e}")
                f_c.write(f"    // ERROR: Could not compute derivative\n")
                f_c.write("    return 0.0; // Default error value\n")
                
            f_c.write("}\n\n")

        # Now, write the function tables
        f_c.write(f"// --- Function Table --- \n\n")
        f_c.write(f"const int {COUNT_NAME} = {len(function_names)};\n\n")
        f_c.write(f"{TYPEDEF_NAME} {TABLE_NAME}[] = {{\n")
        for name in function_names:
            f_c.write(f"    {name},\n")
        f_c.write("};\n\n")
        
        f_c.write(f"// --- Derivative Table --- \n\n")
        f_c.write(f"{TYPEDEF_DERIV_NAME} {DERIV_TABLE_NAME}[] = {{\n")
        for name in derivative_names:
            f_c.write(f"    {name},\n")
        f_c.write("};\n")

    print(f"\n{'='*60}")
    print(f"Successfully generated {H_FILE} and {C_FILE}")
    print(f"Total functions generated: {len(function_names)}")
    print(f"Total derivatives generated: {len(derivative_names)}")
    print(f"{'='*60}")
    
    # Write a mapping file for reference
    mapping_file = 'function_index_mapping.txt'
    with open(mapping_file, 'w') as f_map:
        f_map.write("# Function Index Mapping\n")
        f_map.write("# Format: new_index | original_line | expression\n")
        f_map.write("#" + "="*70 + "\n\n")
        for new_idx, orig_idx in enumerate(original_indices):
            line = valid_expressions[new_idx][1]
            f_map.write(f"{new_idx:3d} | Line {orig_idx:3d} | {line}\n")
        f_map.write("\n" + "#" + "="*70 + "\n")
        f_map.write("# Skipped functions (no dependence on x):\n")
        f_map.write("#" + "="*70 + "\n\n")
        for orig_idx, line in skipped_functions:
            f_map.write(f"Line {orig_idx:3d} | SKIPPED | {line}\n")
    
    print(f"Index mapping written to: {mapping_file}")
    print(f"\nIMPORTANT: Function indices have changed!")
    print(f"  - Function 0 is still: {valid_expressions[0][1]}")
    print(f"  - Check {mapping_file} for the complete mapping")

except Exception as e:
    print(f"An error occurred: {e}")
    import traceback
    traceback.print_exc()