# Cloudopslab

## ☁️ AWS Services Used

- **CloudWatch**: Monitoring, logging, and alerting
- **DynamoDB**: NoSQL database for scalable data storage
- **EC2**: Compute instances for hosting applications
- **IAM**: Identity and access management
- **Lambda**: Serverless functions for event-driven processing
- **RDS**: Managed relational database service
- **S3**: Object storage for data and artifacts
- **VPC**: Network isolation and security

## 💡 Skills Demonstrated

- **AWS Service Configuration**: Hands-on experience with core AWS services
- **Infrastructure as Code**: Automated provisioning and management
- **Troubleshooting**: Systematic problem diagnosis and resolution
- **Documentation**: Clear technical writing and process documentation
- **Monitoring & Logging**: Proactive system observation
- **Security Best Practices**: IAM policies and least-privilege access
## 📦 Prerequisites

- AWS Account with appropriate permissions
- AWS CLI configured (`aws configure`)
- Python 3.8+ installed
- boto3 library (`pip install boto3`)
- Terraform or AWS CloudFormation CLI

## 📖 Usage

### Running Scripts

```bash
python3 commit_autofixer.py
python3 EC2_Start_Stop_Scheduler.py
python3 portfolio_master_auto.py
```

### Testing Components

1. Verify AWS connectivity: `aws sts get-caller-identity`
2. Check resource provisioning in AWS Console
3. Review CloudWatch logs for any errors

## 🔧 Troubleshooting

### Common Issues

**Issue**: AWS credentials not configured
- **Solution**: Run `aws configure` and enter valid credentials

**Issue**: Permission denied errors
- **Solution**: Verify IAM user has required permissions
- Check IAM policy allows actions for services used

**Issue**: EC2 instance not reachable
- **Solution**: Check security group rules allow inbound traffic
- Verify instance is in 'running' state

**Issue**: S3 access denied
- **Solution**: Check bucket policy and IAM permissions
- Verify bucket exists in correct region

**Issue**: Rate limiting or throttling
- **Solution**: Implement exponential backoff
- Check service quotas in AWS Console

## 📁 Project Structure

```
CloudOpsLab/
├── README.md
├── infrastructure/
│   ├── main.tf or template.yaml
│   └── variables.tf
├── scripts/
│   ├── commit_autofixer.py
│   ├── EC2_Start_Stop_Scheduler.py
│   └── portfolio_master_auto.py
├── monitoring/
│   └── cloudwatch_config.yaml
└── docs/
    └── architecture.md
```

## 📊 Monitoring & Logging

This project includes monitoring capabilities:

- **CloudWatch Metrics**: Track resource utilization
- **CloudWatch Alarms**: Alert on threshold breaches
- **CloudWatch Logs**: Centralized application logging

### Setting Up Monitoring

```bash
# Create CloudWatch alarm
aws cloudwatch put-metric-alarm \
  --alarm-name HighCPU \
  --alarm-description 'Alert when CPU exceeds 80%' \
  --metric-name CPUUtilization \
  --threshold 80
```

## 🔮 Future Enhancements

- Implement CI/CD pipeline with AWS CodePipeline
- Add automated testing and validation
- Expand to multi-region deployment
## 👤 Author

**Charles Bucher**
- GitHub: [@Charles-Bucher](https://github.com/Charles-Bucher)
- LinkedIn: [Charles Bucher](https://linkedin.com/in/charles-bucher-cloud)
- Transitioning to Cloud/DevOps | AWS Focused

## 📄 License

This project is open source and available for educational purposes.
