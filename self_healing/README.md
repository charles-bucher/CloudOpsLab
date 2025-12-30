# Self-Healing Scripts

This folder contains scripts for automatic remediation and AWS security automation. These scripts detect issues and take corrective actions to maintain system reliability and security posture.

---

## 🔐 AWS Security & Remediation Scripts

### `guardduty-enable.py`
Automatically enables AWS GuardDuty across your AWS accounts for threat detection.

**Purpose:** Ensure GuardDuty is active for continuous security monitoring  
**Use Case:** Bulk enable security monitoring across multiple accounts or regions

**How to Run:**
```bash
python guardduty-enable.py
```

---

### `remediation.py`
Generic auto-remediation framework for handling common AWS infrastructure issues.

**Purpose:** Automated response to detected problems  
**Use Case:** Reduce manual intervention for routine infrastructure issues

**How to Run:**
```bash
python remediation.py
```

---

## 📊 Portfolio & Code Analysis Tools

### `portfolio_code_quality.ps1` / `PortfolioCodeQualityScanner.ps1`
Scans GitHub repositories for code quality metrics and best practices.

**Purpose:** Evaluate code quality across your portfolio  
**Use Case:** Identify areas for improvement before job applications

**How to Run:**
```powershell
pwsh portfolio_code_quality.ps1
# or
pwsh PortfolioCodeQualityScanner.ps1
```

---

### `portfolio_hireability.ps1` / `PortfolioHireabilityScanner.ps1`
Analyzes GitHub portfolio for factors that impact hireability (documentation, commit history, etc.).

**Purpose:** Get actionable feedback on your GitHub presence  
**Use Case:** Optimize your portfolio for recruiter and hiring manager visibility

**How to Run:**
```powershell
pwsh portfolio_hireability.ps1
# or
pwsh PortfolioHireabilityScanner.ps1
```

---

## 📋 Prerequisites

**For Python Scripts:**
- Python 3.8+
- AWS CLI configured (`aws configure`)
- boto3: `pip install boto3 --break-system-packages`
- IAM permissions for GuardDuty and remediation actions

**For PowerShell Scripts:**
- PowerShell 7+ (cross-platform)
- GitHub access (for portfolio scanning)

---

## ⚠️ Important Notes

- **Test First:** Always test remediation scripts in non-production environments
- **Review Logs:** These scripts take automatic actions—verify results in logs
- **IAM Permissions:** Ensure your AWS credentials have appropriate permissions
- **Backup Files:** `.bak` files are backups of working versions during development

---

## 🎯 Coming Soon

- Auto-restart for stopped EC2 instances
- Disk space cleanup automation
- Failed service recovery scripts
- Lambda-based self-healing functions

---

## 💡 Usage Tips

1. **Start with GuardDuty:** Run `guardduty-enable.py` first to establish security monitoring
2. **Review remediation.py:** Understand what actions it takes before enabling
3. **Use Portfolio Scanners:** Run before applying to jobs to optimize your GitHub presence
4. **Monitor Results:** Check CloudWatch Logs and script output for remediation actions

## TL;DR

_TODO_

## Overview

_TODO_

## Setup Instructions

_TODO_

## Usage Examples

_TODO_

## Incident Scenarios

_TODO_

## Screenshots

_TODO_

## Contact

_TODO_
