#!/usr/bin/env python3
"""
Daily AWS cost snapshot
"""

import boto3
from datetime import date, timedelta

ce = boto3.client("ce")

end = date.today()
start = end - timedelta(days=7)

response = ce.get_cost_and_usage(
    TimePeriod={"Start": str(start), "End": str(end)},
    Granularity="DAILY",
    Metrics=["UnblendedCost"]
)

print("📊 AWS Cost Snapshot (Last 7 Days)")
for day in response["ResultsByTime"]:
    cost = day["Total"]["UnblendedCost"]["Amount"]
    print(f"{day['TimePeriod']['Start']}: ${float(cost):.2f}")
