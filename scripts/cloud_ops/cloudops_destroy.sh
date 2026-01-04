#!/bin/bash
# Safe cleanup script for AWS Secure Lab

set -e

echo "=========================================="
echo "AWS Secure Lab - Destroy Infrastructure"
echo "=========================================="
echo ""

cd "$(dirname "$0")/../terraform"

echo "??  WARNING: This will destroy all infrastructure!"
echo ""
read -p "Are you sure? Type 'yes' to continue: " confirm

if [ "$confirm" != "yes" ]; then
    echo "Cancelled."
    exit 0
fi

echo ""
echo "Step 1: Emptying S3 buckets..."

# Get bucket names
MAIN_BUCKET=$(terraform output -raw s3_bucket_name 2>/dev/null || echo "")
LOGS_BUCKET=$(terraform output -raw s3_logs_bucket_name 2>/dev/null || echo "")

if [ -n "$MAIN_BUCKET" ]; then
    echo "Emptying $MAIN_BUCKET..."
    aws s3 rm s3://$MAIN_BUCKET --recursive 2>/dev/null || true
fi

if [ -n "$LOGS_BUCKET" ]; then
    echo "Emptying $LOGS_BUCKET..."
    aws s3 rm s3://$LOGS_BUCKET --recursive 2>/dev/null || true
fi

echo ""
echo "Step 2: Destroying infrastructure..."
terraform destroy

echo ""
echo "? Cleanup complete!"
