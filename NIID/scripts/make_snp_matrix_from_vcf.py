#!/bin/env python3

import pandas as pd
import re
import matplotlib.pyplot as plt
import seaborn as sns
import sys

#arg1 = vcf file path
#arg2 = outfile path
#arg3 = list of names to order figure

taxa_names=[]
d={}
flag=False
out=sys.argv[2]

with open(sys.argv[1],"r") as sea:
    for x in sea:
        if re.search("CHROM",x):
            flag = True
            line=x.split()
            taxa=line[9:]
            for i in range(len(taxa)):
                #Get list of taxa names for matrix creation later and to use as columns in 'dff'
                taxa_names.append(taxa[i])
                #Make combination names
                for y in taxa:
                    if taxa[i] == y:
                        continue
                    else:
                        d[f"{taxa[i]}+{y}"]=0
            continue
        #Get SNP counts
        sub=[]
        if flag:
            line=x.split()[9:]
            for i in range(0,len(line)):
                for j in range(0,len(line)):
                    if i==j:
                        continue
                    if line[i] != line[j]:
                        d[f"{taxa_names[i]}+{taxa_names[j]}"]+=1
                        d[f"{taxa_names[j]}+{taxa_names[i]}"]+=1
                    else:
                        continue

            #for l in line:
                #if l == "1":
                    #sub.append(taxa_names[line.index(l)])
                    #for s in sub:
                        #for key in d.keys():
                            #if re.search(s,key):
                                #d[key]+=1

df={}
df_list=[]

#Create list of zeros for snp count substitution later on
for i in range(0,len(taxa_names)):
    df_list.append(0)

#Give each list to a dictionary key that is each taxon
for tax in taxa_names:
    df[tax]=df_list.copy()
    
for key in d.keys():
    list_key,name=key.split('+')
    df[list_key][taxa_names.index(name)]=d[key]

#with open(sys.argv[3],"r") as names:
#    Taxa_names=[nam.strip() for nam in names]

length=len(taxa_names)
taxa_names.reverse()

dff=pd.DataFrame.from_dict(df, orient='index',columns=taxa_names)
df2=dff[taxa_names]
df3=df2.reindex(taxa_names)
df3.rename(columns={x:x.split('.')[0] for x in taxa_names},inplace=True)
df3.rename(index={x:x.split('.')[0] for x in taxa_names},inplace=True)

df3.to_csv(f'{out}_snp_matrix.csv')

shape=20
if length >= 10:
    shape = 30
if length >= 15:
    shape = 35

sns.set(font_scale=2.0)
fig, ax = plt.subplots(figsize=(shape,shape), dpi=250)
ax = sns.heatmap(
    data=df3,
    cmap='Blues',
    square=True,
    annot=True,
    fmt='g',
    yticklabels=False,
    linecolor="black",
    cbar=False
)
for t in ax.texts:
    t.set_text('{:,d}'.format(int(t.get_text())))

plt.xticks(fontsize = 35)
#plt.ylabel('Reference')
#plt.xlabel('Query')
plt.title('Total Number of SNPs', fontsize=35)
plt.savefig(f'{out}_snps_matrix.png', bbox_inches='tight')
