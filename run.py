import argparse
import logging
import logging.config
import pickle

import pandas as pd
import yaml

from src.upload import upload, download
from src.downloadSource import downloadSource
from src.createDB import createDB
import src.cleanFull as cf
import src.getModel as gm
from config.flaskconfig import SQLALCHEMY_DATABASE_URI

logging.basicConfig(format='%(name)-12s %(levelname)-8s %(message)s', level=logging.DEBUG)
logger = logging.getLogger('run')

if __name__ == '__main__':

    # Load configuration file for parameters and to path
    with open('config/config.yaml', "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    configloadData = config["loadData"]
    configcleanData = config["cleanData"]
    configmodel = config["model"]

    parser = argparse.ArgumentParser(description = "Scrape Data and upload data to S3/Create DB")

    subparser = parser.add_subparsers(dest='subparser_name')

    sb_createdb = subparser.add_parser("createDB", description = "Create Database")
    sb_createdb.add_argument("--engine_string", default=SQLALCHEMY_DATABASE_URI,
                           help="SQLAlchemy connection URI for database")

    sb_datatos3 = subparser.add_parser("loadData", description = "Put data into S3 bucket")

    sb_cleanData = subparser.add_parser("cleanData", description = "Put data into S3 bucket")
    
    sb_model = subparser.add_parser("model", description = "Put data into S3 bucket")

    args = parser.parse_args()
    sp_used = args.subparser_name

    if sp_used == "createDB":
        createDB(args.engine_string)

    elif sp_used == "loadData":
        downloadSource(**configloadData['downloadSource'])
        upload(**configloadData['uploadtos3'])

    elif sp_used == "cleanData":
        download(**configcleanData['downloadfroms3'])
        data = pd.read_csv(configcleanData['readlocal']['localPath'])
        data2007 = cf.seasonSummary(configcleanData['seasonSummary']['year1'],
         data, configcleanData['seasonSummary']['colName'])
        data2008 = cf.seasonSummary(configcleanData['seasonSummary']['year2'],
         data, configcleanData['seasonSummary']['colName'])
        data2009 = cf.seasonSummary(configcleanData['seasonSummary']['year3'],
         data, configcleanData['seasonSummary']['colName'])
        data2010 = cf.seasonSummary(configcleanData['seasonSummary']['year4'],
         data, configcleanData['seasonSummary']['colName'])
        data2011 = cf.seasonSummary(configcleanData['seasonSummary']['year5'],
         data, configcleanData['seasonSummary']['colName'])
        data2012 = cf.seasonSummary(configcleanData['seasonSummary']['year6'],
         data, configcleanData['seasonSummary']['colName'])
        data2013 = cf.seasonSummary(configcleanData['seasonSummary']['year7'],
         data, configcleanData['seasonSummary']['colName'])
        data2014 = cf.seasonSummary(configcleanData['seasonSummary']['year8'],
         data, configcleanData['seasonSummary']['colName'])
        data2015 = cf.seasonSummary(configcleanData['seasonSummary']['year9'],
         data, configcleanData['seasonSummary']['colName'])
        data2016 = cf.seasonSummary(configcleanData['seasonSummary']['year10'],
         data, configcleanData['seasonSummary']['colName'])
        data2017 = cf.seasonSummary(configcleanData['seasonSummary']['year11'],
         data, configcleanData['seasonSummary']['colName'])
        data2018 = cf.seasonSummary(configcleanData['seasonSummary']['year12'],
         data, configcleanData['seasonSummary']['colName'])
        data2019 = cf.seasonSummary(configcleanData['seasonSummary']['year13'],
         data, configcleanData['seasonSummary']['colName'])
        data2020 = cf.seasonSummary(configcleanData['seasonSummary']['year14'],
         data, configcleanData['seasonSummary']['colName'])

        frames = [data2007, data2008, data2009, data2010, data2011, data2012, data2013,
         data2014, data2015, data2016, data2017, data2018, data2019, data2020]
        allSeasons = cf.allSeason(frames)
        allSeasons = cf.noPush(allSeasons,**configcleanData['noPush'])
        allSeasons = cf.fixNames(allSeasons, **configcleanData['fixNamesHome'])
        allSeasons = cf.fixNames(allSeasons, **configcleanData['fixNamesRoad'])
        allSeasons = cf.onHot(allSeasons, **configcleanData['onHot'])

        target, features = cf.splitFeatures(allSeasons,**configcleanData['splitFeatures'])
        target.to_csv(configcleanData['saveFeatures']['targetPath'])
        features.to_csv(configcleanData['saveFeatures']['featuresPath'])

    elif sp_used == "model":

        target = pd.read_csv(configmodel['loadFeatures']['targetPath'], index_col=0)
        features = pd.read_csv(configmodel['loadFeatures']['featuresPath'], index_col=0)
        rf, X_test, y_test = gm.createModel(features, target, **configmodel['createModel'])
        accuracy = gm.scoreModel(rf, X_test, y_test)
        with open(configmodel['saveModel']['accuracyPath'], 'w') as filehandle:
            filehandle.write("Test Accuracy = "+str(accuracy)+"\n")
        with open(configmodel['saveModel']['modelPath'],'wb') as f:
            pickle.dump(rf,f)
        upload(**configmodel['modeltos3'])
    else:
        parser.print_help()


