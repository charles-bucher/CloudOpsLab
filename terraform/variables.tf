# CloudOpsLab Terraform Variables

variable "aws_region" {
  description = "AWS region to deploy resources"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
  default     = "dev"
  
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

variable "owner_email" {
  description = "Email address of the infrastructure owner"
  type        = string
}

variable "alert_email_addresses" {
  description = "List of email addresses to receive CloudWatch alerts"
  type        = list(string)
  default     = []
}

variable "cloudwatch_namespace" {
  description = "CloudWatch custom metrics namespace"
  type        = string
  default     = "CloudOpsLab"
}

variable "log_retention_days" {
  description = "Number of days to retain CloudWatch logs"
  type        = number
  default     = 90
  
  validation {
    condition     = contains([1, 3, 5, 7, 14, 30, 60, 90, 120, 150, 180, 365, 400, 545, 731, 1827, 3653], var.log_retention_days)
    error_message = "Log retention must be a valid CloudWatch retention value."
  }
}

# CloudWatch Alarm Thresholds
variable "cpu_alarm_threshold" {
  description = "CPU utilization percentage threshold for alarms"
  type        = number
  default     = 80
}

variable "memory_alarm_threshold" {
  description = "Memory utilization percentage threshold for alarms"
  type        = number
  default     = 85
}

variable "disk_alarm_threshold" {
  description = "Disk utilization percentage threshold for alarms"
  type        = number
  default     = 85
}

# Self-Healing Configuration
variable "enable_self_healing" {
  description = "Enable automatic self-healing actions"
  type        = bool
  default     = true
}

variable "self_healing_dry_run" {
  description = "Run self-healing in dry-run mode (no actual changes)"
  type        = bool
  default     = false
}

# Cost Optimization Settings
variable "idle_resource_threshold_days" {
  description = "Number of days before considering a resource idle"
  type        = number
  default     = 30
}

variable "cost_report_schedule" {
  description = "Cron expression for cost report generation"
  type        = string
  default     = "cron(0 8 ? * MON *)"  # Every Monday at 8 AM
}

# Security Settings
variable "mfa_required" {
  description = "Require MFA for IAM users"
  type        = bool
  default     = true
}

variable "encryption_required" {
  description = "Require encryption at rest for all data"
  type        = bool
  default     = true
}

variable "compliance_scan_schedule" {
  description = "Cron expression for compliance scanning"
  type        = string
  default     = "cron(0 2 * * ? *)"  # Daily at 2 AM
}

# Lambda Configuration
variable "lambda_memory_size" {
  description = "Memory size for Lambda functions (MB)"
  type        = number
  default     = 256
}

variable "lambda_timeout" {
  description = "Timeout for Lambda functions (seconds)"
  type        = number
  default     = 300
}

variable "lambda_reserved_concurrent_executions" {
  description = "Reserved concurrent executions for Lambda functions"
  type        = number
  default     = 10
}

# EventBridge Schedules
variable "health_check_schedule" {
  description = "Cron expression for health check execution"
  type        = string
  default     = "rate(5 minutes)"
}

variable "cleanup_schedule" {
  description = "Cron expression for resource cleanup"
  type        = string
  default     = "cron(0 3 * * ? *)"  # Daily at 3 AM
}

variable "backup_schedule" {
  description = "Cron expression for backup execution"
  type        = string
  default     = "cron(0 1 * * ? *)"  # Daily at 1 AM
}

# Tags
variable "additional_tags" {
  description = "Additional tags to apply to all resources"
  type        = map(string)
  default     = {}
}
