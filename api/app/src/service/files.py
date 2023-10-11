"""
Read/write files
"""
from io import BytesIO
from mypy_boto3_s3.client import S3Client


class FileService:
    """
    File service
    """

    def __init__(self, file_client: S3Client, bucket_name: str):
        self.__file_client = file_client
        self.__bucket_name = bucket_name

    def delete_file(self, file_location: str) -> bool:
        """
        Deletes a file
        """
        return (
            self.__file_client.delete_object(
                Bucket=self.__bucket_name,
                Key=file_location,
            )["ResponseMetadata"]["HTTPStatusCode"]
            == 204
        )

    def download(self, file_location: str) -> bytes:
        """
        Downloads a file as a byte stream
        """
        return self.__file_client.get_object(
            Bucket=self.__bucket_name,
            Key=file_location,
        )["Body"].read()

    def upload(self, file_bytes: bytes, file_location: str) -> str:
        """
        Uploads a file as a byte stream
        """
        self.__file_client.upload_fileobj(
            BytesIO(file_bytes),
            self.__bucket_name,
            file_location,
        )
        return {"bucket_name": self.__bucket_name, "file_location": file_location}
