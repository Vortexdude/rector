import boto3
from app.common.exceptions.errors import AwsConnectionError

__all__ = ["s3"]


class S3:
    def __init__(self, region=None):
        self.client = boto3.client('s3')

    def fetch_all(self) -> list[dict[str, str]] | None:
        response = self.client.list_buckets()
        if response['ResponseMetadata']['HTTPStatusCode'] != 200:
            raise AwsConnectionError
        return [{**bucket, 'CreationDate': bucket['CreationDate'].strftime("%Y-%m-%d_%H:%M:%S")} for bucket in response['Buckets']]


s3 = S3()
