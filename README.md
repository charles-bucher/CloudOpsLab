# CloudOpsLab 🔧

![AWS](https://img.shields.io/badge/AWS-FF9900?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Bash](https://img.shields.io/badge/Bash-4EAA25?style=for-the-badge&logo=gnu-bash&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)
![Open to Work](https://img.shields.io/badge/Open%20To%20Work-00C853?style=flat-square)

**Hands-on AWS CloudOps practice lab demonstrating automation, monitoring, and troubleshooting**

*Self-taught cloud engineer learning operational excellence through real-world scenarios*

---

## 🎯 About This Lab

This is my personal CloudOps learning environment where I'm teaching myself AWS operations by **actually doing the work**—not just following tutorials.

### What Makes This Different:

✅ **Real AWS account** - I'm spending ~$20/month from my delivery job to run this  
✅ **Real problems** - I break things on purpose, then learn to fix them  
✅ **Real solutions** - Python and Bash scripts I actually wrote and tested  
✅ **Real documentation** - Everything is documented like production systems  

### My Goal:

Break into cloud operations by proving I can **do the work**, even though I'm entry-level.

---

## 🧪 What I've Built

### 1. CloudWatch Monitoring & Alerting 📊

**What I learned:** How to set up automated monitoring that actually catches issues

![CloudWatch Alarm](docs/screenshots/cloudwatch-alarm-triggered.png)
*CloudWatch alarm I configured - it actually triggered when my test EC2 hit 80% CPU*

**Skills practiced:**
- Creating CloudWatch alarms with proper thresholds
- Setting up SNS topics for notifications
- Configuring email alerts
- Testing alarm logic

**Code:** [`scripts/cloudwatch_alarms.py`](scripts/cloudwatch_alarms.py)

---

### 2. EC2 Auto-Recovery 🔄

**What I learned:** How to make instances self-heal from failures

![EC2 Auto-Recovery](docs/screenshots/ec2-auto-recovery-test.png)
*Testing auto-recovery by simulating an instance failure*

**The scenario:**
1. Configured CloudWatch alarm to detect status check failures
2. Set up automatic recovery action
3. Intentionally broke my test instance
4. Watched it recover automatically
5. Documented the whole process

**Result:** Instance recovered in ~4 minutes without any manual intervention

**Skills practiced:**
- EC2 status checks (system vs instance)
- CloudWatch alarm actions
- Auto-recovery configuration
- Incident response timing

**Code:** [`scripts/ec2_auto_recovery.py`](scripts/ec2_auto_recovery.py)

---

### 3. EC2 Cost Optimization 💰

**What I learned:** How to automate EC2 scheduling to save money

![EC2 Scheduler](automation/screenshots/ec2-scheduler-iam-fix.png)
*Troubleshooting IAM permissions (common real-world problem!)*

**The problem:**
- My Lambda function kept failing with `AccessDenied`
- Had to debug IAM policies
- Fixed permissions
- Learned that IAM troubleshooting is a critical CloudOps skill

**Skills practiced:**
- Lambda function development
- IAM policy debugging
- CloudWatch Events/EventBridge
- Cost optimization strategies

**Code:** [`scripts/ec2_scheduler.py`](scripts/ec2_scheduler.py)

---

### 4. EC2 Management with Boto3 🐍

**What I learned:** Using Python to programmatically manage AWS infrastructure

![EC2 Manager](automation/screenshots/ec2-boto3-client-list.png)
*My Python script listing and managing EC2 instances*

**What it does:**
- List all EC2 instances
- Filter by tags and state
- Start/stop instances in bulk
- Handle API rate limits gracefully

**Skills practiced:**
- Boto3 SDK for Python
- AWS API interaction
- Error handling
- Pagination for large result sets

**Code:** [`scripts/ec2_manager.py`](scripts/ec2_manager.py)

---

### 5. S3 Security Auditing 🔒

**What I learned:** How to detect and fix security misconfigurations

![S3 Public Check](automation/screenshots/s3-public-access-detection.png)
*Script detecting publicly accessible S3 buckets*

**The scenario:**
1. Scan all S3 buckets for public access
2. Identify misconfigured bucket policies
3. Automatically remediate (block public access)
4. Generate audit report

**Result:** Prevented potential data exposure through automated compliance checks

**Skills practiced:**
- S3 security best practices
- Boto3 S3 operations
- Policy analysis
- Security automation

**Code:** [`scripts/s3_public_check.py`](scripts/s3_public_check.py)

---

### 6. Security Auditing 🛡️

**What I learned:** How to audit AWS accounts for security issues

![Security Audit](monitoring/screenshots/security-audit-findings.png)
*Security audit script showing compliance findings*

**What it checks:**
- ✅ IAM users without MFA
- ✅ Overly permissive Security Groups (0.0.0.0/0)
- ✅ S3 buckets with public access
- ✅ Root account usage
- ✅ Unused access keys

**Skills practiced:**
- Security auditing methodology
- Compliance frameworks (CIS, AWS Well-Architected)
- Python reporting
- Remediation tracking

**Code:** [`monitoring/security_audit.py`](monitoring/security_audit.py)

---

### 7. GuardDuty Threat Monitoring 🚨

**What I learned:** How to use GuardDuty for threat detection

![GuardDuty](monitoring/screenshots/guardduty-enabled.png)
*GuardDuty actively monitoring my AWS account*

**Setup:**
- Enabled GuardDuty across account
- Configured severity levels
- Set up automated alerts
- Practiced incident response

**Skills practiced:**
- Threat detection setup
- Security monitoring
- Finding analysis
- Incident response basics

---

### 8. CloudHealth Monitoring 📈

**What I learned:** Building infrastructure health checks

![Health Check](monitoring/screenshots/cloud-health-monitoring.png)
*Health monitoring script detecting infrastructure issues*

**What it monitors:**
- Instance health status
- Disk usage
- Memory utilization
- Application errors from logs

**Skills practiced:**
- Multi-service monitoring
- Health check automation
- Log analysis
- Alert threshold tuning

**Code:** [`monitoring/health_check.py`](monitoring/health_check.py)

---

## 🔄 Self-Healing Infrastructure

**Concept:** Infrastructure that fixes itself automatically

**My learning process:**

```
Issue Occurs → Detection (Alarm) → Automated Remediation → Validation (Testing)
```

### Real Examples I've Implemented:

**1. EC2 Instance Failure**
- **Detection:** CloudWatch status check fails
- **Action:** Automatic instance recovery
- **Result:** 99.9% uptime maintained

**2. High CPU Usage**
- **Detection:** CloudWatch alarm at 80% CPU
- **Action:** SNS alert to me
- **Result:** I can investigate before outage

**3. S3 Bucket Made Public**
- **Detection:** Script finds public bucket
- **Action:** Lambda auto-remediates to private
- **Result:** Data exposure prevented

**4. Idle Resources**
- **Detection:** Script finds unused EC2 instances
- **Action:** Tag for review
- **Result:** Cost savings

**Code:** [`self_healing/`](self_healing/)

---

## 🔍 Troubleshooting I've Done

**Real problems I created and solved** (learning by breaking things)

### Problem → Investigation → Solution → Prevention

#### 1. IAM Permission Denied
**Problem:** My automation script kept failing with `AccessDenied`  
**Investigation:** Reviewed IAM policies and CloudTrail logs  
**Solution:** Added missing S3 permissions to role  
**Learning:** Always check CloudTrail for the exact denied action

#### 2. Lambda Timeout
**Problem:** EC2 start/stop Lambda timing out  
**Investigation:** Analyzed CloudWatch Logs  
**Solution:** Increased timeout and optimized code  
**Learning:** Lambda has hard limits, design accordingly

#### 3. CloudWatch Alarm Not Firing
**Problem:** No alerts received for known issue  
**Investigation:** Checked alarm configuration and SNS  
**Solution:** Fixed alarm metric query and SNS subscription  
**Learning:** Test your monitoring before you need it

**Documentation:** [`troubleshooting/`](troubleshooting/)

---

## 💻 Skills I'm Demonstrating

### AWS Services I've Actually Used:

**Compute & Networking:**
- ✅ EC2 (instance management, auto-recovery, scheduling)
- ✅ VPC (security groups, network monitoring)
- ✅ Lambda (automation functions)

**Storage:**
- ✅ S3 (security auditing, access control)
- ✅ EBS (volume monitoring)

**Security & Compliance:**
- ✅ IAM (policy troubleshooting, least privilege)
- ✅ GuardDuty (threat detection)
- ✅ CloudTrail (audit logging)

**Monitoring:**
- ✅ CloudWatch (logs, metrics, alarms, dashboards)
- ✅ SNS (notifications and alerting)
- ✅ Config (compliance rules)

---

### Technical Skills:

**Programming & Scripting:**
- **Python** - Boto3 SDK, automation scripts
- **Bash** - Linux administration, shell scripting
- **Git** - Version control for all code

**CloudOps Practices:**
- Infrastructure monitoring
- Automated remediation
- Security auditing
- Cost optimization
- Incident response
- Documentation

**Tools:**
- Boto3 (AWS SDK for Python)
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
# 1. Clone the repository
git clone https://github.com/charles-bucher/CloudOpsLab.git
cd CloudOpsLab

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure AWS credentials
aws configure

# 4. Run a script
cd scripts/
python ec2_manager.py --list

# 5. Run security audit
cd ../monitoring/
python security_audit.py
```

### Example: Testing EC2 Auto-Recovery

```bash
# Deploy EC2 with auto-recovery
cd scripts/
python ec2_auto_recovery.py --deploy

# Simulate instance failure
python ec2_auto_recovery.py --simulate-failure

# Monitor recovery
python ec2_auto_recovery.py --check-status

# Verify recovery completed
python ec2_auto_recovery.py --validate
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
├── monitoring/              # Security & monitoring
│   ├── screenshots/         # Proof of monitoring work
│   ├── security_audit.py
│   ├── health_check.py
│   ├── guardduty_handler.py
│   └── issue_tracker.py
├── self_healing/            # Auto-remediation logic
│   ├── ec2_recovery.py
│   ├── s3_remediation.py
│   └── lambda_functions/
├── automation/              # Additional automation
│   └── screenshots/         # Proof of automation work
├── troubleshooting/         # Problem scenarios & solutions
│   ├── iam_debugging.md
│   ├── lambda_timeout.md
│   └── cloudwatch_alarms.md
├── docs/                    # Documentation
│   ├── screenshots/         # Portfolio screenshots
│   ├── architecture.md
│   └── runbooks/            # Operational runbooks
└── README.md               # You are here
```

---

## 📊 My Learning Journey

### What I've Learned:

**Automation:**
- Python + Boto3 makes AWS operations programmable
- Error handling is critical for production automation
- IAM permissions require careful planning
- Testing automation is as important as writing it

**Monitoring:**
- You can't fix what you can't see
- Alerts must be actionable, not noisy
- CloudWatch Logs Insights is powerful for debugging
- GuardDuty catches things humans miss

**Self-Healing:**
- Automate detection before remediation
- Start with simple recovery, add complexity gradually
- Always have manual override capability
- Test failure scenarios regularly

**Operations:**
- Documentation saves time during incidents
- Cost optimization requires continuous monitoring
- Security is a daily practice, not a checkbox
- CloudTrail is your best friend for troubleshooting

---

## 🎯 What I'm Working On Next

**Planned improvements:**
- [ ] ECS container monitoring
- [ ] RDS backup automation
- [ ] Cost optimization reports
- [ ] Multi-region health checks
- [ ] Systems Manager integration
- [ ] Config compliance rules

**Skills I'm practicing:**
- [ ] Lambda with EventBridge
- [ ] Step Functions for workflows
- [ ] Advanced CloudWatch Logs Insights
- [ ] Container orchestration basics

---

## 💰 Cost Transparency

**Monthly AWS Costs for This Lab:**
```
EC2 (2 × t3.micro):      ~$15.00
S3 Storage:              ~$1.00
Data Transfer:           ~$2.00
CloudWatch Logs:         ~$2.00
─────────────────────────────────
Total:                   ~$20.00/month
```

**Funded by:** My part-time delivery job while learning cloud

**Worth it?** Absolutely. I'm building proof, not just theory.

---

## 📸 Screenshots & Evidence

All screenshots in this repo are from **my actual AWS account**. No stock images, no tutorial screenshots.

**Screenshot locations:**
- `docs/screenshots/` - General portfolio screenshots
- `automation/screenshots/` - Automation project screenshots
- `monitoring/screenshots/` - Monitoring & security screenshots

---

## 🙋‍♂️ About Me

**Charles Bucher**  
Self-Taught Cloud Engineer | Career Transition from Delivery Driving

**My Story:**

I'm 40 years old, working as a delivery driver, teaching myself cloud engineering to provide better for my family. Instead of just watching tutorials, I'm actually **building things in AWS** and documenting everything.

**Why trust my work?**
- ✅ Every screenshot is from MY AWS account
- ✅ I spend my own money running these labs ($20/month)
- ✅ I work on these projects after 10-hour delivery shifts
- ✅ I document everything like production systems

**What I'm NOT:**
- ❌ A senior engineer pretending to be entry-level
- ❌ Someone who just copied tutorials
- ❌ A paper cert chaser with no hands-on

**What I AM:**
- ✅ Self-taught and proud of it
- ✅ Honest about being entry-level
- ✅ Willing to start small and prove myself
- ✅ Ready to outwork anyone for this opportunity

---

## 🎯 Current Status

**Studying for:** AWS SysOps Administrator Associate  
**Looking for:** Entry-level Cloud Support / SysOps / DevOps roles  
**Location:** Florida (remote preferred)  
**Salary expectations:** $50k+ (realistic for entry-level)

### What I'm Open To:
- Full-time W2 positions
- Contract work through staffing agencies
- Remote opportunities
- Hybrid roles in Tampa Bay area

---

## 📞 Let's Connect

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/charles-bucher-cloud)
[![Email](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:quietopscb@gmail.com)
[![Portfolio](https://img.shields.io/badge/Portfolio-FF5722?style=for-the-badge&logo=google-chrome&logoColor=white)](https://charles-bucher.github.io/)

---

## 📝 Quick Facts

```yaml
name: Charles Bucher
role: Self-Taught Cloud Engineer
location: Florida
status: Open to Work
focus: AWS CloudOps

skills:
  cloud: [AWS, CloudWatch, EC2, S3, Lambda, IAM]
  scripting: [Python, Bash]
  tools: [Boto3, AWS CLI, Git, Linux]
  practices: [Automation, Monitoring, Security, Troubleshooting]

currently_learning:
  - AWS SysOps Administrator Associate
  - Advanced CloudWatch patterns
  - Infrastructure automation

ideal_role:
  - AWS Cloud Support Associate
  - Junior SysOps Administrator  
  - Cloud Operations Engineer
  - Entry-level DevOps Engineer

motivation: "Family deserves better than paycheck-to-paycheck living"
```

---

## 🏆 Why This Lab Matters

### What This Proves:

**For Hiring Managers:**
- ✅ I can actually use AWS (not just theory)
- ✅ I troubleshoot systematically
- ✅ I document professionally
- ✅ I'm self-motivated (teaching myself after work)

**For Me:**
- ✅ Built confidence in AWS operations
- ✅ Created reusable automation scripts
- ✅ Developed systematic debugging approach
- ✅ Have portfolio proof of hands-on work

**For Other Learners:**
- ✅ Error-driven learning works
- ✅ You don't need expensive courses
- ✅ Free tier + determination = real skills
- ✅ Document everything!

---

## 🤝 Contributing

This is a personal learning project, but I'm open to suggestions!

**Ways to help:**
- 🐛 Report issues or bugs
- 💡 Suggest new scenarios
- 📝 Improve documentation
- ⭐ Star the repo if you find it useful

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

---

## 🙏 Acknowledgments

**Learning Resources:**
- AWS Documentation
- AWS Well-Architected Framework
- Boto3 Documentation
- Real-world experience from this lab

**Inspiration:**
- My family depending on this career change
- The need to prove skills through actual work
- Love for solving technical problems
- This community of self-taught engineers

---

## ⭐ If This Helped You...

If this repo helped you learn CloudOps or gave you ideas for your own portfolio, please give it a star! It helps others find it too.

---

<div align="center">

**Built with ☕, Python, and a lot of trial and error**

### Charles Bucher | Self-Taught Cloud Engineer

*"I can't fake experience, so I'm building proof instead"*

![Profile Views](https://komarev.com/ghpvc/?username=charles-bucher&color=0e75b6&style=flat-square&label=Repo+Views)

</div>

---

<div align="center">

**CloudOpsLab** | Learning operational excellence one automation at a time

[⬆ Back to Top](#cloudopslab-)

</div>