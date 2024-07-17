import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from fastapi import UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from typing import Optional
import io


class S3ImageService:
    def __init__(
        self,
        bucket_name: str,
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
    ):
        self.bucket_name = bucket_name
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )

    def write(self, file: UploadFile, object_name: Optional[str] = None) -> str:
        try:
            if object_name is None:
                object_name = file.filename

            self.s3_client.upload_fileobj(file.file, self.bucket_name, object_name)
            return f"Image {object_name} uploaded successfully"

        except NoCredentialsError:
            raise HTTPException(status_code=401, detail="Credentials not available")
        except ClientError as e:
            raise HTTPException(status_code=400, detail=e.response["Error"]["Message"])

    def download_image(self, object_name: str):
        try:
            file_stream = io.BytesIO()
            self.s3_client.download_fileobj(self.bucket_name, object_name, file_stream)
            file_stream.seek(0)
            return StreamingResponse(file_stream, media_type="image/jpeg")
        except ClientError as e:
            raise HTTPException(status_code=404, detail=e.response["Error"]["Message"])
