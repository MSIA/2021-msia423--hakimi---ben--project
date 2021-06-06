import logging
import logging.config

import pandas as pd


logger = logging.getLogger(__name__)
logger.setLevel("INFO")


def downloadSource(inputPath1, inputPath2, outputPath):

    """
    Downloads the xlxs file from sportsbookreviewonline.com and saves locally as specified to a csv

    Args:
        inputPath1: (String), Required, first half of data link 
        inputPath2: (String), Required, second half of data link
        outputPath: (String), Required, name of the finished, local data path and file once data has been retrieved

    Returns:
        None

    """

    try:
        url_part1 = inputPath1 # "https://www.sportsbookreviewsonline.com/scoresoddsarchives/nfl/nfl%20odds%20"
        url_part2 = inputPath2 #".xlsx"

        ## function creates the full url string with year information and gets that data
        def loaddata(n):

            """ Creates proper year string to add to path to download the data """
        
            year1 = n
            year2 = n+1

            ## account for differences in year formats
            if (n<9):
                year1Str = '200'+str(year1)
                year2Str = '0'+str(year2)
            elif (n==9):
                year1Str = '200'+str(year1)
                year2Str = str(year2)
            else:
                year1Str = '20'+str(year1)
                year2Str = str(year2)
            
            url = url_part1+year1Str+'-'+year2Str+url_part2
            yearData = pd.read_excel(url)
        
            yearData['year']=int(year1Str)
        
            return yearData

        ## get all data from 2007-2020
        df_ls = [loaddata(i) for i in range(7,21)]
        df_full = pd.concat(df_ls)
        df_full

        ## output csv
        df_full.to_csv(outputPath, encoding='utf-8', index=False)

        logger.info("xlsx document %s%s succesfully downloaded from source", inputPath1, inputPath2)

    except:
        logger.error("Failed to download xlsx document %s%s, please check inputs", inputPath1, inputPath2)



    
