# p-medians
This repository contains a Python solution to the optimization problem of the capacitaded p-medians, using a Min-Max Ant System(MMAS) and a General Assignment Problem(GAP) heuristic, based in the paper *De França, Fabrício Olivetti, Fernando J. Von Zuben, and Leandro Nunes De Castro. "Max min ant system and capacitated p-medians: Extensions and improved solutions." Informatica 29.2 (2005)*.

## Compiling and Running
Before executing the program, the Cython files need to be compiled. This can be achieved by running the `setup.py` script as follows:

```
$ python3 setup.py build_ext --inplace
```

After that, the code is executed with the following arguments:

```
$ python3 main.py [-i ITERATIONS] [-a ANTS] [--alpha ALPHA] [--beta BETA] [--rho RHO] dataset
```