# CloudOpsLab Terraform Outputs

output "account_id" {
  description = "AWS Account ID"
  value       = data.aws_caller_identity.current.account_id
}

output "region" {
  description = "AWS Region"
  value       = data.aws_region.current.name
}

output "environment" {
  description = "Environment name"
  value       = var.environment
}

# S3 Outputs
output "s3_bucket_name" {
  description = "Name of the CloudOpsLab S3 bucket"
  value       = aws_s3_bucket.cloudopslab_data.id
}

output "s3_bucket_arn" {
  description = "ARN of the CloudOpsLab S3 bucket"
  value       = aws_s3_bucket.cloudopslab_data.arn
}

# SNS Outputs
output "sns_topic_arn" {
  description = "ARN of the CloudOpsLab alerts SNS topic"
  value       = aws_sns_topic.cloudopslab_alerts.arn
}

output "sns_topic_name" {
  description = "Name of the CloudOpsLab alerts SNS topic"
  value       = aws_sns_topic.cloudopslab_alerts.name
}

# CloudWatch Outputs
output "cloudwatch_log_group_name" {
  description = "Name of the main CloudWatch log group"
  value       = aws_cloudwatch_log_group.cloudopslab.name
}

output "cloudwatch_log_group_arn" {
  description = "ARN of the main CloudWatch log group"
  value       = aws_cloudwatch_log_group.cloudopslab.arn
}

output "lambda_log_group_name" {
  description = "Name of the Lambda CloudWatch log group"
  value       = aws_cloudwatch_log_group.lambda_logs.name
}

# KMS Outputs
output "kms_key_id" {
  description = "ID of the CloudOpsLab KMS key"
  value       = aws_kms_key.cloudopslab.id
}

output "kms_key_arn" {
  description = "ARN of the CloudOpsLab KMS key"
  value       = aws_kms_key.cloudopslab.arn
}

# Module Outputs
output "cloudwatch_dashboard_url" {
  description = "URL to the CloudWatch dashboard"
  value       = module.cloudwatch.dashboard_url
}

output "lambda_function_names" {
  description = "Names of deployed Lambda functions"
  value       = module.lambda.function_names
}

output "lambda_function_arns" {
  description = "ARNs of deployed Lambda functions"
  value       = module.lambda.function_arns
}

output "iam_role_arns" {
  description = "ARNs of IAM roles created"
  value       = module.iam.role_arns
}

output "eventbridge_rule_names" {
  description = "Names of EventBridge rules"
  value       = module.eventbridge.rule_names
}

# Quick Access Commands
output "useful_commands" {
  description = "Useful AWS CLI commands for CloudOpsLab"
  value = <<-EOT
  
  # View CloudWatch Logs
  aws logs tail ${aws_cloudwatch_log_group.cloudopslab.name} --follow
  
  # View Lambda Logs
  aws logs tail ${aws_cloudwatch_log_group.lambda_logs.name} --follow
  
  # List S3 Bucket Contents
  aws s3 ls s3://${aws_s3_bucket.cloudopslab_data.id}/
  
  # View CloudWatch Dashboard
  ${module.cloudwatch.dashboard_url}
  
  # Publish Test Alert
  aws sns publish --topic-arn ${aws_sns_topic.cloudopslab_alerts.arn} --message "Test alert from CloudOpsLab"
  
  EOT
}

# Configuration for CloudOpsLab Scripts
output "cloudopslab_config" {
  description = "Configuration values for CloudOpsLab Python scripts"
  value = {
    aws_region           = data.aws_region.current.name
    s3_bucket           = aws_s3_bucket.cloudopslab_data.id
    sns_topic_arn       = aws_sns_topic.cloudopslab_alerts.arn
    log_group_name      = aws_cloudwatch_log_group.cloudopslab.name
    cloudwatch_namespace = var.cloudwatch_namespace
    environment         = var.environment
  }
  sensitive = false
}

# Environment Variables Export
output "export_environment_variables" {
  description = "Commands to export environment variables for CloudOpsLab scripts"
  value = <<-EOT
  
  # Copy and paste these into your terminal:
  export AWS_REGION="${data.aws_region.current.name}"
  export CLOUDOPSLAB_ENV="${var.environment}"
  export CLOUDOPSLAB_S3_BUCKET="${aws_s3_bucket.cloudopslab_data.id}"
  export CLOUDOPSLAB_SNS_TOPIC="${aws_sns_topic.cloudopslab_alerts.arn}"
  export CLOUDOPSLAB_LOG_GROUP="${aws_cloudwatch_log_group.cloudopslab.name}"
  export CLOUDWATCH_NAMESPACE="${var.cloudwatch_namespace}"
  
  EOT
}
