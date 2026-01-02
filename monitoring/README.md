# Monitoring Scripts

This folder contains scripts for monitoring AWS resources and detecting issues before they impact production. These tools provide proactive visibility into your cloud infrastructure health.

---

## 🏥 AWS Resource Monitoring

### `health_check.py`
Monitors the health and availability of critical AWS resources.

**Monitors:**
- EC2 instance states and status checks
- RDS database availability and connections
- S3 bucket accessibility
- Resource health metrics and logging

**Purpose:** Real-time health visibility across your AWS infrastructure  
**Use Case:** Detect failing resources before they cause service disruptions

**How to Run:**
```bash
python health_check.py
```

**Output:** Logs health status and alerts on detected issues

---

## 🚨 Alert & Notification System

### `alerts.py`
Sends notifications when critical events or threshold breaches occur.

**Features:**
- Configurable alert thresholds
- Multiple notification channels (email, SNS, etc.)
- Event tracking and logging
- Customizable alert rules

**Purpose:** Stay informed about infrastructure changes without constant manual monitoring  
**Use Case:** Get notified immediately when resources fail or performance degrades

**How to Run:**
```bash
python alerts.py
```

**Configuration:** Edit alert thresholds and notification settings in the script

---

## 📋 Prerequisites

- Python 3.8+
- AWS CLI configured (`aws configure`)
- boto3: `pip install boto3 --break-system-packages`
- IAM permissions for CloudWatch, EC2, RDS, S3 (read access)

---

## 🔧 Setup Instructions

1. **Configure AWS Credentials:**
   ```bash
   aws configure
   ```
   Enter your AWS Access Key ID, Secret Access Key, and default region

2. **Install Dependencies:**
   ```bash
   pip install boto3 --break-system-packages
   ```

3. **Test Your Setup:**
   ```bash
   python health_check.py
   ```

4. **Set Up Alerts:**
   Edit `alerts.py` to configure your notification preferences, then run:
   ```bash
   python alerts.py
   ```

---

## ⚠️ Important Notes

- **IAM Permissions:** Ensure AWS credentials have read access to monitored resources
- **CloudWatch Costs:** Monitor CloudWatch usage to avoid unexpected charges
- **Alert Fatigue:** Configure thresholds carefully to avoid excessive notifications
- **Backup Files:** `.bak` files are development backups—use the main `.py` files

---

## 🎯 Coming Soon

- **CloudWatch Log Analyzer:** Parse and analyze logs for errors and patterns
- **Compliance Checker:** Audit resources against AWS best practices
- **Resource Utilization Dashboard:** Visualize resource usage trends
- **Custom Metric Tracking:** Monitor application-specific metrics

---

## 💡 Usage Tips

1. **Run health checks regularly:** Set up a cron job or scheduled task
2. **Review alert configurations:** Test notifications before relying on them
3. **Monitor CloudWatch metrics:** Use these scripts alongside AWS Console for full visibility
4. **Log analysis:** Review script output regularly for trends and patterns
5. **Start simple:** Begin with basic health checks, then add complexity as needed

## TL;DR

_TODO_

## Overview

_TODO_

## Usage Examples

_TODO_

## Incident Scenarios

_TODO_

## Screenshots

_TODO_

## Contact

_TODO_

## Skills Demonstrated
Automation, monitoring, incident response, troubleshooting, and Infrastructure as Code using Terraform/CloudFormation.

## What I Learned
Hands-on experience troubleshooting AWS incidents, applying automation, monitoring with CloudWatch, and ensuring cloud reliability.
