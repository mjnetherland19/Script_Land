import ast
import os
import re
import pandas as pd
from newt_search import *

class Meal:
    def __init__(self,name):
        self.name=name
        self.data={}
        #Will eventually replace the hard-coded RDI values with an API call to calculate per user
        self.rdi=rdi={"Fiber":(21,"g"),"Vitamin A":(700,"ug"),"Vitamin C":(75,"mg"),"Vitamin D":(15,"ug"),
         "Vitamin B-6":(1.5,"mg"),"Vitamin E": (15,"mg"),"Vitamin K":(90,"ug"),"Sugar":(25,"g"),
         "Thiamin":(1.1,"mg"),"Vitamin B-12":(2.4,"ug"),"Riboflavin":(1.1,"mg"),
         "Folate":(400,"ug"),"Niacin":(14,"mg"),"Choline":(425,"mg"),"Pantothenic acid":(5,"mg"),
         "Biotin":(30,"ug"),"Calcium":(1200,"mg"),"Copper":(0.9,"mg"),"Iron":(8,"mg"),"Magnesium":(320,"mg"),
         "Manganese":(1.8,"mg"),"Phosphorus":(700,"mg"),"Selenium":(55,"ug"),"Sodium":(1500,"mg"),"Potassium":(2600,"mg"),
         "Zinc":(8,"mg"),"Cholesterol":(300,"mg"),"Lysine":(2.38,"g"),"Histidine":(0.748,"g"),"Isoleucine":(2.856,"g"),
         "Leucine":(3.74,"g"),"Methionine":(0.8568,"g"),"Phenylalanine":(2.856,"g"),"Threonine":(1.292,"g"),"Tryptophan":(0.272,"g"),
         "Valine":(3.196,"g"),"Fat":(30,"g"),"Protein":(65,"g"),"Energy":(2500,"kcal"),"Carbohydrate":(300,"g")}

    def update_data(self,food_name,food_dict):
        self.data.update({food_name:food_dict})
        return
    def make_meal_df(self):
        #Make self.data into pandas dataframe 'self.meal_df'

        food_newts=[]
        food_names=[]
        newts=None

        for key in self.data.keys():
            food_names.append(key)
            ser = pd.Series(data=self.data[key], index=list(self.data[key].keys()))
            food_newts.append(ser)

        total_food_data_df=pd.concat(food_newts,axis=1).fillna(0.0)
        total_food_data_df.columns=food_names
        
        return total_food_data_df
    
    def getTotal(self,flag=True):
        #View the total newts and DV% so far
        df=self.make_meal_df()
        
        cols=list(df.columns)
        idx=list(df.index)

        df["Total"]=df.sum(axis=1)
        df["DV%"]=df[cols].sum(axis=1)

        new_cols=list(df.columns)

        tot_idx=new_cols.index("Total")
        dv_idx=new_cols.index("DV%")

        for c,v in enumerate(idx):
            df.iloc[c,tot_idx]=str(round(df.iloc[c,tot_idx],2))+self.rdi[v][1]
            df.iloc[c,dv_idx]=(df.iloc[c,dv_idx]/self.rdi[v][0])*100
        
        if flag:
            display(df)
            return
        if not flag:
            return df.T
    
    def saveMeal(self):
        order=["Energy","Fat","Carbohydrate","Sugar","Fiber","Sodium","Protein","Lysine","Histidine",
            "Isoleucine","Leucine","Methionine","Phenylalanine","Threonine","Tryptophan","Valine",
            "Cholesterol","Choline","Vitamin A","Vitamin B-12","Vitamin B-6","Thiamin","Pantothenic acid",
            "Riboflavin","Niacin","Folate","Biotin","Vitamin C","Vitamin D","Vitamin E","Vitamin K","Calcium",
            "Phosphorus","Potassium","Iron","Copper","Manganese","Magnesium","Zinc","Selenium"]
        
        df=self.getTotal(flag=False)
        df2=df[order]
        
        df2.T.to_excel(f"{self.name}.xlsx")
    

def makeMeal(meal):
    while True:                
        food = input("Enter a food to add to your meal.\nEnter 0 to exit this meal.\nEnter \'get\' to see the total so far.\n")
        if food == '':
            continue
        elif food.isdigit():
            if food == "0":
                return 0
        elif food.isalpha():
            food=food.lower()
            if food=="get":
                if len(meal.data)==0:
                    print("No data to show.")
                else:
                    meal.getTotal()
            else:
                food_number,food_name=newt_search(food,meal.rdi)

                if food_number == 0:
                    continue
                else:                        

                    amount=int(input(f"How many grams of {food_name} do you want to use?"))

                    amount_used={key:round((amount*value)/100,2) for (key,value) in zip(food_number.keys(),food_number.values())}

                    meal.update_data(food_name,amount_used)
        else:
            continue

def main():
    flag=False
    while True:
        if flag:
            break
        name=input("Give a name to your meal.\n")
        meal=Meal(name)

        while True:

            makeMeal(meal)            
            break

        while True:
            print("Save meal    1.")
            print("Abandon meal 2.")
            saveMeal=input("Enter 1 or 2 \n").lower()

            if saveMeal == "" or saveMeal.isalpha():
                continue
            elif saveMeal=='1':
                meal.saveMeal()
                flag=True
                break
            elif saveMeal=='2':
                newMeal=input("Do you want to create another meal? [Y/N]\n").lower()
                if newMeal=='':
                    continue
                elif newMeal == "n":
                    flag=True
                    break
                elif newMeal == "y":
                    break
                else:
                    continue


if __name__ == "__main__":
    main()  
