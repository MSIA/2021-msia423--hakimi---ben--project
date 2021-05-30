import logging

import numpy as np
import pandas as pd

def removePK(rowcount, data):
    ## Turn "pk" games into 0 spread games & convert lines to np.int64
    i = 0
    while i < rowcount:
        if data['Open'][i]=="pk":
            data['Open'][i]=np.int64(0)
        elif type(data['Open'][i])==float:
            data['Open'][i]=np.int64(0)
        else:
            data['Open'][i]=np.int64(float((data['Open'][i])))
        i=i+1
    return data

def oneLine(rowcount, data):
    ## Turn "pk" games into 0 spread games & convert lines to np.int64
    data['Team_2']=""
    data['Final_2']=0
    data['Open_2']=0
    data['ML_2']=0
    ## Move data into one line
    i = 0
    while i < rowcount:
        data['Team_2'][i] = data['Team'][i+1] 
        data['Final_2'][i] = data['Final'][i+1] 
        data['Open_2'][i] = data['Open'][i+1] 
        data['ML_2'][i] = data['ML'][i+1] 
        i = i+2
    return data

def findFavored(rowcount, data):
    ## Determine favored team    
    data['Fav'] = "V"
    i = 0
    while i < rowcount:
        if data['Open'][i] > data['Open_2'][i]:
            data['Fav'][i] = "H"
        i = i+2
    return data

def correctSpread(rowcount, data):
    ## Get correct Spread    
    data['Spread'] = data['Open_2']
    i = 0
    while i < rowcount:
        if data['Fav'][i] == "V":
            data['Spread'][i] = data['Open'][i]
        i = i+2
    return data

def homePick(rowcount, data):
    ## Home team selected as favorite in pick-ems
    i = 0
    while i < rowcount:
        if data['Spread'][i] == 0:
            data['Fav'][i] = "H"
        i = i+2
    return data

def whoCovered(rowcount, data):
    ## Final score diff in terms of home team
    data['Diff'] = data['Final_2']-data['Final']
    
    ## If home team covered, H_cov = 1, if not = 0, if push = 2
    data['H_cov']=0
    i = 0
    while i < rowcount:
        if (data['Fav'][i] == "H") & ((data['Diff'][i]) > (data['Spread'][i])):
            data['H_cov'][i]=1
        elif (data['Fav'][i] == "V") & ((data['Diff'][i])*-1 < (data['Spread'][i])):
            data['H_cov'][i]=1
        elif (data['Fav'][i] == "H") & ((data['Diff'][i]) == (data['Spread'][i])):
            data['H_cov'][i]=2
        elif (data['Fav'][i] == "V") & ((data['Diff'][i])*-1 == (data['Spread'][i])):
            data['H_cov'][i]=2
        i = i+2
    return data

def homeSpread(rowcount, data):
    ## Get spread in terms of home team
    data['homeSpread'] = data['Spread']
    i = 0
    while i < rowcount:
        if data['Fav'][i] == "H":
            data['homeSpread'][i] = data['Spread'][i]*(-1)
        i = i+2
    return data

def tidyUp(data):
    ## Reduce to one line per game
    dataUse = data[data['VH']=='V']
    dataUse.reset_index(drop=True)
    
    ## Get Regular Season Data and Rename Columns
    dataRegSeason = dataUse[['Date','Team','Team_2','Fav','Spread','Diff','H_cov','homeSpread']][0:256]
    dataRegSeason.columns = ['Date','V_Team','H_Team','Favorite','Spread','H_diff','Home_Cover','homeSpread']
    return dataRegSeason