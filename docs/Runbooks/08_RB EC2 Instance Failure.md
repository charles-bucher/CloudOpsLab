# Runbook: EC2 Instance Failure Auto-Recovery

**Document ID:** RB-001  
**Last Updated:** January 2026  
**Owner:** Charles Bucher  
**Severity:** P1 (Critical)  

---

## 📋 Overview

### Purpose
This runbook provides step-by-step procedures for responding to EC2 instance status check failures and triggering automated recovery.

### When to Use
- CloudWatch alarm triggers for StatusCheckFailed
- EC2 instance becomes unresponsive
- System or instance status checks fail
- Automated recovery needs verification

### Expected Resolution Time
- **Automated Recovery:** 3-5 minutes
- **Manual Intervention:** 10-15 minutes

---

## 🚨 Detection & Alerting

### Alert Trigger
```
ALARM: "EC2-StatusCheckFailed-i-xxxxx"
Status: ALARM
Metric: StatusCheckFailed (System or Instance)
Threshold: >= 1 for 2 consecutive periods (2 minutes)
```

### Alert Channels
- SNS → Email notification
- SNS → SMS (if configured)
- CloudWatch Dashboard shows alarm state

---

## 🔍 Initial Assessment (1-2 minutes)

### Step 1: Verify Alert
```bash
# Check current instance status
aws ec2 describe-instance-status \
  --instance-ids i-xxxxx \
  --query 'InstanceStatuses[0].[InstanceStatus.Status,SystemStatus.Status]'
```

**Expected Output:**
```
[
    "impaired",  # or "ok"
    "impaired"   # or "ok"
]
```

### Step 2: Identify Failure Type

| Status Check | Meaning | Auto-Recovery |
|--------------|---------|---------------|
| System Status Failed | AWS infrastructure issue | ✅ Yes |
| Instance Status Failed | Instance OS/software issue | ⚠️ Maybe |
| Both Failed | Multiple issues | ✅ Yes |

---

## 🔧 Resolution Steps

### Scenario A: Auto-Recovery Configured (Recommended)

#### Step 1: Verify Auto-Recovery Is Running
```bash
# Check if recovery action is configured
aws ec2 describe-instance-attribute \
  --instance-id i-xxxxx \
  --attribute disableApiTermination
```

#### Step 2: Monitor Recovery Progress
```bash
# Watch instance state transitions
aws ec2 describe-instances \
  --instance-ids i-xxxxx \
  --query 'Reservations[0].Instances[0].State.Name'

# Check every 30 seconds
watch -n 30 'aws ec2 describe-instance-status --instance-ids i-xxxxx'
```

**Expected Recovery Flow:**
```
impaired → stopping → stopped → pending → running → ok
```

#### Step 3: Wait for Auto-Recovery
- **Time:** Usually 3-5 minutes
- **Action:** Monitor CloudWatch for status change
- **Outcome:** Instance recovers automatically

---

### Scenario B: Manual Recovery Required

#### When Manual Intervention Needed:
- Auto-recovery not configured
- Recovery stuck for >10 minutes
- Instance still impaired after recovery

#### Step 1: Stop and Start Instance
```bash
# Stop the instance (NOT terminate!)
aws ec2 stop-instances --instance-ids i-xxxxx

# Wait for stopped state
aws ec2 wait instance-stopped --instance-ids i-xxxxx

# Start the instance
aws ec2 start-instances --instance-ids i-xxxxx

# Wait for running state
aws ec2 wait instance-running --instance-ids i-xxxxx
```

#### Step 2: Verify Instance Health
```bash
# Check status checks
aws ec2 describe-instance-status --instance-ids i-xxxxx

# Test connectivity (if web server)
curl -I http://$(aws ec2 describe-instances \
  --instance-ids i-xxxxx \
  --query 'Reservations[0].Instances[0].PublicIpAddress' \
  --output text)
```

---

## ✅ Verification Steps

### 1. Check Instance Status
```bash
# Both checks should show "ok"
aws ec2 describe-instance-status --instance-ids i-xxxxx \
  --query 'InstanceStatuses[0].[InstanceStatus.Status,SystemStatus.Status]'
```

**Expected Output:**
```
[
    "ok",
    "ok"
]
```

### 2. Verify Application Availability
```bash
# SSH test (if applicable)
ssh -i ~/.ssh/key.pem ec2-user@<instance-ip> 'uptime'

# HTTP test (if web server)
curl -f http://<instance-ip>

# Check logs
aws logs tail /aws/ec2/<instance-id> --follow
```

### 3. Check CloudWatch Alarm
```bash
# Alarm should return to OK state
aws cloudwatch describe-alarms \
  --alarm-names "EC2-StatusCheckFailed-i-xxxxx" \
  --query 'MetricAlarms[0].StateValue'
```

**Expected:** `"OK"`

### 4. Verify Uptime
```bash
# Check how long instance has been running since recovery
ssh ec2-user@<instance-ip> 'uptime'
```

---

## 📊 Post-Recovery Actions

### 1. Document the Incident
```bash
# Get CloudTrail logs of the failure
aws cloudtrail lookup-events \
  --lookup-attributes AttributeKey=ResourceName,AttributeValue=i-xxxxx \
  --max-results 10 \
  --query 'Events[*].[EventTime,EventName,Username]'
```

**Record:**
- Failure time
- Recovery time
- Total downtime
- Root cause (if determined)

### 2. Check for Data Loss
```bash
# Verify EBS volumes
aws ec2 describe-volumes \
  --filters "Name=attachment.instance-id,Values=i-xxxxx" \
  --query 'Volumes[*].[VolumeId,State,Attachments[0].State]'

# Check application logs for errors
aws logs filter-log-events \
  --log-group-name /aws/ec2/<instance-id> \
  --start-time $(date -u -d '1 hour ago' +%s)000 \
  --filter-pattern "ERROR"
```

### 3. Update Monitoring
```bash
# Ensure alarm is still active
aws cloudwatch describe-alarms \
  --alarm-names "EC2-StatusCheckFailed-i-xxxxx"

# Verify SNS subscriptions
aws sns list-subscriptions-by-topic \
  --topic-arn <sns-topic-arn>
```

---

## 🛡️ Prevention Strategies

### 1. Enable Auto-Recovery
```bash
# Configure auto-recovery alarm
aws cloudwatch put-metric-alarm \
  --alarm-name EC2-AutoRecover-i-xxxxx \
  --alarm-description "Auto-recover EC2 on status check failure" \
  --metric-name StatusCheckFailed \
  --namespace AWS/EC2 \
  --statistic Maximum \
  --period 60 \
  --threshold 1 \
  --comparison-operator GreaterThanOrEqualToThreshold \
  --evaluation-periods 2 \
  --alarm-actions arn:aws:automate:<region>:ec2:recover \
  --dimensions Name=InstanceId,Value=i-xxxxx
```

### 2. Implement High Availability
- Use Auto Scaling Groups (ASG)
- Deploy across multiple Availability Zones
- Use Elastic Load Balancer (ELB)
- Implement health checks

### 3. Regular Health Checks
```bash
# Create health check script
#!/bin/bash
aws ec2 describe-instance-status \
  --instance-ids i-xxxxx \
  --query 'InstanceStatuses[0].InstanceStatus.Status' \
  --output text
```

### 4. Monitoring Best Practices
- Set up SNS notifications
- Create CloudWatch dashboards
- Enable detailed monitoring
- Review status check history monthly

---

## 📞 Escalation Path

### Level 1: Automated Recovery (0-5 minutes)
- Auto-recovery attempts restart
- Monitor via CloudWatch

### Level 2: On-Call Engineer (5-15 minutes)
- Manual stop/start if auto-recovery fails
- Check application logs
- Verify data integrity

### Level 3: Senior DevOps (15+ minutes)
- If recovery still fails
- Potential hardware issue
- May need instance replacement

### Level 4: AWS Support (30+ minutes)
- If underlying AWS issue suspected
- Open support ticket
- Request instance migration

---

## 🔍 Troubleshooting

### Issue: Auto-Recovery Not Triggering

**Check:**
```bash
# Verify alarm exists
aws cloudwatch describe-alarms \
  --alarm-names "EC2-AutoRecover-i-xxxxx"

# Check alarm actions
aws cloudwatch describe-alarms \
  --alarm-names "EC2-AutoRecover-i-xxxxx" \
  --query 'MetricAlarms[0].AlarmActions'
```

**Fix:**
- Ensure alarm action is `arn:aws:automate:<region>:ec2:recover`
- Check instance type supports recovery (most do)
- Verify IAM permissions

---

### Issue: Instance Stuck in "Stopping" State

**Check:**
```bash
# Get instance state reason
aws ec2 describe-instances \
  --instance-ids i-xxxxx \
  --query 'Reservations[0].Instances[0].StateTransitionReason'
```

**Actions:**
1. Wait 10 minutes (force stop takes time)
2. Try force stop:
```bash
aws ec2 stop-instances --instance-ids i-xxxxx --force
```
3. If still stuck after 15 minutes, contact AWS Support

---

### Issue: Instance Recovered But Application Down

**Check:**
1. SSH into instance
2. Check application status:
```bash
sudo systemctl status <service-name>
```
3. Check application logs:
```bash
sudo tail -f /var/log/<app>/*.log
```

**Fix:**
- Restart application service
- Check for configuration issues
- Verify database connectivity

---

## 📝 Incident Report Template

```markdown
### EC2 Instance Recovery Incident Report

**Date:** [YYYY-MM-DD]
**Instance ID:** i-xxxxx
**Duration:** [X] minutes

**Timeline:**
- [HH:MM] - Status check failure detected
- [HH:MM] - Auto-recovery initiated
- [HH:MM] - Instance stopped
- [HH:MM] - Instance restarted
- [HH:MM] - Status checks passed
- [HH:MM] - Application verified healthy

**Root Cause:**
[System status failure / Instance status failure / Unknown]

**Impact:**
- Downtime: [X] minutes
- Users affected: [None / Estimated number]
- Data loss: [None / Description]

**Resolution:**
[Automated recovery / Manual restart / Other]

**Prevention:**
- [ ] Auto-recovery verified working
- [ ] Monitoring enhanced
- [ ] Documentation updated
- [ ] Team notified

**Follow-up Actions:**
1. Review instance metrics for patterns
2. Consider moving to ASG if frequent failures
3. Update runbook based on learnings
```

---

## 📚 Related Resources

### AWS Documentation
- [EC2 Status Checks](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/monitoring-system-instance-status-check.html)
- [Auto-Recovery](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-recover.html)
- [CloudWatch Alarms](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AlarmThatSendsEmail.html)

### Related Runbooks
- RB-002: High CPU Alert Response
- RB-005: Lambda Function Troubleshooting
- RB-007: Security Audit Procedures

### Scripts Used
- `automation/ec2_auto_recovery.py`
- `monitoring/health_check.py`

---

## ✅ Runbook Validation

### Test Schedule
- Monthly test of auto-recovery
- Quarterly runbook review
- Update after each incident

### Last Tested
**Date:** [YYYY-MM-DD]  
**Result:** [Pass/Fail]  
**Notes:** [Any observations]

---

## 📋 Checklist

### During Incident:
- [ ] Alert received and acknowledged
- [ ] Instance status verified
- [ ] Auto-recovery monitored (or manual recovery initiated)
- [ ] Application health verified
- [ ] CloudWatch alarm returned to OK
- [ ] Incident documented

### Post-Incident:
- [ ] Root cause identified (if possible)
- [ ] CloudTrail logs reviewed
- [ ] Monitoring confirmed working
- [ ] Prevention measures implemented
- [ ] Incident report completed
- [ ] Team debriefing held

---

**Document Version:** 1.0  
**Change Log:**
- 2026-01-03: Initial runbook created
- [Future updates here]

---

**Runbook Maintainer:** Charles Bucher  
**Contact:** quietopscb@gmail.com  
**Review Frequency:** Quarterly or after significant incidents