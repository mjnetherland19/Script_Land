#!/bin/env python3

import sys
import re
search=re.compile("Complete|Scaffold|Contig|Chromosome|ftp")
with open(sys.argv[1],"r") as rec, open("records_filt.tsv","w") as filt:
    for r in rec:
        line=r.split("\t")
        if not search.search(line[3]):
            for c,v in enumerate(line):
                if search.search(v):
                    Line=line[:2]+[line[c-1]]+line[c:]
                    break
            newline=",".join(Line)
            filt.write(newline)
        else:
            filt.write(",".join(line))
