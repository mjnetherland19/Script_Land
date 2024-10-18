#!/bin/bash

line=$1
logfile=$2
plasmidfinder_args=$3

eval "$(conda shell.bash hook)"
conda activate plasmidfinder

plasmidfinder.py -i assembly/${line}.fasta -o plasmidfinder_out $plasmidfinder_args &>> $logfile

conda deactivate
