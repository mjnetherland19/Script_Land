#!/bin/sh

grab()
{

    	num_genomes=$2
    
	python3 filter_records.py $1
	
	num_records=$(wc -l records_filt.tsv)
	
	if [ $num_records -lt $num_genomes ]
    	then
        	num_genomes=${num_records}
    	fi
	
	python3 best_genome.py records_filt.tsv $num_genomes
	
	sed -i '1d' temp_best
	
	cat temp_best | cut -d, -f5 > curated_accessions
	cat temp_best >> genomes.records
	
	strain=$(cat temp_best | cut -d, -f3-4)
	
	echo $strain

}	

download_genomes()
{
	while read ftp; do
		#$ftp = ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/024/668/725/GCA_024668725.3_ASM2466872v3
		genome_name=$(echo $ftp | rev | cut -d/ -f1 | rev) #GCA_024668725.3_ASM2466872v3
		
		#Replace ftp with https, put into var
		var="https${ftp:3}"
		
		#Get the record file
		rec=$(wget -qO- $var)
		assembly_link=$(echo $rec | grep -Po "(?<=>)${genome_name}_genomic.fna.gz")
		
		wget ${var}/${assembly_link} #to filename = ${assembly_link::-3}
		gunzip $assembly_link
		
		assembly_link=${assembly_link::-3}
	
		change=$(echo ${strain//,/ })
		name=$(echo ${change// /_})

		mv ${assembly_link} "${out}/${name}.fasta"
	done<curated_accessions
}

query_ncbi()
{
	
	name=$1
	esearch -db assembly -query "${name}" < /dev/null | efetch -format docsum | xtract -pattern DocumentSummary -def "N/A" -element SpeciesTaxid -element SpeciesName -element Sub_value -element FtpPath_GenBank -element assembly-status -element FromType -element RefSeq_category -division Meta -block Stats -element Stat > temp.tsv
}

list=$1
out=$2
#Number of genomes to download
if [ -z $3 ]
then
	num=1
else
	num=$3
fi

if [ ! -f $out ]
then
	mkdir $out
fi

while read line
do
	query_ncbi "${line}"
	
	grep "from type" temp.tsv > type_strains
	num1=$(wc -l type_strains | cut -d" " -f1)
	if [ $num1 -eq 0 ]
	then
		grep "represent" temp.tsv > ref_strains
		num2=$(wc -l ref_strains | cut -d" " -f1)
		if [ $num2 -eq 0 ]
		then
			grep "Complete Genome" temp.tsv > complete_strains
			num3=$(wc -l complete_strains | cut -d" " -f1)
			if [ $num3 -eq 0 ]
			then
				grep "Chromosome" temp.tsv > chrom_strains
				num4=$(wc -l chrom_strains | cut -d" " -f1)
				if [ $num4 -eq 0 ]
				then
					grep "Scaffold" temp.tsv > scaff_strains
					num5=$(wc -l scaff_strains | cut -d" " -f1)
					if [ $num5 -eq 0 ]
					then
						grep "Contig" temp.tsv > contig_strains
						num6=$(wc -l contig_strains | cut -d" " -f1)
						if [ $num6 -eq 0 ]
						then
							echo $line
						else
							grab contig_strains $num
						fi
					else
						grab scaff_strains $num
					fi
				else
					grab chrom_strains $num
				fi
			else
				grab complete_strains $num
			fi
		else
			grab ref_strains $num
		fi
	else
		grab type_strains $num
	fi
	
	download_genomes
	
done<${list}
