import sys
import re

def write_all():

    with open("temp_parsed_res","w") as temp:
        for key in rec.keys():
            temp.write(f"{rec[key]}\n")

def best():
    maxx=0
    lizt=list(math.keys())
    if len(lizt) == 1:
            print(f"{rec[lizt[0]]},{strand[lizt[0]]}")
    else:
        for key in math.keys():
            if maxx < math[key]:
                maxx=math[key]
                idx=rec[key]
                st=strand[key]
        print(f"{idx},{st}")

rec={}
math={}
strand={}
maxx=0

with open(sys.argv[1],"r") as out:
    for x in out:
        if re.search("NODE",x):
            #if re.search("\+",x):
            line=x.split()
            contig=line[2]
            start=int(line[-6])
            end=int(line[-5])
            stt=line[8]
            if start > end:
                temp=[start,end]
                start=temp[1]
                end=temp[0]
            rec[contig]=f"{contig}:{start}-{end}"
            math[contig]=float(line[3])
            strand[contig]=stt

if len(math.keys()) > 0:
    best()
