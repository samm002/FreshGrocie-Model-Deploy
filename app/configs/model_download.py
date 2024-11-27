from google.cloud import storage
from .config import Config

bucket_name = Config.BUCKET_NAME
model_path = Config.BUCKET_MODEL_PATH
model_name = Config.MODEL_NAME


class ModelDownloader:
    def __init__(self):
        self.bucket_name = bucket_name
        self.model_path = model_path
        self.model_name = model_name

    def download_model(self):
        print("Downloading model from cloud storage...")
        storage_client = storage.Client()

        bucket = storage_client.bucket(self.bucket_name)

        blob = bucket.blob(self.model_path)
        blob.download_to_filename(self.model_name)

        print(
            f"Downloaded model {self.model_path} "
            f"from bucket {self.bucket_name} to local file {self.model_name}."
        )
