# CloudOpsLab Terraform Variables Example
# Copy this file to terraform.tfvars and customize

# AWS Configuration
aws_region = "us-east-1"
environment = "dev"
owner_email = "your-email@example.com"

# Alert Configuration
alert_email_addresses = [
  "your-email@example.com",
  # "team@example.com",
]

# CloudWatch Settings
cloudwatch_namespace = "CloudOpsLab"
log_retention_days   = 90

# Alarm Thresholds
cpu_alarm_threshold    = 80
memory_alarm_threshold = 85
disk_alarm_threshold   = 85

# Self-Healing Configuration
enable_self_healing   = true
self_healing_dry_run  = false

# Cost Optimization
idle_resource_threshold_days = 30
cost_report_schedule         = "cron(0 8 ? * MON *)"

# Security Settings
mfa_required              = true
encryption_required       = true
compliance_scan_schedule  = "cron(0 2 * * ? *)"

# Lambda Configuration
lambda_memory_size                     = 256
lambda_timeout                         = 300
lambda_reserved_concurrent_executions  = 10

# EventBridge Schedules
health_check_schedule = "rate(5 minutes)"
cleanup_schedule      = "cron(0 3 * * ? *)"
backup_schedule       = "cron(0 1 * * ? *)"

# Additional Tags
additional_tags = {
  # Department = "Engineering"
  # CostCenter = "12345"
}
