import boto3  
import logging

logging.getLogger("boto3").setLevel(logging.ERROR)
logging.getLogger("botocore").setLevel(logging.ERROR)
logging.getLogger("s3fs").setLevel(logging.ERROR)
logging.getLogger("s3transfer").setLevel(logging.ERROR)
logging.getLogger("urllib3").setLevel(logging.ERROR)

logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s", level=logging.DEBUG
)

logger = logging.getLogger(__name__)

def upload(bucket, s3path, fileName):

    """
    Uploads local data file to S3 bucket

    Args:
        bucket: (String), Required, name of S3 Bucket
        s3Path: (String), Required, name to be used when saved to s3
        fileName: (String), Required, local file path

    Returns:
        csv file

    """
    try:    
        s3 = boto3.resource("s3")
        bucket = s3.Bucket(bucket)
        bucket.upload_file(s3path, fileName)

        logger.info("Data uploaded to S3 bucket w/ path: s3://%s/%s", bucket, s3path)

    except:
        logger.error("Unable to load local data to S3 bucket: s3://%s/%s Please check inputs and AWS Credentials", bucket, s3path)