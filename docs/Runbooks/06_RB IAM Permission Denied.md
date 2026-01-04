# Runbook: IAM Permission Denied Troubleshooting

**Document ID:** RB-006  
**Last Updated:** January 2026  
**Owner:** Charles Bucher  
**Severity:** P2 (High)  

---

## 📋 Overview

### Purpose
Systematic troubleshooting of IAM permission issues preventing automation scripts, applications, or users from accessing AWS resources.

### When to Use
- Application returns `AccessDenied` errors
- Automation script fails with permission errors
- CloudTrail shows denied API calls
- User cannot access AWS Console or CLI

### Expected Resolution Time
- **Simple:** 5-10 minutes
- **Complex:** 30-60 minutes

---

## 🚨 Common Error Messages

```
# CLI/SDK errors
An error occurred (AccessDenied) when calling the [Operation]: User: arn:aws:iam::123456789012:user/charles is not authorized to perform: s3:GetObject on resource: arn:aws:s3:::my-bucket/file.txt

# Application errors  
botocore.exceptions.ClientError: An error occurred (AccessDeniedException) when calling the PutItem operation: User is not authorized to perform: dynamodb:PutItem

# CloudFormation errors
CREATE_FAILED: User: arn:aws:iam::123456789012:role/CloudFormationRole is not authorized to perform: ec2:CreateSecurityGroup
```

---

## 🔍 Step-by-Step Troubleshooting

### Step 1: Identify the Components (2 minutes)

Extract from error message:
1. **WHO** is being denied? (User, Role, Service)
2. **WHAT** action are they trying? (s3:GetObject, ec2:DescribeInstances)
3. **WHERE** are they trying to access? (Resource ARN)

**Example:**
```
Error: User: arn:aws:iam::123456789012:user/charles 
       is not authorized to perform: s3:GetObject 
       on resource: arn:aws:s3:::my-bucket/data.txt
```

**Extracted:**
- WHO: `arn:aws:iam::123456789012:user/charles`
- WHAT: `s3:GetObject`
- WHERE: `arn:aws:s3:::my-bucket/data.txt`

---

### Step 2: Find the Identity in CloudTrail (1 minute)

```bash
# Get the EXACT denied action from CloudTrail
aws cloudtrail lookup-events \
  --lookup-attributes \
    AttributeKey=EventName,AttributeValue=GetObject \
  --max-results 10 \
  --query 'Events[?contains(CloudTrailEvent, `AccessDenied`)].[EventTime,EventName,Username,Resources[0].ResourceName]' \
  --output table
```

This shows:
- Exact timestamp
- Exact action attempted
- Identity used
- Resource accessed

---

### Step 3: Check Current Permissions

#### For IAM User:
```bash
# List attached policies
aws iam list-attached-user-policies --user-name charles

# List inline policies
aws iam list-user-policies --user-name charles

# Get policy details
aws iam get-user-policy --user-name charles --policy-name MyPolicy
```

#### For IAM Role (EC2, Lambda):
```bash
# Find role name from error or instance
ROLE_NAME=$(aws sts get-caller-identity --query 'Arn' --output text | cut -d'/' -f2)

# List policies
aws iam list-attached-role-policies --role-name $ROLE_NAME

# Get policy document
aws iam get-policy --policy-arn <policy-arn>
aws iam get-policy-version \
  --policy-arn <policy-arn> \
  --version-id $(aws iam get-policy --policy-arn <policy-arn> --query 'Policy.DefaultVersionId' --output text)
```

---

### Step 4: Use IAM Policy Simulator

```bash
# Test if action would be allowed
aws iam simulate-principal-policy \
  --policy-source-arn arn:aws:iam::123456789012:user/charles \
  --action-names s3:GetObject \
  --resource-arns "arn:aws:s3:::my-bucket/data.txt"
```

**Output:**
```json
{
    "EvaluationResults": [
        {
            "EvalActionName": "s3:GetObject",
            "EvalResourceName": "arn:aws:s3:::my-bucket/data.txt",
            "EvalDecision": "implicitDeny",  # <-- This is the problem!
            "MissingContextValues": []
        }
    ]
}
```

---

## 🔧 Common Issues & Fixes

### Issue 1: Missing Permission in Policy

**Problem:** Policy doesn't include required action

**Check:**
```bash
# Search for action in policy
aws iam get-user-policy --user-name charles --policy-name MyPolicy | grep "s3:GetObject"
```

**Fix:** Add permission
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:ListBucket"  // Often also needed!
      ],
      "Resource": [
        "arn:aws:s3:::my-bucket/*",
        "arn:aws:s3:::my-bucket"
      ]
    }
  ]
}
```

**Apply:**
```bash
aws iam put-user-policy \
  --user-name charles \
  --policy-name S3Access \
  --policy-document file://policy.json
```

---

### Issue 2: Wrong Resource in Policy

**Problem:** Policy allows action but on different resource

**Example:**
```json
// Policy says:
"Resource": "arn:aws:s3:::my-bucket/*"

// But trying to access:
"arn:aws:s3:::other-bucket/file.txt"  // Wrong bucket!
```

**Fix:** Update resource ARN or use wildcard (carefully!)
```json
{
  "Resource": [
    "arn:aws:s3:::my-bucket/*",
    "arn:aws:s3:::other-bucket/*"  // Add this
  ]
}
```

---

### Issue 3: Explicit Deny Overrides Allow

**Problem:** Another policy explicitly denies the action

**Check ALL policies:**
```bash
# User policies
aws iam list-attached-user-policies --user-name charles
aws iam list-user-policies --user-name charles

# Group policies (user's groups)
aws iam list-groups-for-user --user-name charles
aws iam list-attached-group-policies --group-name MyGroup

# Check for SCPs (Organization level)
aws organizations list-policies-for-target --target-id <account-id> --filter SERVICE_CONTROL_POLICY
```

**Look for:**
```json
{
  "Effect": "Deny",  // <-- This overrides everything
  "Action": "s3:*"
}
```

**Fix:** Remove or modify the Deny statement

---

### Issue 4: Resource-Based Policy Denies Access

**Problem:** S3 bucket policy, KMS key policy, etc. denies access

**Check S3 bucket policy:**
```bash
aws s3api get-bucket-policy --bucket my-bucket | jq -r '.Policy' | jq .
```

**Look for:**
```json
{
  "Effect": "Deny",
  "Principal": "*",
  "Action": "s3:GetObject"
}
```

**Fix:** Update bucket policy
```bash
# Remove deny or add exception
aws s3api put-bucket-policy --bucket my-bucket --policy file://new-policy.json
```

---

### Issue 5: Missing Trust Relationship (Roles)

**Problem:** Service can't assume the role

**Check trust policy:**
```bash
aws iam get-role --role-name MyRole --query 'Role.AssumeRolePolicyDocument'
```

**Should include:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"  // Or ec2, ecs, etc.
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

**Fix:**
```bash
aws iam update-assume-role-policy \
  --role-name MyRole \
  --policy-document file://trust-policy.json
```

---

### Issue 6: Session/Token Expired

**Problem:** Temporary credentials expired

**Check:**
```bash
# Get credential expiration
aws sts get-caller-identity

# If using assume-role, check expiration
aws sts get-session-token --query 'Credentials.Expiration'
```

**Fix:**
```bash
# Re-authenticate
aws configure

# Or for assumed role
aws sts assume-role \
  --role-arn arn:aws:iam::123456789012:role/MyRole \
  --role-session-name MySession
```

---

### Issue 7: Condition Not Met

**Problem:** Policy has condition that isn't satisfied

**Example policy:**
```json
{
  "Effect": "Allow",
  "Action": "s3:GetObject",
  "Resource": "*",
  "Condition": {
    "IpAddress": {
      "aws:SourceIp": "203.0.113.0/24"  // Must be from this IP range
    }
  }
}
```

**Check current IP:**
```bash
curl ifconfig.me
```

**Fix:** Either:
1. Access from allowed IP
2. Update policy condition
3. Remove condition if not needed

---

## 🎯 Quick Diagnostic Script

```bash
#!/bin/bash
# iam-permission-debug.sh

USER_ARN="$1"
ACTION="$2"
RESOURCE="$3"

echo "=== IAM Permission Debugger ==="
echo "User/Role: $USER_ARN"
echo "Action: $ACTION"
echo "Resource: $RESOURCE"
echo ""

# Extract user/role name
if [[ $USER_ARN == *"user"* ]]; then
  ENTITY_TYPE="user"
  ENTITY_NAME=$(echo $USER_ARN | cut -d'/' -f2)
else
  ENTITY_TYPE="role"
  ENTITY_NAME=$(echo $USER_ARN | cut -d'/' -f2)
fi

echo "=== Attached Policies ==="
if [ "$ENTITY_TYPE" == "user" ]; then
  aws iam list-attached-user-policies --user-name $ENTITY_NAME
else
  aws iam list-attached-role-policies --role-name $ENTITY_NAME
fi

echo ""
echo "=== Testing Permission ==="
aws iam simulate-principal-policy \
  --policy-source-arn $USER_ARN \
  --action-names $ACTION \
  --resource-arns $RESOURCE

echo ""
echo "=== Recent CloudTrail Denials ==="
aws cloudtrail lookup-events \
  --lookup-attributes AttributeKey=EventName,AttributeValue=$(echo $ACTION | cut -d':' -f2) \
  --max-results 5 \
  --query 'Events[?contains(CloudTrailEvent, `AccessDenied`)].[EventTime,Username]' \
  --output table
```

**Usage:**
```bash
chmod +x iam-permission-debug.sh

./iam-permission-debug.sh \
  "arn:aws:iam::123456789012:user/charles" \
  "s3:GetObject" \
  "arn:aws:s3:::my-bucket/file.txt"
```

---

## 📊 Troubleshooting Flowchart

```
Start
  ↓
Get Error Message
  ↓
Extract: WHO, WHAT, WHERE
  ↓
Check CloudTrail for details ──→ No logs? Check region/time
  ↓
Check Identity Policies
  ↓
Action in policy? ──→ NO ──→ ADD permission ──→ Test
  ↓ YES
Resource matches? ──→ NO ──→ FIX resource ARN ──→ Test
  ↓ YES
Any Deny statements? ──→ YES ──→ REMOVE/FIX Deny ──→ Test
  ↓ NO
Check Resource Policy
  ↓
Denies access? ──→ YES ──→ FIX resource policy ──→ Test
  ↓ NO
Check Trust Policy (if role)
  ↓
Service allowed? ──→ NO ──→ ADD service ──→ Test
  ↓ YES
Check Conditions
  ↓
Condition met? ──→ NO ──→ FIX condition ──→ Test
  ↓ YES
Escalate to AWS Support
```

---

## ✅ Verification

### Test Permission
```bash
# Try the action that was failing
aws s3 cp s3://my-bucket/file.txt ./test.txt

# Or run your script again
python automation/my_script.py
```

### Verify in Policy Simulator
```bash
aws iam simulate-principal-policy \
  --policy-source-arn <user-arn> \
  --action-names <action> \
  --resource-arns <resource>
```

**Expected:** `"EvalDecision": "allowed"`

---

## 🛡️ Prevention

### 1. Use Policy Templates
```json
// templates/s3-read-only-policy.json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::BUCKET_NAME/*",
        "arn:aws:s3:::BUCKET_NAME"
      ]
    }
  ]
}
```

### 2. Test Before Deploy
```bash
# Always test new policies
aws iam simulate-custom-policy \
  --policy-input-list file://new-policy.json \
  --action-names s3:GetObject \
  --resource-arns "arn:aws:s3:::my-bucket/*"
```

### 3. Use Least Privilege
- Start with minimal permissions
- Add only what's needed
- Never use `"Action": "*"` unless absolutely necessary

### 4. Document Permissions
```markdown
## Required Permissions for automation/ec2_manager.py

- ec2:DescribeInstances
- ec2:StartInstances
- ec2:StopInstances
- cloudwatch:GetMetricStatistics
```

---

## 📚 Related Resources

### AWS Documentation
- [IAM Troubleshooting](https://docs.aws.amazon.com/IAM/latest/UserGuide/troubleshoot.html)
- [Policy Evaluation Logic](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html)
- [IAM Policy Simulator](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_testing-policies.html)

### Related Runbooks
- RB-005: Lambda Function Troubleshooting
- RB-007: Security Audit Procedures

---

## ✅ Checklist

- [ ] Error message captured
- [ ] WHO, WHAT, WHERE identified
- [ ] CloudTrail checked
- [ ] Identity policies reviewed
- [ ] Resource policies checked
- [ ] Trust policies verified (if role)
- [ ] Permission added/fixed
- [ ] Policy tested with simulator
- [ ] Actual action tested
- [ ] Documentation updated

---

**Document Version:** 1.0  
**Runbook Maintainer:** Charles Bucher  
**Contact:** quietopscb@gmail.com