import re
import sys
#This script takes a list of file paths, each to a single gene tree, and identifies whether it contains outparalogous sequences. It will then output
#the file paths of inparalogous and outparalogous trees to the appropriate text file


#Used to recognize species names used in trees
species=re.compile("[A-z]{5,16}|[0-z]{2,3}_[A-z]{5,16}")
#Used to discard all information from tree that are not species names
Tree=re.compile(":0\.[0-9]{4,20}|:0.0|:[0-9]e\-[0-9]{2,3}|:[0-9]\.[0-9]{1,5}e\-[0-9]{2,3}:[0-9]\.[0-9]{1,20}|_TRINITY_DN[0-9]{1,5}_c[0-9]{1,5}_g[0-9]_i[0-9]{1,2}")

#newT=list of gene tree file paths, where the path contains one tree per file
newT=sys.argv[1]

with open(f"{newT}","r") as h:
    files=[Species.strip() for Species in h]

outPara=[]

for fil in files:
    dict1={}
    A=[]
    g=0
    flag="no"
    with open(fil, "r") as f:
        F=f.readlines()

    tree=F[0]
    tree=Tree.sub(tree)
    each=tree.split(',')

    #Add species names to dictionary key and use their frequencies as the value
    match=species.findall(tree)
    if match:
        for Species in match:
            if Species in dict1.keys():
                dict1[Species]+=1
            elif Species not in dict1.keys():
                dict1[Species]=0
    #Outparalog detection method #1
    #Creates a list of index values for where multi-species names are found in the tree.
    for Species in dict1:
        if flag=="yes":
            outPara.append(fil)
            break
        if dict1[Species] > 1:
            g=0
            for y in each:
                match=re.search(f"{Species}",y)
                if match:
                    A.append(g)
                g+=1
    #If there is a gap in the numbering, it should indicate that taxa have intervened and broken monophyly
            index=0
            while index < len(A)-1:
                if A[index] != A[index+1]-1:
                    flag="yes"
                    break
                index+=1
            A.clear()
            #Outparalog detection method #2
            #Finds the youngest sister taxa in a clade and checks if both species names match
            for z in dict1:
                one=re.search(f"{Species}\,{z}", tree)
                if one:
                    inclusive=one.group(0)
                    names=inclusive.split(',')
                    if names[0] != names[1]:
                        flag="yes"
                        break
    if flag == "no":
        with open("inparalogFiles.txt","a") as p:
            p.write(f"{fil}\n")
with open("outparalogFiles.txt","a") as out:
    for line in outPara:
        out.write(line+"\n")        
