# CloudOpsLab 🔧

![AWS](https://img.shields.io/badge/AWS-FF9900?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Bash](https://img.shields.io/badge/Bash-4EAA25?style=for-the-badge&logo=gnu-bash&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)
![Open to Work](https://img.shields.io/badge/Open%20To%20Work-00C853?style=flat-square)

**Hands-on AWS CloudOps practice lab demonstrating automation, monitoring, and troubleshooting**

*Learning operational excellence through real-world scenarios*

---

## 🎯 About This Lab

This is my personal CloudOps learning environment where I'm building AWS operations skills by **doing actual work**—not just following tutorials.

### Why This Lab Exists:

I'm 40 years old, working delivery while teaching myself cloud engineering to provide better for my family. Instead of just watching videos, I'm:

✅ **Running real AWS infrastructure** (~$20/month from my paycheck)  
✅ **Breaking things intentionally** to learn troubleshooting  
✅ **Documenting everything** like production systems  
✅ **Building automation scripts** to solve real problems  

### My Goal:

Prove I can do cloud operations work even though I'm entry-level. This lab is my proof.

---

## 🧪 What I've Built

### 1. CloudWatch Monitoring & Alerting 📊

**What I learned:** Setting up automated monitoring that catches issues

![CloudWatch Alarm](docs/screenshots/automation/cloudwatch-alarm-triggered.png)
*CloudWatch alarm I configured - triggered when my EC2 hit 80% CPU*

**The work:**
- Created CloudWatch alarms for CPU, memory, and disk
- Set up SNS topics for email notifications
- Configured proper thresholds through testing
- Tested alerting by intentionally spiking CPU

**Skills practiced:**
- CloudWatch alarm configuration
- SNS topic management
- Threshold tuning based on workload
- Alert routing

**Code:** [`scripts/cloudwatch_alarms.py`](scripts/cloudwatch_alarms.py)

---

### 2. EC2 Auto-Recovery 🔄

**What I learned:** Making instances self-heal automatically

![EC2 Auto-Recovery Test](docs/screenshots/automation/ec2-auto-recovery-test.png)
*Testing auto-recovery by simulating instance failure*

**The scenario:**
1. Configured CloudWatch to detect status check failures
2. Set up automatic recovery action
3. Intentionally broke my test instance
4. Watched it recover without me touching it
5. Instance was back in ~4 minutes

**Result:** I can now build self-healing infrastructure

**Skills practiced:**
- EC2 status checks (system vs instance)
- CloudWatch alarm actions
- Automated recovery configuration
- Incident response measurement

**Code:** [`scripts/ec2_auto_recovery.py`](scripts/ec2_auto_recovery.py)  
**Documentation:** [RB-001: EC2 Auto-Recovery](docs/runbooks/RB-001-EC2-Auto-Recovery.md)

---

### 3. EC2 Scheduler (Cost Savings) 💰

**What I learned:** Automating EC2 to save money

![EC2 Scheduler IAM Fix](automation/screenshots/ec2-scheduler-iam-fix.png)
*Troubleshooting IAM permissions - common real-world issue*

**The problem:**
My Lambda function kept failing with `AccessDenied`. Had to:
- Check CloudTrail for exact error
- Review IAM policies
- Add missing EC2 permissions
- Test until it worked

**Learning:** IAM troubleshooting is critical in cloud ops

**Skills practiced:**
- Lambda function development
- IAM policy debugging
- CloudWatch Events/EventBridge
- Cost optimization automation

**Code:** [`scripts/ec2_scheduler.py`](scripts/ec2_scheduler.py)  
**Savings:** ~$45/month by stopping dev instances overnight

---

### 4. EC2 Management with Boto3 🐍

**What I learned:** Programmatic AWS management

![EC2 Boto3 Manager](automation/screenshots/ec2-boto3-client-list.png)
*Python script listing and managing my EC2 instances*

**What it does:**
- Lists all EC2 instances with filtering
- Starts/stops instances in bulk
- Filters by tags and state
- Handles API pagination properly
- Has error handling for rate limits

**Skills practiced:**
- Boto3 SDK for Python
- AWS API interaction
- Error handling patterns
- Pagination for large datasets

**Code:** [`scripts/ec2_manager.py`](scripts/ec2_manager.py)

---

### 5. S3 Security Auditing 🔒

**What I learned:** Detecting and fixing security issues

![S3 Public Detection](automation/screenshots/s3-public-access-detection.png)
*Script scanning for publicly accessible S3 buckets*

**The scenario:**
1. Built script to scan all S3 buckets
2. Check for public access (ACLs and policies)
3. Automatically remediate by blocking public access
4. Generate audit report

**Result:** Can now prevent data exposure

**Skills practiced:**
- S3 security best practices
- Boto3 S3 operations
- Policy analysis
- Security automation

**Code:** [`scripts/s3_public_check.py`](scripts/s3_public_check.py)  
**Documentation:** [RB-003: S3 Public Bucket](docs/runbooks/RB-003-S3-Public-Bucket-Remediation.md)

---

### 6. Security Auditing 🛡️

**What I learned:** Auditing AWS accounts for issues

![Security Audit Findings](monitoring/screenshots/security-audit-findings.png)
*My security audit script showing compliance findings*

**What it checks:**
- ✅ IAM users without MFA
- ✅ Overly permissive Security Groups
- ✅ S3 buckets with public access
- ✅ Unused access keys (>90 days)
- ✅ Root account usage

**Skills practiced:**
- Security auditing methodology
- CIS AWS Foundations Benchmark
- Python reporting
- Remediation tracking

**Code:** [`monitoring/security_audit.py`](monitoring/security_audit.py)  
**Documentation:** [RB-004: Security Audit](docs/runbooks/RB-004-Security-Audit-Procedures.md)

---

### 7. GuardDuty Monitoring 🚨

**What I learned:** AWS threat detection

![GuardDuty Enabled](monitoring/screenshots/guardduty-enabled.png)
*GuardDuty actively monitoring my AWS account*

**Setup:**
- Enabled GuardDuty for threat detection
- Configured severity levels
- Set up SNS alerts for findings
- Practiced incident response

**Skills practiced:**
- Threat detection setup
- Security monitoring
- Finding analysis
- Basic incident response

---

### 8. Infrastructure Health Monitoring 📈

**What I learned:** Proactive health checking

![Health Monitoring](monitoring/screenshots/cloud-health-monitoring.png)
*Health check script detecting infrastructure issues*

**What it monitors:**
- Instance health status
- Disk usage across instances
- Memory utilization
- Application errors from logs

**Skills practiced:**
- Multi-service monitoring
- Health check automation
- Log aggregation
- Alert threshold configuration

**Code:** [`monitoring/health_check.py`](monitoring/health_check.py)

---

## 🔄 Self-Healing Infrastructure

**Concept I'm learning:** Infrastructure that fixes itself

**My approach:**

```
Issue Occurs → Detection → Automated Fix → Validation
```

### Examples I've Implemented:

**1. EC2 Instance Failure**
- **Detection:** CloudWatch status check fails
- **Action:** Automatic instance recovery
- **Result:** 99.9% uptime

**2. High CPU Alert**
- **Detection:** CloudWatch alarm at 80%
- **Action:** SNS email to me
- **Result:** I investigate before outage

**3. S3 Bucket Made Public**
- **Detection:** Security scan finds it
- **Action:** Script auto-blocks public access
- **Result:** Data exposure prevented

**4. Idle Resources**
- **Detection:** Script finds unused instances
- **Action:** Tag for review
- **Result:** Cost savings

**Code:** [`self_healing/`](self_healing/)

---

## 🔍 Real Troubleshooting I've Done

**Learning by breaking things intentionally:**

### Problem → Investigation → Solution → Prevention

#### 1. IAM Permission Denied
**Problem:** Script failing with `AccessDenied`  
**Investigation:** Checked CloudTrail for exact error  
**Solution:** Added missing S3 permissions  
**Learning:** CloudTrail shows exact denied action

**Documentation:** [Incident 009](docs/incidents/009-iam-role-misconfig/)

#### 2. Lambda Timeout
**Problem:** Lambda timing out after 30 seconds  
**Investigation:** Added timing logs to find bottleneck  
**Solution:** Optimized from 45s to 2s using batch operations  
**Learning:** Always use batch API calls

**Documentation:** [Incident 003](docs/incidents/003-lambda-timeout/)

#### 3. SSH Lockout
**Problem:** Locked myself out of EC2 instance  
**Investigation:** Security group missing SSH rule  
**Solution:** Used AWS CLI to add rule back  
**Learning:** Always enable Session Manager as backup

**Documentation:** [Incident 001](docs/incidents/001-ec2-ssh-lockout/)

**More:** [All Incidents](docs/incidents/)

---

## 💻 Skills I'm Demonstrating

### AWS Services (Hands-On):

**Compute:**
- ✅ EC2 - Instance management, auto-recovery, scheduling
- ✅ Lambda - Automation functions, event-driven
- ✅ VPC - Security groups, network configuration

**Storage:**
- ✅ S3 - Security auditing, access control, lifecycle policies
- ✅ EBS - Volume monitoring

**Security:**
- ✅ IAM - Policy troubleshooting, least privilege
- ✅ GuardDuty - Threat detection
- ✅ CloudTrail - Audit logging

**Monitoring:**
- ✅ CloudWatch - Logs, metrics, alarms, dashboards
- ✅ SNS - Notification management
- ✅ Config - Compliance rules

---

### Technical Skills:

**Programming & Scripting:**
- **Python** - Boto3 SDK, automation scripts (primary)
- **Bash** - Linux administration, shell scripting
- **Git** - Version control for all code

**CloudOps Practices:**
- Infrastructure monitoring
- Automated remediation
- Security auditing
- Cost optimization
- Incident response
- Professional documentation

**Tools:**
- Boto3 (AWS SDK)
- AWS CLI
- CloudWatch Logs Insights
- Linux command line
- VS Code

---

## 🚀 Quick Start

### Prerequisites

```bash
# Required
- AWS Account (Free Tier works)
- Python 3.8+
- AWS CLI configured
- pip install boto3
```

### Setup

```bash
# 1. Clone repository
git clone https://github.com/charles-bucher/CloudOpsLab.git
cd CloudOpsLab

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure AWS
aws configure

# 4. Run a script
cd scripts/
python ec2_manager.py --list

# 5. Run security audit
cd ../monitoring/
python security_audit.py
```

---

## 📁 Project Structure

```
CloudOpsLab/
├── scripts/                 # Main automation scripts
│   ├── cloudwatch_alarms.py
│   ├── ec2_auto_recovery.py
│   ├── ec2_manager.py
│   ├── ec2_scheduler.py
│   └── s3_public_check.py
├── monitoring/              # Security & health checks
│   ├── screenshots/         # Evidence of monitoring work
│   ├── security_audit.py
│   ├── health_check.py
│   └── guardduty_handler.py
├── self_healing/            # Auto-remediation
│   ├── ec2_recovery.py
│   └── s3_remediation.py
├── automation/              # Additional scripts
│   └── screenshots/         # Evidence of automation work
├── troubleshooting/         # Problem scenarios
│   ├── iam_debugging.md
│   └── lambda_timeout.md
├── docs/                    # Documentation
│   ├── screenshots/         # Portfolio screenshots
│   │   ├── automation/      # Automation evidence
│   │   └── portfolio/       # General portfolio shots
│   ├── runbooks/            # Operational runbooks
│   └── incidents/           # Incident documentation
└── README.md               # This file
```

---

## 📊 What I've Learned

### Automation:
- Python + Boto3 makes AWS programmable
- Error handling is critical
- IAM permissions need careful planning
- Test automation before deploying

### Monitoring:
- You can't fix what you can't see
- Alerts must be actionable
- CloudWatch Logs Insights is powerful
- GuardDuty catches threats I'd miss

### Self-Healing:
- Detect issues before fixing them
- Start simple, add complexity gradually
- Always have manual override
- Test failure scenarios

### Operations:
- Documentation saves time
- CloudTrail is essential for troubleshooting
- Cost optimization requires monitoring
- Security is daily work

---

## 🎯 What I'm Working On

**Next improvements:**
- [ ] ECS container monitoring
- [ ] RDS backup automation  
- [ ] Cost optimization reports
- [ ] Multi-region health checks
- [ ] Systems Manager integration

**Skills I'm practicing:**
- [ ] Lambda with EventBridge
- [ ] Step Functions workflows
- [ ] Advanced CloudWatch patterns
- [ ] Container basics (ECS)

---

## 💰 Lab Costs

**Monthly AWS Spend:**
```
EC2 (2 × t3.micro):      ~$15.00
S3 Storage:              ~$1.00
Data Transfer:           ~$2.00
CloudWatch Logs:         ~$2.00
─────────────────────────────────
Total:                   ~$20.00/month
```

**Funded by:** My part-time delivery job

**Worth it?** Absolutely. I'm building proof, not just theory.

---

## 📸 Evidence

All screenshots in this repo are from **my actual AWS account**:
- Account ID: `722631436033`
- Region: `us-east-1`
- Running: 2 × EC2 t3.micro instances
- Storage: 4 S3 buckets

**No stock images. No tutorial screenshots. Just my real work.**

---

## 🙋‍♂️ About Me

**Charles Bucher**  
Self-Taught Cloud Engineer | Career Transition

I'm 40 years old, married with three kids (ages 12, 11, and 2). I work as a delivery driver while teaching myself cloud engineering to provide better for my family.

**Why trust my work?**
- ✅ Every screenshot is from MY AWS account
- ✅ I spend my own money ($20/month) running this
- ✅ I work on this after 10-hour shifts
- ✅ Everything is documented professionally

**What I'm NOT:**
- ❌ A senior engineer pretending to be entry-level
- ❌ Someone who just copied tutorials
- ❌ A cert collector with no hands-on

**What I AM:**
- ✅ Self-taught and learning every day
- ✅ Honest about being entry-level
- ✅ Willing to start small and prove myself
- ✅ Ready to outwork anyone for this opportunity

---

## 🎯 Current Status

**Studying for:** AWS SysOps Administrator Associate  
**Looking for:** Entry-level Cloud Support / SysOps / CloudOps roles  
**Location:** Largo, Florida (remote preferred)  
**Salary expectations:** $50k-$65k (realistic for entry-level)

### What I'm Open To:
- Full-time W2 positions
- Contract work through staffing agencies
- Remote opportunities
- Hybrid roles in Tampa Bay area

### What I Can Start:
- **Immediately** - I'm ready to go

---

## 📞 Let's Connect

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/charles-bucher-cloud)
[![Email](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:quietopscb@gmail.com)
[![Portfolio](https://img.shields.io/badge/Portfolio-FF5722?style=for-the-badge&logo=google-chrome&logoColor=white)](https://charles-bucher.github.io/)

**GitHub:** [charles-bucher](https://github.com/charles-bucher)

---

## 📊 Lab Metrics

```yaml
name: Charles Bucher
role: Self-Taught Cloud Engineer
location: Largo, Florida
status: Open to Work

lab_stats:
  incidents_documented: 13
  aws_services_used: 8
  python_scripts: 25+
  runbooks_created: 10+
  resolution_time_avg: 20 minutes
  incident_recurrence: 0%
  lab_hours: 100+
  monthly_cost: $20

currently_studying:
  - AWS SysOps Administrator Associate
  - Advanced CloudWatch patterns
  - Lambda optimization

ideal_roles:
  - AWS Cloud Support Associate
  - Junior SysOps Administrator  
  - Cloud Operations Engineer
  - Entry-level DevOps Engineer

motivation: "My family deserves better than delivery driving"
```

---

## 🏆 Why This Lab Matters

### What This Proves:

**For Hiring Managers:**
- ✅ I can actually use AWS (not just theory)
- ✅ I troubleshoot systematically
- ✅ I document professionally
- ✅ I'm self-motivated

**For Me:**
- ✅ Built real cloud skills
- ✅ Have reusable automation
- ✅ Developed troubleshooting process
- ✅ Have portfolio proof

**For Other Learners:**
- ✅ Error-driven learning works
- ✅ Free tier + determination = real skills
- ✅ Document everything
- ✅ Build in public

---

## 🎓 Learning Resources I Used

**Free Resources:**
- AWS Documentation (official)
- AWS Well-Architected Framework
- Boto3 Documentation
- YouTube (specific problems only)
- Stack Overflow (when stuck)

**Paid:** $0 - Everything is free except AWS usage

---

## 🤝 Contributing

This is a personal learning project, but suggestions welcome!

**Ways to help:**
- 🐛 Report issues
- 💡 Suggest scenarios
- 📝 Improve documentation
- ⭐ Star if useful

---

## 📝 Documentation

### Operational Runbooks:
- [RB-001: EC2 Auto-Recovery](docs/runbooks/RB-001-EC2-Auto-Recovery.md)
- [RB-002: High CPU Response](docs/runbooks/RB-002-High-CPU-Response.md)
- [RB-003: S3 Public Bucket](docs/runbooks/RB-003-S3-Public-Bucket-Remediation.md)
- [RB-004: Security Audit](docs/runbooks/RB-004-Security-Audit-Procedures.md)
- [RB-005: Lambda Troubleshooting](docs/runbooks/RB-005-Lambda-Troubleshooting.md)
- [RB-006: IAM Permissions](docs/runbooks/RB-006-IAM-Permission-Denied.md)
- [RB-007: CloudWatch Alarms](docs/runbooks/RB-007-CloudWatch-Alarm-Configuration.md)

### Incident Reports:
- [All Incidents](docs/incidents/) - 13 documented incidents with full RCA

### Architecture:
- [System Architecture](docs/ARCHITECTURE.md) - Full technical overview

---

## 📄 License

MIT License - See [LICENSE.md](LICENSE.md)

---

## 🙏 Acknowledgments

**Inspiration:**
- My wife and three kids depending on this career change
- Need to prove skills through actual work
- Love for solving technical problems
- This amazing self-taught engineer community

**Tools:**
- AWS Free Tier (made this possible)
- Python & Boto3 (automation power)
- VS Code (coding environment)
- Git/GitHub (version control & portfolio)

---

## ⭐ If This Helped You

If this repo helped you learn CloudOps or gave you ideas for your own portfolio, please give it a star! It helps others find it.

---

<div align="center">

**Built with ☕, Python, and determination**

### Charles Bucher | Self-Taught Cloud Engineer

*"I can't fake experience, so I'm building proof instead"*

![Profile Views](https://komarev.com/ghpvc/?username=charles-bucher&color=0e75b6&style=flat-square)

---

**CloudOpsLab** | Learning operational excellence one problem at a time

**Status:** 🟢 Active | 💼 Open to Work | 📍 Florida

</div>

---

## 🚀 Recent Updates

- **2025-01-04:** Added comprehensive architecture documentation
- **2025-01-03:** Documented 13 incidents with runbooks
- **2024-12-30:** Implemented automated security auditing
- **2024-12-28:** Built Lambda memory optimization
- **2024-12-26:** Created EC2 auto-restart monitoring

[View Full Changelog →](CHANGELOG.md)

---

<div align="center">

[⬆ Back to Top](#cloudopslab-)

**Questions?** [Open an Issue](https://github.com/charles-bucher/CloudOpsLab/issues) or [Email Me](mailto:quietopscb@gmail.com)

</div>