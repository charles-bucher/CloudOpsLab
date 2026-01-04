#!/usr/bin/env bash
set -e

echo "🔎 Running CloudOpsLab sanity checks"

python scripts/verify_aws_environment.py
python scripts/cost_snapshot.py
python scripts/find_idle_ec2.py
python scripts/security_group_exposure_scan.py

echo "✅ All checks completed"
