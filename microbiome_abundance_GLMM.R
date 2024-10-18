suppressPackageStartupMessages(library(lme4))
suppressPackageStartupMessages(library(car))
suppressPackageStartupMessages(library(dplyr))

save.f <- function(M,taxon,save){
    t3 <-Anova(M,type="III")
    summary=summary(M)

    sink(paste(taxon,"_",save,"_anova.txt",sep=""))
    print(t3)
    sink()

    sink(paste(taxon,"_",save,"_summary.txt",sep=""))
    print(summary)
    sink()
    
}

overdisp_fun <- function(model) {
    rdf <- df.residual(model)
    rp <- residuals(model,type="pearson")
    Pearson.chisq <- sum(rp^2)
    prat <- Pearson.chisq/rdf
    pval <- pchisq(Pearson.chisq, df=rdf, lower.tail=FALSE)
    res=c(chisq=Pearson.chisq,ratio=prat,rdf=rdf,p=pval)
    print(res)
}

#Takes a list of target taxa and a count matrix as input

args = commandArgs(trailingOnly=TRUE)

taxa_list <- scan(args[1], what = "character") 
taxa.df=read.csv(args[2],row.names=1,check.names=F)

taxa.df.log=taxa.df

for (taxa in taxa_list){
    print(taxa)

    taxa.df$Treatment <- as.factor(taxa.df$Treatment)
    taxa.df$Time <- as.factor(taxa.df$Time)
    taxa.df$Period <- as.factor(taxa.df$Period)
    taxa.df$Sequence <- as.factor(taxa.df$Sequence)
    taxa.df$ID <- as.factor(taxa.df$ID)
   
    form=formula(paste(taxa,"~ Treatment + Period + Sequence + (1|ID)"))
    carry=formula(paste(taxa,"~ Treatment*Period + (1|ID)"))
		       
    model.poisson = glmer(form, data = taxa.df,family=poisson)
    model.nb = glmer.nb(form, data = taxa.df)
    
    #Fit a Log-Normal Model
    taxa.df.log$X <- 1:nrow(taxa.df)

    form.lognormal=formula(paste(taxa,"~ Treatment + Period + Sequence + (1|ID) + (1|X)"))
		       
    model.lognormal = glmer(form.lognormal, data = taxa.df.log,family=poisson)

    overdisp_fun(model.lognormal)
    save.f(model.lognormal,taxa,"Log_Normal")
    
    overdisp_fun(model.poisson)
    save.f(model.poisson,taxa,"Poisson")
    
    overdisp_fun(model.nb)
    save.f(model.nb,taxa,"NB")
    
}
