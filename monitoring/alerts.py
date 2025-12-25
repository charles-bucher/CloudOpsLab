import os
import boto3

AWS_722631436033 = os.getenv("AWS_722631436033", "7226-3143-6033")
SNS_TOPIC_ARN = f"arn:aws:sns:us-east-1:{AWS_722631436033}:CloudOpsAlerts"

def send_alert(message: str):
    sns = boto3.client("sns")
    sns.publish(TopicArn=SNS_TOPIC_ARN, Message=message)
    print("Alert sent:", message)

if __name__ == "__main__":
    send_alert("Test alert from CloudOps Suite")
