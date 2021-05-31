import argparse
# from pathlib import Path
import logging
import logging.config
import pickle

logging.config.fileConfig('config/logging/local.conf')
logger = logging.getLogger('penny-lane-pipeline')

import pandas as pd

from src.upload import upload
from src.downloadSource import downloadSource
from src.createDB import createDB
import src.cleanFull as cf
import src.getModel as gm
from config.flaskconfig import SQLALCHEMY_DATABASE_URI

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description = "Scrape Data and upload data to S3/Create DB")
    subparser = parser.add_subparsers(dest='subparser_name')

    sb_createdb = subparser.add_parser("createDB", description = "Create Database")
    sb_createdb.add_argument("--engine_string", default=SQLALCHEMY_DATABASE_URI,
                           help="SQLAlchemy connection URI for database")

    sb_datatos3 = subparser.add_parser("loadData", description = "Put data into S3 bucket")
    sb_datatos3.add_argument("BUCKETNAME", help="Name of S3 Bucket")
    sb_datatos3.add_argument("S3PATH", help="path to S3 Bucket")
    sb_datatos3.add_argument("--FILEPATH", default = "data/external/data.csv", help="name of data to upload")
    sb_datatos3.add_argument("--INPUT1",default = "https://www.sportsbookreviewsonline.com/scoresoddsarchives/nfl/nfl%20odds%20", help="Begining part of path")
    sb_datatos3.add_argument("--INPUT2",default = ".xlsx", help="end of path")
    sb_datatos3.add_argument("--OUTPUTPATH", default = "data/external/data.csv", help="name of output after download")

    sb_cleanData = subparser.add_parser("cleanData", description = "Put data into S3 bucket")
    sb_model = subparser.add_parser("model", description = "Put data into S3 bucket")

    args = parser.parse_args()
    sp_used = args.subparser_name

    if sp_used == "createDB":
        createDB(args.engine_string)
        #createDB('sqlite:///data/msia423_db.db')
    elif sp_used == "loadData":
        downloadSource(args.INPUT1, args.INPUT2, args.OUTPUTPATH)
        upload(args.BUCKETNAME, args.FILEPATH, args.S3PATH)
    elif sp_used == "cleanData":
        data = pd.read_csv('data/data.csv')
        data2007 = cf.seasonSummary(2007, data)
        data2008 = cf.seasonSummary(2008, data)
        data2009 = cf.seasonSummary(2009, data)
        data2010 = cf.seasonSummary(2010, data)
        data2011 = cf.seasonSummary(2011, data)
        data2012 = cf.seasonSummary(2012, data)
        data2013 = cf.seasonSummary(2013, data)
        data2014 = cf.seasonSummary(2014, data)
        data2015 = cf.seasonSummary(2015, data)
        data2016 = cf.seasonSummary(2016, data)
        data2017 = cf.seasonSummary(2017, data)
        data2018 = cf.seasonSummary(2018, data)
        data2019 = cf.seasonSummary(2019, data)
        data2020 = cf.seasonSummary(2020, data)

        frames = [data2007, data2008, data2009, data2010, data2011, data2012, data2013
         , data2014, data2015, data2016, data2017, data2018, data2019, data2020]

        allSeasons = cf.allSeason(frames)
        allSeasons = cf.noPush(allSeasons)
        allSeasons = cf.fixNames(allSeasons, "home")
        allSeasons = cf.fixNames(allSeasons, "away")
        allSeasons = cf.onHot(allSeasons)

        target, features = cf.splitFeatures(allSeasons)
        target.to_csv('data/target.csv')
        features.to_csv('data/features.csv')
        print(target.head())
        print(features.head())

    elif sp_used == "model":

        target = pd.read_csv('data/target.csv', index_col=0)
        features = pd.read_csv('data/features.csv', index_col=0)
        rf, X_test, y_test = gm.createModel(features, target)
        accuracy = gm.scoreModel(rf, X_test, y_test)

        print(accuracy)
        print(list(features.columns))

        with open('models/model.pkl','wb') as f:
            pickle.dump(rf,f)

    else:
        parser.print_help()


