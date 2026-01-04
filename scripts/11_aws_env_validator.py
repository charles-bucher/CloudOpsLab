#!/usr/bin/env python3
"""
Verify AWS environment readiness
"""

import boto3
import sys

def main():
    try:
        sts = boto3.client("sts")
        identity = sts.get_caller_identity()

        print("✅ AWS credentials valid")
        print(f"Account: {identity['Account']}")
        print(f"UserArn: {identity['Arn']}")

        ec2 = boto3.client("ec2")
        regions = ec2.describe_regions()["Regions"]
        print(f"🌍 Available regions: {len(regions)}")

    except Exception as e:
        print("❌ AWS environment verification failed")
        print(str(e))
        sys.exit(1)

if __name__ == "__main__":
    main()
