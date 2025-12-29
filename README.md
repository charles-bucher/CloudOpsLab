# CloudOpsLab ⚡

> **Real-world AWS troubleshooting, automation, and cloud support scripts that actually solve problems.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![AWS](https://img.shields.io/badge/AWS-Cloud-orange.svg)](https://aws.amazon.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-green.svg)](https://www.python.org/)

CloudOpsLab is a hands-on collection of production-ready scripts I've built while learning AWS and CloudOps. Every script here solves a real problem I've encountered or researched—whether it's diagnosing why an EC2 instance won't start, automating security group audits, or building self-healing infrastructure.

**This isn't theory. This is practical cloud support work.**

---

## 🎯 What This Repository Demonstrates

✅ **AWS Troubleshooting** – Diagnosing and fixing real infrastructure issues  
✅ **Automation & Efficiency** – Eliminating manual toil with smart scripts  
✅ **Proactive Monitoring** – Catching problems before they become incidents  
✅ **Self-Healing Systems** – Auto-remediation that keeps services running  
✅ **Cloud Best Practices** – Security, cost optimization, and reliability  

---

## 📂 Repository Structure

```
CloudOpsLab/
│
├── troubleshooting/          # Diagnostic scripts for common AWS issues
│   ├── ec2_connectivity_check.py
│   ├── s3_permission_audit.py
│   └── rds_connection_debugger.py
│
├── automation/               # Scripts that eliminate repetitive tasks
│   ├── security_group_auditor.py
│   ├── snapshot_lifecycle_manager.py
│   └── cost_optimizer.py
│
├── monitoring/               # Health checks and alerting scripts
│   ├── resource_health_monitor.py
│   ├── cloudwatch_log_analyzer.py
│   └── compliance_checker.py
│
├── self_healing/             # Auto-remediation for common failures
│   ├── auto_restart_stopped_instances.py
│   ├── disk_space_cleanup.py
│   └── failed_service_restarter.py
│
└── docs/                     # Documentation and usage guides
    └── USAGE.md
```

---

## 🚀 Quick Start

### Prerequisites
- AWS account (Free Tier works fine)
- Python 3.8+ installed
- AWS CLI configured with credentials
- Basic familiarity with AWS services

### Get Started in 3 Steps

```bash
# 1. Clone the repository
git clone https://github.com/charles-bucher/CloudOpsLab.git
cd CloudOpsLab

# 2. Install dependencies (if needed)
pip install -r requirements.txt

# 3. Run any script (example)
python troubleshooting/ec2_connectivity_check.py
```

📘 **Each folder has its own README** with detailed usage instructions and examples.

---

## 💡 Featured Scripts

### 🔍 EC2 Connectivity Troubleshooter
Diagnoses why you can't SSH/RDP into EC2 instances by checking:
- Security group rules
- Network ACLs
- Route table configurations
- Instance state and status checks

**Use Case:** Save hours troubleshooting connectivity issues—run this first.

---

### 🔐 Security Group Auditor
Identifies overly permissive security groups and flags risks:
- Open SSH (port 22) to 0.0.0.0/0
- Open RDP (port 3389) to the internet
- Unrestricted database ports

**Use Case:** Prevent security incidents before they happen.

---

### 💰 Cost Optimization Scanner
Finds ways to reduce your AWS bill:
- Unattached EBS volumes costing you money
- Idle EC2 instances running 24/7
- Old snapshots that can be deleted

**Use Case:** Show management you saved the company $X per month.

---

### 🩹 Auto-Restart Stopped Instances
Self-healing script that:
1. Monitors critical EC2 instances
2. Detects stopped instances
3. Automatically restarts them
4. Sends notification to admin

**Use Case:** Keep production services running without manual intervention.

---

## 🎓 Skills Showcased

This repository demonstrates skills directly relevant to:
- **Cloud Support Engineer** roles
- **CloudOps / DevOps** positions  
- **AWS Support Associate** jobs
- **Junior Cloud Engineer** roles
- **Infrastructure Support** positions

### Technical Skills
- AWS (EC2, S3, RDS, VPC, CloudWatch, IAM)
- Python scripting and automation
- Bash/PowerShell scripting
- Infrastructure troubleshooting
- Log analysis and debugging
- Cloud security best practices
- Cost optimization strategies

### Professional Skills
- Problem-solving and root cause analysis
- Documentation and knowledge sharing
- Automation mindset
- Proactive monitoring and alerting
- Production incident response

---

## 🛠️ Technologies & Tools

- **Cloud Platform:** AWS (Amazon Web Services)
- **Languages:** Python 3.8+, Bash, PowerShell
- **AWS Services:** EC2, S3, RDS, VPC, CloudWatch, IAM, Lambda
- **Tools:** AWS CLI, boto3 SDK, CloudWatch Logs

---

## 📈 Why This Matters

As someone transitioning into cloud computing, I'm focused on building **practical, demonstrable skills** that employers actually need. Every script in this repository:

1. **Solves a real problem** (not just tutorial exercises)
2. **Uses AWS best practices** (security, efficiency, reliability)
3. **Is production-ready** (error handling, logging, documentation)
4. **Demonstrates initiative** (self-taught, hands-on learning)

This is the kind of work I want to do professionally—helping teams keep their cloud infrastructure running smoothly, automating away repetitive tasks, and solving problems before they impact customers.

---

## 🔗 Connect With Me

- **GitHub:** [github.com/charles-bucher](https://github.com/charles-bucher)
- **LinkedIn:** [linkedin.com/in/charles-bucher-cloud](https://linkedin.com/in/charles-bucher-cloud)

Currently pursuing AWS certifications and seeking entry-level Cloud Support, CloudOps, or DevOps opportunities. Open to remote positions, contract work, and direct-hire roles.

---

## 📝 Current Status

🎯 **Actively Working On:**
- AWS Solutions Architect Associate certification
- Expanding script collection (Lambda functions, terraform automation)
- Building real-world troubleshooting scenarios

📚 **Learning Focus:**
- Infrastructure as Code (Terraform, CloudFormation)
- Container orchestration (ECS, EKS basics)
- CI/CD pipelines and automation

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

Built while learning AWS through:
- AWS Free Tier hands-on practice
- Cloud Academy and A Cloud Guru courses
- Real-world troubleshooting scenarios
- Community documentation and forums

---

**⭐ If you find these scripts useful, please star this repository!**

*CloudOpsLab is a living portfolio—scripts are added regularly as I learn and build.*