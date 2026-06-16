#include "generated_functions.h"

// NOTE: Functions that don't depend on x (scale factor) have been excluded

// Expression 0 (original line 0): a0 + a1*(1-x)
double func_0(double x, double a0, double a1) {
    return a0 + a1*(1 - x);
}

// Derivative of expression 0 with respect to x: d/dx(a0 + a1*(1-x))
double func_0_deriv(double x, double a0, double a1) {
    (void)x;
    (void)a0;
    return -a1;
}

// Expression 1 (original line 1): a0 + a1*(1-x)/(x**2+(1-x)**2)
double func_1(double x, double a0, double a1) {
    return a0 + a1*(1 - x)/(pow(x, 2) + pow(1 - x, 2));
}

// Derivative of expression 1 with respect to x: d/dx(a0 + a1*(1-x)/(x**2+(1-x)**2))
double func_1_deriv(double x, double a0, double a1) {
    (void)a0;
    return a1*(-pow(x, 2) - pow(x - 1, 2) + 2*(x - 1)*(2*x - 1))/pow(pow(x, 2) + pow(x - 1, 2), 2);
}

// Expression 2 (original line 2): a0 + a1*x*(1-x)
double func_2(double x, double a0, double a1) {
    return a0 + a1*x*(1 - x);
}

// Derivative of expression 2 with respect to x: d/dx(a0 + a1*x*(1-x))
double func_2_deriv(double x, double a0, double a1) {
    (void)a0;
    return a1*(1 - 2*x);
}

// Expression 3 (original line 3): a0 - a1 + a1*exp(1-x)
double func_3(double x, double a0, double a1) {
    return a0 + a1*exp(1 - x) - a1;
}

// Derivative of expression 3 with respect to x: d/dx(a0 - a1 + a1*exp(1-x))
double func_3_deriv(double x, double a0, double a1) {
    (void)a0;
    return -a1*exp(1 - x);
}

// Expression 4 (original line 4): a0 - a1*log(x)
double func_4(double x, double a0, double a1) {
    return a0 - a1*log(x);
}

// Derivative of expression 4 with respect to x: d/dx(a0 - a1*log(x))
double func_4_deriv(double x, double a0, double a1) {
    (void)a0;
    return -a1/x;
}

// Expression 5 (original line 5): sqrt(Abs(a0 - x))
double func_5(double x, double a0, double a1) {
    (void)a1;
    return sqrt(fabs(a0 - x));
}

// Derivative of expression 5 with respect to x: d/dx(sqrt(Abs(a0 - x)))
double func_5_deriv(double x, double a0, double a1) {
    (void)a1;
    return ((a0 == x) ? (
   0
)
: (
   (1.0/2.0)*(-a0 + x)/fabs(pow(a0 - x, 3.0/2.0))
));
}

// Expression 6 (original line 6): exp(2*x)
double func_6(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return exp(2*x);
}

// Derivative of expression 6 with respect to x: d/dx(exp(2*x))
double func_6_deriv(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return 2*exp(2*x);
}

// Expression 7 (original line 7): pow(x,(x**2))
double func_7(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return pow(x, pow(x, 2));
}

// Derivative of expression 7 with respect to x: d/dx(pow(x,(x**2)))
double func_7_deriv(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return pow(x, pow(x, 2) + 1)*(2*log(x) + 1);
}

// Expression 8 (original line 8): pow(x,Abs(a0))
double func_8(double x, double a0, double a1) {
    (void)a1;
    return pow(x, fabs(a0));
}

// Derivative of expression 8 with respect to x: d/dx(pow(x,Abs(a0)))
double func_8_deriv(double x, double a0, double a1) {
    (void)a1;
    return pow(x, fabs(a0) - 1)*fabs(a0);
}

// Expression 9 (original line 9): exp(pow(Abs(a0),x))
double func_9(double x, double a0, double a1) {
    (void)a1;
    return exp(pow(fabs(a0), x));
}

// Derivative of expression 9 with respect to x: d/dx(exp(pow(Abs(a0),x)))
double func_9_deriv(double x, double a0, double a1) {
    (void)a1;
    return exp(pow(fabs(a0), x))*log(fabs(a0))*pow(fabs(a0), x);
}

// Expression 10 (original line 10): a0 - exp(x)
double func_10(double x, double a0, double a1) {
    (void)a1;
    return a0 - exp(x);
}

// Derivative of expression 10 with respect to x: d/dx(a0 - exp(x))
double func_10_deriv(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return -exp(x);
}

// Expression 11 (original line 11): pow(x,(3/2))
double func_11(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return pow(x, 3.0/2.0);
}

// Derivative of expression 11 with respect to x: d/dx(pow(x,(3/2)))
double func_11_deriv(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return (3.0/2.0)*sqrt(x);
}

// Expression 12 (original line 12): sqrt(2)*sqrt(x)
double func_12(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return M_SQRT2*sqrt(x);
}

// Derivative of expression 12 with respect to x: d/dx(sqrt(2)*sqrt(x))
double func_12_deriv(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return (1.0/2.0)*M_SQRT2/sqrt(x);
}

// Expression 13 (original line 13): a0 + sqrt(x)
double func_13(double x, double a0, double a1) {
    (void)a1;
    return a0 + sqrt(x);
}

// Derivative of expression 13 with respect to x: d/dx(a0 + sqrt(x))
double func_13_deriv(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return (1.0/2.0)/sqrt(x);
}

// Expression 14 (original line 14): a0 - x**2
double func_14(double x, double a0, double a1) {
    (void)a1;
    return a0 - pow(x, 2);
}

// Derivative of expression 14 with respect to x: d/dx(a0 - x**2)
double func_14_deriv(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return -2*x;
}

// Expression 15 (original line 15): x**4
double func_15(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return pow(x, 4);
}

// Derivative of expression 15 with respect to x: d/dx(x**4)
double func_15_deriv(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return 4*pow(x, 3);
}

// Expression 16 (original line 16): pow(Abs(a0),(x**2))
double func_16(double x, double a0, double a1) {
    (void)a1;
    return pow(fabs(a0), pow(x, 2));
}

// Derivative of expression 16 with respect to x: d/dx(pow(Abs(a0),(x**2)))
double func_16_deriv(double x, double a0, double a1) {
    (void)a1;
    return 2*x*log(fabs(a0))*pow(fabs(a0), pow(x, 2));
}

// Expression 17 (original line 17): -x**2 + x
double func_17(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return -pow(x, 2) + x;
}

// Derivative of expression 17 with respect to x: d/dx(-x**2 + x)
double func_17_deriv(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return 1 - 2*x;
}

// Expression 18 (original line 18): 1/sqrt(x)
double func_18(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return pow(x, -1.0/2.0);
}

// Derivative of expression 18 with respect to x: d/dx(1/sqrt(x))
double func_18_deriv(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return -(1.0/2.0)/pow(x, 3.0/2.0);
}

// Expression 19 (original line 19): Abs(a0)/sqrt(x)
double func_19(double x, double a0, double a1) {
    (void)a1;
    return fabs(a0)/sqrt(x);
}

// Derivative of expression 19 with respect to x: d/dx(Abs(a0)/sqrt(x))
double func_19_deriv(double x, double a0, double a1) {
    (void)a1;
    return -1.0/2.0*fabs(a0)/pow(x, 3.0/2.0);
}

// Expression 20 (original line 20): a0*exp(x)
double func_20(double x, double a0, double a1) {
    (void)a1;
    return a0*exp(x);
}

// Derivative of expression 20 with respect to x: d/dx(a0*exp(x))
double func_20_deriv(double x, double a0, double a1) {
    (void)a1;
    return a0*exp(x);
}

// Expression 21 (original line 21): pow(x,(sqrt(x)))
double func_21(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return pow(x, sqrt(x));
}

// Derivative of expression 21 with respect to x: d/dx(pow(x,(sqrt(x))))
double func_21_deriv(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return (1.0/2.0)*pow(x, sqrt(x) - 1.0/2.0)*(log(x) + 2);
}

// Expression 22 (original line 22): sqrt(x)
double func_22(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return sqrt(x);
}

// Derivative of expression 22 with respect to x: d/dx(sqrt(x))
double func_22_deriv(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return (1.0/2.0)/sqrt(x);
}

// Expression 23 (original line 23): x + Abs(a0)
double func_23(double x, double a0, double a1) {
    (void)a1;
    return x + fabs(a0);
}

// Derivative of expression 23 with respect to x: d/dx(x + Abs(a0))
double func_23_deriv(double x, double a0, double a1) {
    (void)x;
    (void)a0;
    (void)a1;
    return 1;
}

// Expression 24 (original line 24): x - Abs(a0)
double func_24(double x, double a0, double a1) {
    (void)a1;
    return x - fabs(a0);
}

// Derivative of expression 24 with respect to x: d/dx(x - Abs(a0))
double func_24_deriv(double x, double a0, double a1) {
    (void)x;
    (void)a0;
    (void)a1;
    return 1;
}

// Expression 25 (original line 25): exp(4*x)
double func_25(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return exp(4*x);
}

// Derivative of expression 25 with respect to x: d/dx(exp(4*x))
double func_25_deriv(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return 4*exp(4*x);
}

// Expression 26 (original line 26): pow(Abs(a0),(sqrt(x)))
double func_26(double x, double a0, double a1) {
    (void)a1;
    return pow(fabs(a0), sqrt(x));
}

// Derivative of expression 26 with respect to x: d/dx(pow(Abs(a0),(sqrt(x))))
double func_26_deriv(double x, double a0, double a1) {
    (void)a1;
    return (1.0/2.0)*log(fabs(a0))*pow(fabs(a0), sqrt(x))/sqrt(x);
}

// Expression 27 (original line 28): pow(x,a0)
double func_27(double x, double a0, double a1) {
    (void)a1;
    return pow(x, a0);
}

// Derivative of expression 27 with respect to x: d/dx(pow(x,a0))
double func_27_deriv(double x, double a0, double a1) {
    (void)a1;
    return a0*pow(x, a0 - 1);
}

// Expression 28 (original line 29): x*exp(x)
double func_28(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return x*exp(x);
}

// Derivative of expression 28 with respect to x: d/dx(x*exp(x))
double func_28_deriv(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return (x + 1)*exp(x);
}

// Expression 29 (original line 30): a0*x**2
double func_29(double x, double a0, double a1) {
    (void)a1;
    return a0*pow(x, 2);
}

// Derivative of expression 29 with respect to x: d/dx(a0*x**2)
double func_29_deriv(double x, double a0, double a1) {
    (void)a1;
    return 2*a0*x;
}

// Expression 30 (original line 31): x**3
double func_30(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return pow(x, 3);
}

// Derivative of expression 30 with respect to x: d/dx(x**3)
double func_30_deriv(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return 3*pow(x, 2);
}

// Expression 31 (original line 32): Abs(a0)/x**2
double func_31(double x, double a0, double a1) {
    (void)a1;
    return fabs(a0)/pow(x, 2);
}

// Derivative of expression 31 with respect to x: d/dx(Abs(a0)/x**2)
double func_31_deriv(double x, double a0, double a1) {
    (void)a1;
    return -2*fabs(a0)/pow(x, 3);
}

// Expression 32 (original line 33): exp(x**2)
double func_32(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return exp(pow(x, 2));
}

// Derivative of expression 32 with respect to x: d/dx(exp(x**2))
double func_32_deriv(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return 2*x*exp(pow(x, 2));
}

// Expression 33 (original line 34): sqrt(x)*Abs(a0)
double func_33(double x, double a0, double a1) {
    (void)a1;
    return sqrt(x)*fabs(a0);
}

// Derivative of expression 33 with respect to x: d/dx(sqrt(x)*Abs(a0))
double func_33_deriv(double x, double a0, double a1) {
    (void)a1;
    return (1.0/2.0)*fabs(a0)/sqrt(x);
}

// Expression 34 (original line 35): exp(x)
double func_34(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return exp(x);
}

// Derivative of expression 34 with respect to x: d/dx(exp(x))
double func_34_deriv(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return exp(x);
}

// Expression 35 (original line 36): 1/x
double func_35(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return 1.0/x;
}

// Derivative of expression 35 with respect to x: d/dx(1/x)
double func_35_deriv(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return -1/pow(x, 2);
}

// Expression 36 (original line 37): exp(2*sqrt(x))
double func_36(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return exp(2*sqrt(x));
}

// Derivative of expression 36 with respect to x: d/dx(exp(2*sqrt(x)))
double func_36_deriv(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return exp(2*sqrt(x))/sqrt(x);
}

// Expression 37 (original line 38): sqrt(x) - x
double func_37(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return sqrt(x) - x;
}

// Derivative of expression 37 with respect to x: d/dx(sqrt(x) - x)
double func_37_deriv(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return -1 + (1.0/2.0)/sqrt(x);
}

// Expression 38 (original line 39): sqrt(x) + x
double func_38(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return sqrt(x) + x;
}

// Derivative of expression 38 with respect to x: d/dx(sqrt(x) + x)
double func_38_deriv(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return 1 + (1.0/2.0)/sqrt(x);
}

// Expression 39 (original line 40): x*Abs(a0)
double func_39(double x, double a0, double a1) {
    (void)a1;
    return x*fabs(a0);
}

// Derivative of expression 39 with respect to x: d/dx(x*Abs(a0))
double func_39_deriv(double x, double a0, double a1) {
    (void)x;
    (void)a1;
    return fabs(a0);
}

// Expression 40 (original line 41): exp(exp(x)/2)
double func_40(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return exp((1.0/2.0)*exp(x));
}

// Derivative of expression 40 with respect to x: d/dx(exp(exp(x)/2))
double func_40_deriv(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return (1.0/2.0)*exp(x + (1.0/2.0)*exp(x));
}

// Expression 41 (original line 42): -x + exp(x)
double func_41(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return -x + exp(x);
}

// Derivative of expression 41 with respect to x: d/dx(-x + exp(x))
double func_41_deriv(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return exp(x) - 1;
}

// Expression 42 (original line 43): a0/sqrt(x)
double func_42(double x, double a0, double a1) {
    (void)a1;
    return a0/sqrt(x);
}

// Derivative of expression 42 with respect to x: d/dx(a0/sqrt(x))
double func_42_deriv(double x, double a0, double a1) {
    (void)a1;
    return -1.0/2.0*a0/pow(x, 3.0/2.0);
}

// Expression 43 (original line 45): exp(exp(x**2))
double func_43(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return exp(exp(pow(x, 2)));
}

// Derivative of expression 43 with respect to x: d/dx(exp(exp(x**2)))
double func_43_deriv(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return 2*x*exp(pow(x, 2) + exp(pow(x, 2)));
}

// Expression 44 (original line 46): -x + Abs(a0)
double func_44(double x, double a0, double a1) {
    (void)a1;
    return -x + fabs(a0);
}

// Derivative of expression 44 with respect to x: d/dx(-x + Abs(a0))
double func_44_deriv(double x, double a0, double a1) {
    (void)x;
    (void)a0;
    (void)a1;
    return -1;
}

// Expression 45 (original line 47): a0 + exp(x)
double func_45(double x, double a0, double a1) {
    (void)a1;
    return a0 + exp(x);
}

// Derivative of expression 45 with respect to x: d/dx(a0 + exp(x))
double func_45_deriv(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return exp(x);
}

// Expression 46 (original line 49): exp(x**2/2)
double func_46(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return exp((1.0/2.0)*pow(x, 2));
}

// Derivative of expression 46 with respect to x: d/dx(exp(x**2/2))
double func_46_deriv(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return x*exp((1.0/2.0)*pow(x, 2));
}

// Expression 47 (original line 50): x**2*Abs(a0)
double func_47(double x, double a0, double a1) {
    (void)a1;
    return pow(x, 2)*fabs(a0);
}

// Derivative of expression 47 with respect to x: d/dx(x**2*Abs(a0))
double func_47_deriv(double x, double a0, double a1) {
    (void)a1;
    return 2*x*fabs(a0);
}

// Expression 48 (original line 51): x**8
double func_48(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return pow(x, 8);
}

// Derivative of expression 48 with respect to x: d/dx(x**8)
double func_48_deriv(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return 8*pow(x, 7);
}

// Expression 49 (original line 52): sqrt(x)*sqrt(Abs(1/a0))
double func_49(double x, double a0, double a1) {
    (void)a1;
    return sqrt(x)/sqrt(fabs(a0));
}

// Derivative of expression 49 with respect to x: d/dx(sqrt(x)*sqrt(Abs(1/a0)))
double func_49_deriv(double x, double a0, double a1) {
    (void)a1;
    return (1.0/2.0)/(sqrt(x)*fabs(sqrt(a0)));
}

// Expression 50 (original line 53): exp(exp(2*x))
double func_50(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return exp(exp(2*x));
}

// Derivative of expression 50 with respect to x: d/dx(exp(exp(2*x)))
double func_50_deriv(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return 2*exp(2*x + exp(2*x));
}

// Expression 51 (original line 54): exp(x)*Abs(a0)
double func_51(double x, double a0, double a1) {
    (void)a1;
    return exp(x)*fabs(a0);
}

// Derivative of expression 51 with respect to x: d/dx(exp(x)*Abs(a0))
double func_51_deriv(double x, double a0, double a1) {
    (void)a1;
    return exp(x)*fabs(a0);
}

// Expression 52 (original line 57): exp(a0/x)
double func_52(double x, double a0, double a1) {
    (void)a1;
    return exp(a0/x);
}

// Derivative of expression 52 with respect to x: d/dx(exp(a0/x))
double func_52_deriv(double x, double a0, double a1) {
    (void)a1;
    return -a0*exp(a0/x)/pow(x, 2);
}

// Expression 53 (original line 58): a0 - sqrt(x)
double func_53(double x, double a0, double a1) {
    (void)a1;
    return a0 - sqrt(x);
}

// Derivative of expression 53 with respect to x: d/dx(a0 - sqrt(x))
double func_53_deriv(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return -(1.0/2.0)/sqrt(x);
}

// Expression 54 (original line 59): pow(x,(x/2))
double func_54(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return pow(x, (1.0/2.0)*x);
}

// Derivative of expression 54 with respect to x: d/dx(pow(x,(x/2)))
double func_54_deriv(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return (1.0/2.0)*pow(x, (1.0/2.0)*x)*(log(x) + 1);
}

// Expression 55 (original line 61): exp(sqrt(x)/2)
double func_55(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return exp((1.0/2.0)*sqrt(x));
}

// Derivative of expression 55 with respect to x: d/dx(exp(sqrt(x)/2))
double func_55_deriv(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return (1.0/4.0)*exp((1.0/2.0)*sqrt(x))/sqrt(x);
}

// Expression 56 (original line 62): x*exp(-x)
double func_56(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return x*exp(-x);
}

// Derivative of expression 56 with respect to x: d/dx(x*exp(-x))
double func_56_deriv(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return (1 - x)*exp(-x);
}

// Expression 57 (original line 63): 4*x**2
double func_57(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return 4*pow(x, 2);
}

// Derivative of expression 57 with respect to x: d/dx(4*x**2)
double func_57_deriv(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return 8*x;
}

// Expression 58 (original line 64): pow(Abs(a0),(2*x))
double func_58(double x, double a0, double a1) {
    (void)a1;
    return pow(fabs(a0), 2*x);
}

// Derivative of expression 58 with respect to x: d/dx(pow(Abs(a0),(2*x)))
double func_58_deriv(double x, double a0, double a1) {
    (void)a1;
    return 2*log(fabs(a0))*pow(fabs(a0), 2*x);
}

// Expression 59 (original line 65): exp(pow(x,(1/4)))
double func_59(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return exp(pow(x, 1.0/4.0));
}

// Derivative of expression 59 with respect to x: d/dx(exp(pow(x,(1/4))))
double func_59_deriv(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return (1.0/4.0)*exp(pow(x, 1.0/4.0))/pow(x, 3.0/4.0);
}

// Expression 60 (original line 67): exp(exp(sqrt(x)))
double func_60(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return exp(exp(sqrt(x)));
}

// Derivative of expression 60 with respect to x: d/dx(exp(exp(sqrt(x))))
double func_60_deriv(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return (1.0/2.0)*exp(sqrt(x) + exp(sqrt(x)))/sqrt(x);
}

// Expression 61 (original line 68): x
double func_61(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return x;
}

// Derivative of expression 61 with respect to x: d/dx(x)
double func_61_deriv(double x, double a0, double a1) {
    (void)x;
    (void)a0;
    (void)a1;
    return 1;
}

// Expression 62 (original line 69): exp(a0*x)
double func_62(double x, double a0, double a1) {
    (void)a1;
    return exp(a0*x);
}

// Derivative of expression 62 with respect to x: d/dx(exp(a0*x))
double func_62_deriv(double x, double a0, double a1) {
    (void)a1;
    return a0*exp(a0*x);
}

// Expression 63 (original line 70): x**2 + x
double func_63(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return pow(x, 2) + x;
}

// Derivative of expression 63 with respect to x: d/dx(x**2 + x)
double func_63_deriv(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return 2*x + 1;
}

// Expression 64 (original line 71): exp(exp(x/2))
double func_64(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return exp(exp((1.0/2.0)*x));
}

// Derivative of expression 64 with respect to x: d/dx(exp(exp(x/2)))
double func_64_deriv(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return (1.0/2.0)*exp((1.0/2.0)*x + exp((1.0/2.0)*x));
}

// Expression 65 (original line 72): x + exp(x)
double func_65(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return x + exp(x);
}

// Derivative of expression 65 with respect to x: d/dx(x + exp(x))
double func_65_deriv(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return exp(x) + 1;
}

// Expression 66 (original line 73): exp(2*exp(x))
double func_66(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return exp(2*exp(x));
}

// Derivative of expression 66 with respect to x: d/dx(exp(2*exp(x)))
double func_66_deriv(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return 2*exp(x + 2*exp(x));
}

// Expression 67 (original line 74): exp(exp(exp(x)))
double func_67(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return exp(exp(exp(x)));
}

// Derivative of expression 67 with respect to x: d/dx(exp(exp(exp(x))))
double func_67_deriv(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return exp(x + exp(x) + exp(exp(x)));
}

// Expression 68 (original line 75): exp(x/4)
double func_68(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return exp((1.0/4.0)*x);
}

// Derivative of expression 68 with respect to x: d/dx(exp(x/4))
double func_68_deriv(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return (1.0/4.0)*exp((1.0/4.0)*x);
}

// Expression 69 (original line 76): x**2
double func_69(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return pow(x, 2);
}

// Derivative of expression 69 with respect to x: d/dx(x**2)
double func_69_deriv(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return 2*x;
}

// Expression 70 (original line 77): pow(x,(1/8))
double func_70(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return pow(x, 1.0/8.0);
}

// Derivative of expression 70 with respect to x: d/dx(pow(x,(1/8)))
double func_70_deriv(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return (1.0/8.0)/pow(x, 7.0/8.0);
}

// Expression 71 (original line 78): exp(2*x**2)
double func_71(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return exp(2*pow(x, 2));
}

// Derivative of expression 71 with respect to x: d/dx(exp(2*x**2))
double func_71_deriv(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return 4*x*exp(2*pow(x, 2));
}

// Expression 72 (original line 79): x - exp(x)
double func_72(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return x - exp(x);
}

// Derivative of expression 72 with respect to x: d/dx(x - exp(x))
double func_72_deriv(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return 1 - exp(x);
}

// Expression 73 (original line 80): exp(x)/x
double func_73(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return exp(x)/x;
}

// Derivative of expression 73 with respect to x: d/dx(exp(x)/x)
double func_73_deriv(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return (x - 1)*exp(x)/pow(x, 2);
}

// Expression 74 (original line 81): pow(x,(2*x))
double func_74(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return pow(x, 2*x);
}

// Derivative of expression 74 with respect to x: d/dx(pow(x,(2*x)))
double func_74_deriv(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return 2*pow(x, 2*x)*(log(x) + 1);
}

// Expression 75 (original line 83): x**2 - x
double func_75(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return pow(x, 2) - x;
}

// Derivative of expression 75 with respect to x: d/dx(x**2 - x)
double func_75_deriv(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return 2*x - 1;
}

// Expression 76 (original line 84): (a0 - x)**2
double func_76(double x, double a0, double a1) {
    (void)a1;
    return pow(a0 - x, 2);
}

// Derivative of expression 76 with respect to x: d/dx((a0 - x)**2)
double func_76_deriv(double x, double a0, double a1) {
    (void)a1;
    return -2*a0 + 2*x;
}

// Expression 77 (original line 85): Abs(a0)/x
double func_77(double x, double a0, double a1) {
    (void)a1;
    return fabs(a0)/x;
}

// Derivative of expression 77 with respect to x: d/dx(Abs(a0)/x)
double func_77_deriv(double x, double a0, double a1) {
    (void)a1;
    return -fabs(a0)/pow(x, 2);
}

// Expression 78 (original line 86): x/sqrt(Abs(a0))
double func_78(double x, double a0, double a1) {
    (void)a1;
    return x/sqrt(fabs(a0));
}

// Derivative of expression 78 with respect to x: d/dx(x/sqrt(Abs(a0)))
double func_78_deriv(double x, double a0, double a1) {
    (void)x;
    (void)a1;
    return 1.0/fabs(sqrt(a0));
}

// Expression 79 (original line 87): a0 + x**2
double func_79(double x, double a0, double a1) {
    (void)a1;
    return a0 + pow(x, 2);
}

// Derivative of expression 79 with respect to x: d/dx(a0 + x**2)
double func_79_deriv(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return 2*x;
}

// Expression 80 (original line 88): pow(x,exp(x))
double func_80(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return pow(x, exp(x));
}

// Derivative of expression 80 with respect to x: d/dx(pow(x,exp(x)))
double func_80_deriv(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return pow(x, exp(x) - 1)*(x*log(x) + 1)*exp(x);
}

// Expression 81 (original line 89): -sqrt(x) + x
double func_81(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return -sqrt(x) + x;
}

// Derivative of expression 81 with respect to x: d/dx(-sqrt(x) + x)
double func_81_deriv(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return 1 - (1.0/2.0)/sqrt(x);
}

// Expression 82 (original line 90): pow(Abs(a0),exp(x))
double func_82(double x, double a0, double a1) {
    (void)a1;
    return pow(fabs(a0), exp(x));
}

// Derivative of expression 82 with respect to x: d/dx(pow(Abs(a0),exp(x)))
double func_82_deriv(double x, double a0, double a1) {
    (void)a1;
    return exp(x)*log(fabs(a0))*pow(fabs(a0), exp(x));
}

// Expression 83 (original line 91): a0*exp(-x)
double func_83(double x, double a0, double a1) {
    (void)a1;
    return a0*exp(-x);
}

// Derivative of expression 83 with respect to x: d/dx(a0*exp(-x))
double func_83_deriv(double x, double a0, double a1) {
    (void)a1;
    return -a0*exp(-x);
}

// Expression 84 (original line 92): (a0 + x)**2
double func_84(double x, double a0, double a1) {
    (void)a1;
    return pow(a0 + x, 2);
}

// Derivative of expression 84 with respect to x: d/dx((a0 + x)**2)
double func_84_deriv(double x, double a0, double a1) {
    (void)a1;
    return 2*a0 + 2*x;
}

// Expression 85 (original line 96): pow(Abs(a0),(x/2))
double func_85(double x, double a0, double a1) {
    (void)a1;
    return pow(fabs(a0), (1.0/2.0)*x);
}

// Derivative of expression 85 with respect to x: d/dx(pow(Abs(a0),(x/2)))
double func_85_deriv(double x, double a0, double a1) {
    (void)a1;
    return (1.0/2.0)*log(fabs(a0))*pow(fabs(a0), (1.0/2.0)*x);
}

// Expression 86 (original line 97): exp(x**4)
double func_86(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return exp(pow(x, 4));
}

// Derivative of expression 86 with respect to x: d/dx(exp(x**4))
double func_86_deriv(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return 4*pow(x, 3)*exp(pow(x, 4));
}

// Expression 87 (original line 99): a0*sqrt(x)
double func_87(double x, double a0, double a1) {
    (void)a1;
    return a0*sqrt(x);
}

// Derivative of expression 87 with respect to x: d/dx(a0*sqrt(x))
double func_87_deriv(double x, double a0, double a1) {
    (void)a1;
    return (1.0/2.0)*a0/sqrt(x);
}

// Expression 88 (original line 100): exp(-x)*Abs(a0)
double func_88(double x, double a0, double a1) {
    (void)a1;
    return exp(-x)*fabs(a0);
}

// Derivative of expression 88 with respect to x: d/dx(exp(-x)*Abs(a0))
double func_88_deriv(double x, double a0, double a1) {
    (void)a1;
    return -exp(-x)*fabs(a0);
}

// Expression 89 (original line 101): exp(pow(x,x))
double func_89(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return exp(pow(x, x));
}

// Derivative of expression 89 with respect to x: d/dx(exp(pow(x,x)))
double func_89_deriv(double x, double a0, double a1) {
    (void)a0;
    (void)a1;
    return pow(x, x)*(log(x) + 1)*exp(pow(x, x));
}

// Expression 90 (original line 102): a0/x**2
double func_90(double x, double a0, double a1) {
    (void)a1;
    return a0/pow(x, 2);
}

// Derivative of expression 90 with respect to x: d/dx(a0/x**2)
double func_90_deriv(double x, double a0, double a1) {
    (void)a1;
    return -2*a0/pow(x, 3);
}

// Expression 91 (original line 103): exp(pow(x,a0))
double func_91(double x, double a0, double a1) {
    (void)a1;
    return exp(pow(x, a0));
}

// Derivative of expression 91 with respect to x: d/dx(exp(pow(x,a0)))
double func_91_deriv(double x, double a0, double a1) {
    (void)a1;
    return a0*pow(x, a0 - 1)*exp(pow(x, a0));
}

// --- Function Table --- 

const int function_count = 92;

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
    func_22,
    func_23,
    func_24,
    func_25,
    func_26,
    func_27,
    func_28,
    func_29,
    func_30,
    func_31,
    func_32,
    func_33,
    func_34,
    func_35,
    func_36,
    func_37,
    func_38,
    func_39,
    func_40,
    func_41,
    func_42,
    func_43,
    func_44,
    func_45,
    func_46,
    func_47,
    func_48,
    func_49,
    func_50,
    func_51,
    func_52,
    func_53,
    func_54,
    func_55,
    func_56,
    func_57,
    func_58,
    func_59,
    func_60,
    func_61,
    func_62,
    func_63,
    func_64,
    func_65,
    func_66,
    func_67,
    func_68,
    func_69,
    func_70,
    func_71,
    func_72,
    func_73,
    func_74,
    func_75,
    func_76,
    func_77,
    func_78,
    func_79,
    func_80,
    func_81,
    func_82,
    func_83,
    func_84,
    func_85,
    func_86,
    func_87,
    func_88,
    func_89,
    func_90,
    func_91,
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
    func_22_deriv,
    func_23_deriv,
    func_24_deriv,
    func_25_deriv,
    func_26_deriv,
    func_27_deriv,
    func_28_deriv,
    func_29_deriv,
    func_30_deriv,
    func_31_deriv,
    func_32_deriv,
    func_33_deriv,
    func_34_deriv,
    func_35_deriv,
    func_36_deriv,
    func_37_deriv,
    func_38_deriv,
    func_39_deriv,
    func_40_deriv,
    func_41_deriv,
    func_42_deriv,
    func_43_deriv,
    func_44_deriv,
    func_45_deriv,
    func_46_deriv,
    func_47_deriv,
    func_48_deriv,
    func_49_deriv,
    func_50_deriv,
    func_51_deriv,
    func_52_deriv,
    func_53_deriv,
    func_54_deriv,
    func_55_deriv,
    func_56_deriv,
    func_57_deriv,
    func_58_deriv,
    func_59_deriv,
    func_60_deriv,
    func_61_deriv,
    func_62_deriv,
    func_63_deriv,
    func_64_deriv,
    func_65_deriv,
    func_66_deriv,
    func_67_deriv,
    func_68_deriv,
    func_69_deriv,
    func_70_deriv,
    func_71_deriv,
    func_72_deriv,
    func_73_deriv,
    func_74_deriv,
    func_75_deriv,
    func_76_deriv,
    func_77_deriv,
    func_78_deriv,
    func_79_deriv,
    func_80_deriv,
    func_81_deriv,
    func_82_deriv,
    func_83_deriv,
    func_84_deriv,
    func_85_deriv,
    func_86_deriv,
    func_87_deriv,
    func_88_deriv,
    func_89_deriv,
    func_90_deriv,
    func_91_deriv,
};
