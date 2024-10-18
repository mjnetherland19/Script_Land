#!/bin/env python3

import sys
import re

#Isolated ID | Assembly Length | # of Contigs | Longest Contig | GC% | N50

flags=re.compile("Assembly|Total length|# contigs|Largest contig|GC|N50")

with open(sys.argv[1],"r") as report, open("Assembly_Statistics.csv","a") as assem:
    for x in report:
        line=x.strip().split()
        if len(line) < 4:
            match=flags.search(x)
            if match:
                if match.group(0) == "N50":
                    assem.write(f"{line[-1]}\n")
                else:
                    assem.write(f"{line[-1]},")

