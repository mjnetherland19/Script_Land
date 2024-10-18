#!/bin/bash

sp_genomes=$1
outdir=$2
logfile=$3

eval "$(conda shell.bash hook)"
conda activate parsnp1.7.4

parsnp -c -r ! -d ${sp_genomes} -p 1 -o ${outdir} --vcf &>> ${logfile}

conda deactivate
