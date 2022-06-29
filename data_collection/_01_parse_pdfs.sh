#!/bin/bash
#SBATCH --job-name=revArray
#SBATCH --nodes=1 --ntasks=1
#SBATCH --output=logs/test_%A_%a.out
#SBATCH --error=logs/test_%A_%a.err
#SBATCH --array=0-9

python 01_parse_pdfs.py -i $SLURM_ARRAY_TASK_ID -p data -g ../grobid-0.7.1/

