import pandas as pd
import numpy as np

def downloadSource(inputPath1, inputPath2, outputPath):

    url_part1 = inputPath1 # "https://www.sportsbookreviewsonline.com/scoresoddsarchives/nfl/nfl%20odds%20"
    url_part2 = inputPath2 #".xlsx"

    def loaddata(n):
    
        year1 = n
        year2 = n+1
    
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

    df_ls = [loaddata(i) for i in range(7,21)]
    df_full = pd.concat(df_ls)
    df_full

    df_full.to_csv(outputPath, encoding='utf-8', index=False)



    



