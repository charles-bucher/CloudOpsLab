# ec2_auto_recovery.py
# Import required libraries
import boto3


ec2 = boto3.client("ec2")
def recover_unhealthy_instances():
    """
        Function to recover_unhealthy_instances.
    """

    instances = ec2.describe_instance_status(IncludeAllInstances=True)["InstanceStatuses"]
    for i in instances:
        if i["InstanceState"]["Name"] == "running":
            checks = i["SystemStatus"]["Status"]
            if checks != "ok":
                ec2.reboot_instances(InstanceIds=[i["InstanceId"]])
                print(f"Rebooted unhealthy instance: {i['InstanceId']}")

if __name__ == "__main__":
    recover_unhealthy_instances()