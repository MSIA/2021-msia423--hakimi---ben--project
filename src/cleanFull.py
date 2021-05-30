import logging

import numpy as np
import pandas as pd

import src.cleanRaw as cr

def seasonSummary(year, data):
    data = data[data['year']==year]
    data = data.reset_index(drop=True)
    rowcount = data.shape[0]
    data = cr.removePK(rowcount, data)
    data = cr.oneLine(rowcount, data)
    data = cr.findFavored(rowcount, data)
    data = cr.correctSpread(rowcount, data)
    data = cr.homePick(rowcount, data)
    data = cr.whoCovered(rowcount, data)
    data = cr.homeSpread(rowcount, data)
    data = cr.tidyUp(data)
    return data

def allSeason(list):
    allSeasonData = pd.concat(list)
    allSeasonData = allSeasonData.reset_index(drop=True)
    return allSeasonData

def noPush(data):
    data[data['Home_Cover']!=2]
    data = data.reset_index(drop=True)
    return data

###### RENAME FUNCTION
def fixNames(data, side):
    numLines = data.shape[0]
    if side == "home":
        i = 0
        while i < numLines:
            if data['H_Team'][i]=="BuffaloBills":
                data['H_Team'][i]="Buffalo"
            elif data['H_Team'][i]=="LasVegas" or data['H_Team'][i]=="Oakland":
                data['H_Team'][i]="LVRaiders"
            elif data['H_Team'][i]=="SanDiego":
                data['H_Team'][i]="LAChargers"
            elif data['H_Team'][i]=="SanDiego":
                data['H_Team'][i]="LAChargers"
            elif data['H_Team'][i]=="Washingtom":
                data['H_Team'][i]="Washington"
            elif data['H_Team'][i]=="LosAngeles" or data['H_Team'][i]=="St.Louis":
                data['H_Team'][i]="LARams"
            elif data['H_Team'][i]=="HoustonTexans":
                data['H_Team'][i]="Houston"
            elif data['H_Team'][i]=="NewYork":
                data['H_Team'][i]="NYGiants"
            elif data['H_Team'][i]=="Tampa":
                data['H_Team'][i]="TampaBay"
            elif data['H_Team'][i]=="Kansas" or data['H_Team'][i]=="KCChiefs":
                data['H_Team'][i]="KansasCity"
            i = i+1    
    elif side == "away":
        i = 0
        while i < numLines:
            if data['V_Team'][i]=="BuffaloBills":
                data['V_Team'][i]="Buffalo"
            elif data['V_Team'][i]=="LasVegas" or data['V_Team'][i]=="Oakland":
                data['V_Team'][i]="LVRaiders"
            elif data['V_Team'][i]=="SanDiego":
                data['V_Team'][i]="LAChargers"
            elif data['V_Team'][i]=="SanDiego":
                data['V_Team'][i]="LAChargers"
            elif data['V_Team'][i]=="Washingtom":
                data['V_Team'][i]="Washington"
            elif data['V_Team'][i]=="LosAngeles" or data['V_Team'][i]=="St.Louis":
                data['V_Team'][i]="LARams"
            elif data['V_Team'][i]=="HoustonTexans":
                data['V_Team'][i]="Houston"
            i = i+1    
    return data

def onHot(data):
    useful = data[['V_Team', 'H_Team','homeSpread','Home_Cover']]
    useful['V_Team'] = useful['V_Team'] + "V"
    oneHotV = pd.get_dummies(useful['V_Team'])
    useful = useful.drop('V_Team',axis = 1)
    useful = pd.concat([useful, oneHotV], axis = 1)
    oneHotH = pd.get_dummies(useful['H_Team'])
    useful = useful.drop('H_Team',axis = 1)
    useful = pd.concat([useful, oneHotH], axis = 1)
    return useful

def splitFeatures(data):
    target = data['Home_Cover']
    features = data.drop('Home_Cover',axis = 1)
    
    return target, features