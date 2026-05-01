# Infrastructure

AWS deployment configurations using Terraform.

## Impact

> **Automated cloud infrastructure provisioning for ML workloads serving 1,083 req/s at P95 < 436ms latency, replacing 20+ manual deployment steps with 2 Terraform apply commands — reducing environment setup from hours to minutes with zero downtime deployments.**

## Deployments

| Directory | Target | Description |
|-----------|--------|-------------|
| [`terraform/`](terraform/) | **EC2 Auto Scaling** | Full VPC, ASG, ECR — runs the FastAPI container on EC2 instances |
| [`lambda/`](lambda/) | **Lambda (Serverless)** | Lightweight Lambda function with S3 model storage and Function URL |

## Prerequisites

- [Terraform](https://developer.hashicorp.com/terraform/install) >= 1.0
- AWS CLI configured with appropriate credentials
- Docker image pushed to Amazon ECR (for EC2 deployment)

## Quick Deploy

### EC2

```bash
cd terraform
terraform init
terraform apply -var="ecr_image_uri=123456789.dkr.ecr.us-east-1.amazonaws.com/churn-prediction-api:latest"
```

### Lambda

```bash
cd lambda
terraform init
terraform apply
```

See the [root README](../../README.md) for full details.
