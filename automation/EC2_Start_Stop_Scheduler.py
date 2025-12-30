#!/usr/bin/env python3
"""
EC2 Start/Stop Scheduler
Automates EC2 instance start/stop operations
"""

import boto3
import sys
from botocore.exceptions import ClientError

# Configuration
INSTANCE_IDS = ["i-0123456789abcdef0"]  # Replace with your actual instance IDs

def get_ec2_client():
    """Initialize EC2 client with error handling"""
    try:
        return boto3.client("ec2")
    except Exception as e:
        print(f"❌ Failed to initialize AWS EC2 client: {e}")
        print("   Make sure your AWS credentials are configured (run: aws configure)")
        sys.exit(1)

def validate_instances(ec2, instance_ids):
    """Validate that instances exist"""
    try:
        response = ec2.describe_instances(InstanceIds=instance_ids)
        
        valid_instances = []
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                valid_instances.append(instance['InstanceId'])
        
        return valid_instances
    except ClientError as e:
        if e.response['Error']['Code'] == 'InvalidInstanceID.NotFound':
            print(f"❌ Error: Some instance IDs not found")
            print(f"   Please update INSTANCE_IDS in the script with valid instance IDs")
            return []
        else:
            print(f"❌ Error validating instances: {e}")
            return []

def get_instance_states(ec2, instance_ids):
    """Get current state of instances"""
    try:
        response = ec2.describe_instances(InstanceIds=instance_ids)
        
        states = {}
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                instance_id = instance['InstanceId']
                state = instance['State']['Name']
                instance_type = instance['InstanceType']
                
                # Get name tag if it exists
                name = "N/A"
                if 'Tags' in instance:
                    for tag in instance['Tags']:
                        if tag['Key'] == 'Name':
                            name = tag['Value']
                            break
                
                states[instance_id] = {
                    'state': state,
                    'type': instance_type,
                    'name': name
                }
        
        return states
    except Exception as e:
        print(f"❌ Error getting instance states: {e}")
        return {}

def stop_instances(ec2, instance_ids):
    """Stop EC2 instances"""
    print("\n" + "=" * 60)
    print("STOPPING EC2 INSTANCES")
    print("=" * 60)
    
    # Get current states
    states = get_instance_states(ec2, instance_ids)
    
    # Check which instances are actually running
    running_instances = [iid for iid in instance_ids if states.get(iid, {}).get('state') == 'running']
    
    if not running_instances:
        print("ℹ️  No instances are currently running")
        return
    
    try:
        print(f"\n🛑 Stopping {len(running_instances)} instance(s)...")
        
        for instance_id in running_instances:
            info = states[instance_id]
            print(f"   • {instance_id} ({info['name']}) - {info['type']}")
        
        response = ec2.stop_instances(InstanceIds=running_instances)
        
        print("\n✅ Stop command sent successfully")
        print("\nInstance Status:")
        for instance in response['StoppingInstances']:
            current_state = instance['CurrentState']['Name']
            previous_state = instance['PreviousState']['Name']
            print(f"   • {instance['InstanceId']}: {previous_state} → {current_state}")
        
        print("\n💡 Instances will fully stop in 30-60 seconds")
        
    except ClientError as e:
        print(f"\n❌ Error stopping instances: {e}")
        sys.exit(1)

def start_instances(ec2, instance_ids):
    """Start EC2 instances"""
    print("\n" + "=" * 60)
    print("STARTING EC2 INSTANCES")
    print("=" * 60)
    
    # Get current states
    states = get_instance_states(ec2, instance_ids)
    
    # Check which instances are actually stopped
    stopped_instances = [iid for iid in instance_ids if states.get(iid, {}).get('state') == 'stopped']
    
    if not stopped_instances:
        print("ℹ️  No instances are currently stopped")
        print("\nCurrent States:")
        for instance_id, info in states.items():
            print(f"   • {instance_id} ({info['name']}): {info['state']}")
        return
    
    try:
        print(f"\n🚀 Starting {len(stopped_instances)} instance(s)...")
        
        for instance_id in stopped_instances:
            info = states[instance_id]
            print(f"   • {instance_id} ({info['name']}) - {info['type']}")
        
        response = ec2.start_instances(InstanceIds=stopped_instances)
        
        print("\n✅ Start command sent successfully")
        print("\nInstance Status:")
        for instance in response['StartingInstances']:
            current_state = instance['CurrentState']['Name']
            previous_state = instance['PreviousState']['Name']
            print(f"   • {instance['InstanceId']}: {previous_state} → {current_state}")
        
        print("\n💡 Instances will be fully running in 30-60 seconds")
        
    except ClientError as e:
        print(f"\n❌ Error starting instances: {e}")
        sys.exit(1)

def list_instances(ec2, instance_ids):
    """List current state of instances"""
    print("\n" + "=" * 60)
    print("CURRENT INSTANCE STATUS")
    print("=" * 60 + "\n")
    
    states = get_instance_states(ec2, instance_ids)
    
    if not states:
        print("ℹ️  No instances found")
        return
    
    for instance_id, info in states.items():
        state = info['state']
        
        # Color code by state
        if state == 'running':
            status_symbol = "🟢"
        elif state == 'stopped':
            status_symbol = "🔴"
        elif state == 'stopping':
            status_symbol = "🟡"
        elif state == 'pending':
            status_symbol = "🟡"
        else:
            status_symbol = "⚪"
        
        print(f"{status_symbol} {instance_id}")
        print(f"   Name: {info['name']}")
        print(f"   Type: {info['type']}")
        print(f"   State: {state.upper()}")
        print()

def main():
    """Main execution"""
    # Check for command line argument
    if len(sys.argv) < 2:
        print("❌ Error: Missing action argument")
        print("\nUsage: python EC2_Start_Stop_Scheduler.py [start|stop|status]")
        print("\nExamples:")
        print("  python EC2_Start_Stop_Scheduler.py start   # Start instances")
        print("  python EC2_Start_Stop_Scheduler.py stop    # Stop instances")
        print("  python EC2_Start_Stop_Scheduler.py status  # Check status")
        sys.exit(1)
    
    action = sys.argv[1].lower()
    
    # Initialize EC2 client
    ec2 = get_ec2_client()
    
    # Validate instance IDs
    print("🔍 Validating instance IDs...")
    valid_instances = validate_instances(ec2, INSTANCE_IDS)
    
    if not valid_instances:
        print("\n❌ No valid instances found")
        print("   Please update INSTANCE_IDS in the script with valid EC2 instance IDs")
        print("\n💡 To find your instance IDs:")
        print("   1. Go to AWS Console → EC2 → Instances")
        print("   2. Copy instance IDs (format: i-xxxxxxxxxxxx)")
        print("   3. Update INSTANCE_IDS list in this script")
        sys.exit(1)
    
    print(f"✅ Found {len(valid_instances)} valid instance(s)\n")
    
    # Execute action
    if action == "start":
        start_instances(ec2, valid_instances)
    elif action == "stop":
        stop_instances(ec2, valid_instances)
    elif action == "status" or action == "list":
        list_instances(ec2, valid_instances)
    else:
        print(f"❌ Unknown action: {action}")
        print("\nUsage: python EC2_Start_Stop_Scheduler.py [start|stop|status]")
        sys.exit(1)

if __name__ == "__main__":
    main()