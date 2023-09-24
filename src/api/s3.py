from core import settings
import boto3


class SingletonClass:
    _instances = dict()

    def __new__(cls):
        if not cls in cls._instances:
            instance = super().__new__(cls)
            cls._instances[cls] = instance

        return cls._instances[cls]


class AWSConnection(SingletonClass):
    """
    A class that creates a connection to s3 storage.
    """

    def __call__(
        self,
        aws_access_key_id: str = settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key: str = settings.AWS_SECRET_ACCESS_KEY,
        region_name: str = settings.AWS_REGION,
    ):
        return boto3.client(
            "s3",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name,
        )


class AWSServices:
    """
    A class that provides some functionality for AWS.
    """

    @staticmethod
    def get_object_from_s3(s3_key: str) -> bytes:
        aws_connection = AWSConnection()
        response = aws_connection().get_object(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=s3_key
        )
        return response["Body"].read()

    @staticmethod
    def generate_url(
        obj_name: str, bucket_name: str = settings.AWS_STORAGE_BUCKET_NAME
    ) -> str:
        aws_connection = AWSConnection()
        return aws_connection().generate_presigned_url(
            "get_object",
            Params={
                "Bucket": bucket_name,
                "Key": obj_name,
                "ResponseContentType": "image/jpeg",
            },
        )

    @staticmethod
    def put_object_to_AWS(
        new_obj_name: str, body, bucket_name: str = settings.AWS_STORAGE_BUCKET_NAME
    ) -> None:
        aws_connection = AWSConnection()
        aws_connection().put_object(
            Bucket=bucket_name,
            Key=new_obj_name,
            Body=body,
        )
