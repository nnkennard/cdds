#!/bin/bash
#SBATCH --job-name=revArray
#SBATCH --nodes=1 --ntasks=1
#SBATCH --output=logs/test_%A_%a.out
#SBATCH --error=logs/test_%A_%a.err
#SBATCH --array=0-9

python 00_download_from_openreview.py -i $SLURM_ARRAY_TASK_ID -p data
