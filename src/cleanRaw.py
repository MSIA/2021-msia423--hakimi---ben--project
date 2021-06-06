import logging
import logging.config

import numpy as np


logger = logging.getLogger(__name__)
logger.setLevel("INFO")


def removePK(rowcount, data):
    """Turn "pk" games into 0 spread games & convert lines to np.int64"""
    try:
        i = 0
        while i < rowcount:
            if data['Open'][i]=="pk":
                data['Open'][i]=np.int64(0)
            elif type(data['Open'][i])==float:
                data['Open'][i]=np.int64(0)
            else:
                data['Open'][i]=np.int64(float((data['Open'][i])))
            i=i+1
        logger.info("Succesfully executed removePK cleaning step")
        return data
    except:
        logger.error("Unable to run removePK cleaning operation")


def oneLine(rowcount, data):
    """Move Data into one line"""
    try:
        data['Team_2']=""
        data['Final_2']=0
        data['Open_2']=0
        data['ML_2']=0
        i = 0
        while i < rowcount:
            data['Team_2'][i] = data['Team'][i+1] 
            data['Final_2'][i] = data['Final'][i+1] 
            data['Open_2'][i] = data['Open'][i+1] 
            data['ML_2'][i] = data['ML'][i+1] 
            i = i+2
        logger.info("Succesfully executed oneLine cleaning step")
        return data
    except:
        logger.error("Unable to run oneLine cleaning operation")

def findFavored(rowcount, data):
    """Determine favored team"""
    try:
        data['Fav'] = "V"
        i = 0
        while i < rowcount:
            if data['Open'][i] > data['Open_2'][i]:
                data['Fav'][i] = "H"
            i = i+2
        logger.info("Succesfully executed findFavored cleaning step")
        return data
    except:
        logger.error("Unable to run findFavored cleaning operation")

def correctSpread(rowcount, data):
    """Get correct Spread"""    
    try:
        data['Spread'] = data['Open_2']
        i = 0
        while i < rowcount:
            if data['Fav'][i] == "V":
                data['Spread'][i] = data['Open'][i]
            i = i+2
        logger.info("Succesfully executed correctSpread cleaning step")
        return data
    except:
        logger.error("Unable to run correctSpread cleaning operation")

def homePick(rowcount, data):
    """Home team selected as favorite in pick-ems"""  
    try:
        i = 0
        while i < rowcount:
            if data['Spread'][i] == 0:
                data['Fav'][i] = "H"
            i = i+2
        logger.info("Succesfully executed homePick cleaning step")
        return data
    except:
        logger.error("Unable to run homePick cleaning operation")

def whoCovered(rowcount, data):
    """Determine which team covered"""
    try:
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
        logger.info("Succesfully executed whoCovered cleaning step")
        return data
    except:
        logger.error("Unable to run whoCovered cleaning operation")

def homeSpread(rowcount, data):
    """Get spread in terms of home team"""
    try:
        data['homeSpread'] = data['Spread']
        i = 0
        while i < rowcount:
            if data['Fav'][i] == "H":
                data['homeSpread'][i] = data['Spread'][i]*(-1)
            i = i+2
        logger.info("Succesfully executed homeSpread cleaning step")
        return data
    except:
        logger.error("Unable to run homeSpread cleaning operation")
    

def tidyUp(data):
    """Reduce Data to onle line per game and only take regular season data"""
    try:
        ## Reduce to one line per game
        dataUse = data[data['VH']=='V']
        dataUse.reset_index(drop=True)
        
        ## Get Regular Season Data and Rename Columns
        dataRegSeason = dataUse[['Date','Team','Team_2','Fav','Spread','Diff','H_cov','homeSpread']][0:256]
        dataRegSeason.columns = ['Date','V_Team','H_Team','Favorite','Spread','H_diff','Home_Cover','homeSpread']
        logger.info("Succesfully executed tidyUp cleaning step")
        return dataRegSeason
    except:
        logger.error("Unable to run tidyUp cleaning operation")