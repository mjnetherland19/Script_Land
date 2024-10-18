#!/bin/bash

prefix=$1
ref=$2
query=$3

eval "$(conda shell.bash hook)"
conda activate mummer4

nucmer -p $prefix $ref $query

show-tiling -c -p assembly/${line}.fasta ${prefix}.delta
