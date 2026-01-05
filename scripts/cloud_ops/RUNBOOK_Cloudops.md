
It reflects **real Cloud Operations responsibilities**:
- Proactive monitoring
- Incident detection
- Root cause analysis
- Automated remediation
- Post-incident validation

This is not a lab guide. It is an **operations reference**.

---

## Scope
Applies to AWS environments containing:
- EC2
- S3
- IAM
- Lambda
- CloudWatch
- GuardDuty

Used by:
- Cloud Support Engineers
- CloudOps Engineers
- Junior DevOps
- Platform Operations

---

## Operating Principles
- **Detect early**
- **Automate safely**
- **Fix root causes**
- **Validate continuously**
- **Never break prod**

---

## When to Run CloudOps Scripts

| Scenario | Action |
|-------|-------|
High CPU alarm | Run EC2 diagnostics |
IAM access error | Run credential audit |
Security alert | Run GuardDuty + exposure scans |
Cost spike | Run cost baseline scripts |
Before release | Run environment validation |
Daily ops | Run inventory & health scans |

---

## Script Categories

---

## 🔍 Monitoring & Detection

### CloudWatch Alert Handler
**Script**
- `cloudops_01_cloud_alerts.py`

**Purpose**
- Detects CloudWatch alarms
- Identifies affected resources
- Provides next-step guidance

**Run**
```bash
python cloudops_01_cloud_alerts.py
Cloud Health Check
Script

cloudops_02_cloud_health_check.py

Purpose

Validates EC2, S3, IAM, Lambda health

Flags degraded services

Run

bash
Copy code
python cloudops_02_cloud_health_check.py
🔐 Security Operations
GuardDuty Threat Monitor
Script

cloudops_03_guardduty_threat_monitoring_enabler.py

Purpose

Confirms GuardDuty status

Pulls recent findings

Highlights high-severity issues

Run

bash
Copy code
python cloudops_03_guardduty_threat_monitoring_enabler.py
IAM Credential Exposure Audit
Script

cloudops_08_iam_credential_exposure_audit.ps1

Purpose

Identifies:

Stale access keys

Unused IAM users

Over-permissioned identities

Flags credential exposure risk

Run

powershell
Copy code
.\cloudops_08_iam_credential_exposure_audit.ps1
⚠️ Read-only — no changes applied

💰 Cost & Optimization
Cost Baseline Snapshot
Script

cloudops_04_cloud_cost_baseline_snapshot.py

Purpose

Captures daily cost baseline

Detects abnormal spend patterns

EC2 Cost Optimization Scheduler
Script

cloudops_05_ec2_cost_optimization_scheduler.py

Purpose

Identifies idle EC2 instances

Recommends stop/schedule actions

🔁 Self-Healing & Recovery
EC2 Recovery Check
Script

cloudops_06_ec2_recovery_check.py

Purpose

Detects stopped or failed EC2 instances

Verifies auto-recovery configuration

Idle Resource Detector
Script

cloudops_07_ec2_idle_resource_detector.py

Purpose

Flags unused EC2 resources

Prevents waste and drift

🧪 Validation & Assurance
Environment Validator
Script

cloudops_11_aws_environment_validator.py

Purpose

Ensures required AWS services are configured

Validates IAM, logging, monitoring, security

Cloud Environment Scanner
Script

cloudops_12_cloud_environment_scanner.py

Purpose

Full environment inventory

Used for audits and onboarding

📊 Portfolio & Reporting
Portfolio Resource Scan
Script

cloudops_13_portfolio_resource_scan.py

Purpose

Summarizes all active resources

Produces portfolio-ready output

Portfolio Audit Check
Script

cloudops_14_portfolio_audit_check.py

Purpose

Final quality gate

Confirms operational readiness

Portfolio Summary Runner
Script

cloudops_15_portfolio_summary_runner.py

Purpose

Aggregates results from all CloudOps scripts

Generates executive-style summary

Failure Handling
If a script fails:

Capture error output

Check IAM permissions

Validate region configuration

Re-run in verbose/debug mode

Escalate only after root cause identified

Logging & Evidence
All scripts should:

Print human-readable output

Be screenshot-ready

Support incident documentation

Screenshots belong in:

bash
Copy code
cloud_ops/screenshots/
Best Practices
Never hardcode credentials

Always run audits before remediation

Prefer read-only scans first

Treat this repo like production tooling

Why This Runbook Matters
Most portfolios show automation.

This shows:

Operational judgment

Security awareness

Cost responsibility

Incident readiness

This is CloudOps, not scripting.

Maintainer
Charles Bucher
Role Simulated: CloudOps / Platform Engineer

yaml
Copy code

---

## 📂 Correct placement
CloudOpsLab/
└── cloud_ops/
├── CLOUDOPS_RUNBOOK.md ✅
├── cloudops_01_cloud_alerts.py
├── cloudops_02_cloud_health_check.py
├── cloudops_08_iam_credential_exposure_audit.ps1
└── ...

yaml
Copy code
