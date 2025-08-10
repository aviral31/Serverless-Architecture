import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    # List all S3 buckets
    response = s3.list_buckets()
    for bucket in response['Buckets']:
        #check for encryption status
        print(f'Checking bucket: {bucket["Name"]}')
        try:
            s3.get_bucket_encryption(Bucket=bucket['Name'])
            print(f'Bucket {bucket["Name"]} has encryption enabled.')
        except s3.exceptions.ClientError:
            if e.response["Error"]["Code"] == "ServerSideEncryptionConfigurationNotFoundError":
                print(f"[WARNING] Bucket '{bucket_name}' does NOT have encryption enabled!")
            else:
                print(f"[ERROR] Could not check bucket '{bucket_name}': {e}")
    
