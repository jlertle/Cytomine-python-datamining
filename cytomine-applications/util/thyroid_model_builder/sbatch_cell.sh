#!/bin/bash
#SBATCH --job-name=cell_model_train
#SBATCH --output=/home/mass/GRD/r.mormont/out/training/cell_out.res
#SBATCH --ntasks=8
#SBATCH --cpus-per-task=1
#SBATCH --time=24:00:00
#SBATCH --mem=16G
#SBATCH --partition=Cytomine
bash /home/mass/GRD/r.mormont/sftp/cytomine-applications/thyroid_model_builder/train_cell.sh