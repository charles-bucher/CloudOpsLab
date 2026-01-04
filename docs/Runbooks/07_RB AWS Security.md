# Runbook: AWS Security Audit Procedures

**Document ID:** RB-007  
**Last Updated:** January 2026  
**Owner:** Charles Bucher  
**Severity:** P3 (Routine Maintenance)  

---

## 📋 Overview

### Purpose
Systematic security auditing of AWS environment to identify misconfigurations and compliance violations.

### When to Use
- Monthly security review
- Before compliance audit
- After major infrastructure changes
- Post-incident review
- New project initialization

### Expected Duration
- **Quick audit:** 15-20 minutes
- **Comprehensive audit:** 1-2 hours

---

## 🎯 Audit Scope

### Services Covered:
- ✅ IAM (Users, Roles, Policies)
- ✅ EC2 (Instances, Security Groups)
- ✅ S3 (Buckets, Policies)
- ✅ VPC (Network Configuration)
- ✅ CloudTrail (Logging)
- ✅ GuardDuty (Threat Detection)

---

## 🔍 Phase 1: IAM Security Audit

### 1.1 Check for Root Account Usage

**What to Check:** Root account should never be used for daily operations

```bash
# Check recent root account activity
aws cloudtrail lookup-events \
  --lookup-attributes AttributeKey=EventName,AttributeValue=ConsoleLogin \
  --max-results 50 \
  --query 'Events[?contains(Username, `root`)].[EventTime,Username,SourceIPAddress]' \
  --output table
```

**🔴 CRITICAL FINDING:** Any recent root login

**Fix:**
- Create IAM admin user
- Enable MFA on root
- Lock root credentials in safe

---

### 1.2 Check IAM Users Without MFA

```bash
# List users without MFA
aws iam get-credential-report > /dev/null 2>&1
sleep 5
aws iam get-credential-report \
  --query 'Content' \
  --output text | base64 -d > credential-report.csv

# Parse for users without MFA
awk -F',' '$4=="true" && $8=="false" {print $1}' credential-report.csv
```

**🟠 HIGH FINDING:** IAM users without MFA

**Fix:**
```bash
# Enable MFA for user
aws iam enable-mfa-device \
  --user-name username \
  --serial-number arn:aws:iam::123456789012:mfa/username \
  --authentication-code1 123456 \
  --authentication-code2 789012
```

---

### 1.3 Find Unused Access Keys

```bash
# Find access keys older than 90 days
aws iam get-credential-report --query 'Content' --output text | base64 -d | \
  awk -F',' 'NR>1 {
    if ($11 == "true") {
      cmd = "date -d \""$10"\" +%s"
      cmd | getline key1_date
      close(cmd)
      now = systime()
      days = (now - key1_date) / 86400
      if (days > 90) print $1, "Key1:", int(days), "days old"
    }
    if ($16 == "true") {
      cmd = "date -d \""$15"\" +%s"
      cmd | getline key2_date
      close(cmd)
      days = (now - key2_date) / 86400
      if (days > 90) print $1, "Key2:", int(days), "days old"
    }
  }'
```

**🟡 MEDIUM FINDING:** Access keys > 90 days old

**Fix:**
```bash
# Rotate access key
aws iam create-access-key --user-name username
# Update applications with new key
# Then delete old key
aws iam delete-access-key --user-name username --access-key-id AKIA...
```

---

### 1.4 Check for Overly Permissive Policies

```bash
# Find policies with admin access
aws iam list-policies --scope Local --query 'Policies[*].[PolicyName,Arn]' | \
  while read -r name arn; do
    policy=$(aws iam get-policy-version \
      --policy-arn "$arn" \
      --version-id $(aws iam get-policy --policy-arn "$arn" --query 'Policy.DefaultVersionId' --output text))
    
    # Check for "Action": "*"
    if echo "$policy" | grep -q '"Action": "\*"'; then
      echo "🔴 CRITICAL: $name has Action: * (full admin)"
    fi
  done
```

**🔴 CRITICAL FINDING:** Policies with `"Action": "*"`

**Fix:** Apply least privilege principle
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:DescribeInstances",
        "ec2:StartInstances",
        "ec2:StopInstances"
      ],
      "Resource": "*"
    }
  ]
}
```

---

## 🔍 Phase 2: EC2 Security Audit

### 2.1 Check Security Groups for 0.0.0.0/0 Access

```bash
# Find security groups allowing SSH from anywhere
aws ec2 describe-security-groups \
  --query 'SecurityGroups[*].[GroupId,GroupName,IpPermissions]' \
  --output json | jq -r '.[] | 
    select(.[2][]? | 
      select(.FromPort == 22 or .FromPort == 3389) | 
      select(.IpRanges[]?.CidrIp == "0.0.0.0/0")
    ) | .[0] + " " + .[1] + " allows public SSH/RDP"'
```

**🔴 CRITICAL FINDING:** SSH (22) or RDP (3389) open to 0.0.0.0/0

**Fix:**
```bash
# Remove public access
aws ec2 revoke-security-group-ingress \
  --group-id sg-xxxxx \
  --protocol tcp \
  --port 22 \
  --cidr 0.0.0.0/0

# Add your specific IP
aws ec2 authorize-security-group-ingress \
  --group-id sg-xxxxx \
  --protocol tcp \
  --port 22 \
  --cidr YOUR_IP/32
```

---

### 2.2 Find Instances Without Tags

```bash
# List untagged instances
aws ec2 describe-instances \
  --query 'Reservations[*].Instances[?length(Tags)==`0`].[InstanceId,State.Name]' \
  --output table
```

**🟡 MEDIUM FINDING:** Instances without tags

**Fix:**
```bash
# Add required tags
aws ec2 create-tags \
  --resources i-xxxxx \
  --tags \
    Key=Name,Value=WebServer \
    Key=Environment,Value=Production \
    Key=Owner,Value=TeamName \
    Key=CostCenter,Value=Engineering
```

---

### 2.3 Check for Public IP Addresses on Private Instances

```bash
# Find instances with public IPs in private subnets
aws ec2 describe-instances \
  --query 'Reservations[*].Instances[?PublicIpAddress!=`null`].[InstanceId,PublicIpAddress,PrivateIpAddress,Tags[?Key==`Name`].Value|[0]]' \
  --output table
```

**🟠 HIGH FINDING:** Database/internal servers with public IPs

**Fix:**
- Terminate and recreate in private subnet
- Use VPN/bastion host for access
- Remove public IP association

---

## 🔍 Phase 3: S3 Security Audit

### 3.1 Find Public S3 Buckets

```bash
# Check all buckets for public access
for bucket in $(aws s3 ls | awk '{print $3}'); do
  echo "Checking: $bucket"
  
  # Check public access block
  aws s3api get-public-access-block --bucket $bucket 2>/dev/null || echo "  ⚠️  No public access block set"
  
  # Check ACL
  acl=$(aws s3api get-bucket-acl --bucket $bucket 2>/dev/null)
  if echo "$acl" | grep -q "AllUsers\|AuthenticatedUsers"; then
    echo "  🔴 PUBLIC ACL detected!"
  fi
  
  # Check bucket policy
  policy=$(aws s3api get-bucket-policy --bucket $bucket 2>/dev/null)
  if echo "$policy" | grep -q '"Principal": "\*"'; then
    echo "  🔴 PUBLIC POLICY detected!"
  fi
done
```

**🔴 CRITICAL FINDING:** Public S3 buckets

**Fix:** See RB-003: S3 Public Bucket Remediation

---

### 3.2 Check S3 Encryption

```bash
# Check if buckets have default encryption
for bucket in $(aws s3 ls | awk '{print $3}'); do
  encryption=$(aws s3api get-bucket-encryption --bucket $bucket 2>&1)
  
  if echo "$encryption" | grep -q "ServerSideEncryptionConfigurationNotFoundError"; then
    echo "🟠 $bucket: No default encryption"
  else
    echo "✅ $bucket: Encryption enabled"
  fi
done
```

**🟠 HIGH FINDING:** Buckets without encryption

**Fix:**
```bash
# Enable AES-256 encryption
aws s3api put-bucket-encryption \
  --bucket my-bucket \
  --server-side-encryption-configuration '{
    "Rules": [{
      "ApplyServerSideEncryptionByDefault": {
        "SSEAlgorithm": "AES256"
      },
      "BucketKeyEnabled": true
    }]
  }'
```

---

### 3.3 Check S3 Versioning

```bash
# Check versioning status
for bucket in $(aws s3 ls | awk '{print $3}'); do
  versioning=$(aws s3api get-bucket-versioning --bucket $bucket --query 'Status' --output text)
  
  if [ "$versioning" != "Enabled" ]; then
    echo "⚠️  $bucket: Versioning not enabled"
  fi
done
```

**🟡 MEDIUM FINDING:** Versioning not enabled (ransomware protection)

**Fix:**
```bash
aws s3api put-bucket-versioning \
  --bucket my-bucket \
  --versioning-configuration Status=Enabled
```

---

## 🔍 Phase 4: VPC Security Audit

### 4.1 Check VPC Flow Logs

```bash
# List VPCs without flow logs
vpcs=$(aws ec2 describe-vpcs --query 'Vpcs[*].VpcId' --output text)

for vpc in $vpcs; do
  flow_logs=$(aws ec2 describe-flow-logs --filter Name=resource-id,Values=$vpc --query 'FlowLogs' --output text)
  
  if [ -z "$flow_logs" ]; then
    echo "⚠️  VPC $vpc: No flow logs enabled"
  fi
done
```

**🟡 MEDIUM FINDING:** VPC without flow logs

**Fix:**
```bash
# Create CloudWatch log group
aws logs create-log-group --log-group-name /aws/vpc/flowlogs

# Create IAM role for flow logs
# Then enable flow logs
aws ec2 create-flow-logs \
  --resource-type VPC \
  --resource-ids vpc-xxxxx \
  --traffic-type ALL \
  --log-destination-type cloud-watch-logs \
  --log-group-name /aws/vpc/flowlogs \
  --deliver-logs-permission-arn arn:aws:iam::123:role/flowlogsRole
```

---

### 4.2 Check for Default VPC Usage

```bash
# Find instances in default VPC
aws ec2 describe-instances \
  --filters Name=vpc-id,Values=$(aws ec2 describe-vpcs --filters Name=isDefault,Values=true --query 'Vpcs[0].VpcId' --output text) \
  --query 'Reservations[*].Instances[*].[InstanceId,Tags[?Key==`Name`].Value|[0]]' \
  --output table
```

**🟠 HIGH FINDING:** Production resources in default VPC

**Fix:**
- Create custom VPC with proper CIDR
- Migrate instances to custom VPC
- Delete default VPC (if policy allows)

---

## 🔍 Phase 5: Logging & Monitoring Audit

### 5.1 Verify CloudTrail is Enabled

```bash
# Check if CloudTrail is logging
aws cloudtrail get-trail-status --name my-trail --query 'IsLogging'
```

**🔴 CRITICAL FINDING:** CloudTrail not enabled or not logging

**Fix:**
```bash
# Create S3 bucket for logs
aws s3 mb s3://my-cloudtrail-logs

# Enable CloudTrail
aws cloudtrail create-trail \
  --name my-trail \
  --s3-bucket-name my-cloudtrail-logs

aws cloudtrail start-logging --name my-trail
```

---

### 5.2 Check GuardDuty Status

```bash
# Check if GuardDuty is enabled
aws guardduty list-detectors --query 'DetectorIds[0]' --output text
```

**🟠 HIGH FINDING:** GuardDuty not enabled

**Fix:**
```bash
# Enable GuardDuty
aws guardduty create-detector --enable
```

---

### 5.3 Review GuardDuty Findings

```bash
# Get recent GuardDuty findings
DETECTOR_ID=$(aws guardduty list-detectors --query 'DetectorIds[0]' --output text)

aws guardduty list-findings \
  --detector-id $DETECTOR_ID \
  --max-results 50 \
  --query 'FindingIds' \
  --output text | \
  xargs -I {} aws guardduty get-findings \
    --detector-id $DETECTOR_ID \
    --finding-ids {} \
    --query 'Findings[*].[Severity,Type,Title]' \
    --output table
```

**Review and act on findings.**

---

## 📊 Automated Security Audit Script

```python
#!/usr/bin/env python3
"""
security_audit.py - Comprehensive AWS security audit
"""
import boto3
import json
from datetime import datetime, timedelta
from collections import defaultdict

class SecurityAuditor:
    def __init__(self):
        self.findings = defaultdict(list)
        self.iam = boto3.client('iam')
        self.ec2 = boto3.client('ec2')
        self.s3 = boto3.client('s3')
        self.cloudtrail = boto3.client('cloudtrail')
        self.guardduty = boto3.client('guardduty')
        
    def audit_iam(self):
        """Audit IAM configuration"""
        print("🔍 Auditing IAM...")
        
        # Check root account usage
        events = self.cloudtrail.lookup_events(
            LookupAttributes=[{
                'AttributeKey': 'EventName',
                'AttributeValue': 'ConsoleLogin'
            }],
            MaxResults=50
        )
        
        for event in events['Events']:
            if 'root' in event.get('Username', ''):
                self.findings['CRITICAL'].append({
                    'service': 'IAM',
                    'finding': 'Root account login detected',
                    'resource': 'root',
                    'timestamp': event['EventTime']
                })
        
        # Check users without MFA
        users = self.iam.list_users()['Users']
        for user in users:
            mfa_devices = self.iam.list_mfa_devices(
                UserName=user['UserName']
            )
            
            if not mfa_devices['MFADevices']:
                self.findings['HIGH'].append({
                    'service': 'IAM',
                    'finding': 'User without MFA',
                    'resource': user['UserName']
                })
    
    def audit_ec2(self):
        """Audit EC2 security"""
        print("🔍 Auditing EC2...")
        
        # Check security groups
        sgs = self.ec2.describe_security_groups()['SecurityGroups']
        
        for sg in sgs:
            for rule in sg.get('IpPermissions', []):
                # Check for SSH/RDP from anywhere
                if rule.get('FromPort') in [22, 3389]:
                    for ip_range in rule.get('IpRanges', []):
                        if ip_range.get('CidrIp') == '0.0.0.0/0':
                            self.findings['CRITICAL'].append({
                                'service': 'EC2',
                                'finding': f'Port {rule["FromPort"]} open to internet',
                                'resource': sg['GroupId'],
                                'detail': sg['GroupName']
                            })
    
    def audit_s3(self):
        """Audit S3 security"""
        print("🔍 Auditing S3...")
        
        buckets = self.s3.list_buckets()['Buckets']
        
        for bucket in buckets:
            bucket_name = bucket['Name']
            
            # Check public access block
            try:
                self.s3.get_public_access_block(Bucket=bucket_name)
            except:
                self.findings['HIGH'].append({
                    'service': 'S3',
                    'finding': 'No public access block configured',
                    'resource': bucket_name
                })
            
            # Check encryption
            try:
                self.s3.get_bucket_encryption(Bucket=bucket_name)
            except:
                self.findings['HIGH'].append({
                    'service': 'S3',
                    'finding': 'Encryption not enabled',
                    'resource': bucket_name
                })
            
            # Check versioning
            versioning = self.s3.get_bucket_versioning(Bucket=bucket_name)
            if versioning.get('Status') != 'Enabled':
                self.findings['MEDIUM'].append({
                    'service': 'S3',
                    'finding': 'Versioning not enabled',
                    'resource': bucket_name
                })
    
    def audit_logging(self):
        """Audit logging configuration"""
        print("🔍 Auditing Logging...")
        
        # Check CloudTrail
        trails = self.cloudtrail.describe_trails()['trailList']
        if not trails:
            self.findings['CRITICAL'].append({
                'service': 'CloudTrail',
                'finding': 'CloudTrail not configured',
                'resource': 'Account'
            })
        
        # Check GuardDuty
        detectors = self.guardduty.list_detectors()
        if not detectors['DetectorIds']:
            self.findings['HIGH'].append({
                'service': 'GuardDuty',
                'finding': 'GuardDuty not enabled',
                'resource': 'Account'
            })
    
    def generate_report(self):
        """Generate audit report"""
        print("\n" + "="*60)
        print("AWS SECURITY AUDIT REPORT")
        print("="*60)
        print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Count findings by severity
        severity_counts = {
            'CRITICAL': len(self.findings['CRITICAL']),
            'HIGH': len(self.findings['HIGH']),
            'MEDIUM': len(self.findings['MEDIUM']),
            'LOW': len(self.findings['LOW'])
        }
        
        print("SUMMARY:")
        print(f"  🔴 Critical: {severity_counts['CRITICAL']}")
        print(f"  🟠 High: {severity_counts['HIGH']}")
        print(f"  🟡 Medium: {severity_counts['MEDIUM']}")
        print(f"  🟢 Low: {severity_counts['LOW']}")
        print()
        
        # Print detailed findings
        for severity in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']:
            if self.findings[severity]:
                print(f"\n{severity} FINDINGS:")
                print("-" * 60)
                for finding in self.findings[severity]:
                    print(f"  Service: {finding['service']}")
                    print(f"  Finding: {finding['finding']}")
                    print(f"  Resource: {finding['resource']}")
                    if 'detail' in finding:
                        print(f"  Detail: {finding['detail']}")
                    print()
        
        print("="*60)
        print("END OF REPORT")
        print("="*60)
    
    def run_audit(self):
        """Run complete audit"""
        print("Starting AWS Security Audit...")
        print()
        
        self.audit_iam()
        self.audit_ec2()
        self.audit_s3()
        self.audit_logging()
        
        self.generate_report()

if __name__ == '__main__':
    auditor = SecurityAuditor()
    auditor.run_audit()
```

**Usage:**
```bash
python3 security_audit.py > audit-report-$(date +%Y%m%d).txt
```

---

## ✅ Audit Checklist

### IAM:
- [ ] No root account usage (last 30 days)
- [ ] All users have MFA enabled
- [ ] No access keys > 90 days old
- [ ] No policies with Action: "*"
- [ ] Password policy meets requirements

### EC2:
- [ ] No SSH/RDP open to 0.0.0.0/0
- [ ] All instances have required tags
- [ ] No public IPs on private instances
- [ ] All AMIs encrypted
- [ ] EBS volumes encrypted

### S3:
- [ ] No public buckets (unless intentional)
- [ ] All buckets have encryption
- [ ] Versioning enabled
- [ ] Access logging configured
- [ ] Lifecycle policies in place

### VPC:
- [ ] Flow logs enabled
- [ ] No resources in default VPC
- [ ] NACLs properly configured
- [ ] No unused security groups

### Logging:
- [ ] CloudTrail enabled & logging
- [ ] GuardDuty enabled
- [ ] Config rules active
- [ ] Log retention configured

---

## 📚 Related Resources

### AWS Documentation
- [AWS Security Best Practices](https://aws.amazon.com/architecture/security-identity-compliance/)
- [CIS AWS Foundations Benchmark](https://www.cisecurity.org/benchmark/amazon_web_services)
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)

### Related Runbooks
- RB-003: S3 Public Bucket Remediation
- RB-006: IAM Permission Denied

---

**Document Version:** 1.0  
**Runbook Maintainer:** Charles Bucher  
**Contact:** quietopscb@gmail.com  
**Review Frequency:** Monthly