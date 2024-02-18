
suppressPackageStartupMessages(library(broom.mixed))
suppressPackageStartupMessages(library(dplyr))
suppressPackageStartupMessages(library(lme4))
suppressPackageStartupMessages(library(optimx))
suppressPackageStartupMessages(library(lme4))
suppressPackageStartupMessages(library(dplyr))
suppressPackageStartupMessages(library(pROC))

check.allFit=function(model)
{	

	allfit=allFit(model)

	sum.allfit=summary(allfit)

	print("Model log-likelihoods")
	print(sum.allfit$llik)

	#https://stackoverflow.com/questions/70537291/lmer-model-failed-to-converge-with-1-negative-eigenvalue
	print("NLL_rel: negative log-likelihood relative to the best fit")
	print(glance(allfit) |> select(optimizer, AIC, NLL_rel) |> arrange(NLL_rel))

	print("Look here to see if all the \"good\" models have similar parameter values.")
	print("If so, then ignoring convergence warnings is often permitted")

	print(tidy(default.optim.allfit, conf.int = TRUE) |> arrange(effect, term, estimate) |> select(-c(std.error, statistic)),n=50)

}

#This program will perform GLMM training in a loop testing different nAGQ values
#The resulting model will be tested with allFit to understand the best optimizer for each model
#You will also recieve outputs of model summary, prediction, and validation AUC

args = commandArgs(trailingOnly=TRUE)

#Training dataset
trn=read.csv(args[1],row.names=1)
#Validation dataset
val=read.csv(args[2],row.names=1)
#Number of random factors in dataset - the columns with random factor values need to be at the end of your dataframe - this includes the reponse variable column
num_rand_factors=args[3]
#Name of the reponse column
response=args[4]
#String of random variables formula
random_str=args[5]

print("Files read")

num=length(colnames(trn))-num_rand_factors
form=as.formula(paste(response,"~",paste(colnames(trn)[0:num],collapse="+"),random_str))
print(form)

print("Start Loop")

for (k in 15:20){
	print(k)
    	model1=glmer(form,data = trn, family = binomial,control=glmerControl(optimizer="bobyqa",optCtrl=list(maxfun=2e5)),nAGQ=k)
    	saveRDS(model1, file = paste("model_",k,".rds",sep=""))
	
	print(summary(model1))
	
	check.allFit(model1)
    	
	model1.predict <- predict(model1,newdata=val,type="response",allow.new.levels=T)
    	print(model1.predict)
    	
	model1.auc = auc(val$Healthy,model1.predict)
    	print(model1.auc)
}
