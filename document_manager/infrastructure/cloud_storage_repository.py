import io
import os
import uuid

from google.cloud import storage

from ..utils import get_extension, get_base_path

bucket_name = os.getenv('GCLOUD_BUCKET', default='massive_proyecto_final')
testing = os.getenv('TESTING', 'False').lower() == 'true'
client = storage.Client()


def get_bucket():
    if testing:
        return bucket
    else:
        return client.bucket(bucket_name)


bucket = client.bucket(bucket_name)


class CloudStorageRepository:
    def __init__(self):
        self.bucket_name = bucket_name
        self.bucket = bucket

    @staticmethod
    def generate_path(full_file_name) -> tuple[str, str]:
        file_name = str(uuid.uuid4())
        extension = get_extension(full_file_name)
        base_path = get_base_path()

        return file_name, f"{base_path}/{file_name}.{extension}"

    def upload_file(self, file_obj, destination_blob_name) -> str | None:
        blob = self.bucket.blob(destination_blob_name)

        try:
            blob.upload_from_file(file_obj, content_type=file_obj.content_type)
            print("Upload object '{}' to storage. srcFile: {}, bucket: {}, destination: {}"
                  .format(file_obj.filename, blob.name, self.bucket_name, destination_blob_name))

            return f'{self.bucket_name}/{destination_blob_name}'
        except Exception as e:
            print("Error uploading object '{}' to storage. srcFile: {}, bucket: {}, destination: {}, error: {}"
                  .format(file_obj.filename, blob.name, self.bucket_name, destination_blob_name, e))

            return None

    def download_file(self, destination_blob_name):
        blob = self.bucket.blob(destination_blob_name)
        buffer = io.BytesIO()

        try:
            blob.download_to_file(buffer)
            buffer.seek(0)

            return buffer, blob.content_type
        except Exception as e:
            print("Error downloading object '{}' from storage. bucket: {}, destination: {}, error: {}"
                  .format(blob.name, self.bucket_name, destination_blob_name, e))

            return None, None
