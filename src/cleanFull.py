import logging
import logging.config

import pandas as pd

import src.cleanRaw as cr


logger = logging.getLogger(__name__)
logger.setLevel("INFO")


def seasonSummary(year, data, yearCol):
    """
    Combine Intermediate Cleaning Functions from cleanRaw.py

    Args:
        year: (int), required, Year to get summary data for
        data: dataframe, required
        yearCol: (str), required, name of column where year is stored
    
    Returns:
        dataframe
    """
    try:
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
        logger.info("Succesfully executed seasonSummary cleaning step for dataset w/ year=%s", str(year))
        return data
    except:
        logger.error("Unable to run seasonSummary cleaning operation for dataset w/ year=%s", str(year))

def allSeason(list, dataname):
    """Concat List of dataframes"""
    try:
        allSeasonData = pd.concat(list)
        allSeasonData = allSeasonData.reset_index(drop=True)
        allSeasonData.name = "allSeasons"
        logger.info("Succesfully executed allSeason cleaning step for datasets in %s", list)
        return allSeasonData
    except:
        logger.error("Unable to run allSeason cleaning operation for datasets in %s", list)

def noPush(data, colName):
    """
    Removes data where outcome is a push

    Args:
        data: dataframe, required
        colName: (str), required, name of column where cover information is stored
    
    Returns:
        dataframe
    """
    try:
        data[data['Home_Cover']!=2]
        data = data.reset_index(drop=True)
        logger.info("Succesfully executed noPush cleaning step for dataset")
        return data
    except:
        logger.error("Unable to run noPush cleaning operation for dataset")

def fixNames(data, side, homeCol, roadCol):
    """
    Renames columns to account for teams moving/rebranding and human input errors

    Args:
        data: dataframe, required
        side: (str), required, home or away
        homeCol: (str), required, name of column where Home Team name is stored
        roadCol: (str), required, name of column where Road Team name is stored
    
    Returns:
        dataframe
    """
    try:
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
        logger.info("Succesfully executed fixNames cleaning step for the %s teams in dataset", side)
        return data
    except:
        logger.error("Unable to run fixNames cleaning operation for the %s teams in dataset", side)

def onHot(data, homeCol, roadCol):
    """
    Creates one hot encoded columns for all categorical variables

    Args:
        data: dataframe, required
        homeCol: (str), required, name of column where Home Team name is stored
        roadCol: (str), required, name of column where Road Team name is stored
        usefulList: list, required, list of column names to be used in modeling
    
    Returns:
        dataframe
    """
    try:
        useful = data[['V_Team', 'H_Team','homeSpread','Home_Cover']]
        useful['V_Team'] = useful['V_Team'] + "V"
        oneHotV = pd.get_dummies(useful['V_Team'])
        useful = useful.drop('V_Team',axis = 1)
        useful = pd.concat([useful, oneHotV], axis = 1)
        oneHotH = pd.get_dummies(useful['H_Team'])
        useful = useful.drop('H_Team',axis = 1)
        useful = pd.concat([useful, oneHotH], axis = 1)
        # if len(usefulList > 1):
        logger.info("Succesfully executed oneHot cleaning step for dataset")
        return useful
        # elif len(usefulList == 1):
        #     logger.warning("noPush cleaning step was used on dataset and only one column was used saved")
        # elif len(usefulList == 0):
        #     logger.warning("noPush cleaning step was used on dataset and an empty dataframe was saved")
    except:
        logger.error("Unable to run oneHot cleaning operation for dataset")

def splitFeatures(data, targetName):
    """
    Split data into input and response variables
    
    Args:
        data: dataframe, required, full dataframe
        targetName: (str), required, name of response variable column

    Returns:
        Two dataframes, one with response variable the other with input variables
    """
    try:
        target = data['Home_Cover']
        features = data.drop('Home_Cover',axis = 1)
        logger.info("Succesfully executed splitFeatures cleaning step for dataset")
        return target, features
    except:
        logger.error("Unable to run splitFeatures cleaning operation for dataset")