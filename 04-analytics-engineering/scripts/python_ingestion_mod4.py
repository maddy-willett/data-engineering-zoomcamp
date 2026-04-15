import os
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from google.cloud import storage
from google.api_core.exceptions import NotFound, Forbidden
import time 

BUCKET_NAME = "maddys_mod4_bucket"

# intialize the clint 
client = storage.Client(project='nytaxiproject-492423')

BASE_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data/" # modified to now be dynamic to the year & color
COLORS = ["yellow", "green"]
YEARS = [2019, 2020]
MONTHS = [f"{i:02d}" for i in range (1, 13)] # to loop through all the months
TASKS = [(t, str(y), m) for t in COLORS for y in YEARS for m in MONTHS] # to get all combos of year-months-colors
DOWNLOAD_DIR =  "."

CHUNKSIZE =  8 * 1024 * 1024

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

bucket = client.bucket(BUCKET_NAME)


def download_file(task):
    color, year, month = task 
    file_name = f"{color}_tripdata_{year}-{month}.parquet"
    url = f"{BASE_URL}{file_name}"
    file_path = os.path.join(DOWNLOAD_DIR, file_name)

    try: 
        print(f"Downloading {url}...")
        urllib.request.urlretrieve(url, file_path)
        print(f"Downloaded: {file_path}")
        return file_path
    except Exception as e:
        print(f"Failed to download {url}: e") # provide error msg
        return None


def create_bucket(bucket_name):
    try:
        # get bucket details
        bucket = client.get_bucket(bucket_name)

        #check if bucket belongs to current project
        project_bucket_ids = [bckt.id for bckt in client.list_buckets()]
        if bucket_name in project_bucket_ids:
            print(f"Bucket '{bucket_name}' exists and belongs to your project. Proceeding...") #ensuring unique names
        else: 
            print(f"A bucket with the name '{bucket_name}' already exists, but it does not belong to your project.")
            sys.exit(1)

    except NotFound: 
        # if the bucket does not exist, create it
        bucket = client.create_bucket(bucket_name)
        print(f"Created bucket '{bucket_name}'")
    except Forbidden: 
        # if the request is forbidden, it means the bucket exists but I do not have access to it
        print(f"A bucket with the name '{bucket_name}' exists, but it is not accessible. Bucket name is taken. Please try a different bucket name.")
        sys.exit(1)

            
def verify_gcs_upload(blob_name):
    return storage.Blob(bucket=bucket, name=blob_name).exists(client)


def upload_to_gcs(file_path, max_retries=3):
    blob_name = os.path.basename(file_path)
    blob = bucket.blob(blob_name)
    blob.chunk_size = CHUNKSIZE

    create_bucket(BUCKET_NAME)

    # uploading files
    for attempt in range(max_retries):
        try:
            print(f"Uploading {file_path} to {BUCKET_NAME} (Attempt {attempt + 1})...")
            blob.upload_from_filename(file_path)
            print(f"Uploaded: gs://{BUCKET_NAME}/{blob_name}")

            if verify_gcs_upload(blob_name):
                print(f"Verification successful for {blob_name}")
                return
            else:
                print(f"Verification failed for {blob_name}, retrying...")
        except Exception as e:
            print(f"Failed to upload {file_path} to GCS: {e}")

        time.sleep(5)

    print(f"Giving up on {file_path} after {max_retries} attempts.")


if __name__ == "__main__":
    create_bucket(BUCKET_NAME)

    with ThreadPoolExecutor(max_workers=4) as executor:
        file_paths = list(executor.map(download_file, TASKS))

    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(upload_to_gcs, filter(None, file_paths))  # Remove None values

    print("All files processed and verified.")

