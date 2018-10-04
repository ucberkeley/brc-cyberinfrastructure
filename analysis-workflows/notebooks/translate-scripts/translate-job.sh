#!/bin/bash
# Job name: 
#SBATCH --job-name=google-translate
#
# Account:
#ACCOUNT --account=ac_scsguest
#
# Partition:
#SBATCH --partition=savio
#
# Wall clock limit:
#SBATCH --time=00:01:00
#
## Command(s) to run:
module load python/3.6
source activate translate_env
export PYTHONIOENCODING="utf-8"
ipython $HOME/brc-cyberinfrastructure/analysis-workflows/notebooks/GoogleTranslateAPI.py
