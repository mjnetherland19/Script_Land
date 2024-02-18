import requests
import re
import sys
import ast
import pandas as pd

def newtSearch(query,rdi):

    rdi_list=list(rdi.keys())
    
    print(f"Searching USDA database for: {query}")
    
    #params = {"query":f"{query}","dataType":["Foundation","SR Legacy","Survey (FNDSS)","Branded"],"pageSize":200, "pageNumber":1}
    params = {"query":f"{query}","dataType":["Foundation","SR Legacy"],"pageSize":200, "pageNumber":1}

    r = requests.get("https://api.nal.usda.gov/fdc/v1/foods/search?api_key=YOUR_KEY_HERE",params=params)
    stat = r.status_code

    data=r.json()
    if data["totalHits"]==0:
        print("No foods match your query.")
        print("Check your spelling and try again.")
        
        return 0,0
    
    names=[]
    mem={}

    for attrib in data["foods"]:
        name=attrib["description"]
        newts=attrib["foodNutrients"]
        newtName="nutrientName"

        Name=name.split(',')
        
        if Name[0] not in mem.keys():
            mem[Name[0]]=[(name,newts)]
        else:
            mem[Name[0]].append((name,newts))

        keys=list(mem.keys())
    
    while True:
        #Get categories of query
        for count, value in enumerate(keys):
                foodName=keys[count]
                print(f"{count+1}. {foodName}")
        print()

        num=input("Enter the number of the category you would like to see food of or enter \'0\' to exit.\n")
        if num.isalpha() or num == '':
            continue
            
        print(f"You entered: {num}\n")
        
        if num == "0":
            return 0,0
        else:
            #Get subcategories
            num=int(num)-1
            sublist=mem[keys[num]]
            
            for c, v in enumerate(sublist):
                print(f"{c+1}: {v[0]}")
            
            #Choose subcategorey
            while True:
                #Used for Vitamin K
                vu=None
                vk=0 #Initialized to aggregate Vitamin K amounts

                foodDict={}
                
                while True:
                    foodSelect=input("Enter the number of the food you want to see nutrients for or enter 0 to exit.\n")
                    if foodSelect == '':
                        continue
                    if foodSelect.isdigit:
                        if int(foodSelect) < len(sublist)+1:
                            break
                        else:
                            continue
                
                if foodSelect=="0":
                    break
                
                singleNewts=mem[keys[num]][int(foodSelect)-1][1]
                foodName=mem[keys[num]][int(foodSelect)-1][0]
                
                print(f"Displaying the nutrients for 100g of {foodName}\n")
                
                for newtInfo in singleNewts:
                    newtName=newtInfo["nutrientName"]
                    
                    newtName=newtName.split(",")[0]
                    newtName=newtName.split("(")[0].strip()
                    
                    if re.search("Sugar",newtName):
                        newtName="Sugar"
                    
                    amount=newtInfo["value"]
                    unit=newtInfo["unitName"].lower()
                    
                    if unit == "iu": #Skip nutrients with Internation Units
                        continue
                        
                    if unit == "kj":
                        amount=round(amount/4.184,0)
                        unit = "kcal"
                    
                    if newtName not in foodDict.keys():
                        if amount and unit:
                            unit=unit.lower()
                            amountStr=f"{amount} {unit}"
                            if re.search("Total lipid",newtName) or re.search("Total fat",newtName):
                                foodDict.update({"Fat":amount})
                            
                            elif re.search("Vitamin K",newtName):
                                if vu:
                                    foodDict.update({"Vitamin K":vk})
                                else:
                                    vk+=amount
                                    vu=unit
                            elif newtName in rdi_list:
                                foodDict[newtName]=amount
                            
                            print(f"{newtName : <35}{amountStr : >10}")
                            
                #Impute zeros
                for key in rdi_list:
                    if key not in list(foodDict.keys()):
                        foodDict[key]=0.0
                
                while True:
                    add=input("Do you want to add this food to your meal? [Y/N]\n").lower()
                    if add == '':
                        continue
                    if add == "y":
                        return foodDict,foodName
                    elif add == "n":
                        for i in range(1, len(keys)):
                            foodName=keys[i-1]
                            print(f"{i}. {foodName}")
                        break
                    else:
                        continue
                break
