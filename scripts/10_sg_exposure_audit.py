#!/usr/bin/env python3
"""
Detect overly permissive security groups
"""

import boto3

ec2 = boto3.client("ec2")

groups = ec2.describe_security_groups()["SecurityGroups"]

print("🔐 Security Group Exposure Scan")

for sg in groups:
    for rule in sg["IpPermissions"]:
        for ip in rule.get("IpRanges", []):
            if ip["CidrIp"] == "0.0.0.0/0":
                print(f"🚨 {sg['GroupName']} ({sg['GroupId']}) open to the world")
