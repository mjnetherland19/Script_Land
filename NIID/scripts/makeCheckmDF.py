#!/bin/env python3

import sys
import re

#Isolate ID | Completeness | Contamination | Strain Heterogeneity

with open(sys.argv[1],"r") as report, open(sys.argv[2],"a") as assem:
    for x in report:
        line=x.strip().split()
        if re.search("UID",x):
            samp=line[0]
            comp=line[-3]
            cont=line[-2]
            strain=line[-1]
            assem.write(f"{samp},{comp},{cont},{strain}\n")
