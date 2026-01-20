#!/bin/bash
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=48
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=3700
#SBATCH --time=12:00:00
#SBATCH --job-name=lownorm01

MY_NUM_THREADS=$SLURM_CPUS_PER_TASK
export OMP_NUM_THREADS=$MY_NUM_THREADS

module purge
module load GCC/11.3.0 GCC/11.3.0 OpenMPI/4.1.4 SciPy-bundle/2022.05 parallel/20220722

# Run $SLURM_NTASKS tasks in parallel
MY_PARALLEL_OPTS="-N 1 --delay 2 -j $SLURM_NTASKS --joblog parallel-${SLURM_JOBID}.log"
MY_SRUN_OPTS="-N 1 -n 1 --exclusive"
MY_EXEC='python "$HOME/non_stat_results/simulation_cases.py" {1} lownorm 10000 0.1'
parallel $MY_PARALLEL_OPTS srun $MY_SRUN_OPTS $MY_EXEC ::: {0..99}
