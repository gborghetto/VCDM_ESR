#ifndef GENERATED_FUNCTIONS_H
#define GENERATED_FUNCTIONS_H

#include <math.h> // For pow, fabs, etc.

// Define a function pointer type for our equation of state
typedef double (*eos_function)(double, double, double);

// Define a function pointer type for derivatives
typedef double (*eos_function_deriv)(double, double, double);

// Declare the function table (array of function pointers)
extern eos_function function_table[];

// Declare the derivative table (array of function pointers)
extern eos_function_deriv derivative_table[];

// Declare the total number of functions
extern const int function_count;

#endif // GENERATED_FUNCTIONS_H
