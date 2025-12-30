# s3_backup.py
import boto3
from datetime import datetime

SOURCE_BUCKET = "your-source-bucket"
BACKUP_BUCKET = "your-backup-bucket"

s3 = boto3.resource("s3")
source = s3.Bucket(SOURCE_BUCKET)
backup = s3.Bucket(BACKUP_BUCKET)

def backup_s3():
    timestamp = datetime.utcnow().strftime("%Y-%m-%d-%H-%M")
    for obj in source.objects.all():
        copy_source = {"Bucket": SOURCE_BUCKET, "Key": obj.key}
        dest_key = f"{timestamp}/{obj.key}"
        backup.copy(copy_source, dest_key)
        print(f"Copied {obj.key} -> {dest_key}")

if __name__ == "__main__":
    backup_s3()
