Skip to content
Navigation Menu
charles-bucher
CloudOpsLab

Type / to search
Code
Issues
Pull requests
Actions
Projects
Wiki
Security
Insights
Settings
Files
Go to file
t
automation
List_pngs.sh
README.md
commit_autofixer.py
portfolio_master_auto.py
repo_autofixer.py
repo_lint_fixer.py
repo_safe_autofixer.py
repo_string_fixer.py
docs
monitoring
self_healing
troubleshooting
.gitignore
LICENSE
README.md
CloudOpsLab
/automation/
author
Charles Bucher
Add categorized scripts and remove outdated README
b38b053
 · 
9 minutes ago
Name	Last commit message	Last commit date
..
List_pngs.sh
Add CloudOpsLab scripts, backups, and updated READMEs
39 minutes ago
README.md
Add CloudOpsLab scripts, backups, and updated READMEs
39 minutes ago
commit_autofixer.py
Add categorized scripts and remove outdated README
9 minutes ago
portfolio_master_auto.py
Add categorized scripts and remove outdated README
9 minutes ago
repo_autofixer.py
Add categorized scripts and remove outdated README
9 minutes ago
repo_lint_fixer.py
Add categorized scripts and remove outdated README
9 minutes ago
repo_safe_autofixer.py
Add categorized scripts and remove outdated README
9 minutes ago
repo_string_fixer.py
Add categorized scripts and remove outdated README
9 minutes ago
README.md
automation/README.md

Automation Scripts
This folder contains scripts designed to automate CloudOps workflows and AWS tasks. These scripts reduce manual work, enforce best practices, and maintain AWS environments.

Scripts
cloud_portfolio_master_auto.py – Generates JSON reports of AWS cloud resources for portfolio tracking.
cloud_repo_autofixer.py – Automatically detects and fixes repository issues.
How to Run
python cloud_portfolio_master_auto.py
python cloud_repo_autofixer.py

Dependencies

Python 3.11+

AWS CLI configured (aws configure)

Required Python packages (install via pip install -r requirements.txt if available)

Notes

Ensure AWS credentials are set before running scripts.

Scripts may overwrite or update files; back up important data if necessary.
