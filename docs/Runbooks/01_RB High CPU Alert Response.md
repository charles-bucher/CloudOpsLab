# Runbook: High CPU Alert Response

**Document ID:** RB-002  
**Last Updated:** January 2026  
**Owner:** Charles Bucher  
**Severity:** P2 (High)  

---

## 📋 Overview

### Purpose
Respond to high CPU utilization alerts on EC2 instances, identify root cause, and implement remediation.

### When to Use
- CloudWatch alarm triggers for high CPU (>80%)
- Instance performance degradation reported
- Application slowness or timeouts
- Cost optimization review identifies high CPU instances

### Expected Resolution Time
- **Investigation:** 5-10 minutes
- **Resolution:** 10-30 minutes (depending on cause)

---

## 🚨 Detection & Alerting

### Alert Trigger
```
ALARM: "EC2-HighCPU-i-xxxxx"
Status: ALARM
Metric: CPUUtilization
Threshold: >= 80% for 2 consecutive periods (10 minutes)
Current Value: 92%
```

### Alert Channels
- SNS →Email notification
- CloudWatch Dashboard (RED)
- Optional: PagerDuty, Slack

---

## 🔍 Initial Assessment (2-5 minutes)

### Step 1: Verify Alert Accuracy
```bash
# Check current CPU utilization
aws cloudwatch get-metric-statistics \
  --namespace AWS/EC2 \
  --metric-name CPUUtilization \
  --dimensions Name=InstanceId,Value=i-xxxxx \
  --start-time $(date -u -d '30 minutes ago' --iso-8601=seconds) \
  --end-time $(date -u --iso-8601=seconds) \
  --period 300 \
  --statistics Average,Maximum \
  --query 'Datapoints[*].[Timestamp,Average,Maximum]' \
  --output table
```

### Step 2: Check Instance Details
```bash
# Get instance type and current state
aws ec2 describe-instances \
  --instance-ids i-xxxxx \
  --query 'Reservations[0].Instances[0].[InstanceType,State.Name,LaunchTime]' \
  --output text
```

### Step 3: Review Recent Changes
```bash
# Check CloudTrail for recent changes
aws cloudtrail lookup-events \
  --lookup-attributes AttributeKey=ResourceName,AttributeValue=i-xxxxx \
  --max-results 20 \
  --query 'Events[*].[EventTime,EventName,Username]' \
  --output table
```

---

## 🔍 Investigation Steps

### Step 1: SSH into Instance
```bash
# Connect to instance
ssh -i ~/.ssh/key.pem ec2-user@<instance-ip>
```

### Step 2: Check Real-Time CPU Usage
```bash
# Top processes by CPU
top -b -n 1 | head -20

# Specific CPU-intensive processes
ps aux --sort=-%cpu | head -10

# CPU usage breakdown
mpstat 1 5
```

**Look for:**
- Unexpected processes
- Runaway scripts
- Memory swap activity (high wa%)
- Multiple processes consuming CPU

### Step 3: Check System Load
```bash
# Load average (should be < number of CPUs)
uptime

# Number of CPUs
nproc

# Detailed load info
cat /proc/loadavg
```

**Rule of Thumb:**
- Load < CPUs = OK
- Load = CPUs = Saturated
- Load > CPUs = Overloaded

### Step 4: Check for Specific Issues

#### A) Memory Issues Causing CPU Spike
```bash
# Check memory usage
free -h

# Check swap usage (high swap = problem)
swapon --show

# Memory-hungry processes
ps aux --sort=-%mem | head -10
```

#### B) Disk I/O Causing Wait
```bash
# Check disk I/O wait
iostat -x 1 5

# Disk usage
df -h

# I/O intensive processes
iotop -o -n 3
```

#### C) Network Activity
```bash
# Network connections
netstat -tunap | wc -l

# Active connections by state
netstat -ant | awk '{print $6}' | sort | uniq -c | sort -rn
```

### Step 5: Check Application Logs
```bash
# Recent application errors
sudo tail -100 /var/log/application.log | grep -i error

# Web server logs (if applicable)
sudo tail -100 /var/log/nginx/error.log
sudo tail -100 /var/log/apache2/error.log

# System logs
sudo journalctl -u <service-name> --since "30 minutes ago"
```

---

## 🔧 Resolution Steps

### Scenario A: Runaway Process

#### Step 1: Identify the Process
```bash
# Get PID and details of CPU hog
ps aux --sort=-%cpu | head -5
```

#### Step 2: Check Process Details
```bash
# What is this process doing?
ps -p <PID> -o pid,ppid,cmd,%cpu,%mem,etime

# Process open files
lsof -p <PID>

# Process threads
ps -T -p <PID>
```

#### Step 3: Decide Action

**If legitimate process:**
```bash
# Nice down (lower priority)
sudo renice +10 -p <PID>
```

**If stuck/zombie process:**
```bash
# Try graceful stop
sudo kill -15 <PID>

# Wait 30 seconds, then force if needed
sudo kill -9 <PID>
```

**If scheduled job:**
```bash
# Check cron jobs
crontab -l
sudo crontab -l

# Disable problematic job temporarily
crontab -e  # Comment out the line
```

---

### Scenario B: Insufficient Resources

#### Step 1: Check Instance Size
```bash
# Current instance type
aws ec2 describe-instances \
  --instance-ids i-xxxxx \
  --query 'Reservations[0].Instances[0].InstanceType'
```

#### Step 2: Review CPU History
```bash
# Check if this is a pattern
aws cloudwatch get-metric-statistics \
  --namespace AWS/EC2 \
  --metric-name CPUUtilization \
  --dimensions Name=InstanceId,Value=i-xxxxx \
  --start-time $(date -u -d '7 days ago' --iso-8601=seconds) \
  --end-time $(date -u --iso-8601=seconds) \
  --period 3600 \
  --statistics Average,Maximum \
  --query 'Datapoints[*].[Timestamp,Average,Maximum]' \
  --output table
```

#### Step 3: Resize Instance (If Needed)

**Option A: Vertical Scaling (More CPU)**
```bash
# Stop instance
aws ec2 stop-instances --instance-ids i-xxxxx
aws ec2 wait instance-stopped --instance-ids i-xxxxx

# Change instance type
aws ec2 modify-instance-attribute \
  --instance-id i-xxxxx \
  --instance-type t3.large

# Start instance
aws ec2 start-instances --instance-ids i-xxxxx
```

**Option B: Horizontal Scaling (Add Instances)**
- Use Auto Scaling Group
- Deploy load balancer
- Distribute traffic

---

### Scenario C: Application Issue

#### Step 1: Restart Application Service
```bash
# Check service status
sudo systemctl status <service-name>

# Restart service
sudo systemctl restart <service-name>

# Verify restart
sudo systemctl status <service-name>
```

#### Step 2: Check Application Configuration
```bash
# Review config for issues
sudo cat /etc/<app>/config.conf

# Check for misconfiguration
# - Connection pool sizes
# - Thread limits
# - Cache settings
```

#### Step 3: Monitor After Restart
```bash
# Watch CPU in real-time
watch -n 5 'ps aux --sort=-%cpu | head -10'

# Monitor service logs
sudo journalctl -u <service-name> -f
```

---

### Scenario D: External Attack (DDoS, Brute Force)

#### Step 1: Check Connection Count
```bash
# Total connections
netstat -an | wc -l

# Connections by IP
netstat -ntu | awk '{print $5}' | cut -d: -f1 | sort | uniq -c | sort -rn | head -20
```

#### Step 2: Block Malicious IPs
```bash
# Block IP with iptables
sudo iptables -A INPUT -s <bad-ip> -j DROP

# Or update Security Group
aws ec2 revoke-security-group-ingress \
  --group-id sg-xxxxx \
  --cidr <bad-ip>/32 \
  --protocol tcp \
  --port 80
```

#### Step 3: Enable AWS Shield/WAF
```bash
# Contact AWS Support for Shield
# Or configure WAF rules
```

---

## ✅ Verification Steps

### 1. Check CPU Has Normalized
```bash
# Real-time check
ssh ec2-user@<instance-ip> 'uptime && top -b -n 1 | head -5'

# CloudWatch check
aws cloudwatch get-metric-statistics \
  --namespace AWS/EC2 \
  --metric-name CPUUtilization \
  --dimensions Name=InstanceId,Value=i-xxxxx \
  --start-time $(date -u -d '10 minutes ago' --iso-8601=seconds) \
  --end-time $(date -u --iso-8601=seconds) \
  --period 300 \
  --statistics Average
```

**Expected:** CPU < 60% for normal operations

### 2. Verify Application Health
```bash
# HTTP health check
curl -f http://<instance-ip>/health

# Application-specific checks
# Database queries working?
# API endpoints responding?
```

### 3. Check CloudWatch Alarm
```bash
# Alarm should return to OK
aws cloudwatch describe-alarms \
  --alarm-names "EC2-HighCPU-i-xxxxx" \
  --query 'MetricAlarms[0].StateValue'
```

**Expected:** `"OK"`

### 4. Monitor for 30 Minutes
```bash
# Set up continuous monitoring
watch -n 60 'aws cloudwatch get-metric-statistics \
  --namespace AWS/EC2 \
  --metric-name CPUUtilization \
  --dimensions Name=InstanceId,Value=i-xxxxx \
  --start-time $(date -u -d "5 minutes ago" --iso-8601=seconds) \
  --end-time $(date -u --iso-8601=seconds) \
  --period 300 \
  --statistics Average'
```

---

## 📊 Post-Incident Actions

### 1. Document Findings
```markdown
**Root Cause:** [Process name / Resource limitation / Application bug]
**Duration:** [X] minutes
**Peak CPU:** [X]%
**Resolution:** [Process killed / Instance resized / Application restarted]
```

### 2. Implement Permanent Fix

| Cause | Permanent Fix |
|-------|---------------|
| Runaway cron job | Fix script logic, add timeouts |
| Memory leak | Update application code |
| Too small instance | Resize or use Auto Scaling |
| Inefficient query | Optimize database queries |
| No caching | Implement Redis/Memcached |

### 3. Update Monitoring
```bash
# Add more granular CPU alarms if needed
aws cloudwatch put-metric-alarm \
  --alarm-name EC2-MediumCPU-i-xxxxx \
  --metric-name CPUUtilization \
  --namespace AWS/EC2 \
  --statistic Average \
  --period 300 \
  --threshold 60 \
  --comparison-operator GreaterThanThreshold \
  --evaluation-periods 2 \
  --dimensions Name=InstanceId,Value=i-xxxxx \
  --alarm-actions <sns-topic-arn>
```

---

## 🛡️ Prevention Strategies

### 1. Right-Size Instances
```bash
# Use AWS Compute Optimizer
aws compute-optimizer get-ec2-instance-recommendations \
  --instance-arns arn:aws:ec2:<region>:<account-id>:instance/i-xxxxx
```

### 2. Implement Auto Scaling
```hcl
# Terraform example
resource "aws_autoscaling_policy" "cpu_scaling" {
  name                   = "cpu-scaling-policy"
  scaling_adjustment     = 1
  adjustment_type        = "ChangeInCapacity"
  cooldown              = 300
  autoscaling_group_name = aws_autoscaling_group.main.name
}

resource "aws_cloudwatch_metric_alarm" "cpu_high" {
  alarm_name          = "cpu-utilization-high"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = 300
  statistic           = "Average"
  threshold           = 70
  alarm_actions       = [aws_autoscaling_policy.cpu_scaling.arn]
}
```

### 3. Application Optimization
- Add caching layer (Redis, Memcached)
- Optimize database queries
- Implement rate limiting
- Use CDN for static content
- Enable connection pooling

### 4. Regular Performance Reviews
```bash
# Weekly CPU analysis script
#!/bin/bash
INSTANCE_ID="i-xxxxx"
aws cloudwatch get-metric-statistics \
  --namespace AWS/EC2 \
  --metric-name CPUUtilization \
  --dimensions Name=InstanceId,Value=$INSTANCE_ID \
  --start-time $(date -u -d '7 days ago' --iso-8601=seconds) \
  --end-time $(date -u --iso-8601=seconds) \
  --period 3600 \
  --statistics Average,Maximum \
  | jq -r '.Datapoints | sort_by(.Timestamp) | .[] | "\(.Timestamp) Avg:\(.Average) Max:\(.Maximum)"'
```

---

## 📞 Escalation Path

### Level 1: Initial Response (0-10 minutes)
- Acknowledge alert
- Run initial assessment
- Identify obvious issues (runaway process)

### Level 2: Investigation (10-30 minutes)
- Deep dive into logs
- Check for application bugs
- Consider resource constraints

### Level 3: Senior DevOps (30+ minutes)
- Complex performance issues
- Architectural decisions needed
- Scaling strategy review

### Level 4: Development Team (1+ hour)
- Application code changes needed
- Performance optimization required
- New features causing issues

---

## 🔍 Troubleshooting

### Issue: CPU Drops When SSH'ing In

**Cause:** Process is CPU-bound only when system is idle (nice jobs, background tasks)

**Action:**
- Check cron jobs: `crontab -l`
- Check systemd timers: `systemctl list-timers`
- Review `nice` processes: `ps aux | grep "  N  "`

---

### Issue: CPU High But Top Shows Nothing

**Cause:** I/O wait is counted as CPU in some metrics

**Check:**
```bash
# Check I/O wait specifically
iostat -x 1 5 | grep "avg-cpu"

# Look for "wa%" column
```

**Action:**
- If `wa%` is high, it's a disk I/O problem, not CPU
- Use `iotop` to find I/O intensive process
- Consider faster EBS volume type (gp3, io2)

---

### Issue: CPU Spikes Periodically

**Cause:** Scheduled jobs (cron, systemd timers)

**Investigate:**
```bash
# Check all cron jobs
sudo grep -r "." /etc/cron.* /var/spool/cron/

# Check systemd timers
systemctl list-timers --all

# Match spike time with job schedule
```

**Action:**
- Optimize job (add LIMIT to queries, etc.)
- Split job into smaller chunks
- Run during off-peak hours
- Add proper logging

---

## 📝 Incident Report Template

```markdown
### High CPU Incident Report

**Date:** [YYYY-MM-DD HH:MM]
**Instance ID:** i-xxxxx
**Duration:** [X] minutes
**Peak CPU:** [X]%

**Detection:**
- CloudWatch alarm triggered at [HH:MM]
- Alert received via [SNS/Email/Slack]

**Investigation:**
- Process identified: [process name/PID]
- Root cause: [runaway script / insufficient resources / application bug]
- Contributing factors: [recent deployment / traffic spike / cron job]

**Resolution:**
- Action taken: [killed process / restarted service / resized instance]
- CPU normalized at [HH:MM]
- Total resolution time: [X] minutes

**Impact:**
- User-facing impact: [None / Slow response times / Partial outage]
- Estimated users affected: [number]
- Data loss: [None / Description]

**Prevention:**
1. [Specific action taken]
2. [Monitoring added]
3. [Code fix deployed]

**Follow-up:**
- [ ] Update application monitoring
- [ ] Review instance sizing
- [ ] Optimize code/queries
- [ ] Update runbook
```

---

## 📚 Related Resources

### AWS Documentation
- [EC2 CloudWatch Metrics](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/viewing_metrics_with_cloudwatch.html)
- [Auto Scaling](https://docs.aws.amazon.com/autoscaling/ec2/userguide/what-is-amazon-ec2-auto-scaling.html)
- [Compute Optimizer](https://aws.amazon.com/compute-optimizer/)

### Related Runbooks
- RB-001: EC2 Instance Failure Auto-Recovery
- RB-003: S3 Public Bucket Remediation
- RB-005: Lambda Function Troubleshooting

### Scripts Used
- `automation/ec2_manager.py`
- `monitoring/health_check.py`

---

## ✅ Checklist

### During Incident:
- [ ] Alert acknowledged
- [ ] CPU level verified via CloudWatch
- [ ] SSH'd into instance
- [ ] Top processes identified
- [ ] Root cause determined
- [ ] Resolution action taken
- [ ] CPU normalized and verified
- [ ] Application health confirmed
- [ ] Alarm returned to OK state

### Post-Incident:
- [ ] Incident documented
- [ ] Root cause analysis completed
- [ ] Prevention measures implemented
- [ ] Monitoring enhanced
- [ ] Team notified
- [ ] Runbook updated if needed

---

**Document Version:** 1.0  
**Change Log:**
- 2026-01-03: Initial runbook created

**Runbook Maintainer:** Charles Bucher  
**Contact:** quietopscb@gmail.com  
**Review Frequency:** Quarterly