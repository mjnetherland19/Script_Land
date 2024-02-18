#!/bin/env python3

from sklearn.metrics import balanced_accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import mean_absolute_error,accuracy_score, confusion_matrix, classification_report, roc_curve, RocCurveDisplay,roc_auc_score
import pandas as pd
import sys
from sklearn.model_selection import train_test_split
import numpy as np

def metrics(val_y,predict):
    cm=confusion_matrix(val_y,predict))
    disp = ConfusionMatrixDisplay(confusion_matrix=cm)
    disp.plot()
    plt.show()

def plotImportance(importa,name,auc):
    fig, ax = plt.subplots(figsize=(20,2), dpi=200)
    
    importa.plot.bar(ax=ax)    
    ax.set_title(f"Feature importances using MDI\nAUC: {auc}")
    ax.set_ylabel("Mean decrease in impurity")
    
    fig.savefig(f"RF_importance.png",bbox_inches="tight")

    plt.close()

def xs_y(df,conts,dep):
    xs=df[conts].copy()
    return xs,df[dep] if dep in df else None

def runForest(fullest,conts,response):

    trn_df,val_df = train_test_split(fullest, test_size=0.25)

    trn_xs,trn_y = xs_y(trn_df,conts,response)
    val_xs,val_y = xs_y(val_df,conts,response)

    rf = RandomForestClassifier(350, min_samples_leaf=5,max_features="sqrt")
    rf.fit(trn_xs, trn_y)

    #Extract importance values of features
    importances = rf.feature_importances_
    importa = pd.DataFrame(importances, index=trn_xs.columns,columns=['Import'])
    importa=importa.sort_values(by='Import',ascending=False)
    importa=importa.loc[~(importa==0).all(axis=1)]
    
    #Get prediction values
    proba=rf.predict_proba(val_xs)[:, 1]
    predict=rf.predict(val_xs)
    
    #Get accuracy values
    roc_auc = roc_auc_score(val_y,proba)
    rounded=round(roc_auc,2)
    balanced=round(balanced_accuracy_score(val_y, predict),2)
    
    #Get RF importance plot
    plotImportance(importa,rounded)
    #Get Confusion Matrix
    metrics(val_y,predict)
    #Get ROC curve plot   
    fpr, tpr, _ = roc_curve(val_y,  proba)
    rocDisplay=RocCurveDisplay(fpr=fpr, tpr=tpr).plot()

    return importa

d={}
df=pd.read_csv(sys.argv[1],index_col=0).fillna(0.0)
response=sys.argv[2]

#Encode response variable choices as 0 and 1
for count,option in enumerate(list(df[response].unique())):
    df.replace(option,count,inplace=True)
    df.replace(option,count,inplace=True)

conts=list(df.columns)
conts.remove(response)

#Run Random Forest
imp=runForest(df,conts,response)

#Write importances to file
imp_list=list(imp["Import"])
with open(f"RF_importance.csv","w") as rank:
    for c,x in enumerate(imp.index):
        rank.write(f"{x},{imp_list[c]}\n")
