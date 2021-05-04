import argparse
from pathlib import Path

import logging.config
logging.config.fileConfig('config/logging/local.conf')
logger = logging.getLogger('penny-lane-pipeline')

from src.upload import upload
from src.downloadSource import downloadSource
import src.createDB

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description = "Upload data folder to specified S3 bucket")
    parser.add_argument("BUCKETNAME", help="Name of S3 Bucket")
    parser.add_argument("S3PATH", help="path to S3 Bucket")
    parser.add_argument("--FILEPATH", default = "data.csv", help="name of data to upload")
    parser.add_argument("--INPUT1",default = "https://www.sportsbookreviewsonline.com/scoresoddsarchives/nfl/nfl%20odds%20", help="Begining part of path")
    parser.add_argument("--INPUT2",default = ".xlsx", help="end of path")
    parser.add_argument("--OUTPUTPATH", default = "data.csv", help="name of output after download")

    args = parser.parse_args()

    downloadSource(args.INPUT1, args.INPUT2, args.OUTPUTPATH)
    upload(args.BUCKETNAME, args.FILEPATH, args.S3PATH)


# upload

## bucket name = 2021-msia423-hakimi-ben  
## file path
## s3 path

# Download Source

## input path1 and input path 2
## output path