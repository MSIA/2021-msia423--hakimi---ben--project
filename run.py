import argparse
# from pathlib import Path

import logging.config

logging.config.fileConfig('config/logging/local.conf')
logger = logging.getLogger()

from src.upload import upload
from src.downloadSource import downloadSource
from src.createDB import createDB
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
    sb_datatos3.add_argument("--OUTPUTPATH", default = "data/external/data.csv", help="path to data saved locally")

    args = parser.parse_args()
    sp_used = args.subparser_name

    if sp_used == "createDB":
        createDB(args.engine_string)
    elif sp_used == "loadData":
        downloadSource(args.INPUT1, args.INPUT2, args.OUTPUTPATH)
        upload(args.BUCKETNAME, args.FILEPATH, args.S3PATH)
    else:
        parser.print_help()
