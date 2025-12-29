import boto3


def remediate_instance(instance_id):
    ec2 = boto3.client("ec2")
    print(f"Attempting remediation for {instance_id}...")
    ec2.reboot_instances(InstanceIds=[instance_id])


if __name__ == "__main__":
    remediate_instance("i-1234567890abcdef0")
