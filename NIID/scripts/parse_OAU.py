import pandas as pd
import re
import json
import glob
import sys
import seaborn as sns
import matplotlib.pyplot as plt

flag=0
dic2={}
Taxonomy={}

g=sys.argv[1]

#Output type
output=sys.argv[2]
target=sys.argv[3]

ani=0
strain=""

if output == "matrix":
    with open("melt.csv","w") as melt:
        melt.write(f"Query,Subject,Ident\n")
elif output == "table":
    with open("table.csv","w") as Table:
         Table.write(f"Taxa,Taxonomy,Ident,Query,Reference\n")

prefix=g.split("/")[-1].split(".")[0]

with open(g,"r") as f:
    for x in f:
        if re.search("{",x):
            d2 = json.loads(x)

for k,v in d2.items():
    if type(v) == type(list()):
        continue
    else:
        pairing = v

taxa=set()
for k,v in d2.items():
    if type(v) == type(list()):
        for pos in v:
            for key,value in pos.items():
                if re.search("pair",key):
                    pair=str(value)
                    both=pairing[pair]
                    Query,Subject=both.split("|")
                    
                    Q=".".join(Query.strip().split(".")[:-1])
                    S=".".join(Subject.strip().split(".")[:-1])
                
                taxa.add(Q)
                taxa.add(S)

                if key == "queryCoverage":
                    query=round(value,2)
                elif key == "orthoaniValue":
                    ident=round(value,2)
                    if re.search(target,Q):
                        if ident > ani:
                            ani=ident
                            strain=S
                    else:
                        if ident > ani:
                            ani=ident
                            strain=Q
                elif key == "subjectCoverage":
                    subj=round(value,2)
                
        
            if output == "matrix":
                with open("melt.csv","a") as melt:
                    melt.write(f"{Q},{S},{ident}\n")
                    melt.write(f"{S},{Q},{ident}\n")
            elif output == "table":
                print("Printing from json")
                with open("table.csv","a") as Table:
                    if S_acc in Taxonomy.keys():
                        Table.write(f"{S},{Taxonomy[S_acc].strip()},{ident},{query*100},{subj*100}\n")
                    else:
                        Table.write(f"{dic2[global_acc]},{Taxonomy[global_acc].strip()},{ident},{query*100},{subj*100}\n")

with open("target","w") as tar:
    tar.write(strain)

if output == "matrix":
    with open("melt.csv","a") as melt:
        for t in taxa:
            melt.write(f"{t},{t},{100.0}\n")

df=pd.read_csv("melt.csv")
matrix=df.pivot_table(index="Query",columns="Subject",values="Ident").fillna(0)
matrix.to_csv(f"orthoani_matrix.csv")

Taxa_names=list(taxa)

Taxa_names.reverse()
df2=matrix[Taxa_names]
df3=df2.reindex(Taxa_names)

sns.set(font_scale=2.5)
fig, ax = plt.subplots(figsize=(20,20))
ax = sns.heatmap(
    data=df3,
    cmap='Greens',
    square=True,
    annot=True,
    fmt='g',
    yticklabels=True,
    linecolor="black",
    cbar=False
)
plt.xticks(fontsize = 35,rotation=90)
plt.ylabel("")
plt.xlabel("")
plt.title('OrthoANI Values')
plt.savefig('orthoani_matrix.png', bbox_inches='tight')
