import os
import sys

import requests
import boto3

from huggingface_hub import list_repo_files

MODELS_AWS_ACCESS_KEY_ID = os.environ['MODELS_AWS_ACCESS_KEY_ID']
MODELS_AWS_SECRET_ACCESS_KEY = os.environ['MODELS_AWS_SECRET_ACCESS_KEY']
MODELS_HF_TOKEN = os.environ['MODELS_HF_TOKEN']
MODELS_BUCKET_NAME = os.environ['MODELS_BUCKET_NAME']
MODELS_PATH=os.environ['MODELS_PATH']




if __name__ == "__main__":
    try:
        repo_id = sys.argv[1]
    except IndexError:
        print("Usage: python upload-from-hf-to-s3-stream.py <repo_id>")
        print("ENV vars required:")
        print("MODELS_AWS_ACCESS_KEY_ID")
        print("MODELS_AWS_SECRET_ACCESS_KEY")
        print("MODELS_HF_TOKEN")
        print("MODELS_BUCKET_NAME")
        print("MODELS_PATH")
        print("Example: python upload-from-hf-to-s3-stream.py meta-llama/Llama-3.1-8B-Instruct")
        sys.exit(1)


    headers = {
        "Authorization": f"Bearer {MODELS_HF_TOKEN}",
    }

    s3 = boto3.client(
        "s3",
        aws_access_key_id=MODELS_AWS_ACCESS_KEY_ID,
        aws_secret_access_key=MODELS_AWS_SECRET_ACCESS_KEY,
        region_name="us-east-1",
        endpoint_url="https://s3.us-east-1.amazonaws.com",
    )
    files = list_repo_files(repo_id)

    for file in list_repo_files(repo_id):
        if "/" in file:
            print(f"Skipping {file} as it is nested inside a directory")
            continue

        file_url = f"https://huggingface.co/{repo_id}/resolve/main/{file}"
        target_path = f"{MODELS_PATH}/{file}"

        try:
            if s3.head_object(Bucket=MODELS_BUCKET_NAME, Key=target_path):
                print(f"Skipping {file} as it already exists in S3")
                continue
        except Exception:
            pass

        print(f"Streaming: {file}")
        with requests.get(file_url, stream=True, headers=headers) as response:
            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError as e:
                print(f"Error downloading {file}: {e}")
                continue

            response.raise_for_status()
            with response.raw as data:
                s3.upload_fileobj(data, MODELS_BUCKET_NAME, target_path)

