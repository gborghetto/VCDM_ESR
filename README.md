# VCDM_ESR

This repository contains the modified implementation of the [CLASS](https://github.com/lesgourg/class_public) Boltzmann solver used in the SPIDER (Symbolic regression PIpeline for Dark Energy Reconstruction) framework, developed in the context of the VCDM minimally modified gravity theory.

The code was developed and used in:

> Borghetto, Malhotra, Arora, De Felice, Mukohyama, Tasinato, Zavala, *"Data-Driven Discovery of a Simple Phantom-Crossing Dark Energy Parametrization"*, arXiv:2606.17951 (2026)

## Description

The code extends the standard CLASS Boltzmann solver to support VCDM, a minimally modified gravity framework in which both background evolution and linear perturbations can be consistently evolved across the phantom divide. This allows for a theoretically controlled reconstruction of the dark energy equation of state w(a) without introducing additional propagating degrees of freedom.

The SPIDER pipeline consists of three stages:

**1. Function Generation**
Candidate analytic expressions for w(a) are generated using the [ESR generation module](https://github.com/DeaglanBartlett/ESR/tree/main/esr/generation), which exhaustively enumerates all analytic expressions of a given complexity. The operator basis and complexity are specified in `duplicate_checker.py` in the ESR generation module — running this script produces a `unique_equations.txt` file containing all unique, non-redundant candidate expressions. The file `C_generator.py` in the `class_functions_generation/` folder then reads this file and converts the expressions into a CLASS-compatible format, generating `generated_functions.c`, `generated_functions.h`, and `function_index_mapping.txt`. These files define the function library that CLASS loads and evaluates throughout the pipeline.

Once `C_generator.py` has been run, the generated C files need to be compiled into a shared library so that CLASS can load and call the functions at runtime. From the `ESR_tests/` folder, run:

```bash
gcc -shared -fPIC -o generated_functions.dylib generated_functions.c -lm
cd source
gcc -I../include -o generated_functions.dylib generated_functions.c -lm -dynamiclib
ln -sf generated_functions.dylib generated_functions.so
```

The first command compiles the C file into a shared library. The second recompiles including the CLASS headers. The final command creates a symbolic link so the library is accessible as both `.dylib` (Mac) and `.so` (Linux).

**2. Boltzmann Evaluation**
Each candidate w(a) is implemented in the modified VCDM version of CLASS, which evolves the full background and linear perturbation equations self-consistently, returning CMB power spectra, matter power spectrum, and background quantities.

**3. Fitting and Ranking**
Candidates are evaluated against CMB, BAO, and supernova data via Cobaya, ranked by χ² and Bayesian evidence, and compared against standard parametrizations such as CPL and ΛCDM.

## Dependencies

- [CLASS](https://github.com/lesgourg/class_public)
- [ESR](https://github.com/DeaglanBartlett/ESR)
- [Cobaya](https://cobaya.readthedocs.io/)
- [PolyChord](https://github.com/PolyChord/PolyChordLite)
- Python 3, numpy, sympy, mpi4py

## Authors

Giulia Borghetto, Ameek Malhotra, Simran Arora, Antonio De Felice, Shinji Mukohyama, Gianmassimo Tasinato, Ivonne Zavala

## Citation

If you use this code, please cite:

```
@article{Borghetto:2026,
  author = {Borghetto, Giulia and Malhotra, Ameek and Arora, Simran and De Felice, Antonio and Mukohyama, Shinji and Tasinato, Gianmassimo and Zavala, Ivonne},
  title = {Data-Driven Discovery of a Simple Phantom-Crossing Dark Energy Parametrization},
  eprint = {2606.17951},
  archivePrefix = {arXiv},
  primaryClass = {astro-ph.CO},
  year = {2026}
}
```