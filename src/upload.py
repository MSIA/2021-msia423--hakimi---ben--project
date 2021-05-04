import boto3  

def upload(bucket, fileName, s3path):
    s3 = boto3.resource("s3")
    bucket = s3.Bucket(bucket)
    bucket.upload_file(fileName, s3path)