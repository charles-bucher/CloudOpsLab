# CloudOpsLab Infrastructure
# Main Terraform configuration

terraform {
  required_version = ">= 1.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = "CloudOpsLab"
      ManagedBy   = "Terraform"
      Environment = var.environment
      Owner       = var.owner_email
    }
  }
}

# Data sources
data "aws_caller_identity" "current" {}
data "aws_region" "current" {}

# Local variables
locals {
  account_id = data.aws_caller_identity.current.account_id
  region     = data.aws_region.current.name
  
  common_tags = {
    Project     = "CloudOpsLab"
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
  
  cloudwatch_namespace = var.cloudwatch_namespace
}

# CloudWatch Log Groups
resource "aws_cloudwatch_log_group" "cloudopslab" {
  name              = "/cloudopslab/${var.environment}"
  retention_in_days = var.log_retention_days

  tags = merge(local.common_tags, {
    Name = "cloudopslab-logs"
  })
}

resource "aws_cloudwatch_log_group" "lambda_logs" {
  name              = "/aws/lambda/cloudopslab-${var.environment}"
  retention_in_days = var.log_retention_days

  tags = merge(local.common_tags, {
    Name = "cloudopslab-lambda-logs"
  })
}

# SNS Topic for Alerts
resource "aws_sns_topic" "cloudopslab_alerts" {
  name              = "cloudopslab-${var.environment}-alerts"
  display_name      = "CloudOpsLab Alerts"
  kms_master_key_id = aws_kms_key.cloudopslab.id

  tags = merge(local.common_tags, {
    Name = "cloudopslab-alerts"
  })
}

resource "aws_sns_topic_subscription" "email_alerts" {
  for_each = toset(var.alert_email_addresses)
  
  topic_arn = aws_sns_topic.cloudopslab_alerts.arn
  protocol  = "email"
  endpoint  = each.value
}

# KMS Key for Encryption
resource "aws_kms_key" "cloudopslab" {
  description             = "CloudOpsLab encryption key"
  deletion_window_in_days = 10
  enable_key_rotation     = true

  tags = merge(local.common_tags, {
    Name = "cloudopslab-kms"
  })
}

resource "aws_kms_alias" "cloudopslab" {
  name          = "alias/cloudopslab-${var.environment}"
  target_key_id = aws_kms_key.cloudopslab.key_id
}

# S3 Bucket for Logs and Backups
resource "aws_s3_bucket" "cloudopslab_data" {
  bucket = "cloudopslab-${var.environment}-${local.account_id}"

  tags = merge(local.common_tags, {
    Name = "cloudopslab-data"
  })
}

resource "aws_s3_bucket_versioning" "cloudopslab_data" {
  bucket = aws_s3_bucket.cloudopslab_data.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "cloudopslab_data" {
  bucket = aws_s3_bucket.cloudopslab_data.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "aws:kms"
      kms_master_key_id = aws_kms_key.cloudopslab.arn
    }
  }
}

resource "aws_s3_bucket_public_access_block" "cloudopslab_data" {
  bucket = aws_s3_bucket.cloudopslab_data.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_lifecycle_configuration" "cloudopslab_data" {
  bucket = aws_s3_bucket.cloudopslab_data.id

  rule {
    id     = "logs-lifecycle"
    status = "Enabled"

    filter {
      prefix = "logs/"
    }

    transition {
      days          = 90
      storage_class = "GLACIER"
    }

    expiration {
      days = 365
    }
  }

  rule {
    id     = "backups-lifecycle"
    status = "Enabled"

    filter {
      prefix = "backups/"
    }

    transition {
      days          = 30
      storage_class = "STANDARD_IA"
    }

    expiration {
      days = 90
    }
  }
}

# Import module configurations
module "cloudwatch" {
  source = "./modules/cloudwatch"

  environment          = var.environment
  cloudwatch_namespace = local.cloudwatch_namespace
  sns_topic_arn        = aws_sns_topic.cloudopslab_alerts.arn
  log_group_name       = aws_cloudwatch_log_group.cloudopslab.name
  
  # Alarm thresholds
  cpu_threshold        = var.cpu_alarm_threshold
  memory_threshold     = var.memory_alarm_threshold
  disk_threshold       = var.disk_alarm_threshold
  
  common_tags = local.common_tags
}

module "eventbridge" {
  source = "./modules/eventbridge"

  environment       = var.environment
  lambda_arns       = module.lambda.function_arns
  sns_topic_arn     = aws_sns_topic.cloudopslab_alerts.arn
  
  common_tags = local.common_tags
}

module "lambda" {
  source = "./modules/lambda"

  environment       = var.environment
  s3_bucket         = aws_s3_bucket.cloudopslab_data.id
  sns_topic_arn     = aws_sns_topic.cloudopslab_alerts.arn
  log_group_name    = aws_cloudwatch_log_group.lambda_logs.name
  
  common_tags = local.common_tags
}

module "iam" {
  source = "./modules/iam"

  environment    = var.environment
  s3_bucket_arn  = aws_s3_bucket.cloudopslab_data.arn
  sns_topic_arn  = aws_sns_topic.cloudopslab_alerts.arn
  kms_key_arn    = aws_kms_key.cloudopslab.arn
  
  common_tags = local.common_tags
}
