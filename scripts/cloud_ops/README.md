Overview
Purpose
This folder contains CloudOps automation, monitoring, auditing, remediation, and backup scripts used to operate and secure cloud portfolios. Scripts are intended to run from CI pipelines, automation runners, or scheduled jobs and are organized to separate cloud-level operations from repository-level portfolio tooling.
Audience
Cloud engineers, SREs, security engineers, and automation owners responsible for multi-account cloud governance and repository hygiene.

Folder Structure
- scripts/ — Cloud operations scripts for monitoring, cost, security, remediation, and backups.
- scripts/portfolio_ops/ — Repository-level automation, linting, compliance, and remediation tools.

Scripts Summary
|  |  |  |  | 
|  |  |  |  | 
|  |  |  |  | 
|  |  |  |  | 
|  |  |  |  | 
|  |  |  |  | 
|  |  |  |  | 
|  |  |  |  | 
|  |  |  |  | 
|  |  |  |  | 
|  |  |  |  | 
|  |  |  |  | 
|  |  |  |  | 
|  |  |  |  | 
|  |  |  |  | 
|  |  |  |  | 
|  |  |  |  | 
|  |  |  |  | 
|  |  |  |  | 



Prerequisites and Setup
Runtime
- Python 3.8 or newer recommended.
- Dependencies Install with pip install -r requirements.txt if a requirements file exists.
Credentials and Permissions
- Configure cloud credentials via CLI profiles or environment variables.
- Ensure executing identity follows least-privilege principles and has required read and remediation permissions.
Secrets and Configuration
- Store secrets in a secrets manager or CI secret store.
- Use environment variables or a central config file for region, account IDs, notification endpoints, and thresholds.
- Avoid committing secrets or sensitive configuration to the repo.

Usage Examples and Best Practices
Run a script locally
python scripts/07_idle_ec2_finder.py --profile prod --region us-east-1 --dry-run


Common flags
- --dry-run to preview changes for remediation scripts.
- --profile to select cloud account profile.
- --region to scope scans to a region.
- --output to specify CSV/JSON output or S3 target.
Scheduling
- Use cron, AWS EventBridge, Azure Logic Apps, or GitHub Actions for periodic runs.
- Integrate 01_cloud_alerts.py with notification endpoints for actionable alerts.
Logging and Observability
- Centralize logs to CloudWatch, Azure Monitor, or a logging service for auditability.
- Emit metrics for key scripts to track execution success, findings count, and remediation outcomes.
Safety
- Always run remediation scripts with --dry-run first.
- Require approval gates for destructive or high-risk automated changes.
- Keep backups or snapshots before running mass-remediation or string-cleaner tasks.

Contributing and Governance
Contributing
- Open a pull request with a clear description, tests, and reproduction steps.
- Include unit tests or integration tests for new checks or remediations.
Code Review
- Require peer review for changes that modify remediation logic or permission scopes.
Testing
- Add CI jobs that run linters, unit tests, and a dry-run of remediation logic against sample repos.
Changelog and Release Notes
- Document behavior changes and new remediation rules in a changelog entry.
