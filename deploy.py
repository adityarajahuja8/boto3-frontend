
import boto3
import os
import mimetypes

# 1. Tell the script which bucket to use
BUCKET_NAME = os.environ.get('AWS_S3_BUCKET')

s3 = boto3.client('s3')

def upload_files():
    print("Starting deployment...")
    
    # 2. Look through all files in your folder
    for root, dirs, files in os.walk('.'):
        for file in files:
            # Skip the script and hidden git files
            if file == 'deploy.py' or '.git' in root:
                continue
                
            file_path = os.path.join(root, file)
            s3_key = os.path.relpath(file_path, '.')

            # 3. Figure out if the file is HTML, CSS, or an image
            content_type, _ = mimetypes.guess_type(file_path)
            
            # 4. Upload to AWS
            s3.upload_file(
                file_path, 
                BUCKET_NAME, 
                s3_key,
                ExtraArgs={'ContentType': content_type or 'text/plain'}
            )
            print(f"Uploaded: {s3_key}")

if __name__ == "__main__":
    upload_files()