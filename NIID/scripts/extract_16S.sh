#!/bin/bash


path="/data/databases/bacteria_16S_HMM"
script_dir="/home/mike_netherland/Script_Land/extract_ribosomal"

contigs=$1

name=$(echo $contigs | cut -d. -f1)

nhmmscan --dfamtblout ${name}.res --noali ${path}/bacteria_16S.hmm $contigs >/dev/null

res=$(python3 ${script_dir}/parse_hmmer.py ${name}.res)
echo $res
seq=$(echo $res | cut -d, -f1)
strand=$(echo $res | cut -d, -f2)

samtools faidx $contigs ${seq} > ${name}_16S.fasta

#python3 rename.py fasta_18S/${name}_18S.fasta $strand
