#!/bin/env python3

import sys
import json

g=sys.argv[1]

with open(g,"r") as f:
    res = json.load(f)

seq=""

for key in res["data"].keys():
    if len(res["data"][key]) > 0:
        seq+=res["data"][key][0]["dna"]

with open(f"concatenated_core_genes.fasta","w") as ind:
    ind.write(f">concat_contig\n")
    ind.write(f"{seq}\n")


