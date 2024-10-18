# netherCode
Here you can find examples of my code.

## NCBI Isolate ID (NIID pipeline)
Pronounced NEED. This is a pipeline for bacterial isolate identification that does not require a specific database, using only NCBI. Its accuracy depends on the use of core gene (UBCG2) and 16S (HMM built from NCBI Targeted Loci database) extraction and subsequent BLAST against NCBI's nt or nr database. Verification of BLAST hits is conducted with ANI (OrthoANI) and core-genome SNP analysis (Parsnp). Genomes are automatically downloaded from NCBI for use in verification using Esearch (Entrez Direct Utilities).

## Other scripts

randome_forest.py: Runs a Random Forest model with scikit-learn and outputs model importance, confusion matrix, and ROC curve plots

enterotype.cluster.R: Calculates and ordinates the Jensen-Shannon distance metric from a metagenomic taxa relative abundance matrix and finds the optimum clustering via PAM clustering, Calinski-Harabasz (CH) Index, and silhouette validation. Outputs CH index and silhouette plots of k cluster values.
