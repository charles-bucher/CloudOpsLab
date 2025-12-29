automation/README.md
# Automation Scripts

This folder contains scripts designed to automate CloudOps workflows and AWS tasks. These scripts reduce manual work, enforce best practices, and maintain AWS environments.

## Scripts

- `cloud_portfolio_master_auto.py` – Generates JSON reports of AWS cloud resources for portfolio tracking.
- `cloud_repo_autofixer.py` – Automatically detects and fixes repository issues.

## How to Run

```bash
python cloud_portfolio_master_auto.py
python cloud_repo_autofixer.py

Dependencies

Python 3.11+

AWS CLI configured (aws configure)

Required Python packages (install via pip install -r requirements.txt if available)

Notes

Ensure AWS credentials are set before running scripts.

Scripts may overwrite or update files; back up important data if necessary.