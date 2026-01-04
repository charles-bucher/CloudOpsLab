# Runbook: CloudWatch Alarm Not Firing

**Document ID:** RB-004  
**Last Updated:** January 2026  
**Owner:** Charles Bucher  
**Severity:** P2 (High)  

---

## 📋 Overview

### Purpose
Troubleshoot CloudWatch alarms that aren't triggering when they should, ensuring monitoring reliability.

### When to Use
- Known issue occurred but no alert received
- Testing alarm and it doesn't trigger
- Alarm shows "Insufficient Data"
- SNS notifications not received
- Alarm state stuck

### Expected Resolution Time
- **Configuration issue:** 5-10 minutes
- **Data/metrics issue:** 10-20 minutes

---

## 🚨 Symptoms

### Common Indicators:
- CPU at 95%, but no alert received
- Alarm dashboard shows "OK" when metrics show problem
- Test event doesn't trigger notification
- Alarm shows "Insufficient Data" for extended period
- Notification went to wrong email/SNS topic

---

## 🔍 Step 1: Verify Alarm Exists & Is Enabled

### Check Alarm Status
```bash
# List all alarms
aws cloudwatch describe-alarms --query 'MetricAlarms[*].[AlarmName,StateValue]' --output table

# Check specific alarm
aws cloudwatch describe-alarms \
  --alarm-names "EC2-HighCPU-i-xxxxx" \
  --query 'MetricAlarms[0].[AlarmName,StateValue,ActionsEnabled]'
```

**Expected Output:**
```
[
    "EC2-HighCPU-i-xxxxx",
    "OK",              # or "ALARM" or "INSUFFICIENT_DATA"
    true               # Must be true!
]
```

### Common Issue: Actions Disabled
```bash
# Enable alarm actions
aws cloudwatch enable-alarm-actions \
  --alarm-names "EC2-HighCPU-i-xxxxx"
```

---

## 🔍 Step 2: Check Alarm Configuration

### Get Full Alarm Details
```bash
aws cloudwatch describe-alarms \
  --alarm-names "EC2-HighCPU-i-xxxxx" \
  | jq '.'
```

### Key Settings to Verify:

#### 1. Metric Name & Namespace
```json
{
  "MetricName": "CPUUtilization",  // Correct spelling?
  "Namespace": "AWS/EC2",           // Right namespace?
  "Dimensions": [
    {
      "Name": "InstanceId",
      "Value": "i-xxxxx"             // Correct instance ID?
    }
  ]
}
```

**Common Mistakes:**
- ❌ Typo in metric name: `"CPUUtilisation"` (British spelling won't work)
- ❌ Wrong namespace: `"EC2"` instead of `"AWS/EC2"`
- ❌ Wrong dimension: Instance ID changed after alarm created

#### 2. Threshold & Comparison Operator
```json
{
  "Threshold": 80.0,
  "ComparisonOperator": "GreaterThanThreshold",
  "Statistic": "Average",
  "Period": 300,
  "EvaluationPeriods": 2
}
```

**Verify Math:**
- Alarm triggers when: Average CPU > 80% for 2 periods of 5 minutes (10 minutes total)
- Is your threshold too high?
- Is evaluation period too long?

#### 3. Treat Missing Data
```json
{
  "TreatMissingData": "notBreaching"  // or "missing", "ignore", "breaching"
}
```

**Impact:**
- `"notBreaching"` - Missing data = OK (won't trigger alarm)
- `"breaching"` - Missing data = ALARM (triggers immediately)
- `"ignore"` - Missing data = maintains current state
- `"missing"` - Missing data = INSUFFICIENT_DATA

---

## 🔍 Step 3: Verify Metric Data Exists

### Check if Metrics Are Being Sent
```bash
# Get recent metric data
aws cloudwatch get-metric-statistics \
  --namespace AWS/EC2 \
  --metric-name CPUUtilization \
  --dimensions Name=InstanceId,Value=i-xxxxx \
  --start-time $(date -u -d '1 hour ago' --iso-8601=seconds) \
  --end-time $(date -u --iso-8601=seconds) \
  --period 300 \
  --statistics Average,Maximum \
  --query 'Datapoints[*].[Timestamp,Average,Maximum]' \
  --output table
```

### Problem: No Data Returned

**Possible Causes:**
1. **Instance stopped/terminated**
```bash
aws ec2 describe-instances --instance-ids i-xxxxx --query 'Reservations[0].Instances[0].State.Name'
```

2. **Wrong dimension value**
```bash
# List all instances to verify ID
aws ec2 describe-instances --query 'Reservations[*].Instances[*].[InstanceId,Tags[?Key==`Name`].Value|[0]]' --output table
```

3. **Metric not enabled** (for custom metrics)
```bash
# Check if custom metrics are being published
aws cloudwatch list-metrics --namespace MyApp
```

---

## 🔍 Step 4: Check Alarm Actions

### Verify SNS Topic Configuration
```bash
# Get alarm actions
ALARM_ACTIONS=$(aws cloudwatch describe-alarms \
  --alarm-names "EC2-HighCPU-i-xxxxx" \
  --query 'MetricAlarms[0].AlarmActions' \
  --output text)

echo "Alarm will notify: $ALARM_ACTIONS"

# Verify SNS topic exists
aws sns get-topic-attributes --topic-arn "$ALARM_ACTIONS"
```

### Common Issues:

#### Issue 1: No Actions Configured
```bash
# Alarm has no actions!
aws cloudwatch describe-alarms \
  --alarm-names "EC2-HighCPU-i-xxxxx" \
  --query 'MetricAlarms[0].AlarmActions'

# Output: []  <-- Empty!
```

**Fix:**
```bash
# Add SNS topic to alarm
aws cloudwatch put-metric-alarm \
  --alarm-name "EC2-HighCPU-i-xxxxx" \
  --alarm-actions arn:aws:sns:us-east-1:123456789012:MyAlertTopic \
  --metric-name CPUUtilization \
  --namespace AWS/EC2 \
  --statistic Average \
  --period 300 \
  --threshold 80 \
  --comparison-operator GreaterThanThreshold \
  --evaluation-periods 2 \
  --dimensions Name=InstanceId,Value=i-xxxxx
```

#### Issue 2: SNS Topic Doesn't Exist
```bash
# Check if topic exists
aws sns list-topics | grep MyAlertTopic

# If not found, create it
aws sns create-topic --name MyAlertTopic
```

#### Issue 3: No Subscriptions to SNS Topic
```bash
# Check subscriptions
aws sns list-subscriptions-by-topic \
  --topic-arn arn:aws:sns:us-east-1:123456789012:MyAlertTopic

# Output: empty subscriptions list
```

**Fix:**
```bash
# Subscribe email to topic
aws sns subscribe \
  --topic-arn arn:aws:sns:us-east-1:123456789012:MyAlertTopic \
  --protocol email \
  --notification-endpoint your-email@example.com

# Check your email and confirm subscription!
```

---

## 🔍 Step 5: Test the Alarm

### Method 1: Set Alarm State Manually (Quickest Test)
```bash
# Force alarm into ALARM state
aws cloudwatch set-alarm-state \
  --alarm-name "EC2-HighCPU-i-xxxxx" \
  --state-value ALARM \
  --state-reason "Testing alarm notification"

# Check if you receive notification
# Then reset to OK
aws cloudwatch set-alarm-state \
  --alarm-name "EC2-HighCPU-i-xxxxx" \
  --state-value OK \
  --state-reason "Test complete"
```

**Expected:** You should receive SNS notification within 1 minute

### Method 2: Trigger Real Metric Breach
```bash
# For EC2 CPU alarm, stress test the instance
ssh ec2-user@<instance-ip>

# Install stress tool
sudo yum install stress -y

# Generate 100% CPU for 15 minutes
stress --cpu 4 --timeout 900s

# Monitor alarm state
watch -n 30 'aws cloudwatch describe-alarms --alarm-names "EC2-HighCPU-i-xxxxx" --query "MetricAlarms[0].StateValue"'
```

---

## 🔧 Common Issues & Fixes

### Issue 1: Alarm Shows "Insufficient Data"

**Causes:**
- Metric not being sent
- Instance stopped
- Recent alarm creation (needs data points)
- `TreatMissingData` set incorrectly

**Fix:**
```bash
# Check if data exists
aws cloudwatch get-metric-statistics \
  --namespace AWS/EC2 \
  --metric-name CPUUtilization \
  --dimensions Name=InstanceId,Value=i-xxxxx \
  --start-time $(date -u -d '30 minutes ago' --iso-8601=seconds) \
  --end-time $(date -u --iso-8601=seconds) \
  --period 300 \
  --statistics Average

# If no data, check instance
aws ec2 describe-instances --instance-ids i-xxxxx
```

---

### Issue 2: Alarm Threshold Never Reached

**Problem:** Threshold set too high

**Check Historical Data:**
```bash
# Get max CPU over last 24 hours
aws cloudwatch get-metric-statistics \
  --namespace AWS/EC2 \
  --metric-name CPUUtilization \
  --dimensions Name=InstanceId,Value=i-xxxxx \
  --start-time $(date -u -d '24 hours ago' --iso-8601=seconds) \
  --end-time $(date -u --iso-8601=seconds) \
  --period 3600 \
  --statistics Maximum \
  --query 'Datapoints[*].Maximum' \
  | jq 'max'
```

**If max was 75% but threshold is 80%, alarm will never fire!**

**Fix:**
```bash
# Lower threshold to 70%
aws cloudwatch put-metric-alarm \
  --alarm-name "EC2-HighCPU-i-xxxxx" \
  --threshold 70 \
  --[other params same]
```

---

### Issue 3: Wrong Statistic Used

**Problem:** Using "Average" when spikes are brief

**Example:**
```
Time:    10:00  10:05  10:10  10:15
CPU:      40%    95%    45%    40%
Average:  55% (below 80% threshold - no alarm!)
Maximum:  95% (above 80% threshold - would alarm!)
```

**Fix:**
```bash
# Use Maximum instead of Average for spike detection
aws cloudwatch put-metric-alarm \
  --alarm-name "EC2-HighCPU-i-xxxxx" \
  --statistic Maximum \  # Changed from Average
  --[other params]
```

---

### Issue 4: Evaluation Period Too Long

**Problem:** Alarm requires sustained breach

**Example:**
```
EvaluationPeriods: 5
Period: 300 (5 minutes)
= Must be breached for 25 minutes!
```

**Fix:**
```bash
# Reduce evaluation periods
aws cloudwatch put-metric-alarm \
  --alarm-name "EC2-HighCPU-i-xxxxx" \
  --evaluation-periods 2 \  # Down from 5
  --period 300 \
  --[other params]
```

---

### Issue 5: Email Goes to Spam

**Problem:** SNS emails flagged as spam

**Check:**
1. Check spam/junk folder
2. Look for subscription confirmation email
3. Add `no-reply@sns.amazonaws.com` to contacts

**Alternative:** Use SMS or integrate with Slack/PagerDuty
```bash
# Add SMS notification
aws sns subscribe \
  --topic-arn arn:aws:sns:us-east-1:123456789012:MyAlertTopic \
  --protocol sms \
  --notification-endpoint +1234567890
```

---

## 📊 Alarm Troubleshooting Flowchart

```
Alarm Not Firing
      ↓
Is alarm enabled? ──NO──→ Enable alarm actions
      ↓ YES
Does metric data exist? ──NO──→ Check instance/metric source
      ↓ YES
Is threshold ever reached? ──NO──→ Adjust threshold
      ↓ YES
Are actions configured? ──NO──→ Add SNS topic
      ↓ YES
Does SNS topic exist? ──NO──→ Create SNS topic
      ↓ YES
Any subscriptions? ──NO──→ Subscribe email/SMS
      ↓ YES
Test with set-alarm-state ──FAIL──→ Check SNS permissions
      ↓ PASS
Test with real metric ──FAIL──→ Review alarm logic
      ↓ PASS
Monitor for 24 hours
```

---

## ✅ Verification Checklist

After fixing alarm:

- [ ] Alarm state shows correctly
```bash
aws cloudwatch describe-alarms --alarm-names "EC2-HighCPU-i-xxxxx"
```

- [ ] Test with `set-alarm-state` succeeds
```bash
aws cloudwatch set-alarm-state --alarm-name "EC2-HighCPU-i-xxxxx" --state-value ALARM --state-reason "Test"
```

- [ ] Notification received (check email/SMS)

- [ ] Test with real metric breach
```bash
# Generate high CPU and verify alarm triggers
```

- [ ] Alarm history shows state changes
```bash
aws cloudwatch describe-alarm-history --alarm-name "EC2-HighCPU-i-xxxxx" --max-records 10
```

---

## 🛡️ Prevention & Best Practices

### 1. Test Alarms When Created
```bash
# Create alarm
aws cloudwatch put-metric-alarm [params]

# Immediately test it
aws cloudwatch set-alarm-state \
  --alarm-name "MyNewAlarm" \
  --state-value ALARM \
  --state-reason "Initial test"

# Verify notification received
```

### 2. Use Alarm Naming Convention
```bash
# Good naming: <Service>-<Metric>-<Resource>
"EC2-HighCPU-i-123abc"
"RDS-LowStorage-mydb"
"Lambda-HighErrors-myfunction"

# Bad naming:
"Alarm1"
"Test"
"MyAlarm"
```

### 3. Document Expected Alarm Behavior
```markdown
## Alarm: EC2-HighCPU-i-xxxxx

**Triggers when:** CPU > 80% for 10 minutes
**Notifies:** ops-team@company.com
**Expected frequency:** Rarely (should investigate if weekly)
**Action:** Check application logs, consider scaling
**Last tested:** 2026-01-03
```

### 4. Create Monitoring Dashboard
```bash
# Create dashboard showing all alarm states
aws cloudwatch put-dashboard --dashboard-name "AlarmStatus" --dashboard-body '{
  "widgets": [
    {
      "type": "metric",
      "properties": {
        "metrics": [
          ["AWS/EC2", "CPUUtilization", {"stat": "Average"}]
        ],
        "period": 300,
        "stat": "Average",
        "region": "us-east-1",
        "title": "EC2 CPU with Alarm Threshold",
        "yAxis": {
          "left": {
            "min": 0,
            "max": 100
          }
        },
        "annotations": {
          "horizontal": [
            {
              "value": 80,
              "label": "Alarm Threshold",
              "fill": "above"
            }
          ]
        }
      }
    }
  ]
}'
```

### 5. Set Up Alarm for Alarms
```bash
# Create composite alarm that triggers if any alarm fails
aws cloudwatch put-composite-alarm \
  --alarm-name "AnyAlarmTriggered" \
  --alarm-rule "ALARM(EC2-HighCPU) OR ALARM(RDS-LowStorage)" \
  --alarm-actions arn:aws:sns:us-east-1:123:critical-alerts
```

---

## 📝 Alarm Testing Script

```bash
#!/bin/bash
# test-alarm.sh - Test CloudWatch alarm configuration

ALARM_NAME="$1"

if [ -z "$ALARM_NAME" ]; then
    echo "Usage: $0 <alarm-name>"
    exit 1
fi

echo "=== Testing Alarm: $ALARM_NAME ==="
echo ""

# 1. Check if alarm exists
echo "1. Checking if alarm exists..."
aws cloudwatch describe-alarms --alarm-names "$ALARM_NAME" > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "   ❌ Alarm not found!"
    exit 1
fi
echo "   ✅ Alarm exists"

# 2. Check if actions enabled
echo "2. Checking if actions are enabled..."
ACTIONS_ENABLED=$(aws cloudwatch describe-alarms \
    --alarm-names "$ALARM_NAME" \
    --query 'MetricAlarms[0].ActionsEnabled' \
    --output text)

if [ "$ACTIONS_ENABLED" == "True" ]; then
    echo "   ✅ Actions enabled"
else
    echo "   ❌ Actions disabled!"
    echo "   Fix: aws cloudwatch enable-alarm-actions --alarm-names $ALARM_NAME"
fi

# 3. Check for SNS actions
echo "3. Checking SNS actions..."
ALARM_ACTIONS=$(aws cloudwatch describe-alarms \
    --alarm-names "$ALARM_NAME" \
    --query 'MetricAlarms[0].AlarmActions' \
    --output text)

if [ -z "$ALARM_ACTIONS" ] || [ "$ALARM_ACTIONS" == "None" ]; then
    echo "   ❌ No alarm actions configured!"
else
    echo "   ✅ Alarm actions: $ALARM_ACTIONS"
    
    # Check SNS subscriptions
    aws sns list-subscriptions-by-topic --topic-arn "$ALARM_ACTIONS" > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        SUBS=$(aws sns list-subscriptions-by-topic \
            --topic-arn "$ALARM_ACTIONS" \
            --query 'Subscriptions[*].Endpoint' \
            --output text)
        echo "   ✅ Subscriptions: $SUBS"
    fi
fi

# 4. Check for metric data
echo "4. Checking for recent metric data..."
NAMESPACE=$(aws cloudwatch describe-alarms --alarm-names "$ALARM_NAME" --query 'MetricAlarms[0].Namespace' --output text)
METRIC=$(aws cloudwatch describe-alarms --alarm-names "$ALARM_NAME" --query 'MetricAlarms[0].MetricName' --output text)
DIMENSIONS=$(aws cloudwatch describe-alarms --alarm-names "$ALARM_NAME" --query 'MetricAlarms[0].Dimensions' --output json)

DATA_POINTS=$(aws cloudwatch get-metric-statistics \
    --namespace "$NAMESPACE" \
    --metric-name "$METRIC" \
    --dimensions "$DIMENSIONS" \
    --start-time $(date -u -d '1 hour ago' --iso-8601=seconds) \
    --end-time $(date -u --iso-8601=seconds) \
    --period 300 \
    --statistics Average \
    --query 'length(Datapoints)')

if [ "$DATA_POINTS" -gt 0 ]; then
    echo "   ✅ Found $DATA_POINTS data points"
else
    echo "   ❌ No metric data found!"
fi

# 5. Test notification
echo "5. Testing notification..."
echo "   Setting alarm to ALARM state..."
aws cloudwatch set-alarm-state \
    --alarm-name "$ALARM_NAME" \
    --state-value ALARM \
    --state-reason "Test notification"

echo "   ⏳ Check your email/SMS for notification (30 seconds)..."
sleep 30

echo "   Resetting alarm to OK..."
aws cloudwatch set-alarm-state \
    --alarm-name "$ALARM_NAME" \
    --state-value OK \
    --state-reason "Test complete"

echo ""
echo "=== Test Complete ==="
echo "Did you receive notification? (yes/no)"
```

**Usage:**
```bash
chmod +x test-alarm.sh
./test-alarm.sh "EC2-HighCPU-i-xxxxx"
```

---

## 📚 Related Resources

### AWS Documentation
- [CloudWatch Alarm States](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AlarmThatSendsEmail.html)
- [Troubleshooting CloudWatch](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cloudwatch_troubleshooting.html)
- [SNS Troubleshooting](https://docs.aws.amazon.com/sns/latest/dg/sns-troubleshooting.html)

### Related Runbooks
- RB-001: EC2 Auto-Recovery
- RB-002: High CPU Response
- RB-005: Lambda Troubleshooting

---

**Document Version:** 1.0  
**Runbook Maintainer:** Charles Bucher  
**Contact:** quietopscb@gmail.com  
**Review Frequency:** Quarterly