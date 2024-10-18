#if 'need larger value of 'ncol' as pivoting occurred', comment out by="axis" lines


suppressPackageStartupMessages(library(vegan))
suppressPackageStartupMessages(library(DESeq2))


forward <- function(fwd.form) {
  
	fwd.rda=eval(fwd.form)

	fwd.square=RsquareAdj(fwd.rda)
	fwd.anova=anova.cca(fwd.rda, step = 1000)
	fwd.term=anova.cca(fwd.rda, step = 1000,by="term")
	#fwd.axis=anova.cca(fwd.rda, step = 1000,by="axis")
	print("Forward-Selected Model")
	print(fwd.form)
	#print("Forward-Selected Summary")
	#print(summary(fwd.rda))
	print("Forward-Selected Model Adjusted R-squared")
	print(fwd.square)
	print("Forward-Selected Model ANOVA")
	print(fwd.anova)
	print("Forward-Selected Model ANOVA: Variables")
	print(fwd.term)
	#print("Forward-Selected Model ANOVA: Axes")
	#print(fwd.axis)
	
	perc <- round(100*(summary(fwd.rda)$cont$importance[2, 1:2]), 2)
	
	png(file="fwd_rda_scale1.png",width=600, height=600)
	plot(fwd.rda, scaling = 1, type = "text",main = "Forward-Selected Model RDA - Type 1 Scaling",xlab = paste0("RDA1 (", perc[1], "%)"), ylab = paste0("RDA2 (", perc[2], "%)"))
	dev.off()

	png(file="fwd_rda__scale2.png",width=600, height=600)
	plot(fwd.rda, scaling = 2, type = "text",main = "Forward-Selected - Type 2 Scaling",xlab = paste0("RDA1 (", perc[1], "%)"), ylab = paste0("RDA2 (", perc[2], "%)"))
	dev.off()
}

do_rda <- function(sp,env) {

	noFwd="rda(formula = sp ~ 1, data = env, na.action = na.omit)"
	print("Get RDA model")
	wet.rda=rda(formula=sp ~ .,data=env,na.action=na.omit)
	print("Get R squared")
	square=RsquareAdj(wet.rda)
	print("Get forward selected")
	fwd.sel <- ordiR2step(rda(sp ~ 1, data = env,na.action=na.omit), scope = formula(wet.rda),direction = "forward",R2scope = TRUE, pstep = 1000,trace = FALSE)
	fwd.form <- fwd.sel$call
	print("Forward Form")
	print(fwd.form)
	wet.anova=anova.cca(wet.rda, step = 1000)

	wet.term=anova.cca(wet.rda, step = 1000,by="term")

	#wet.axis=anova.cca(wet.rda, step = 1000,by="axis")

	#print("Total Model Summary")
	#print(summary(wet.rda))
	print("Total Model Adjusted R-squared")
	print(square)
	print("Total Model ANOVA")
	print(wet.anova)
	print("Total Model ANOVA: Variables")
	print(wet.term)
	#print("Total Model ANOVA: Axes")
	#print(wet.axis)

	perc <- round(100*(summary(wet.rda)$cont$importance[2, 1:2]), 2)
	
	png(file="rda_scale1.png",width=600, height=600)
	plot(wet.rda, scaling = 1, type = "text",main = "Full Model RDA - Type 1 Scaling",xlab = paste0("RDA1 (", perc[1], "%)"), ylab = paste0("RDA2 (", perc[2], "%)"))
	#ordiplot(wet.rda, scaling = 1, type = "text")
	dev.off()

	png(file="rda_scale2.png",width=600, height=600)
	plot(wet.rda, scaling = 2, type = "text",main = "Full Model RDA - Type 2 Scaling",xlab = paste0("RDA1 (", perc[1], "%)"), ylab = paste0("RDA2 (", perc[2], "%)"))
	#ordiplot(wet.rda, scaling = 2, type = "text")
	dev.off()

	if (fwd.form != noFwd ){
		forward(fwd.form)
	}else{
		print("No useful forward-selected model")
	}

	print("Conducted RDA")

}

do_permanova <- function(dist,meta) {
	data.perm=adonis2(data.dist~., data=meta, permutations=999, by="terms", na.action=na.omit)
	write.table(data.perm,"permanova.out")
}

do_envfit <- function(ord,meta) {
	envfit=envfit(ord,meta,permutations=999,na.rm=T)
	print(envfit)
}

test_dispersion <- function(){
	disper=betadisper(data.dist,env.scaled)
	disper.test=permutest(disper.test,pariwise=T)
	write.table(disper,"dispersion.out")
	write.table(disper.test,"dispersion_permutest.out")

}

args = commandArgs(trailingOnly=TRUE)

sp = read.csv(args[1],row.names=1,check.names=F)
print("Read taxa")
env = read.csv(args[2],row.names=1)
print("Read environment")
#print(str(env))

env.scaled=as.data.frame(scale(env))

print("Loaded Data")
print("File used for Abundance Matrix")
print(args[1])
print("File used for Environmnetal Matrix")
print(args[2])

data.dist=vegdist(sp,method="bray")
bray.ord=cmdscale(as.matrix(data.dist))

do_rda(sp,env.scaled)
do_permanova(data.dist,env.scaled)
do_envfit(bray.ord,env.scaled)
