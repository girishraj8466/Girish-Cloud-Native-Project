import os
from google.cloud import storage

# Initialize the storage client
storage_client = storage.Client()

def get_list_of_files(bucket_name):
    """Lists all the blobs in the bucket."""
    bucket = storage_client.bucket(bucket_name)
    blobs = bucket.list_blobs()

    files = [blob.name for blob in blobs]
    return files

def upload_file(bucket_name, file_path):
    """Uploads a file to the bucket."""
    bucket = storage_client.bucket(bucket_name)
    file_name = os.path.basename(file_path)
    blob = bucket.blob(file_name)

    blob.upload_from_filename(file_path)
    print(f"File {file_name} uploaded to {bucket_name}.")

def download_file(bucket_name, file_name):
    """Downloads a file from the bucket to a local file."""
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    local_path = f"/tmp/{file_name}"

    blob.download_to_filename(local_path)
    print(f"File {file_name} downloaded from {bucket_name} to {local_path}.")
