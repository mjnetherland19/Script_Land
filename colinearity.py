#!/bin/env python3

import pandas as pd
import sys
from sklearn.linear_model import LinearRegression

#'df' must have samples as rows and predictors as columns

def calculate_vif(dff, features):
    vif, tolerance = {}, {}    # all the features that you want to examine
    for feature in features:
        # extract all the other features you will regress against
        X = [f for f in features if f != feature]
        X, y = dff[X], dff[feature]        # extract r-squared from the fit
        r2 = LinearRegression().fit(X, y).score(X, y)
        if r2 == 1.0:
            r2=0.9999999999999999
        # calculate tolerance
        tolerance[feature] = 1 - r2        # calculate VIF
        vif[feature] = 1/(tolerance[feature])    # return VIF DataFrame
    return pd.DataFrame({'VIF': vif, 'Tolerance': tolerance})

df = pd.read_csv(sys.argv[1],index_col=0)
df=df.abs()
cols=list(df.columns)
#Output directory
out=sys.argv[2]

#Get all predictors' VIF
print("First colin")
vif_df=calculate_vif(dff=df, features=cols)
vif_df.to_csv(f"{out}/all_vif.csv")
vif_df=vif_df.reset_index().rename(columns={"index":"preds"})

#Grab all highly correlated features
preds=[]
for count, i in enumerate(vif_df["VIF"]):
    if i >=5:
        idx=vif_df["preds"].iloc[count]
        preds.append(idx)

#Iteratively test the imporvement of the sum of VIF by eliminating predictors sequentially
if len(preds) > 0:
    cur=preds[0]
    nex=preds[1]
    with open(f"{out}/vif_sums_atEachStage.txt","w") as sums:
        Cur=cols.copy()
        Cur.remove(cur)
        print("Second colin")
        cur_df=calculate_vif(dff=df, features=Cur)
        #cur_df.to_csv("{out}/cur_df.csv")
        curSum=cur_df['VIF'].sum()
        sums.write(f"{cur}\n")
        sums.write(f"{curSum}\n")

        Nex=cols.copy()
        Nex.remove(nex)
        print("Third colin")
        nex_df=calculate_vif(dff=df, features=Nex)
        #nex_df.to_csv("{out}/nex_df.csv")
        nexSum=nex_df['VIF'].sum()
        sums.write(f"{nex}\n")
        sums.write(f"{nexSum}\n")

        if curSum < nexSum:
            cols.remove(nex)
            Iter=cur
            iterSum=curSum
        else:
            cols.remove(cur)
            Iter=nex
            iterSum=nexSum

        for i in range(2,len(preds)):
            Preds=cols.copy()
            Preds.remove(preds[i])
            print(f"{i} colin")
            test_df=calculate_vif(dff=df, features=Preds)
            #test_df.to_csv(f"{out}/test_df_{i}.csv")
            sumTest=test_df['VIF'].sum()
            print(sumTest)
            sums.write(f"{preds[i]}\n")
            sums.write(f"{sumTest}\n")
            if sumTest < iterSum:
                cols.remove(Iter)
                iterSum=sumTest
                Iter=preds[i]
            else:
                cols.remove(preds[i])
#Save final VIF table
test_df.to_csv(f"{out}/final_vif_{i}.csv")

#Save reduced dataframe, having been sanitized of colinear predictors
final=df[cols]
final.to_csv(f"{out}/df_no_colinear.csv")
