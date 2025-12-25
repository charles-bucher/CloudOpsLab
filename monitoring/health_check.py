import boto3
from botocore.exceptions import ClientError

def run_health_check():
    findings = []

    ec2 = boto3.client("ec2")

    try:
        response = ec2.describe_instances()
        instances = [
            i
            for r in response["Reservations"]
            for i in r["Instances"]
        ]

        if not instances:
            findings.append("No EC2 instances found")

        for instance in instances:
            instance_id = instance["InstanceId"]
            state = instance["State"]["Name"]

            if state != "running":
                findings.append(
                    f"EC2 instance {instance_id} is in state '{state}'"
                )

    except ClientError as e:
        findings.append(f"AWS error: {e}")

    return findings


def main():
    print("[INFO] Starting AWS health check...")

    results = run_health_check()

    if not results:
        print("[OK] No health issues detected.")
    else:
        print("[WARN] Health issues found:")
        for item in results:
            print(f" - {item}")

    print("[INFO] Health check complete.")


if __name__ == "__main__":
    main()
