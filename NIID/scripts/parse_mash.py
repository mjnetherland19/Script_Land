import sys

i=100
target=""
with open("mash.out","r") as mash:
    for m in mash:
        line=m.split(",")
        num=float(line[-3])
        if num < i:
            i=num
            target=line[0]
print(target)
