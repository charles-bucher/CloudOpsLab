## **3️⃣ troubleshooting/README.md**

```markdown
# Troubleshooting Scripts

This folder contains scripts and labs designed to simulate and troubleshoot AWS cloud issues. Useful for learning, testing, and real-world incident scenarios.

## Scripts

- `ec2_connectivity_check.py` – Diagnoses EC2 SSH/RDP connectivity problems.
- `s3_permission_audit.py` – Identifies permission issues in S3 buckets.
- `rds_connection_debugger.py` – Troubleshoots RDS connectivity errors.
- Add more scripts as developed.

## How to Run

```bash
python ec2_connectivity_check.py
python s3_permission_audit.py
python rds_connection_debugger.py
Dependencies
Python 3.11+

AWS CLI configured (aws configure)

Required Python packages (boto3, requests, etc.)

Notes
Always test in a sandbox environment to avoid impacting production.

Designed for learning and practical troubleshooting exercises.

yaml
Copy code
