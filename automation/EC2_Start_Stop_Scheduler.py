# ec2_scheduler.py
import boto3

INSTANCE_IDS = ["i-0123456789abcdef0"]  # replace with your instance IDs
ec2 = boto3.client("ec2")

def stop_instances():
    ec2.stop_instances(InstanceIds=INSTANCE_IDS)
    print(f"Stopped instances: {INSTANCE_IDS}")

def start_instances():
    ec2.start_instances(InstanceIds=INSTANCE_IDS)
    print(f"Started instances: {INSTANCE_IDS}")

if __name__ == "__main__":
    import sys
    action = sys.argv[1].lower()
    if action == "start":
        start_instances()
    elif action == "stop":
        stop_instances()
    else:
        print("Usage: python ec2_scheduler.py start|stop")
