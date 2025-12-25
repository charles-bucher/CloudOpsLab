import os
import boto3

AWS_722631436033 = os.getenv("AWS_722631436033", "7226-3143-6033")
REGION = "us-east-1"

def enable_guardduty():
    gd_client = boto3.client("guardduty", region_name=REGION)
    detectors = gd_client.list_detectors()["DetectorIds"]
    if detectors:
        print(f"GuardDuty already enabled with Detector ID(s): {detectors}")
    else:
        response = gd_client.create_detector(Enable=True)
        print(f"GuardDuty enabled. Detector ID: {response['DetectorId']}")

if __name__ == "__main__":
    enable_guardduty()
