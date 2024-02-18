args = commandArgs(trailingOnly=TRUE)

suppressPackageStartupMessages(library(cluster))

#for index.G1
suppressPackageStartupMessages(library(clusterSim))

#For obs.pco() and s.class()
suppressPackageStartupMessages(library(ade4))

#args 1 = distance matrix
#args 2 = prefix for output files

pam.clustering=function(x,k) 
{
	require(cluster)
	cluster = as.vector(pam(x, k, diss=TRUE,cluster.only=TRUE))
	return(cluster)
}

pcoa <- function(data.dist,data.cluster,file) #Ordinate and save coordinates and cluster labels
{	
	obs.pcoa=dudi.pco(data.dist, scannf=F, nf=3) #nf=X specifies the number of principal components
	forMatPlot=cbind(obs.pcoa$li,data.cluster)
	write.csv(forMatPlot, file=file)
} 

data = read.csv(args[1], row.names=1)
data.dist=as.dist(read.csv(args[2],row.names=1))

nclusters=NULL
sil=NULL

for (k in 1:5)
{ 
    if (k==1)
    {
	    nclusters[k]=NA
	    sil[k]=NA
    } 
    else
    {
	data.cluster_temp=pam.clustering(data.dist, k)
	nclusters[k]=index.G1(t(data),data.cluster_temp,  d = data.dist, centrotypes = "medoids")

	obs.silhouette=mean(silhouette(data.cluster_temp, data.dist)[,3])
	sil[k]=obs.silhouette
    }
}

png(paste0(args[3],"_CH.png"), width=600, height=350)
plot(nclusters, type="h", xlab="# clusters", ylab="CH Index")
dev.off()

png(paste0(args[3],"_Silhouette.png"), width=600, height=350)
plot(sil, type="h", xlab="# clusters", ylab="Silhouette Coefficient")
dev.off()

#Save best cluster
best.ch=match(max(nclusters,na.rm=TRUE),nclusters)
best.sil=match(max(sil,na.rm=TRUE),sil)

print(nclusters)
print(sil)

print(best.ch)
print(best.sil)

if (best.ch == best.sil)
{
	data.cluster=pam.clustering(data.dist, best.ch)
	pcoa(data.dist,data.cluster,paste0(args[3],"_CH_coords.csv"))
}else
{
	data.cluster=pam.clustering(data.dist, best.ch)
	pcoa(data.dist,data.cluster,paste0(args[3],"_CH_coords.csv"))
	
	data.cluster=pam.clustering(data.dist, best.sil)
	pcoa(data.dist,data.cluster,paste0(args[3],"_Silhouette_coords.csv"))

}
