# EC2 High CPU Utilization Runbook

## Purpose
Provide a repeatable process to detect, investigate, remediate, and prevent high CPU utilization on EC2 instances.

---

## Symptoms
- CloudWatch alarm triggers for CPUUtilization > 80%
- Increased application latency
- SSH sessions slow or unresponsive
- Load balancer health checks failing

---

## Impact
- Degraded application performance
- Potential outage if sustained
- Increased AWS costs due to inefficient resource usage

---

## Detection
- CloudWatch Metric: `CPUUtilization`
- Alarm Threshold: >= 80% for 5 minutes
- SNS notification sent to on-call

---

## Investigation Steps
1. Identify affected instance:
   ```bash
   aws ec2 describe-instances --instance-ids <instance-id>
