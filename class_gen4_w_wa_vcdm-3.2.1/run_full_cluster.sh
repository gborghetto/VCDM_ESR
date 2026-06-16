#!/bin/bash --login
###
### SLURM job script for VCDM multi-function analysis with job arrays
###
#SBATCH --job-name=vcdm_multifunction
#SBATCH --array=0-9                   # 16 jobs, each handling 10 functions (for 160 total)
#SBATCH --output=logs/vcdm_%a.out      # Individual output files for each array job
#SBATCH --error=logs/vcdm_%a.err       # Individual error files for each array job
#SBATCH --time=2-23:59                 # Maximum job time: 2 days, 23 hours, 59 minutes
#SBATCH --account=scw2169              # Your SLURM account
#SBATCH --ntasks=1                     # One task per job array element
#SBATCH --cpus-per-task=8              # 8 CPUs per task
#SBATCH --mem-per-cpu=4096             # 4GB memory per CPU (total: 32GB per job)
#SBATCH --mail-type=END,FAIL           # Email on job completion or failure
#SBATCH --mail-user=2362707@swansea.ac.uk

# Load required modules
module load anaconda/2023.09
module load compiler/gnu/12/1.0
module load mpi/openmpi/4.1.5

# Activate conda environment
source activate /scratch/s.2362707/swansea/ 

# Set number of OpenMP threads
export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK

# Create logs directory if it doesn't exist
mkdir -p logs

# Configuration parameters
TOTAL_FUNCTIONS=92                    # Total number of w(a) functions
FUNCTIONS_PER_JOB=10                   # Number of functions per job array element
CLASS_PATH="/scratch/s.2362707/VCDM/class_gen4_w_wa_vcdm-3.2.1"
OUTPUT_BASE="/scratch/s.2362707/VCDM/class_gen4_w_wa_vcdm-3.2.1/chains_noSN/multi_function_analysis"

# Calculate function range for this job
START_FUNC=$(( SLURM_ARRAY_TASK_ID * FUNCTIONS_PER_JOB ))
END_FUNC=$(( START_FUNC + FUNCTIONS_PER_JOB - 1 ))

# Make sure we don't exceed total functions
if [ $END_FUNC -ge $TOTAL_FUNCTIONS ]; then
    END_FUNC=$(( TOTAL_FUNCTIONS - 1 ))
fi

echo "==================================================="
echo "SLURM Job Array Information:"
echo "  Job Array ID: $SLURM_ARRAY_JOB_ID"
echo "  Task ID: $SLURM_ARRAY_TASK_ID"
echo "  Total Array Jobs: $SLURM_ARRAY_TASK_COUNT"
echo "  Function Range: $START_FUNC to $END_FUNC"
echo "  CLASS Path: $CLASS_PATH"
echo "  Output Base: $OUTPUT_BASE"
echo "==================================================="

# Run the Python script for this range of functions
echo "Starting VCDM multi-function analysis..."
echo "Command: python run_full_final.py --functions $START_FUNC-$END_FUNC --force"

python run_full_final.py \
    --functions $START_FUNC-$END_FUNC \
    --force \
    2>&1 | tee "logs/vcdm_${SLURM_ARRAY_TASK_ID}_detailed.log"

# Capture exit code
EXIT_CODE=$?

echo "==================================================="
echo "Job completion status:"
if [ $EXIT_CODE -eq 0 ]; then
    echo "  Status: SUCCESS"
    echo "  All functions in range [$START_FUNC, $END_FUNC] completed successfully"
else
    echo "  Status: FAILED (exit code: $EXIT_CODE)"
    echo "  Some functions in range [$START_FUNC, $END_FUNC] failed"
fi
echo "  Detailed log: logs/vcdm_${SLURM_ARRAY_TASK_ID}_detailed.log"
echo "==================================================="

exit $EXIT_CODE
