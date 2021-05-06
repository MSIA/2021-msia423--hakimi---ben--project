import boto3  

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
    
    s3 = boto3.resource("s3")
    bucket = s3.Bucket(bucket)
    bucket.upload_file(s3path, fileName)