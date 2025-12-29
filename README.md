# CloudOpsLab 🚀

[![AWS](https://img.shields.io/badge/AWS-Cloud_Support-FF9900?style=for-the-badge&logo=amazon-aws&logoColor=white)](https://aws.amazon.com/)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![PowerShell](https://img.shields.io/badge/PowerShell-5.1+-5391FE?style=for-the-badge&logo=powershell&logoColor=white)](https://docs.microsoft.com/en-us/powershell/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

**Hands-on AWS CloudOps scripts for troubleshooting, automation, monitoring, and self-healing**

A practical repository demonstrating real-world cloud operations skills through automated troubleshooting scripts, monitoring solutions, and self-healing infrastructure patterns for AWS environments.

---

## 📋 Overview

CloudOpsLab is a comprehensive collection of cloud operations scripts and automation tools designed to showcase practical CloudOps, DevOps, and cloud support engineering skills. This repository contains real-world solutions for:

- **AWS Troubleshooting**: Diagnostic scripts for EC2, S3, Lambda, RDS, and VPC issues
- **Automation**: Self-healing infrastructure and automated remediation workflows
- **Monitoring**: CloudWatch integration, custom metrics, and alerting solutions
- **Cost Optimization**: Resource usage analysis and cost-saving recommendations
- **Security**: IAM auditing, security group validation, and compliance checking
- **Incident Response**: Automated incident detection and resolution playbooks

**Perfect for**: Cloud Support Engineers, DevOps Engineers, SREs, and CloudOps professionals building hands-on AWS expertise.

---

## 🏗️ Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      AWS Cloud Environment                   │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │   EC2        │    │   Lambda     │    │   S3         │  │
│  │ Instances    │◄───┤  Functions   │◄───┤  Buckets     │  │
│  └──────────────┘    └──────────────┘    └──────────────┘  │
│         │                    │                    │          │
│         └────────────────────┴────────────────────┘          │
│                              │                               │
│                    ┌─────────▼──────────┐                   │
│                    │   CloudWatch       │                   │
│                    │   Logs & Metrics   │                   │
│                    └─────────┬──────────┘                   │
│                              │                               │
│                    ┌─────────▼──────────┐                   │
│                    │   EventBridge      │                   │
│                    │   Rules & Triggers │                   │
│                    └─────────┬──────────┘                   │
│                              │                               │
│         ┌────────────────────┴────────────────────┐         │
│         │                                          │         │
│  ┌──────▼────────┐                      ┌─────────▼──────┐ │
│  │ SNS Alerts    │                      │ Automation     │ │
│  │ Notifications │                      │ Scripts        │ │
│  └───────────────┘                      └────────────────┘ │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

### Script Categories

```
CloudOpsLab/
│
├── troubleshooting/          # AWS service diagnostic scripts
│   ├── ec2_diagnostics.py
│   ├── s3_troubleshoot.py
│   ├── lambda_debug.py
│   └── vpc_network_check.py
│
├── automation/               # Self-healing and automation
│   ├── auto_remediation.py
│   ├── self_healing_ec2.py
│   └── scheduled_cleanup.py
│
├── monitoring/               # CloudWatch and alerting
│   ├── custom_metrics.py
│   ├── log_analysis.py
│   └── health_checks.py
│
├── cost_optimization/        # Cost analysis and savings
│   ├── resource_analyzer.py
│   ├── cost_report.py
│   └── idle_resource_finder.py
│
├── security/                 # Security auditing and compliance
│   ├── iam_audit.py
│   ├── security_group_check.py
│   └── compliance_scanner.py
│
└── incident_response/        # Incident handling playbooks
    ├── incident_detector.py
    ├── auto_responder.py
    └── root_cause_analyzer.py
```

---

## ✨ Features

### 🔍 AWS Troubleshooting Scripts
- **EC2 Instance Diagnostics**: Check instance state, status checks, system logs, and network connectivity
- **S3 Bucket Analysis**: Validate bucket permissions, lifecycle policies, encryption, and access patterns
- **Lambda Function Debugging**: Analyze execution logs, timeout issues, memory usage, and cold starts
- **VPC Network Troubleshooting**: Security group validation, route table checks, and connectivity testing
- **RDS Database Health**: Connection testing, performance metrics, and backup verification

### 🤖 Automation & Self-Healing
- **Auto-Remediation**: Automatically fix common AWS configuration issues
- **Self-Healing EC2**: Detect and recover unhealthy instances automatically
- **Resource Cleanup**: Scheduled removal of unused EBS volumes, snapshots, and elastic IPs
- **Backup Automation**: Automated EBS snapshots and S3 versioning management
- **Tag Enforcement**: Automatically tag resources based on organizational policies

### 📊 Monitoring & Alerting
- **Custom CloudWatch Metrics**: Application-level metrics and business KPIs
- **Log Aggregation**: Centralized log collection from multiple AWS services
- **Health Checks**: Automated endpoint monitoring and availability testing
- **Performance Analysis**: Resource utilization trending and capacity planning
- **Alert Routing**: Multi-channel notifications (SNS, email, Slack)

### 💰 Cost Optimization
- **Resource Usage Analysis**: Identify underutilized EC2 instances, RDS databases, and load balancers
- **Cost Reports**: Automated daily/weekly cost summaries by service and tag
- **Idle Resource Detection**: Find stopped instances, unattached volumes, and unused elastic IPs
- **Right-Sizing Recommendations**: EC2 instance optimization suggestions
- **Reserved Instance Planning**: RI coverage analysis and purchase recommendations

### 🔒 Security & Compliance
- **IAM Policy Auditing**: Review overly permissive policies and unused credentials
- **Security Group Validation**: Detect open ports and overly permissive rules
- **Encryption Verification**: Check S3 bucket and EBS volume encryption status
- **Compliance Scanning**: CIS AWS Foundations Benchmark checks
- **Access Logging**: S3 bucket and CloudTrail log analysis

### 🚨 Incident Response
- **Automated Detection**: Pattern-based incident identification from logs and metrics
- **Response Playbooks**: Predefined workflows for common incident types
- **Root Cause Analysis**: Automated log correlation and timeline reconstruction
- **Post-Incident Reports**: Automated incident documentation and lessons learned
- **Escalation Management**: Severity-based notification routing

---

## 🛠️ Setup

### Prerequisites

- **AWS Account** with appropriate IAM permissions
- **Python 3.9+** installed
- **AWS CLI** configured with credentials
- **boto3** (AWS SDK for Python)
- **PowerShell 5.1+** (for PowerShell scripts)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/charles-bucher/CloudOpsLab.git
cd CloudOpsLab
```

2. **Install Python dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure AWS credentials**
```bash
aws configure
# Enter your AWS Access Key ID
# Enter your AWS Secret Access Key
# Enter your default region (e.g., us-east-1)
# Enter your default output format (json)
```

4. **Set environment variables** (optional)
```bash
export AWS_REGION=us-east-1
export AWS_PROFILE=default
export CLOUDOPSLAB_ENV=production
```

5. **Verify installation**
```bash
python troubleshooting/ec2_diagnostics.py --help
```

### IAM Permissions Required

The scripts require the following AWS IAM permissions:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:Describe*",
        "ec2:GetConsoleOutput",
        "s3:ListBucket",
        "s3:GetBucketPolicy",
        "lambda:GetFunction",
        "lambda:ListFunctions",
        "cloudwatch:GetMetricStatistics",
        "cloudwatch:PutMetricData",
        "logs:DescribeLogStreams",
        "logs:GetLogEvents",
        "sns:Publish",
        "iam:GetUser",
        "iam:ListUsers"
      ],
      "Resource": "*"
    }
  ]
}
```

---

## 💻 Usage

### EC2 Instance Diagnostics

**Check instance health and troubleshoot issues:**

```bash
# Basic instance health check
python troubleshooting/ec2_diagnostics.py --instance-id i-1234567890abcdef0

# Detailed diagnostics with system logs
python troubleshooting/ec2_diagnostics.py --instance-id i-1234567890abcdef0 --verbose

# Check all instances in a region
python troubleshooting/ec2_diagnostics.py --region us-east-1 --all-instances

# Filter by tag
python troubleshooting/ec2_diagnostics.py --tag Environment=Production
```

**Example Output:**
```
✓ Instance i-1234567890abcdef0 is running
✓ Status checks: 2/2 passed
✓ System reachability: OK
✓ Instance reachability: OK
⚠ High CPU utilization: 87% (threshold: 80%)
✓ Network connectivity: OK
✓ Security groups: 2 attached
```

---

### S3 Bucket Troubleshooting

**Analyze S3 bucket configuration and access issues:**

```bash
# Check bucket permissions and policies
python troubleshooting/s3_troubleshoot.py --bucket-name my-app-bucket

# Verify encryption and versioning
python troubleshooting/s3_troubleshoot.py --bucket-name my-app-bucket --check-encryption

# Analyze access patterns and logs
python troubleshooting/s3_troubleshoot.py --bucket-name my-app-bucket --access-analysis

# Check lifecycle policies
python troubleshooting/s3_troubleshoot.py --bucket-name my-app-bucket --lifecycle-check
```

---

### Lambda Function Debugging

**Diagnose Lambda execution issues and performance problems:**

```bash
# Analyze recent Lambda invocations
python troubleshooting/lambda_debug.py --function-name my-function

# Check for timeout and memory issues
python troubleshooting/lambda_debug.py --function-name my-function --performance-check

# View detailed error logs
python troubleshooting/lambda_debug.py --function-name my-function --errors-only

# Cold start analysis
python troubleshooting/lambda_debug.py --function-name my-function --cold-start-analysis
```

---

### Self-Healing EC2 Automation

**Automatically detect and recover unhealthy EC2 instances:**

```bash
# Enable self-healing for specific instances
python automation/self_healing_ec2.py --instance-ids i-123,i-456 --enable

# Monitor all instances with auto-recovery
python automation/self_healing_ec2.py --all-instances --auto-recover

# Configure health check parameters
python automation/self_healing_ec2.py --health-check-interval 60 --failure-threshold 3

# Dry run mode (no actions taken)
python automation/self_healing_ec2.py --all-instances --dry-run
```

**Self-Healing Actions:**
- Restart unhealthy instances
- Replace failed instances from ASG
- Alert administrators via SNS
- Log all actions to CloudWatch

---

### Cost Optimization Analysis

**Identify cost-saving opportunities:**

```bash
# Generate comprehensive cost report
python cost_optimization/resource_analyzer.py --full-report

# Find idle resources
python cost_optimization/idle_resource_finder.py --region us-east-1

# Right-sizing recommendations
python cost_optimization/resource_analyzer.py --rightsizing-recommendations

# Export report to S3
python cost_optimization/cost_report.py --output-bucket cost-reports --format json
```

**Example Output:**
```
💰 Cost Optimization Opportunities Found:

1. Idle EC2 Instances (7 found)
   • i-abc123: t3.large, stopped 45 days, $50/month savings
   • i-def456: m5.xlarge, <5% CPU, $120/month savings

2. Unattached EBS Volumes (12 found)
   • vol-123: 500GB gp3, unused 90 days, $40/month savings
   • vol-456: 1TB io2, unused 30 days, $125/month savings

3. Unused Elastic IPs (3 found)
   • eipalloc-xyz: unattached, $3.60/month savings

Total Potential Monthly Savings: $338.60
```

---

### CloudWatch Monitoring & Alerts

**Set up custom metrics and alerts:**

```bash
# Create custom CloudWatch metric
python monitoring/custom_metrics.py --metric-name AppResponseTime --value 245 --unit Milliseconds

# Configure CloudWatch alarms
python monitoring/health_checks.py --create-alarm --metric CPUUtilization --threshold 80

# Analyze CloudWatch logs
python monitoring/log_analysis.py --log-group /aws/lambda/my-function --start-time 1h

# Generate health dashboard
python monitoring/health_checks.py --dashboard --services ec2,rds,lambda
```

---

### Security Auditing

**Perform security checks and compliance scans:**

```bash
# Audit IAM users and policies
python security/iam_audit.py --check-mfa --check-access-keys

# Security group analysis
python security/security_group_check.py --region us-east-1 --check-open-ports

# Compliance scanning (CIS Benchmark)
python security/compliance_scanner.py --benchmark cis --output-format pdf

# S3 bucket security assessment
python security/s3_security_check.py --all-buckets --check-encryption
```

---

### Incident Response

**Automated incident detection and response:**

```bash
# Monitor for incidents
python incident_response/incident_detector.py --monitor --alert-sns-topic arn:aws:sns:...

# Trigger automated response playbook
python incident_response/auto_responder.py --incident-type high-cpu --instance-id i-123

# Root cause analysis
python incident_response/root_cause_analyzer.py --incident-id INC-2024-001 --time-range 2h

# Generate incident report
python incident_response/incident_detector.py --generate-report --incident-id INC-2024-001
```

---

## 🎯 Skills Demonstrated

This repository showcases practical skills essential for **Cloud Support Engineers**, **DevOps Engineers**, **SREs**, and **CloudOps** professionals:

### Cloud Platform Expertise
- ✅ **AWS Service Mastery**: EC2, S3, Lambda, RDS, VPC, CloudWatch, IAM, SNS, EventBridge
- ✅ **AWS CLI & SDK**: Proficient with boto3 (Python) and AWS CLI for automation
- ✅ **Multi-Region Operations**: Cross-region resource management and disaster recovery

### Troubleshooting & Diagnostics
- ✅ **Log Analysis**: CloudWatch Logs, application logs, system logs, VPC Flow Logs
- ✅ **Performance Debugging**: CPU, memory, disk I/O, network throughput analysis
- ✅ **Root Cause Analysis**: Systematic problem identification and resolution
- ✅ **Network Troubleshooting**: Security groups, NACLs, route tables, VPC peering

### Automation & Scripting
- ✅ **Python Scripting**: boto3, error handling, API integration, data processing
- ✅ **PowerShell**: Windows automation, Active Directory integration
- ✅ **Bash Scripting**: Linux system administration and automation
- ✅ **Infrastructure as Code**: Terraform basics, CloudFormation templates

### Monitoring & Observability
- ✅ **CloudWatch Integration**: Custom metrics, alarms, dashboards, log insights
- ✅ **Alerting Systems**: SNS, email, Slack integration, PagerDuty
- ✅ **Health Checks**: Endpoint monitoring, availability testing, synthetic monitoring
- ✅ **Performance Metrics**: KPI tracking, SLA monitoring, capacity planning

### DevOps & SRE Practices
- ✅ **CI/CD Understanding**: Deployment automation, testing strategies
- ✅ **Self-Healing Systems**: Automated remediation and recovery workflows
- ✅ **Incident Management**: Detection, response, escalation, post-mortems
- ✅ **Change Management**: Safe deployment practices, rollback procedures

### Security & Compliance
- ✅ **IAM Best Practices**: Least privilege, MFA enforcement, access key rotation
- ✅ **Security Auditing**: Vulnerability scanning, compliance checking
- ✅ **Encryption**: At-rest and in-transit encryption validation
- ✅ **Compliance Standards**: CIS Benchmarks, AWS Well-Architected Framework

### Cost Management
- ✅ **Cost Analysis**: Service-level cost breakdown and trending
- ✅ **Resource Optimization**: Right-sizing, idle resource identification
- ✅ **Budget Management**: Cost allocation tags, budget alerts
- ✅ **Reserved Instance Planning**: RI coverage and utilization analysis

### Communication & Documentation
- ✅ **Technical Documentation**: Clear README files, inline code comments
- ✅ **Incident Reports**: Structured post-incident documentation
- ✅ **Runbooks**: Step-by-step operational procedures
- ✅ **Knowledge Sharing**: Well-organized GitHub repository structure

---

## 📁 Project Structure

```
CloudOpsLab/
│
├── README.md                          # This file
├── LICENSE                            # MIT License
├── requirements.txt                   # Python dependencies
├── .gitignore                        # Git ignore rules
│
├── troubleshooting/                   # AWS troubleshooting scripts
│   ├── ec2_diagnostics.py            # EC2 instance health checks
│   ├── s3_troubleshoot.py            # S3 bucket analysis
│   ├── lambda_debug.py               # Lambda function debugging
│   ├── vpc_network_check.py          # VPC and network diagnostics
│   ├── rds_health_check.py           # RDS database monitoring
│   └── README.md                     # Troubleshooting guide
│
├── automation/                        # Automation scripts
│   ├── auto_remediation.py           # Automated issue fixing
│   ├── self_healing_ec2.py           # EC2 self-healing
│   ├── scheduled_cleanup.py          # Resource cleanup
│   ├── backup_automation.py          # Automated backups
│   ├── tag_enforcer.py               # Resource tagging
│   └── README.md                     # Automation guide
│
├── monitoring/                        # Monitoring and alerting
│   ├── custom_metrics.py             # Custom CloudWatch metrics
│   ├── log_analysis.py               # Log aggregation and parsing
│   ├── health_checks.py              # Endpoint monitoring
│   ├── performance_analyzer.py       # Performance trending
│   ├── alert_manager.py              # Alert routing
│   └── README.md                     # Monitoring guide
│
├── cost_optimization/                 # Cost management
│   ├── resource_analyzer.py          # Resource usage analysis
│   ├── cost_report.py                # Cost reporting
│   ├── idle_resource_finder.py       # Unused resource detection
│   ├── rightsizing_advisor.py        # Instance optimization
│   ├── ri_planner.py                 # Reserved Instance planning
│   └── README.md                     # Cost optimization guide
│
├── security/                          # Security and compliance
│   ├── iam_audit.py                  # IAM policy review
│   ├── security_group_check.py       # Security group validation
│   ├── compliance_scanner.py         # Compliance checking
│   ├── encryption_validator.py       # Encryption verification
│   ├── access_log_analyzer.py        # Access pattern analysis
│   └── README.md                     # Security guide
│
├── incident_response/                 # Incident management
│   ├── incident_detector.py          # Automated detection
│   ├── auto_responder.py             # Response automation
│   ├── root_cause_analyzer.py        # RCA automation
│   ├── escalation_manager.py         # Escalation workflows
│   ├── post_incident_reporter.py     # Incident documentation
│   └── README.md                     # Incident response guide
│
├── utils/                             # Shared utilities
│   ├── aws_client.py                 # AWS client wrapper
│   ├── logger.py                     # Logging configuration
│   ├── config.py                     # Configuration management
│   ├── notifications.py              # SNS/email helpers
│   └── metrics_helper.py             # CloudWatch helpers
│
├── tests/                             # Unit tests
│   ├── test_troubleshooting.py
│   ├── test_automation.py
│   └── test_monitoring.py
│
├── docs/                              # Additional documentation
│   ├── TROUBLESHOOTING_GUIDE.md
│   ├── AUTOMATION_PLAYBOOKS.md
│   ├── MONITORING_SETUP.md
│   └── INCIDENT_RESPONSE.md
│
└── examples/                          # Usage examples
    ├── example_workflows.md
    ├── sample_outputs/
    └── demo_scenarios/
```

---

## 🔧 Configuration

### Environment Variables

```bash
# AWS Configuration
export AWS_REGION=us-east-1
export AWS_PROFILE=cloudops
export AWS_DEFAULT_OUTPUT=json

# CloudOpsLab Settings
export CLOUDOPSLAB_ENV=production
export CLOUDOPSLAB_LOG_LEVEL=INFO
export CLOUDOPSLAB_SNS_TOPIC=arn:aws:sns:us-east-1:123456789012:cloudops-alerts

# Monitoring Configuration
export CLOUDWATCH_NAMESPACE=CloudOpsLab
export METRIC_RETENTION_DAYS=90
export HEALTH_CHECK_INTERVAL=60

# Cost Optimization
export COST_REPORT_BUCKET=cloudops-cost-reports
export IDLE_RESOURCE_THRESHOLD_DAYS=30
export CPU_UTILIZATION_THRESHOLD=5

# Security Settings
export ENABLE_MFA_CHECK=true
export ENABLE_ENCRYPTION_CHECK=true
export SECURITY_SCAN_SCHEDULE="0 2 * * *"
```

### Configuration File (config.yaml)

```yaml
aws:
  region: us-east-1
  profile: default
  
monitoring:
  cloudwatch_namespace: CloudOpsLab
  metric_retention_days: 90
  health_check_interval: 60
  alert_sns_topic: arn:aws:sns:us-east-1:123456789012:cloudops-alerts

automation:
  self_healing_enabled: true
  auto_remediation_enabled: true
  cleanup_schedule: "0 3 * * *"
  backup_schedule: "0 1 * * *"

cost_optimization:
  report_bucket: cloudops-cost-reports
  idle_threshold_days: 30
  cpu_threshold_percent: 5
  report_schedule: "0 8 * * MON"

security:
  iam_audit_enabled: true
  mfa_required: true
  encryption_required: true
  compliance_scan_schedule: "0 2 * * *"

logging:
  level: INFO
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  file: cloudopslab.log
```

---

## 🧪 Testing

Run unit tests to verify functionality:

```bash
# Run all tests
pytest tests/

# Run specific test module
pytest tests/test_troubleshooting.py

# Run with coverage report
pytest --cov=cloudopslab tests/

# Run tests for specific functionality
pytest tests/ -k "ec2"
```

---

## 📚 Additional Resources

### AWS Documentation
- [AWS CLI Command Reference](https://docs.aws.amazon.com/cli/latest/reference/)
- [Boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
- [CloudWatch Documentation](https://docs.aws.amazon.com/cloudwatch/)
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)

### CloudOps Best Practices
- [AWS Cloud Operations](https://aws.amazon.com/cloudops/)
- [Site Reliability Engineering](https://sre.google/)
- [The DevOps Handbook](https://itrevolution.com/the-devops-handbook/)

### Related Projects
- [AWS Error-Driven Troubleshooting Lab](https://github.com/charles-bucher/AWS_Error_Driven_Troubleshooting_Lab)
- [AWS Cloud Support Simulator](https://github.com/charles-bucher/AWS_Cloud_Support_Sim)
- [AWS CloudOps Suite](https://github.com/charles-bucher/AWS_Cloudops_Suite)

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 Charles Bucher

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

## 📧 Contact

**Charles Bucher**  
AWS Cloud Support & DevOps Engineer

- 📧 Email: [quietopscb@gmail.com](mailto:quietopscb@gmail.com)
- 💼 LinkedIn: [charles-bucher-cloud](https://www.linkedin.com/in/charles-bucher-cloud)
- 🌐 Portfolio: [charles-bucher.github.io](https://charles-bucher.github.io/)
- 💻 GitHub: [@charles-bucher](https://github.com/charles-bucher)

---

## ⭐ Show Your Support

If you find this project helpful, please consider giving it a star! ⭐

[![Star History Chart](https://api.star-history.com/svg?repos=charles-bucher/CloudOpsLab&type=Date)](https://star-history.com/#charles-bucher/CloudOpsLab&Date)

---

## 🎯 Project Goals

This repository demonstrates:

1. **Practical CloudOps Skills**: Real-world troubleshooting and automation
2. **AWS Service Expertise**: Deep understanding of core AWS services
3. **Problem-Solving Ability**: Systematic approach to incident resolution
4. **Automation Mindset**: Building self-healing and efficient systems
5. **Professional Documentation**: Clear, comprehensive technical writing
6. **Career Readiness**: Skills directly applicable to cloud support roles

---

<div align="center">

**Built with ☁️ by Charles Bucher**

*Transitioning to cloud operations through hands-on learning and real-world projects*

[![AWS](https://img.shields.io/badge/AWS-Certified_Ready-FF9900?style=flat-square&logo=amazon-aws&logoColor=white)](https://aws.amazon.com/certification/)
[![Python](https://img.shields.io/badge/Python-Expert-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![CloudOps](https://img.shields.io/badge/CloudOps-Professional-0078D4?style=flat-square)](https://github.com/charles-bucher/CloudOpsLab)

</div>