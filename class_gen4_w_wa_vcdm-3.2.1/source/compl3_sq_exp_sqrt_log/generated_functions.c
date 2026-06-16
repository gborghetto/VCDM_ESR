#include "generated_functions.h"

// NOTE: Functions that don't depend on x (scale factor) have been excluded

// Expression 0 (original line 0): exp(x**2)
double func_0(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return exp(pow(x, 2));
}

// Derivative of expression 0 with respect to x: d/dx(exp(x**2))
double func_0_deriv(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return 2*x*exp(pow(x, 2));
}

// Expression 1 (original line 1): x
double func_1(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return x;
}

// Derivative of expression 1 with respect to x: d/dx(x)
double func_1_deriv(double x, double a0, double a1) {
    (void)x;
    (void)a0;
    (void)a1;
    return 1;
}

// Expression 2 (original line 2): pow(x,a0)
double func_2(double x, double a0, double a1) {
    (void)a1;
    return pow(x, a0);
}

// Derivative of expression 2 with respect to x: d/dx(pow(x,a0))
double func_2_deriv(double x, double a0, double a1) {
    (void)a1;
    return a0*pow(x, a0 - 1);
}

// Expression 3 (original line 3): x**4
double func_3(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return pow(x, 4);
}

// Derivative of expression 3 with respect to x: d/dx(x**4)
double func_3_deriv(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return 4*pow(x, 3);
}

// Expression 4 (original line 4): sqrt(Abs(log(x)))
double func_4(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return sqrt(fabs(log(x)));
}

// Derivative of expression 4 with respect to x: d/dx(sqrt(Abs(log(x))))
double func_4_deriv(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return ((x == 0) ? (
   NAN
)
: ((log(x) == 0) ? (
   0
)
: (
   (1.0/2.0)*log(fabs(x))/(x*fabs(pow(log(x), 3.0/2.0)))
)));
}

// Expression 5 (original line 5): exp(sqrt(x))
double func_5(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return exp(sqrt(x));
}

// Derivative of expression 5 with respect to x: d/dx(exp(sqrt(x)))
double func_5_deriv(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return (1.0/2.0)*exp(sqrt(x))/sqrt(x);
}

// Expression 6 (original line 6): x**2
double func_6(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return pow(x, 2);
}

// Derivative of expression 6 with respect to x: d/dx(x**2)
double func_6_deriv(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return 2*x;
}

// Expression 7 (original line 7): log(sqrt(x))
double func_7(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return log(sqrt(x));
}

// Derivative of expression 7 with respect to x: d/dx(log(sqrt(x)))
double func_7_deriv(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return (1.0/2.0)/x;
}

// Expression 8 (original line 10): exp(x/2)
double func_8(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return exp((1.0/2.0)*x);
}

// Derivative of expression 8 with respect to x: d/dx(exp(x/2))
double func_8_deriv(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return (1.0/2.0)*exp((1.0/2.0)*x);
}

// Expression 9 (original line 11): a0 - x
double func_9(double x, double a0, double a1) {
    (void)a1;
    return a0 - x;
}

// Derivative of expression 9 with respect to x: d/dx(a0 - x)
double func_9_deriv(double x, double a0, double a1) {
    (void)x;
    (void)a0;
    (void)a1;
    return -1;
}

// Expression 10 (original line 12): a0/x
double func_10(double x, double a0, double a1) {
    (void)a1;
    return a0/x;
}

// Derivative of expression 10 with respect to x: d/dx(a0/x)
double func_10_deriv(double x, double a0, double a1) {
    (void)a1;
    return -a0/pow(x, 2);
}

// Expression 11 (original line 13): pow(x,(1/4))
double func_11(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return pow(x, 1.0/4.0);
}

// Derivative of expression 11 with respect to x: d/dx(pow(x,(1/4)))
double func_11_deriv(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return (1.0/4.0)/pow(x, 3.0/4.0);
}

// Expression 12 (original line 14): exp(2*x)
double func_12(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return exp(2*x);
}

// Derivative of expression 12 with respect to x: d/dx(exp(2*x))
double func_12_deriv(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return 2*exp(2*x);
}

// Expression 13 (original line 15): a0 + x
double func_13(double x, double a0, double a1) {
    (void)a1;
    return a0 + x;
}

// Derivative of expression 13 with respect to x: d/dx(a0 + x)
double func_13_deriv(double x, double a0, double a1) {
    (void)x;
    (void)a0;
    (void)a1;
    return 1;
}

// Expression 14 (original line 17): a0*x
double func_14(double x, double a0, double a1) {
    (void)a1;
    return a0*x;
}

// Derivative of expression 14 with respect to x: d/dx(a0*x)
double func_14_deriv(double x, double a0, double a1) {
    (void)x;
    (void)a1;
    return a0;
}

// Expression 15 (original line 18): log(x**2)
double func_15(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return log(pow(x, 2));
}

// Derivative of expression 15 with respect to x: d/dx(log(x**2))
double func_15_deriv(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return 2/x;
}

// Expression 16 (original line 19): exp(exp(x))
double func_16(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return exp(exp(x));
}

// Derivative of expression 16 with respect to x: d/dx(exp(exp(x)))
double func_16_deriv(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return exp(x + exp(x));
}

// Expression 17 (original line 20): 2*x
double func_17(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return 2*x;
}

// Derivative of expression 17 with respect to x: d/dx(2*x)
double func_17_deriv(double x, double a0, double a1) {
    (void)x;
    (void)a0;
    (void)a1;
    return 2;
}

// Expression 18 (original line 21): pow(Abs(a0),x)
double func_18(double x, double a0, double a1) {
    (void)a1;
    return pow(fabs(a0), x);
}

// Derivative of expression 18 with respect to x: d/dx(pow(Abs(a0),x))
double func_18_deriv(double x, double a0, double a1) {
    (void)a1;
    return log(fabs(a0))*pow(fabs(a0), x);
}

// Expression 19 (original line 23): log(Abs(log(x)))
double func_19(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return log(fabs(log(x)));
}

// Derivative of expression 19 with respect to x: d/dx(log(Abs(log(x))))
double func_19_deriv(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return ((x == 0) ? (
   NAN
)
: ((log(x) == 0) ? (
   0
)
: (
   log(fabs(x))/(x*fabs(pow(log(x), 2)))
)));
}

// Expression 20 (original line 24): pow(x,x)
double func_20(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return pow(x, x);
}

// Derivative of expression 20 with respect to x: d/dx(pow(x,x))
double func_20_deriv(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return pow(x, x)*(log(x) + 1);
}

// Expression 21 (original line 25): log(x)**2
double func_21(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return pow(log(x), 2);
}

// Derivative of expression 21 with respect to x: d/dx(log(x)**2)
double func_21_deriv(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return 2*log(x)/x;
}

// --- Function Table --- 

const int function_count = 22;

eos_function function_table[] = {
    func_0,
    func_1,
    func_2,
    func_3,
    func_4,
    func_5,
    func_6,
    func_7,
    func_8,
    func_9,
    func_10,
    func_11,
    func_12,
    func_13,
    func_14,
    func_15,
    func_16,
    func_17,
    func_18,
    func_19,
    func_20,
    func_21,
};

// --- Derivative Table --- 

eos_function_deriv derivative_table[] = {
    func_0_deriv,
    func_1_deriv,
    func_2_deriv,
    func_3_deriv,
    func_4_deriv,
    func_5_deriv,
    func_6_deriv,
    func_7_deriv,
    func_8_deriv,
    func_9_deriv,
    func_10_deriv,
    func_11_deriv,
    func_12_deriv,
    func_13_deriv,
    func_14_deriv,
    func_15_deriv,
    func_16_deriv,
    func_17_deriv,
    func_18_deriv,
    func_19_deriv,
    func_20_deriv,
    func_21_deriv,
};
