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
        data = data[data[yearCol]==year] 
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
    except TypeError:
        logger.error("An invalid data type was input into the seasonSummary cleaning function") 
        raise TypeError 
    except:
        logger.error("Unable to run seasonSummary cleaning operation for dataset w/ year=%s", str(year))

def allSeason(list):
    """Concat List of dataframes"""
    try:
        allSeasonData = pd.concat(list)
        allSeasonData = allSeasonData.reset_index(drop=True)
        logger.info("Succesfully executed allSeason cleaning step for datasets in %s", list)
        return allSeasonData
    except TypeError:
        logger.error("An invalid data type was input into the allSeason cleaning function") 
        raise TypeError 
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
        data = data[data[colName]!=2] 
        data = data.reset_index(drop=True)
        logger.info("Succesfully executed noPush cleaning step for dataset")
        return data
    except TypeError:
        logger.error("An invalid data type was input into the noPush cleaning function") 
        raise TypeError 
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
                if data[homeCol][i]=="BuffaloBills":
                    data[homeCol][i]="Buffalo"
                elif data[homeCol][i]=="LasVegas" or data[homeCol][i]=="Oakland":
                    data[homeCol][i]="LVRaiders"
                elif data[homeCol][i]=="SanDiego":
                    data[homeCol][i]="LAChargers"
                elif data[homeCol][i]=="SanDiego":
                    data[homeCol][i]="LAChargers"
                elif data[homeCol][i]=="Washingtom":
                    data[homeCol][i]="Washington"
                elif data[homeCol][i]=="LosAngeles" or data[homeCol][i]=="St.Louis":
                    data[homeCol][i]="LARams"
                elif data[homeCol][i]=="HoustonTexans":
                    data[homeCol][i]="Houston"
                elif data[homeCol][i]=="NewYork":
                    data[homeCol][i]="NYGiants"
                elif data[homeCol][i]=="Tampa":
                    data[homeCol][i]="TampaBay"
                elif data[homeCol][i]=="Kansas" or data[homeCol][i]=="KCChiefs":
                    data[homeCol][i]="KansasCity"
                i = i+1    
        elif side == "away":
            i = 0
            while i < numLines:
                if data[roadCol][i]=="BuffaloBills":
                    data[roadCol][i]="Buffalo"
                elif data[roadCol][i]=="LasVegas" or data[roadCol][i]=="Oakland":
                    data[roadCol][i]="LVRaiders"
                elif data[roadCol][i]=="SanDiego":
                    data[roadCol][i]="LAChargers"
                elif data[roadCol][i]=="SanDiego":
                    data[roadCol][i]="LAChargers"
                elif data[roadCol][i]=="Washingtom":
                    data[roadCol][i]="Washington"
                elif data[roadCol][i]=="LosAngeles" or data[roadCol][i]=="St.Louis":
                    data[roadCol][i]="LARams"
                elif data[roadCol][i]=="HoustonTexans":
                    data[roadCol][i]="Houston"
                i = i+1    
        logger.info("Succesfully executed fixNames cleaning step for the %s teams in dataset", side)
        return data
    except TypeError:
        logger.error("An invalid data type was input into the fixNames cleaning function") 
        raise TypeError 
    except:
        logger.error("Unable to run fixNames cleaning operation for the %s teams in dataset", side)

def onHot(data, homeCol, roadCol, usefulList):
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
        useful = data[usefulList]
        useful[roadCol] = useful[roadCol] + "V"
        oneHotV = pd.get_dummies(useful[roadCol])
        useful = useful.drop(roadCol,axis = 1)
        useful = pd.concat([useful, oneHotV], axis = 1)
        oneHotH = pd.get_dummies(useful[homeCol])
        useful = useful.drop(homeCol,axis = 1)
        useful = pd.concat([useful, oneHotH], axis = 1)
        if (len(usefulList) > 1):
            logger.info("Succesfully executed oneHot cleaning step for dataset")
            return useful
        elif (len(usefulList) == 1):
            logger.warning("noPush cleaning step was used on dataset and only one column was saved")
            return useful
        elif (len(usefulList) == 0):
            logger.warning("noPush cleaning step was used on dataset and an empty dataframe was saved")
            return useful
    except TypeError:
        logger.error("An invalid data type was input into the oneHot cleaning function") 
        raise TypeError 
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
        target = data[targetName]
        features = data.drop(targetName,axis = 1)
        logger.info("Succesfully executed splitFeatures cleaning step for dataset")
        return target, features
    except TypeError:
        logger.error("An invalid data type was input into the splitFeatures cleaning function") 
        raise TypeError 
    except:
        logger.error("Unable to run splitFeatures cleaning operation for dataset")