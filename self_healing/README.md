---

## **2️⃣ self_healing/README.md**

```markdown
# Self-Healing Scripts

This folder contains scripts that automatically detect and remediate common AWS issues. Self-healing scripts reduce downtime and maintain system reliability without manual intervention.

## Scripts

- `auto_restart_stopped_instances.py` – Detects stopped EC2 instances and restarts them automatically.
- `disk_space_cleanup.py` – Monitors disk usage and removes temporary or old files to free space.
- `failed_service_restarter.py` – Checks services for failures and restarts them.
- `PortfolioCodeQualityScanner.ps1` – Scans code portfolios for quality metrics (PowerShell).
- `PortfolioHireabilityScanner.ps1` – Evaluates portfolios for hireability metrics (PowerShell).
- `guardduty-enable.py` – Enables GuardDuty across AWS accounts.
- `remediation.py` – Generic auto-remediation framework for AWS issues.

## How to Run

```bash
python auto_restart_stopped_instances.py
python disk_space_cleanup.py
python failed_service_restarter.py
# PowerShell scripts
pwsh PortfolioCodeQualityScanner.ps1
pwsh PortfolioHireabilityScanner.ps1
Dependencies
Python 3.11+ or PowerShell 7+

AWS CLI configured (aws configure)

Required Python packages (boto3, requests, etc.)

Proper IAM permissions to perform remediation actions

Notes
Scripts may take corrective actions automatically; review logs for verification.

Always test in a non-production environment before running new remediation scripts.

yaml
Copy code
