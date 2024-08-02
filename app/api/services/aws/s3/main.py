import boto3
from botocore.exceptions import ClientError
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

    def upload_file(self, bucket: str, file_name: str, key: str):
        """
        Upload a file to an S3 bucket.

        Args:
            bucket (str): S3 bucket name.
            file_name (str): Local file name to be uploaded.
            key (str): Key in the S3 bucket.

        Returns:
            bool: True if upload is successful, False otherwise.
        """
        try:
            with open(file_name, 'rb') as f:
                content = f.read()

            self.client.put_object(
                Body=bytes(content),
                Bucket=bucket,
                Key=key
            )
            print("Uploading file to s3")
        except ClientError as e:
            raise e
        return True


s3 = S3()
