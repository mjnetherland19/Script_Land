# netherCode
Here you can find examples of my code.

## Uploaded 2024

Meal_Planning.py and newt_search.py: for the manual querying of the USDA nutritional database for meal planning and diet formulation. Eventually I will turn it into a Kivy app, but for now it is quite plain. You will need to register your own API key with the USDA and add it to the code.

glmm_loop_and_allFit.R: for GLMM model training, validation, and diagnosis of convergence issues with the lme4 R package

colinearity.py: Calculates the colinearity between predictor variables with the Variance Inflation Factor(VIF) and iteratively removes variables with the highest VIF and recalculates for total VIF to determine if the iterative removal should continue 

randome_forest.py: Runs a Random Forest model with scikit-learn and outputs model importance, confusion matrix, and ROC curve plots

enterotype.cluster.R: Calculates and ordinates the Jensen-Shannon distance metric from a metagenomic taxa relative abundance matrix and finds the optimum clustering via PAM clustering, Calinski-Harabasz (CH) Index, and silhouette validation. Outputs CH index and silhouette plots of k cluster values.

find_optimum_pam_cluster.R: Extracted method from enterotype.cluster.R to find the optimum clustering of any input distance matrix

## Uploaded 2022

chloroplast_assembly_pipeline: a bash script that outlines the methods of assembling a draft chloroplast genome

cleanCript: a bash script that cleans and assembles RNA-seq reads. 

getClient.py: Test script to access the client list from a local Senaite install

getInParalogsNuc.py: Identifies the presence of out-paralog sequences from Newick phylogenetic trees

importSamples.py: A simple GUI that allows the user to pick the Client and Contact and imports their sample data from and Excel file into Senaite

reorganizeGenome.py: Finds a locus given a .bed file and removes the nucleotides preceding the locus and appends them to the bottom of the genome. I should think this is suitable for chromosomes as well. It was developed for chloroplast genomes.
