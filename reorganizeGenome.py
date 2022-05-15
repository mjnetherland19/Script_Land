import sys
import re

#This script will find the loci name that you wish for the genome to begin with, as specified
#by 'targetLoci', cut the preceding nucleotides, and add them to the end

#Genome to be rearranged
inputGenome = sys.argv[1]
#Output file name
outputGenome = sys.argv[2]
#.bed file of loci starting and ending numbers, in a format needed to be used by the bedtools getfasta command
formattedBed = sys.argv[3]
targetLoci = sys.argv[4]
#The length of nucleotides per line in the input genome file
seq_length= sys.argv[5];

Loci=""
chunk=[]
Loci=""
with open(formattedBed, "r") as bed:
    for line in bed:
	if re.search(f"{tagetLoci}",line):
	    bedLine=y.split("\t")
	    justBeforeLoci=int(bedLine[1])-1
	    lociStart = int(bedLine[1])
	    lociEnd = int(bedLine[2])

#Load genome into list
with open(f"{inputGenome}","r") as genome:
	genomeLines=[line.strip() for line in genome]

#Produce string to hold the sequences that come before target loci
remainderLength = (justBeforeLoci % seq_length)
remainderIndex = int(justBeforeLoci / seq_length)+1
times = int(justBeforeLoci / seq_length)

for r in range(1,times):
	chunk.append(genomeLines[r])

chunk.append(genomeLines[remainderIndex][:remainderLength+1])

#The partial nucleotides from the line containing the target loci and the preceding loci
Loci_first=genomeLines[remainderIndex][(remainderLength+1):]

#The variables below are only important for concatenating the lines
#of the target sequence for output, so that it can be verified that
#indeed the reorganized genome now begins with the target loci
Loci_Length = lociEnd = lociStart
Loci_rest = Loci_Length - len(Loci_first)
Loci_times = (times + 2) + (int(Loci_rest / seq_length))
Loci_remainder = (Loci_remainder % seq_length)

with open(f"{outputGenome}","w") as reorgi, open("targetLoci.toverify","w") as target:
	#Write the genome header
	reorg.write(genomeLines[0]+"\n")

	#Write the partial nucleotides from the line containing the
	#target loci and the preceding loci
	reorg.write(Loci_first)

	#Write the rest of the genome
	for r in range((times+2),len(genomeLines)):
		reorg.write(genomeLines[r])

	#Attach the sequences taken from the beginning, to the end
	for seq in chunk:
		reorg.write(seq)

	#String containing the target loci will be written to a file
	Loci+=Loci_first
	for r in range((times+2),Loci_times):
		Loci+=genomeLines[r]
	Loci+=genomeLines[Loci_times+1][:Loci_remainder]
	target.write(Loci)
