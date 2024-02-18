#!/usr/bin/env Rscript

#Code adapted from: https://enterotype.embl.de/enterotypes.html

#"Unassigned" genera fraction is not used in the calculation of the Jensen-Shannon Distance.

#For the JSD function to work the data table must be in the format: Samples as columns and taxa abundance as rows. The first row can be labels (?)

#arg 1 - taxa relative abundance matrix: Data table format needs to be samples as columns, genus as rows, if not then t()
#arg 2 - PCoA coordinate output file name
#arg 3 - png file name
#arg 4 - "best" or "else"

args = commandArgs(trailingOnly=TRUE)

suppressPackageStartupMessages(library(cluster))

#for index.G1
suppressPackageStartupMessages(library(clusterSim))

#For obs.pco() and s.class()
suppressPackageStartupMessages(library(ade4))

pcoa <- function(data.dist,data.cluster,file) #Ordinate and save coordinates and cluster labels
{	
	obs.pcoa=dudi.pco(data.dist, scannf=F, nf=3) #nf=X specifies the number of principal components
	forMatPlot=cbind(obs.pcoa$li,data.cluster)
	write.csv(forMatPlot, file=file)
} 

#Function to create metric version of JSD
dist.JSD <- function(inMatrix, pseudocount=0.000001, ...)
{
	KLD <- function(x,y) sum(x *log(x/y))
	JSD<- function(x,y) sqrt(0.5 * KLD(x, (x+y)/2) + 0.5 * KLD(y, (x+y)/2))
	
	matrixColSize <- length(colnames(inMatrix))
	matrixRowSize <- length(rownames(inMatrix))
	
	colnames <- colnames(inMatrix)
	resultsMatrix <- matrix(0, matrixColSize, matrixColSize)
        
  	inMatrix = apply(inMatrix,1:2,function(x) ifelse (x==0,pseudocount,x))

	write("Begin new matrix", stdout())
	write(dim(inMatrix), stdout())
	for(i in 1:matrixColSize)
	{
		
		for(j in 1:matrixColSize)
		{ 
			resultsMatrix[i,j]=JSD(as.vector(inMatrix[,i]),as.vector(inMatrix[,j]))
		}
	}

	colnames -> colnames(resultsMatrix) -> rownames(resultsMatrix)

	write(dim(resultsMatrix), stdout())
	write("Made new matrix", stdout())

	as.dist(resultsMatrix)->resultsMatrix
	attr(resultsMatrix, "method") <- "dist"
	return(resultsMatrix) 
 }
 
 # x is a distance matrix and k the number of clusters
 pam.clustering=function(x,k) 
 {
    require(cluster)
    cluster = as.vector(pam(x, k, diss=TRUE,cluster.only=TRUE))
    return(cluster)
 }


data = read.csv(args[1], row.names=1)
#data=t(data)
data.dist=dist.JSD(data)
write.csv(as.matrix(data.dist), file=paste0(args[2],"_jsd_distance_matrix.csv"))

nclusters=NULL
sil=NULL
for (k in 1:10)
{ 
    if (k==1)
    {
	    nclusters[k]=NA 
    } 
    else
    {
	data.cluster_temp=pam.clustering(data.dist, k)
	nclusters[k]=index.G1(t(data),data.cluster_temp,  d = data.dist, centrotypes = "medoids")

	obs.silhouette=mean(silhouette(data.cluster_temp, data.dist)[,3])
	sil[k]=obs.silhouette
    }
}

png(paste0(args[2],"_CH.png"), width=600, height=350)
plot(nclusters, type="h", xlab="# clusters", ylab="CH Index")
dev.off()

png(paste0(args[2],"_Silhouette.png"), width=600, height=350)
plot(nclusters, type="h", xlab="# clusters", ylab="Silhouette Coefficient")
dev.off()

#Save best cluster
best.ch=match(max(nclusters,na.rm=TRUE),nclusters)
best.sil=match(max(sil,na.rm=TRUE),sil)

if (best.ch == best.sil)
{
	data.cluster=pam.clustering(data.dist, best.ch)
	pcoa(data.dist,data.cluster,paste0(args[2],"_CH_coords.csv"))
}else
{
	data.cluster=pam.clustering(data.dist, best.ch)
	pcoa(data.dist,data.cluster,paste0(args[2],"_CH_coords.csv"))
	
	data.cluster=pam.clustering(data.dist, best.sil)
	pcoa(data.dist,data.cluster,paste0(args[2],"_Silhouette_coords.csv"))

}
