# Runbook: S3 Public Bucket Remediation

**Document ID:** RB-003  
**Last Updated:** January 2026  
**Owner:** Charles Bucher  
**Severity:** P1 (Critical - Security)  

---

## 📋 Overview

### Purpose
Immediate response to S3 buckets accidentally made public, preventing data exposure.

### When to Use
- Security audit detects public S3 bucket
- GuardDuty alert: "S3 bucket has suspicious access"
- Config rule violation: S3 bucket public access
- Manual discovery of public bucket

### Expected Resolution Time
- **Automated:** 1-2 minutes
- **Manual:** 3-5 minutes

---

## 🚨 Detection & Alerting

### Alert Types

**1. GuardDuty Finding:**
```
[CRITICAL] Policy:S3/BucketAnonymousAccessGranted
Bucket: my-bucket
Risk: HIGH
Action: Bucket policy allows public read/write
```

**2. AWS Config Rule:**
```
Rule: s3-bucket-public-read-prohibited
Status: NON_COMPLIANT
Bucket: my-bucket
```

**3. Security Audit Script:**
```bash
python monitoring/s3_public_check.py

OUTPUT:
❌ ALERT: Bucket 'my-bucket' is publicly accessible!
   ACL: public-read
   Policy: Allows s3:GetObject for Principal: *
```

---

## 🔍 Initial Assessment (30 seconds)

### Step 1: Confirm Public Access
```bash
# Check bucket ACL
aws s3api get-bucket-acl --bucket my-bucket

# Check bucket policy
aws s3api get-bucket-policy --bucket my-bucket

# Check public access block configuration
aws s3api get-public-access-block --bucket my-bucket
```

### Step 2: Assess Risk Level

| Configuration | Risk Level | Action |
|---------------|------------|--------|
| Public-read + sensitive data | 🔴 CRITICAL | Immediate block |
| Public-read + public website | 🟡 MEDIUM | Review intent |
| Public-write access | 🔴 CRITICAL | Immediate block |
| ListBucket public | 🟠 HIGH | Block unless required |

### Step 3: Determine Intent
```bash
# Check bucket tags for intended use
aws s3api get-bucket-tagging --bucket my-bucket

# Common public buckets:
# - Static websites
# - Public downloads
# - Public images/assets
```

**Ask:** Should this bucket be public?
- ❌ **NO** → Proceed with immediate remediation
- ✅ **YES** → Document and apply least-privilege public access

---

## 🔧 Immediate Remediation (CRITICAL)

### Option A: Automated Script (Fastest)
```bash
# Run auto-remediation script
python automation/s3_public_remediate.py --bucket my-bucket --block-all

# Script does:
# 1. Enables public access block
# 2. Removes public ACLs
# 3. Removes public bucket policies
# 4. Logs action to CloudWatch
```

### Option B: Manual Commands (2 minutes)

#### Step 1: Block ALL Public Access (Recommended)
```bash
aws s3api put-public-access-block \
  --bucket my-bucket \
  --public-access-block-configuration \
    BlockPublicAcls=true,\
IgnorePublicAcls=true,\
BlockPublicPolicy=true,\
RestrictPublicBuckets=true
```

**This immediately prevents:**
- New public ACLs
- New public bucket policies
- Public access even with existing permissions

#### Step 2: Remove Public ACL
```bash
# Replace public ACL with private
aws s3api put-bucket-acl \
  --bucket my-bucket \
  --acl private
```

#### Step 3: Remove Public Bucket Policy
```bash
# Option 1: Delete entire policy (if nothing else needed)
aws s3api delete-bucket-policy --bucket my-bucket

# Option 2: Update policy to remove public statements
aws s3api get-bucket-policy --bucket my-bucket > policy.json
# Edit policy.json to remove statements with "Principal": "*"
aws s3api put-bucket-policy \
  --bucket my-bucket \
  --policy file://policy.json
```

---

## ✅ Verification (1 minute)

### 1. Check Public Access Block
```bash
aws s3api get-public-access-block --bucket my-bucket
```

**Expected Output:**
```json
{
    "PublicAccessBlockConfiguration": {
        "BlockPublicAcls": true,
        "IgnorePublicAcls": true,
        "BlockPublicPolicy": true,
        "RestrictPublicBuckets": true
    }
}
```

### 2. Verify Bucket is Private
```bash
# Try anonymous access (should fail)
curl -I https://my-bucket.s3.amazonaws.com/

# Expected: 403 Forbidden or 404 Not Found
```

### 3. Test Legitimate Access Still Works
```bash
# Authenticated access should work
aws s3 ls s3://my-bucket/

# Application access should work (if using IAM role)
```

### 4. Check Security Tools
```bash
# Run security audit again
python monitoring/s3_public_check.py --bucket my-bucket

# Expected: ✅ Bucket 'my-bucket' is private
```

---

## 📊 Post-Remediation Investigation

### 1. Determine How Bucket Became Public
```bash
# Check CloudTrail for bucket policy/ACL changes
aws cloudtrail lookup-events \
  --lookup-attributes AttributeKey=ResourceName,AttributeValue=my-bucket \
  --max-results 50 \
  --query 'Events[?EventName==`PutBucketPolicy` || EventName==`PutBucketAcl`].[EventTime,EventName,Username]' \
  --output table
```

**Common Causes:**
- Manual error during configuration
- Automated script misconfiguration
- Terraform/CloudFormation template error
- Third-party tool default settings
- Copied configuration from public example

### 2. Check for Data Exposure
```bash
# Check if bucket was accessed while public
aws cloudtrail lookup-events \
  --lookup-attributes AttributeKey=ResourceName,AttributeValue=my-bucket \
  --max-results 100 \
  --query 'Events[?EventName==`GetObject`].[EventTime,SourceIPAddress,UserAgent]' \
  --output table

# Check S3 server access logs (if enabled)
aws s3 sync s3://my-bucket-logs/$(date +%Y-%m-%d)/ ./logs/
grep "GET " ./logs/* | grep -v "MyApp"  # Look for unexpected access
```

**Indicators of Compromise:**
- Unknown IP addresses accessing objects
- High volume of GetObject requests
- Access from unexpected geographic locations
- Non-standard User-Agent strings

### 3. Audit Bucket Contents
```bash
# List all objects (check for sensitive data)
aws s3 ls s3://my-bucket/ --recursive | wc -l

# Check for common sensitive files
aws s3 ls s3://my-bucket/ --recursive | grep -E "\.(env|key|pem|p12|pfx|sql|csv|xls)"
```

---

## 🛡️ Prevention Strategies

### 1. Enable Public Access Block Account-Wide
```bash
# Block public access for ALL buckets in account
aws s3control put-public-access-block \
  --account-id $(aws sts get-caller-identity --query Account --output text) \
  --public-access-block-configuration \
    BlockPublicAcls=true,\
IgnorePublicAcls=true,\
BlockPublicPolicy=true,\
RestrictPublicBuckets=true
```

### 2. Implement AWS Config Rules
```bash
# Deploy Config rule to detect public buckets
aws configservice put-config-rule \
  --config-rule '{
    "ConfigRuleName": "s3-bucket-public-read-prohibited",
    "Source": {
      "Owner": "AWS",
      "SourceIdentifier": "S3_BUCKET_PUBLIC_READ_PROHIBITED"
    }
  }'

# Auto-remediate with Lambda
aws configservice put-remediation-configuration \
  --config-rule-name s3-bucket-public-read-prohibited \
  --remediation-configuration '{
    "TargetType": "SSM_DOCUMENT",
    "TargetIdentifier": "AWS-PublishSNSNotification",
    "Automatic": true,
    "MaximumAutomaticAttempts": 5,
    "RetryAttemptSeconds": 60
  }'
```

### 3. Use S3 Bucket Policies with Conditions
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DenyPublicAccess",
      "Effect": "Deny",
      "Principal": "*",
      "Action": "s3:*",
      "Resource": [
        "arn:aws:s3:::my-bucket",
        "arn:aws:s3:::my-bucket/*"
      ],
      "Condition": {
        "StringNotEquals": {
          "aws:PrincipalAccount": "YOUR_ACCOUNT_ID"
        }
      }
    }
  ]
}
```

### 4. Implement Monitoring & Alerting
```python
# automation/s3_monitor.py
import boto3

def check_all_buckets():
    s3 = boto3.client('s3')
    sns = boto3.client('sns')
    
    for bucket in s3.list_buckets()['Buckets']:
        try:
            # Check public access block
            response = s3.get_public_access_block(
                Bucket=bucket['Name']
            )
            config = response['PublicAccessBlockConfiguration']
            
            if not all([
                config['BlockPublicAcls'],
                config['BlockPublicPolicy']
            ]):
                # Alert!
                sns.publish(
                    TopicArn='arn:aws:sns:region:account:alerts',
                    Subject=f"PUBLIC S3 BUCKET: {bucket['Name']}",
                    Message=f"Bucket {bucket['Name']} may be public!"
                )
        except:
            # No public access block = potentially public!
            sns.publish(
                TopicArn='arn:aws:sns:region:account:alerts',
                Subject=f"UNPROTECTED S3 BUCKET: {bucket['Name']}",
                Message=f"Bucket {bucket['Name']} has no public access block!"
            )
```

### 5. Use Terraform/IaC with Safe Defaults
```hcl
# terraform/modules/s3/main.tf
resource "aws_s3_bucket" "main" {
  bucket = var.bucket_name
}

# ALWAYS include this
resource "aws_s3_bucket_public_access_block" "main" {
  bucket = aws_s3_bucket.main.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Default to private ACL
resource "aws_s3_bucket_acl" "main" {
  bucket = aws_s3_bucket.main.id
  acl    = "private"
}
```

---

## 📞 Escalation Path

### Level 1: Immediate Remediation (0-5 minutes)
- **Action:** Block public access immediately
- **Owner:** On-call engineer, Security team

### Level 2: Investigation (5-30 minutes)
- **Action:** Determine cause, check for data exposure
- **Owner:** Security team, DevOps lead

### Level 3: Incident Response (30+ minutes)
- **Action:** Full forensics if data accessed
- **Owner:** Security team, CISO
- **Consider:** External security consultant

### Level 4: Legal/Compliance (If data exposed)
- **Action:** Breach notification (if required)
- **Owner:** Legal team, Compliance officer

---

## 🚨 Special Cases

### Case 1: Bucket SHOULD Be Public (Static Website)

**If legitimate public bucket:**
```bash
# Use least-privilege public access
aws s3api put-bucket-policy --bucket my-public-website --policy '{
  "Version": "2012-10-17",
  "Statement": [{
    "Sid": "PublicReadGetObject",
    "Effect": "Allow",
    "Principal": "*",
    "Action": "s3:GetObject",
    "Resource": "arn:aws:s3:::my-public-website/*"
  }]
}'

# Still block public write/list
aws s3api put-public-access-block \
  --bucket my-public-website \
  --public-access-block-configuration \
    BlockPublicAcls=true,\
IgnorePublicAcls=true,\
BlockPublicPolicy=false,\  # Allow public policy for GetObject
RestrictPublicBuckets=false
```

**Document it:**
- Add tag: `Public=true`, `Purpose=StaticWebsite`
- Document in team wiki
- Add to "intentionally public" list
- Review quarterly

---

### Case 2: Data Definitely Exposed

**Immediate Actions:**
```bash
# 1. Block access
# 2. Create forensic snapshot
aws s3 sync s3://my-bucket/ s3://forensic-bucket-$(date +%Y%m%d)/ --storage-class GLACIER

# 3. Notify required parties
python scripts/breach_notification.py --bucket my-bucket

# 4. Document everything
aws cloudtrail lookup-events \
  --lookup-attributes AttributeKey=ResourceName,AttributeValue=my-bucket \
  --start-time $(date -u -d '7 days ago' --iso-8601=seconds) > incident_log.json
```

**Follow company breach response plan.**

---

## 📝 Incident Report Template

```markdown
### S3 Public Bucket Incident Report

**Date:** [YYYY-MM-DD HH:MM]
**Bucket Name:** [bucket-name]
**Account ID:** [account-id]

**Detection:**
- Method: [GuardDuty / Config / Audit Script / Manual]
- Detected at: [HH:MM UTC]
- Detected by: [Person/System]

**Exposure Window:**
- Bucket made public: [YYYY-MM-DD HH:MM] (from CloudTrail)
- Remediated: [YYYY-MM-DD HH:MM]
- **Total exposure:** [X hours/minutes]

**Public Access Configuration:**
- ACL: [public-read / public-read-write]
- Bucket Policy: [Yes/No - describe if yes]
- Public Access Block: [Not configured / Partial / None]

**Data Exposure:**
- Object count: [number]
- Total size: [GB]
- Sensitive data: [Yes/No - describe]
- Known access: [number of GetObject events from unknown IPs]

**Root Cause:**
[Terraform error / Manual misconfiguration / Script bug / etc.]

**Remediation:**
- Public access blocked: [HH:MM]
- Verification completed: [HH:MM]
- All access tests passed: [Yes/No]

**Impact Assessment:**
- Data accessed by unauthorized parties: [Yes/No/Unknown]
- Compliance impact: [HIPAA/PCI/SOC2/GDPR - list applicable]
- Customer impact: [None / Potential / Confirmed]

**Prevention:**
1. [Specific action taken]
2. [Monitoring added]
3. [Process changed]
4. [Training completed]

**Follow-up:**
- [ ] Notify compliance team
- [ ] Review all S3 buckets
- [ ] Update IaC templates
- [ ] Team training on S3 security
- [ ] Implement account-wide public access block
```

---

## 📚 Related Resources

### AWS Documentation
- [S3 Block Public Access](https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-control-block-public-access.html)
- [S3 Bucket Policies](https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucket-policies.html)
- [S3 Security Best Practices](https://docs.aws.amazon.com/AmazonS3/latest/userguide/security-best-practices.html)

### Related Runbooks
- RB-004: GuardDuty Finding Response
- RB-006: IAM Permission Denied
- RB-007: Security Audit Procedures

### Scripts Used
- `automation/s3_public_check.py`
- `automation/s3_public_remediate.py`
- `monitoring/security_audit.py`

---

## ✅ Checklist

### Immediate Response:
- [ ] Public access confirmed
- [ ] Risk level assessed
- [ ] Public access blocked (all 4 settings)
- [ ] Bucket verified private
- [ ] Legitimate access still works

### Investigation:
- [ ] CloudTrail reviewed for cause
- [ ] Access logs checked for exposure
- [ ] Bucket contents audited
- [ ] Sensitive data identified

### Prevention:
- [ ] Account-wide block implemented
- [ ] Config rules deployed
- [ ] IaC templates updated
- [ ] Team training completed
- [ ] Monitoring enhanced

### Documentation:
- [ ] Incident report completed
- [ ] Root cause documented
- [ ] Timeline established
- [ ] Lessons learned captured

---

**Document Version:** 1.0  
**Last Tested:** [YYYY-MM-DD]  
**Next Review:** Quarterly

**Runbook Maintainer:** Charles Bucher  
**Contact:** quietopscb@gmail.com