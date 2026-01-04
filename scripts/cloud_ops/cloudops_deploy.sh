#!/bin/bash
# Quick deployment script for AWS Secure Lab

set -e

echo "=========================================="
echo "AWS Secure Lab - Quick Deploy"
echo "=========================================="
echo ""

cd "$(dirname "$0")/../terraform"

# Check if terraform.tfvars exists
if [ ! -f terraform.tfvars ]; then
    echo "? terraform.tfvars not found!"
    echo ""
    echo "Creating from template..."
    cp terraform.tfvars.example terraform.tfvars
    echo ""
    echo "??  Please edit terraform.tfvars with your values:"
    echo "   - my_ip_address (run: curl ifconfig.me)"
    echo "   - key_pair_name"
    echo ""
    echo "Then run this script again."
    exit 1
fi

echo "Step 1: Initializing Terraform..."
terraform init

echo ""
echo "Step 2: Validating configuration..."
terraform validate

echo ""
echo "Step 3: Planning deployment..."
terraform plan

echo ""
echo "=========================================="
read -p "Deploy infrastructure? (yes/no): " confirm

if [ "$confirm" = "yes" ]; then
    echo ""
    echo "Step 4: Deploying..."
    terraform apply -auto-approve
    
    echo ""
    echo "=========================================="
    echo "? Deployment complete!"
    echo "=========================================="
    terraform output
else
    echo "Deployment cancelled."
fi
