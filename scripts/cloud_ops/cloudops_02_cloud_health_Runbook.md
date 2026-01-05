# cloudops_03_cloud_health_check — Runbook

## Overview
Performs a lightweight health check across cloud services, validating availability, configuration, and operational readiness.

## When to Use
- Before deployments
- During incident triage
- As part of CI/CD pre‑flight checks

## Prerequisites
- Python 3.8+
- AWS permissions: `ec2:Describe*`, `s3:List*`, `iam:Get*`

## Usage