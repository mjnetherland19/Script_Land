#!/bin/bash

#arg 1 - dir with bins to prokka

assembly_file=$1
logfile=$2


eval "$(conda shell.bash hook)"
conda activate prokka_env

for x in ${assembly_file}/*
do
	name=$(basename $x | rev | cut -d. -f2- | rev)
	
	echo "RUNNING COMMAND PROKKA --OUTDIR ${name}_prokka --prefix $name $x $logfile"
	prokka --outdir ${name}_prokka --prefix $name $x &>> $logfile #$logfile &>> $logfile
done
