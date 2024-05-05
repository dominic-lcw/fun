import os

import boto3
import json
from botocore.exceptions import ClientError


class SecretsManager:

    @staticmethod    
    def get_secret(secret_name: str, region = 'ap-southeast-2') -> str:
        """ This requires the use of boto3.session but not boto3.client.
        """

        session = boto3.Session(
            aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
            region_name=region
        )
        client = session.client(
            service_name = 'secretsmanager',
            region_name = region
        )

        try:
            get_secret_value_response = client.get_secret_value(
                SecretId=secret_name
            )
        except ClientError as e:
            # For a list of exceptions thrown, see
            # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
            raise e
        
        secret = get_secret_value_response['SecretString']

        return secret