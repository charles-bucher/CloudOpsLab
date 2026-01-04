# s3_public_scan.py
# Import required libraries
import boto3


s3 = boto3.client("s3")
def check_public_buckets():
    """
        Function to check_public_buckets.
    """

    buckets = s3.list_buckets()["Buckets"]
    for bucket in buckets:
        acl = s3.get_bucket_acl(Bucket=bucket["Name"])
        for grant in acl["Grants"]:
            if "URI" in grant["Grantee"] and "AllUsers" in grant["Grantee"]["URI"]:
                print(f"Public bucket found: {bucket['Name']}")

if __name__ == "__main__":
    check_public_buckets()