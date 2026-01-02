#!/usr/bin/env python3
"""
S3 Backup Script
Backs up objects from one S3 bucket to another with timestamped versioning
"""

# Import required libraries
import boto3
import sys
from datetime import datetime
from botocore.exceptions import ClientError


# Configuration
SOURCE_BUCKET = "your-source-bucket"      # Replace with your source bucket name
BACKUP_BUCKET = "your-backup-bucket"      # Replace with your backup bucket name
MAX_OBJECTS = 1000                         # Safety limit to prevent accidental large backups

def validate_buckets(s3_client):
    """Validate that both buckets exist and are accessible."""
    buckets_valid = True
    
    # Check source bucket
    try:
        s3_client.head_bucket(Bucket=SOURCE_BUCKET)
        print(f"✅ Source bucket accessible: {SOURCE_BUCKET}")
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == '404':
            print(f"❌ Source bucket not found: {SOURCE_BUCKET}")
        elif error_code == '403':
            print(f"❌ Access denied to source bucket: {SOURCE_BUCKET}")
        else:
            print(f"❌ Error accessing source bucket: {e}")
        buckets_valid = False
    
    # Check backup bucket
    try:
        s3_client.head_bucket(Bucket=BACKUP_BUCKET)
        print(f"✅ Backup bucket accessible: {BACKUP_BUCKET}")
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == '404':
            print(f"❌ Backup bucket not found: {BACKUP_BUCKET}")
        elif error_code == '403':
            print(f"❌ Access denied to backup bucket: {BACKUP_BUCKET}")
        else:
            print(f"❌ Error accessing backup bucket: {e}")
        buckets_valid = False
    
    return buckets_valid

def get_bucket_size(s3_resource, bucket_name):
    """Calculate total size of objects in bucket."""
    bucket = s3_resource.Bucket(bucket_name)
    total_size = 0
    object_count = 0
    
    try:
        for obj in bucket.objects.all():
            total_size += obj.size
            object_count += 1
    except Exception as e:
        print(f"⚠️  Could not calculate bucket size: {e}")
        return 0, 0
    
    return total_size, object_count

def format_size(bytes):
    """Format bytes into human-readable size."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes < 1024.0:
            return f"{bytes:.2f} {unit}"
        bytes /= 1024.0
    return f"{bytes:.2f} PB"

def backup_s3(dry_run=False):
    """
    Backup S3 bucket contents with timestamp.
    
    Args:
        dry_run: If True, only show what would be copied without actually copying
    """
    # Initialize AWS clients
    try:
        s3_client = boto3.client("s3")
        s3_resource = boto3.resource("s3")
    except Exception as e:
        print(f"❌ Failed to initialize AWS S3 client: {e}")
        print("   Make sure your AWS credentials are configured (run: aws configure)")
        sys.exit(1)
    
    print("\n" + "=" * 70)
    print("🔄 S3 BACKUP UTILITY")
    print("=" * 70 + "\n")
    
    # Validate configuration
    if SOURCE_BUCKET == "your-source-bucket" or BACKUP_BUCKET == "your-backup-bucket":
        print("❌ ERROR: Bucket names not configured")
        print("\n📝 Please edit the script and update:")
        print(f"   SOURCE_BUCKET = 'your-actual-source-bucket'")
        print(f"   BACKUP_BUCKET = 'your-actual-backup-bucket'")
        sys.exit(1)
    
    if SOURCE_BUCKET == BACKUP_BUCKET:
        print("❌ ERROR: Source and backup buckets cannot be the same")
        sys.exit(1)
    
    # Validate buckets exist and are accessible
    print("🔍 Validating buckets...")
    if not validate_buckets(s3_client):
        print("\n❌ Bucket validation failed")
        sys.exit(1)
    
    # Get source bucket info
    print("\n📊 Analyzing source bucket...")
    total_size, object_count = get_bucket_size(s3_resource, SOURCE_BUCKET)
    
    if object_count == 0:
        print("⚠️  Source bucket is empty - nothing to backup")
        sys.exit(0)
    
    print(f"   Objects found: {object_count}")
    print(f"   Total size: {format_size(total_size)}")
    
    # Safety check
    if object_count > MAX_OBJECTS:
        print(f"\n⚠️  WARNING: Bucket contains {object_count} objects (limit: {MAX_OBJECTS})")
        response = input("   Continue anyway? (yes/no): ")
        if response.lower() != 'yes':
            print("   Backup cancelled")
            sys.exit(0)
    
    # Generate timestamp for backup folder
    timestamp = datetime.utcnow().strftime("%Y-%m-%d-%H-%M-%S")
    
    if dry_run:
        print(f"\n🔍 DRY RUN MODE - No files will be copied")
    
    print(f"\n📁 Backup folder: {timestamp}/")
    print(f"{'=' * 70}\n")
    
    # Perform backup
    source_bucket = s3_resource.Bucket(SOURCE_BUCKET)
    backup_bucket = s3_resource.Bucket(BACKUP_BUCKET)
    
    copied_count = 0
    failed_count = 0
    total_copied_size = 0
    
    try:
        for i, obj in enumerate(source_bucket.objects.all(), 1):
            try:
                copy_source = {"Bucket": SOURCE_BUCKET, "Key": obj.key}
                dest_key = f"{timestamp}/{obj.key}"
                
                # Show progress
                print(f"[{i}/{object_count}] {obj.key} ({format_size(obj.size)})")
                
                if not dry_run:
                    # Perform the copy
                    backup_bucket.copy(copy_source, dest_key)
                    copied_count += 1
                    total_copied_size += obj.size
                    print(f"   ✅ Copied to: {dest_key}")
                else:
                    print(f"   🔍 Would copy to: {dest_key}")
                    copied_count += 1
                
            except ClientError as e:
                failed_count += 1
                print(f"   ❌ Failed: {e}")
            except Exception as e:
                failed_count += 1
                print(f"   ❌ Unexpected error: {e}")
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Backup interrupted by user")
        print(f"   Copied {copied_count} objects before interruption")
        sys.exit(1)
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 BACKUP SUMMARY")
    print("=" * 70)
    print(f"\nSource: s3://{SOURCE_BUCKET}")
    print(f"Destination: s3://{BACKUP_BUCKET}/{timestamp}/")
    print(f"\nObjects processed: {object_count}")
    
    if not dry_run:
        print(f"Successfully copied: {copied_count}")
        print(f"Failed: {failed_count}")
        print(f"Total size copied: {format_size(total_copied_size)}")
        
        if failed_count > 0:
            print(f"\n⚠️  {failed_count} object(s) failed to copy")
            sys.exit(1)
        else:
            print("\n✅ Backup completed successfully!")
    else:
        print(f"\n🔍 DRY RUN - {copied_count} objects would be copied")
    
    print("=" * 70 + "\n")

def main():
    """Main execution with command line argument support."""
    # Check for dry-run flag
    dry_run = "--dry-run" in sys.argv or "-n" in sys.argv
    
    if "--help" in sys.argv or "-h" in sys.argv:
        print("\nS3 Backup Utility")
        print("\nUsage: python s3_backup.py [options]")
        print("\nOptions:")
        print("  --dry-run, -n    Show what would be copied without actually copying")
        print("  --help, -h       Show this help message")
        print("\nConfiguration:")
        print(f"  Source bucket: {SOURCE_BUCKET}")
        print(f"  Backup bucket: {BACKUP_BUCKET}")
        sys.exit(0)
    
    backup_s3(dry_run=dry_run)

if __name__ == "__main__":
    main()