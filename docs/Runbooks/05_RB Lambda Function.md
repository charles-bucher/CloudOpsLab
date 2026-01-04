# Runbook: Lambda Function Troubleshooting

**Document ID:** RB-005  
**Last Updated:** January 2026  
**Owner:** Charles Bucher  
**Severity:** P2 (High)  

---

## 📋 Overview

### Purpose
Systematically troubleshoot Lambda function failures including timeouts, permission errors, and runtime issues.

### When to Use
- Lambda function returns errors
- Function times out
- CloudWatch shows invocation failures
- Integration with other services fails
- Automation scripts using Lambda not working

### Expected Resolution Time
- **Simple errors:** 5-10 minutes
- **Complex issues:** 20-45 minutes

---

## 🚨 Common Lambda Errors

### 1. Timeout Errors
```
Task timed out after 3.00 seconds
```

### 2. Memory Errors
```
Runtime.OutOfMemory: Memory Size: 128 MB Max Memory Used: 129 MB
```

### 3. Permission Errors
```
AccessDeniedException: User is not authorized to perform: dynamodb:PutItem
```

### 4. Runtime Errors
```
Unable to import module 'lambda_function': No module named 'boto3'
```

### 5. Cold Start Issues
```
[ERROR] Initialization took longer than 10 seconds
```

---

## 🔍 Step 1: Check CloudWatch Logs (2 minutes)

### View Recent Errors
```bash
# Get Lambda function logs
aws logs tail /aws/lambda/my-function --follow

# Filter for errors only
aws logs filter-log-events \
  --log-group-name /aws/lambda/my-function \
  --start-time $(date -u -d '1 hour ago' +%s)000 \
  --filter-pattern "ERROR"

# Get specific invocation
aws logs filter-log-events \
  --log-group-name /aws/lambda/my-function \
  --filter-pattern "RequestId: abc123" \
  --start-time $(date -u -d '1 hour ago' +%s)000
```

### What to Look For:
- **Timeout:** `Task timed out after X.XX seconds`
- **Memory:** `Memory Size: X MB Max Memory Used: X MB`
- **Permissions:** `AccessDeniedException`, `UnauthorizedException`
- **Import errors:** `Unable to import module`, `No module named`
- **Runtime errors:** Stack traces, exception messages

---

## 🔧 Issue 1: Lambda Timeout

### Problem Detection
```
[ERROR] 2026-01-03T12:34:56.789Z abc-123-def Task timed out after 3.00 seconds
```

### Investigation

#### Step 1: Check Current Timeout Setting
```bash
aws lambda get-function-configuration \
  --function-name my-function \
  --query 'Timeout'
```

**Default:** 3 seconds  
**Maximum:** 900 seconds (15 minutes)

#### Step 2: Analyze Execution Duration
```bash
# Get recent execution times
aws logs filter-log-events \
  --log-group-name /aws/lambda/my-function \
  --filter-pattern "Duration:" \
  --start-time $(date -u -d '1 day ago' +%s)000 \
  | grep "Duration" \
  | awk '{print $5}' \
  | sort -n
```

#### Step 3: Identify What's Slow
```python
# Add timing to your Lambda code
import time

def lambda_handler(event, context):
    start = time.time()
    
    # Operation 1
    result1 = slow_database_query()
    print(f"DB Query took: {time.time() - start:.2f}s")
    
    # Operation 2  
    result2 = external_api_call()
    print(f"API Call took: {time.time() - start:.2f}s")
    
    return result
```

### Resolution

#### Option A: Increase Timeout (Quick Fix)
```bash
# Increase timeout to 30 seconds
aws lambda update-function-configuration \
  --function-name my-function \
  --timeout 30
```

#### Option B: Optimize Code (Better Fix)

**Common Optimizations:**

1. **Use connection pooling:**
```python
# BAD - Creates new connection each time
def lambda_handler(event, context):
    db = connect_to_database()  # Slow!
    result = db.query()
    return result

# GOOD - Reuse connection
import os
DB_CONNECTION = None

def get_db_connection():
    global DB_CONNECTION
    if DB_CONNECTION is None:
        DB_CONNECTION = connect_to_database()
    return DB_CONNECTION

def lambda_handler(event, context):
    db = get_db_connection()  # Fast!
    result = db.query()
    return result
```

2. **Parallelize operations:**
```python
import concurrent.futures

def lambda_handler(event, context):
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        # Run multiple operations concurrently
        future1 = executor.submit(fetch_from_api_1)
        future2 = executor.submit(fetch_from_api_2)
        future3 = executor.submit(fetch_from_database)
        
        # Wait for all to complete
        results = [f.result() for f in [future1, future2, future3]]
    
    return results
```

3. **Move large data processing outside Lambda:**
```python
# Instead of processing in Lambda, use Step Functions
# Or trigger ECS task for heavy processing
```

---

## 🔧 Issue 2: Out of Memory

### Problem Detection
```
Runtime.OutOfMemory: Memory Size: 128 MB Max Memory Used: 135 MB
```

### Investigation

#### Step 1: Check Memory Configuration
```bash
aws lambda get-function-configuration \
  --function-name my-function \
  --query '[MemorySize,Timeout]'
```

#### Step 2: Review Memory Usage Patterns
```bash
# Extract max memory from logs
aws logs filter-log-events \
  --log-group-name /aws/lambda/my-function \
  --filter-pattern "Max Memory Used" \
  --start-time $(date -u -d '1 day ago' +%s)000 \
  | grep "Max Memory Used" \
  | awk '{print $(NF-1)}' \
  | sort -n | tail -20
```

### Resolution

#### Option A: Increase Memory
```bash
# Increase from 128 MB to 512 MB
aws lambda update-function-configuration \
  --function-name my-function \
  --memory-size 512
```

**Note:** More memory = more CPU too!

#### Option B: Optimize Memory Usage

**Common Memory Leaks:**

1. **Large objects in global scope:**
```python
# BAD - Loaded every cold start
LARGE_DATA = load_10mb_file()  # Memory leak!

def lambda_handler(event, context):
    process(LARGE_DATA)

# GOOD - Load only when needed
def lambda_handler(event, context):
    data = load_data_from_s3()  # Load on demand
    process(data)
    data = None  # Explicitly free memory
```

2. **Not closing connections:**
```python
# BAD
def lambda_handler(event, context):
    s3 = boto3.client('s3')
    # Client never explicitly closed

# GOOD
def lambda_handler(event, context):
    with boto3.client('s3') as s3:
        # Automatically closed after use
        result = s3.get_object(Bucket='bucket', Key='key')
```

---

## 🔧 Issue 3: Permission Errors

### Problem Detection
```
[ERROR] AccessDeniedException: User: arn:aws:sts::123:assumed-role/MyLambdaRole/my-function is not authorized to perform: dynamodb:PutItem
```

### Investigation

#### Step 1: Identify Required Permission
From error message, extract:
- **Action:** `dynamodb:PutItem`
- **Resource:** DynamoDB table ARN (if shown)
- **Role:** Lambda execution role

#### Step 2: Check Lambda Execution Role
```bash
# Get Lambda role
ROLE_ARN=$(aws lambda get-function-configuration \
  --function-name my-function \
  --query 'Role' \
  --output text)

echo "Lambda Role: $ROLE_ARN"

# Extract role name
ROLE_NAME=$(echo $ROLE_ARN | cut -d'/' -f2)

# List attached policies
aws iam list-attached-role-policies --role-name $ROLE_NAME
```

#### Step 3: Review Policy Permissions
```bash
# Get policy document
POLICY_ARN=$(aws iam list-attached-role-policies \
  --role-name $ROLE_NAME \
  --query 'AttachedPolicies[0].PolicyArn' \
  --output text)

# View policy
aws iam get-policy --policy-arn $POLICY_ARN
aws iam get-policy-version \
  --policy-arn $POLICY_ARN \
  --version-id $(aws iam get-policy --policy-arn $POLICY_ARN --query 'Policy.DefaultVersionId' --output text)
```

### Resolution

#### Add Missing Permission
```bash
# Create policy document
cat > lambda-policy.json << 'EOF'
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "dynamodb:PutItem",
        "dynamodb:GetItem",
        "dynamodb:UpdateItem"
      ],
      "Resource": "arn:aws:dynamodb:us-east-1:123456789012:table/MyTable"
    }
  ]
}
EOF

# Attach to role
aws iam put-role-policy \
  --role-name $ROLE_NAME \
  --policy-name DynamoDBAccess \
  --policy-document file://lambda-policy.json
```

#### Test Permission
```bash
# Test Lambda again
aws lambda invoke \
  --function-name my-function \
  --payload '{"test": "data"}' \
  response.json

cat response.json
```

---

## 🔧 Issue 4: Import/Module Errors

### Problem Detection
```
[ERROR] Unable to import module 'lambda_function': No module named 'requests'
```

### Common Causes:
1. Missing package in deployment
2. Wrong Python version
3. Package needs compilation (numpy, pandas)
4. Incorrect file structure

### Investigation

#### Step 1: Check Deployment Package
```bash
# Download current deployment
aws lambda get-function --function-name my-function \
  --query 'Code.Location' --output text | xargs curl -o function.zip

# Inspect contents
unzip -l function.zip
```

#### Step 2: Check for Package
```bash
# Check if package exists
unzip -l function.zip | grep requests
```

### Resolution

#### Option A: Package with Dependencies
```bash
# Create deployment package
mkdir lambda-package
cd lambda-package

# Install dependencies
pip install requests -t .

# Add your Lambda code
cp ../lambda_function.py .

# Create zip
zip -r ../lambda-deployment.zip .

# Upload
cd ..
aws lambda update-function-code \
  --function-name my-function \
  --zip-file fileb://lambda-deployment.zip
```

#### Option B: Use Lambda Layers
```bash
# Create layer with dependencies
mkdir python
pip install requests -t python/
zip -r requests-layer.zip python

# Publish layer
aws lambda publish-layer-version \
  --layer-name requests-layer \
  --zip-file fileb://requests-layer.zip \
  --compatible-runtimes python3.9 python3.10

# Attach to function
aws lambda update-function-configuration \
  --function-name my-function \
  --layers arn:aws:lambda:us-east-1:123:layer:requests-layer:1
```

#### Option C: Use Container Images (for compiled packages)
```dockerfile
FROM public.ecr.aws/lambda/python:3.9

# Copy requirements
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Install dependencies
RUN pip install -r requirements.txt

# Copy function code
COPY lambda_function.py ${LAMBDA_TASK_ROOT}

# Set handler
CMD ["lambda_function.lambda_handler"]
```

---

## 🔧 Issue 5: Cold Start Performance

### Problem Detection
```
REPORT Duration: 8523.45 ms  Billed Duration: 8524 ms  Init Duration: 8234.12 ms
```

**Init Duration > 3 seconds = Problem**

### Investigation

#### Check Cold Start Frequency
```bash
# Find cold starts (look for Init Duration)
aws logs filter-log-events \
  --log-group-name /aws/lambda/my-function \
  --filter-pattern "Init Duration" \
  --start-time $(date -u -d '1 day ago' +%s)000
```

### Resolution

#### Option A: Provisioned Concurrency
```bash
# Keep function warm
aws lambda put-provisioned-concurrency-config \
  --function-name my-function \
  --provisioned-concurrent-executions 2
```

**Cost:** Higher, but eliminates cold starts

#### Option B: Optimize Initialization

**Move slow operations out of global scope:**
```python
# BAD - Runs on every cold start
import heavy_library  # 5 seconds!
DATABASE = connect_to_db()  # 3 seconds!

def lambda_handler(event, context):
    return process()

# GOOD - Lazy loading
DATABASE = None

def get_database():
    global DATABASE
    if DATABASE is None:
        DATABASE = connect_to_db()
    return DATABASE

def lambda_handler(event, context):
    db = get_database()
    return process(db)
```

#### Option C: Use Smaller Deployment Packages
```bash
# Remove unnecessary files
find . -type f -name "*.pyc" -delete
find . -type d -name "__pycache__" -delete
find . -type d -name "tests" -exec rm -rf {} +
```

---

## ✅ Verification Checklist

After fixing Lambda issue:

- [ ] **Test invocation succeeds:**
```bash
aws lambda invoke \
  --function-name my-function \
  --payload '{"test": "data"}' \
  response.json && cat response.json
```

- [ ] **Check CloudWatch logs:**
```bash
aws logs tail /aws/lambda/my-function --since 5m
```

- [ ] **Verify metrics:**
```bash
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name Errors \
  --dimensions Name=FunctionName,Value=my-function \
  --start-time $(date -u -d '1 hour ago' --iso-8601=seconds) \
  --end-time $(date -u --iso-8601=seconds) \
  --period 300 \
  --statistics Sum
```

- [ ] **Test integrated workflow:**
  - If triggered by S3, upload test file
  - If triggered by API Gateway, make HTTP request
  - If scheduled, wait for next execution

---

## 📊 Lambda Troubleshooting Flowchart

```
Lambda Error
    ↓
Check CloudWatch Logs
    ↓
├─ Timeout Error? ──→ Increase timeout or optimize code
├─ Memory Error? ──→ Increase memory or fix memory leaks
├─ Permission Error? ──→ Update IAM role policy
├─ Import Error? ──→ Fix deployment package
├─ Cold Start Issue? ──→ Use provisioned concurrency
└─ Other Runtime Error? ──→ Debug with logging

    ↓
Test Fix
    ↓
Monitor for 24 hours
    ↓
Document solution
```

---

## 🛡️ Prevention Strategies

### 1. Add Comprehensive Logging
```python
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info(f"Received event: {event}")
    
    try:
        result = process_event(event)
        logger.info(f"Processing successful: {result}")
        return result
    except Exception as e:
        logger.error(f"Error processing event: {e}", exc_info=True)
        raise
```

### 2. Set Appropriate Timeouts
```bash
# Calculate needed timeout from testing
# Add 20% buffer
# Never use default 3 seconds for complex operations
```

### 3. Use Dead Letter Queues
```bash
# Create DLQ
aws sqs create-queue --queue-name lambda-dlq

# Configure Lambda to use it
aws lambda update-function-configuration \
  --function-name my-function \
  --dead-letter-config TargetArn=arn:aws:sqs:us-east-1:123:lambda-dlq
```

### 4. Implement Monitoring
```python
# Add custom metrics
import boto3
cloudwatch = boto3.client('cloudwatch')

def lambda_handler(event, context):
    try:
        result = process()
        
        # Track success
        cloudwatch.put_metric_data(
            Namespace='MyApp/Lambda',
            MetricData=[{
                'MetricName': 'SuccessfulInvocations',
                'Value': 1,
                'Unit': 'Count'
            }]
        )
        
        return result
    except Exception as e:
        # Track failure
        cloudwatch.put_metric_data(
            Namespace='MyApp/Lambda',
            MetricData=[{
                'MetricName': 'FailedInvocations',
                'Value': 1,
                'Unit': 'Count'
            }]
        )
        raise
```

### 5. Test Locally
```bash
# Use SAM CLI for local testing
sam local invoke MyFunction --event event.json
```

---

## 📝 Lambda Debugging Script

```python
#!/usr/bin/env python3
"""
lambda_debugger.py - Quick Lambda troubleshooting
"""
import boto3
import json
from datetime import datetime, timedelta

def debug_lambda(function_name):
    lambda_client = boto3.client('lambda')
    logs_client = boto3.client('logs')
    
    print(f"=== Debugging Lambda: {function_name} ===\n")
    
    # 1. Get configuration
    print("1. Configuration:")
    config = lambda_client.get_function_configuration(
        FunctionName=function_name
    )
    print(f"   Timeout: {config['Timeout']}s")
    print(f"   Memory: {config['MemorySize']} MB")
    print(f"   Runtime: {config['Runtime']}")
    print(f"   Role: {config['Role']}")
    
    # 2. Check recent errors
    print("\n2. Recent Errors (last hour):")
    log_group = f"/aws/lambda/{function_name}"
    
    start_time = int((datetime.now() - timedelta(hours=1)).timestamp() * 1000)
    
    errors = logs_client.filter_log_events(
        logGroupName=log_group,
        startTime=start_time,
        filterPattern="ERROR"
    )
    
    for event in errors['events'][:5]:
        print(f"   {event['message'][:100]}...")
    
    # 3. Check metrics
    print("\n3. Metrics (last hour):")
    cloudwatch = boto3.client('cloudwatch')
    
    metrics = {
        'Invocations': 'Count',
        'Errors': 'Count',
        'Duration': 'Average',
        'Throttles': 'Count'
    }
    
    for metric_name, stat in metrics.items():
        response = cloudwatch.get_metric_statistics(
            Namespace='AWS/Lambda',
            MetricName=metric_name,
            Dimensions=[{'Name': 'FunctionName', 'Value': function_name}],
            StartTime=datetime.now() - timedelta(hours=1),
            EndTime=datetime.now(),
            Period=3600,
            Statistics=[stat]
        )
        
        if response['Datapoints']:
            value = response['Datapoints'][0][stat]
            print(f"   {metric_name}: {value}")
    
    # 4. Test invocation
    print("\n4. Test Invocation:")
    try:
        response = lambda_client.invoke(
            FunctionName=function_name,
            InvocationType='RequestResponse',
            Payload=json.dumps({'test': True})
        )
        
        if response['StatusCode'] == 200:
            print("   ✅ Test invocation successful")
        else:
            print(f"   ❌ Test failed: {response['StatusCode']}")
            
    except Exception as e:
        print(f"   ❌ Test error: {e}")

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("Usage: python lambda_debugger.py <function-name>")
        sys.exit(1)
    
    debug_lambda(sys.argv[1])
```

**Usage:**
```bash
python lambda_debugger.py my-function
```

---

## 📚 Related Resources

### AWS Documentation
- [Lambda Troubleshooting](https://docs.aws.amazon.com/lambda/latest/dg/lambda-troubleshooting.html)
- [Lambda Best Practices](https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html)
- [Lambda Limits](https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-limits.html)

### Related Runbooks
- RB-001: EC2 Auto-Recovery
- RB-006: IAM Permission Denied
- RB-007: Security Audit Procedures

---

**Document Version:** 1.0  
**Runbook Maintainer:** Charles Bucher  
**Contact:** quietopscb@gmail.com  
**Review Frequency:** Quarterly