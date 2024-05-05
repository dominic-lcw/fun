import os

import boto3
import pandas as pd
from io import StringIO, BytesIO
import tempfile

__all__ = ['S3',]

class S3:

    def __init__(self, bucket):
        self.bucket = bucket
        self.s3 = boto3.client('s3', aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
                                    aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"])
    
    def create_bucket(bucket_name):
        """ Create s3 bucket.
            Restricted to region: ap-southeast-2
        """
        s3 = boto3.client('s3')
        s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': 'ap-southeast-2'})

    def bucket_exists(self) -> bool:
        try:
            self.s3.head_bucket(Bucket = self.bucket)
            return True
        except boto3.exceptions.botocore.exceptions.ClientError:
            return False

    def put(self, df, key) -> None:
        """ Write a dataframe to parquet file on S3.
        """
        with tempfile.TemporaryDirectory() as tempdir:
            
            _, ext = os.path.splitext(key)
            if ext == '.csv':
                df.to_csv(os.path.join(tempdir, 'temp.csv'), index=False)
            elif ext == '.parquet':
                df.to_parquet(os.path.join(tempdir, 'temp.parquet'))

            with open(os.path.join(tempdir, 'temp.parquet'), 'rb') as data:
                self.s3.put_object(Bucket = self.bucket, Key = key, Body = data)
    
    def get(self, key) -> None:

        _, ext = os.path.splitext(key)
        obj = self.s3.get_object(Bucket = self.bucket, Key = key)

        if ext == '.csv':
            df = pd.read_csv(BytesIO(obj['Body'].read()))
        elif ext == '.parquet':
            df = pd.read_parquet(BytesIO(obj['Body'].read()))
        else:
            raise ValueError(f"Unsupoprted file type: {ext}")
        return df