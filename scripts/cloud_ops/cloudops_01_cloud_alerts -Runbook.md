# cloudops_01_cloud_alerts — Runbook

## Overview
This script monitors cloud resources for operational or security alerts and sends notifications to configured endpoints. It acts as an early‑warning system for Cloud Support teams.

## When to Use
- Detecting abnormal cloud activity
- Monitoring for cost spikes, security events, or service degradation
- Integrating alerts into Slack, email, SNS, or ticketing systems

## Prerequisites
- Python 3.8+
- AWS CLI configured (`aws configure` or environment variables)
- IAM permissions: `cloudwatch:Describe*`, `sns:Publish`, `logs:GetLogEvents`

## Usage
### Basic Run