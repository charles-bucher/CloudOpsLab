Self-Healing 🛠️

This folder contains scripts designed for automatic remediation of cloud and system issues. These scripts detect common problems and fix them without manual intervention, showcasing CloudOps automation and problem-solving skills.

📂 Folder Contents
Script Name	Purpose	Notes
auto_restart_ec2.ps1	Detects stopped EC2 instances and restarts them automatically	Requires AWS CLI configured
s3_fix_permissions.ps1	Checks S3 bucket permissions and corrects misconfigurations	Helps enforce security best practices
cloudwatch_auto_resolve.ps1	Responds to specific CloudWatch alarms with automated actions	Demonstrates self-healing workflows
resource_cleanup.py	Automatically removes unused resources to save costs	Python script, uses boto3

(Add more scripts as you create them)

⚡ How to Use

Ensure AWS CLI or required Python modules are installed.

Run scripts with PowerShell or Python in this folder. Example:

.\auto_restart_ec2.ps1


Scripts will detect and resolve issues automatically.

Check logs for actions taken and results.

💡 Best Practices

Test scripts in a staging environment before production.

Log all automated actions for auditing purposes.

Combine self-healing scripts with monitoring scripts for proactive CloudOps workflows.

Keep scripts modular and parameterized for reuse.

🎯 Purpose

This folder demonstrates your ability to:

Implement automation and self-healing workflows in cloud environments

Reduce downtime and manual intervention

Show initiative and advanced CloudOps problem-solving skills

Build portfolio-ready scripts for recruiters and employers

