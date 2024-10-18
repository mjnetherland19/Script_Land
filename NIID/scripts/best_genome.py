#!/bin/env python3
import sys
import pandas as pd



df=pd.read_csv(sys.argv[1],sep=",",names=["Taxid","Species Name","Strain Name","FtpPath_GenBank","Asembly Status","Type Strain","Reference Genome","alt_loci_count","chromosome_count","contig_count","contig_l50","contig_n50","non_chromosome_replicon_count","replicon_count_all","scaffold_count_all","scaffold_count_placed","scaffold_count_unlocalized","scaffold_count_unplaced","scaffold_l50","scaffold_n50","total_length","ungapped_length"]).fillna("Empty")

num=sys.argv[2]
sub=["Taxid","Species Name","Strain Name","FtpPath_GenBank","Asembly Status","Type Strain","Reference Genome","scaffold_count_all"]

df2=df[sub]

df3=df2.sort_values("scaffold_count_all")

df4=df3.iloc[:int(num)]

df4.to_csv("temp_best",sep=",")
