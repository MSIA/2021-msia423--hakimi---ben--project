import logging

import boto3  

## Change level of following loggers to avoid over-use
logging.getLogger("boto3").setLevel(logging.ERROR)
logging.getLogger("botocore").setLevel(logging.ERROR)
logging.getLogger("s3fs").setLevel(logging.ERROR)
logging.getLogger("s3transfer").setLevel(logging.ERROR)
logging.getLogger("urllib3").setLevel(logging.ERROR)

## configure and name logger
logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s", level=logging.DEBUG
)
logger = logging.getLogger(__name__)

## function to be called in run.py
def upload(bucket, s3path, fileName):

    """
    Uploads local data file to S3 bucket

    Args:
        bucket: (String), Required, name of S3 Bucket
        s3Path: (String), Required, path to and name of file when saved in S3
        fileName: (String), Required, local file path data is being uploaded from

    Returns:
        None

    """
    try:    
        s3 = boto3.resource("s3")
        bucket = s3.Bucket(bucket)
        bucket.upload_file(s3path, fileName)

        logger.info("Data uploaded to S3 bucket w/ %s File Name= %s", bucket, s3path)

    except:
        logger.error("Unable to load local data to S3 bucket w/ %s File Name= %s, Please check inputs and AWS Credentials", bucket, s3path)
