# non-stationary-ews
Code and data associated with the paper: Linearised dynamics and apparent early-warning behaviour in epidemic systems

Primary authors (contributed equally): Joshua Looker.
Other authors (contributed equally): Kat Rock, Louise Dyson
Corresponding author email address: joshua.looker@warwick.ac.uk

## Theoretical analysis
Code to reproduce phase-planes and theoretical variance evolution can be found in the `trajectory_jacobian_sir.ipynb` notebook.

## Simulation analysis
Code to run the simulations can be found in `simulation_cases.py` and `sim.sbatch` (note that these were run on a high-performance computing cluster) and to produce the plots can be found in the `simulations.ipynb` notebook.
.npy files should be set up in a directory named `Sim_results` to work with the `simulations.ipynb` notebook.