#!/usr/bin/env python3
"""
Find idle EC2 instances (low CPU)
"""

import boto3
from datetime import datetime, timedelta

ec2 = boto3.client("ec2")
cw = boto3.client("cloudwatch")

instances = ec2.describe_instances()

print("🧹 Idle EC2 Report")

for r in instances["Reservations"]:
    for i in r["Instances"]:
        instance_id = i["InstanceId"]

        metrics = cw.get_metric_statistics(
            Namespace="AWS/EC2",
            MetricName="CPUUtilization",
            Dimensions=[{"Name": "InstanceId", "Value": instance_id}],
            StartTime=datetime.utcnow() - timedelta(days=7),
            EndTime=datetime.utcnow(),
            Period=86400,
            Statistics=["Average"]
        )

        if not metrics["Datapoints"]:
            continue

        avg_cpu = sum(d["Average"] for d in metrics["Datapoints"]) / len(metrics["Datapoints"])

        if avg_cpu < 5:
            print(f"⚠️ {instance_id} idle — avg CPU {avg_cpu:.2f}%")
