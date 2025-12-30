#!/usr/bin/env python3
"""
CloudOpsLab Health Check Script
Performs system health checks on AWS resources
"""

import boto3
import sys
from datetime import datetime

def check_ec2_health():
    """Check EC2 instance health"""
    try:
        ec2 = boto3.client('ec2')
        response = ec2.describe_instance_status()
        
        healthy_count = 0
        unhealthy_count = 0
        
        print("=" * 60)
        print("EC2 INSTANCE HEALTH CHECK")
        print("=" * 60)
        
        if not response['InstanceStatuses']:
            print("ℹ️  No running instances found")
            return True
        
        for instance in response['InstanceStatuses']:
            instance_id = instance['InstanceId']
            instance_state = instance['InstanceState']['Name']
            system_status = instance['SystemStatus']['Status']
            instance_status = instance['InstanceStatus']['Status']
            
            if system_status == 'ok' and instance_status == 'ok':
                print(f"✅ {instance_id}: HEALTHY")
                print(f"   State: {instance_state}")
                print(f"   System Status: {system_status}")
                print(f"   Instance Status: {instance_status}")
                healthy_count += 1
            else:
                print(f"❌ {instance_id}: UNHEALTHY")
                print(f"   State: {instance_state}")
                print(f"   System Status: {system_status}")
                print(f"   Instance Status: {instance_status}")
                unhealthy_count += 1
            print()
        
        print("-" * 60)
        print(f"Total Healthy: {healthy_count}")
        print(f"Total Unhealthy: {unhealthy_count}")
        print("-" * 60)
        
        return unhealthy_count == 0
        
    except Exception as e:
        print(f"❌ Error checking EC2 health: {e}")
        return False

def check_s3_health():
    """Check S3 bucket accessibility"""
    try:
        s3 = boto3.client('s3')
        response = s3.list_buckets()
        
        print("\n" + "=" * 60)
        print("S3 BUCKET HEALTH CHECK")
        print("=" * 60)
        
        if not response['Buckets']:
            print("ℹ️  No S3 buckets found")
            return True
        
        accessible_count = 0
        error_count = 0
        
        for bucket in response['Buckets']:
            bucket_name = bucket['Name']
            try:
                # Try to get bucket location (quick access test)
                s3.get_bucket_location(Bucket=bucket_name)
                print(f"✅ {bucket_name}: ACCESSIBLE")
                accessible_count += 1
            except Exception as e:
                print(f"❌ {bucket_name}: ERROR - {str(e)}")
                error_count += 1
        
        print("-" * 60)
        print(f"Total Accessible: {accessible_count}")
        print(f"Total Errors: {error_count}")
        print("-" * 60)
        
        return error_count == 0
        
    except Exception as e:
        print(f"❌ Error checking S3 health: {e}")
        return False

def check_lambda_health():
    """Check Lambda function health"""
    try:
        lambda_client = boto3.client('lambda')
        response = lambda_client.list_functions()
        
        print("\n" + "=" * 60)
        print("LAMBDA FUNCTION HEALTH CHECK")
        print("=" * 60)
        
        if not response['Functions']:
            print("ℹ️  No Lambda functions found")
            return True
        
        healthy_count = 0
        
        for function in response['Functions']:
            function_name = function['FunctionName']
            state = function.get('State', 'Unknown')
            last_modified = function['LastModified']
            
            if state == 'Active':
                print(f"✅ {function_name}: ACTIVE")
                print(f"   Runtime: {function['Runtime']}")
                print(f"   Last Modified: {last_modified}")
                healthy_count += 1
            else:
                print(f"⚠️  {function_name}: {state}")
                print(f"   Runtime: {function['Runtime']}")
                print(f"   Last Modified: {last_modified}")
            print()
        
        print("-" * 60)
        print(f"Total Functions: {len(response['Functions'])}")
        print(f"Active Functions: {healthy_count}")
        print("-" * 60)
        
        return True
        
    except Exception as e:
        print(f"❌ Error checking Lambda health: {e}")
        return False

def main():
    """Main health check execution"""
    print("\n" + "=" * 60)
    print("CLOUDOPSLAB HEALTH CHECK")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60 + "\n")
    
    all_healthy = True
    
    # Run all health checks
    ec2_healthy = check_ec2_health()
    s3_healthy = check_s3_health()
    lambda_healthy = check_lambda_health()
    
    all_healthy = ec2_healthy and s3_healthy and lambda_healthy
    
    # Final summary
    print("\n" + "=" * 60)
    print("OVERALL HEALTH STATUS")
    print("=" * 60)
    
    if all_healthy:
        print("✅ ALL SYSTEMS HEALTHY")
        sys.exit(0)
    else:
        print("❌ SOME SYSTEMS UNHEALTHY - ATTENTION REQUIRED")
        sys.exit(1)

if __name__ == "__main__":
    main()