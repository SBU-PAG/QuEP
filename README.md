# QuEP

This code was developed to simulate an electron probe's trajectory through a plasma wakefield accelerator. It does so by taking previously simulated fields and propagating an electron through these fields. This allows us to quickly estimate the trajectories of multiple electrons without the repeated use of computationally expensive simulations.

The `master` branch contains the most up-to-date code.

### Running the Simulation
To run the simulation, add an initialization file in the `input` folder, such as the file `example.py`, which would be input to the simulation using
```
python main.py input.example
```

The following parameters must be specified in the initialization file (case insensitive):

* simulation_name - `quasi3D` only (for now!)
* shape - `hline`, `vline`, `single`, or `rectangle`
* iterations - Maximum number of steps before tracking in plasma is stopped
* mode - An extra flag to be used by any simulation. See simulation files under `/include/simulations` for specifications. 
* fname - File name
* x_c, y_c, xi_c - Center coordinates of probe 
* px_0, py_0, pz_0 - Initial momenta of probe
* x_s - Screen distances. Used in certain plotting macros.
* s1, s2, s3 - Shape parameters. See initialization files under `/include/shape` for specifications. 
* ydensity, xidensity - Number of electrons to be distributed in specified direction. See initialization files under `/include/shape` for specifications.
* resolution - An unused parameter that can refer to the spacing between electrons, if `shape` initialization files are modified.

A `.npz` file that includes the final x, y, xi, and z positions of each electron, as well as the final x, y, and z momenta, will then be saved.

### Plotting Results
To plot generated data, set the appropriate plotting script macros' booleans to `True` in `index.py` (be sure to check the file name readout location), then run
```
python index.py input.example
```

### Requirements
This simulation requires the python packages h5py, importlib, numpy, and multiprocessing.

A non-multiprocessing version of the code can be found on the version-1.0 branch

### Compatible Plasma Simulations (`/include/simulations`):

* Quasi3D 

### Repository Structure 

The `master` branch contains the most up-to-date code. 

The `version-1.0` branch contains the first complete version of the code, where positions of electrons *inside* the plasma are tracked. No output files are saved in this version; plots are immediately generated. Multiprocessing is also not implemented here.

The respective `unit-test` branches contain input files and plotting macros used to verify QuEP. 

The `plotting` branch is used as a working branch.

### Contact
Contact Marisa Petrusky (marisapetrusky@gmail.com) for questions about this code. Source code can be found at https://github.com/marisapetrusky/QuEP/
