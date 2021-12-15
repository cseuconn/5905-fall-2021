#!/bin/bash
#SBATCH -N 1
#SBATCH -n 36
#SBATCH -p generalsky
module purge
module load gcc/9.2.0 libffi/3.2.1 bzip2/1.0.6 tcl/8.6.6.8606 sqlite/3.30.1 lzma/4.32.7 python/3.9.2
python3 E:/Cloud-Systems/Ramya-Nachiket/src/clustering_Kmeans.py