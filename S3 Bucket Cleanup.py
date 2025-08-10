import boto3
from datetime import datetime, timezone, timedelta

def lambda_handler(event, context):
    # CONFIGURE THESE
    BUCKET_NAME = "aviralpaliwal3105"  
    DAYS_OLD = 30 

    s3 = boto3.client("s3")

    # Calculate the cutoff date
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=DAYS_OLD)

    # List all objects in the bucket
    response = s3.list_objects_v2(Bucket=BUCKET_NAME)

    if "Contents" not in response:
        print("Bucket is empty.")
        return

    for obj in response["Contents"]:
        file_name = obj["Key"]
        last_modified = obj["LastModified"]

        # Check if the file is older than cutoff
        if last_modified < cutoff_date:
            # Delete the object
            s3.delete_object(Bucket=BUCKET_NAME, Key=file_name)
            print(f"Deleted: {file_name} (Last Modified: {last_modified})")
        else:
            print(f"Kept: {file_name} (Last Modified: {last_modified})")
