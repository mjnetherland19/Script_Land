#!/bin/env python3

import re
import sys

Key={}
with open("/data/genovi_key.csv","r") as fil:
    for c,k in enumerate(fil):
        line=k.strip().split(",")
        letter=line[0]
        rest=",".join(line[1:])

        Key[letter] = rest

path=sys.argv[1] #"85_Rise_4/download/Rise-002_subsample/genovi"
name=sys.argv[2] #"Rise-002"

with open(f"{path}/genovi_COG_Classification.csv","r") as rep:
    for r in rep:
        if re.search("Replicon",r):
            keys=r.strip().split(",")[1:]
        elif re.search("Total",r):
            total=r.strip().split(",")[1:]
        elif re.search("Percentage",r):
            perc=r.strip().split(",")[1:]

genovi_table=[["COG","Function of genes","Number of genes","% of total"]]
for c,letter in enumerate(keys):
    temp=[letter,Key[letter],total[c],perc[c]]
    genovi_table.append(temp)

with open(f"{path}/{name}_genovi_table.csv","w") as tab:
    for x in genovi_table:
        string=""
        for y in x:
            string+=f'"{y}",'
        tab.write(f"{string[:-1]}\n")
