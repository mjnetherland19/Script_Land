#!/bin/bash

line=$1
logfile=$2
genovi_args=$3

eval "$(conda shell.bash hook)"
conda activate genovi

#SeqSero2_package.py -m k -t 2 -i R1.fastq.gz R2.fastq.gz
gbkfile=${line}
if [[ ! -f  $gbkfile ]]; then
    echo "The Prokka output's GBK file doesn't exist. Did you run Prokka?"
    exit
fi
genovi -i $gbkfile $genovi_args -s draft &>> $logfile

conda deactivate
