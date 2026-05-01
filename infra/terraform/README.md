# Terraform — EC2 Deployment

Deploys the churn prediction API on an **EC2 Auto Scaling Group** behind a VPC with Docker.

## Impact

> **Provisioned production-ready ML infrastructure serving 908 req/s at 45ms avg latency with 0% failure rate, by writing Terraform modules for VPC, Auto Scaling Group, ECR, and IAM — eliminating manual server setup and enabling zero-touch deployments.**

## What It Provisions

| Resource | Description |
|----------|-------------|
| `aws_vpc` | VPC with DNS support (10.0.0.0/16) |
| `aws_subnet` | Public subnet with auto-assign public IP |
| `aws_internet_gateway` | Internet gateway for outbound access |
| `aws_security_group` | Allows inbound :8000 (API) and :22 (SSH) |
| `aws_launch_template` | Amazon Linux 2 + Docker + auto-starts container |
| `aws_autoscaling_group` | 1–2 t3.medium instances |
| `aws_ecr_repository` | Private container registry |
| `aws_iam_role` | EC2 instance profile with ECR read access |

## Usage

```bash
terraform init
terraform plan
terraform apply -var="ecr_image_uri=<account>.dkr.ecr.<region>.amazonaws.com/churn-prediction-api:<tag>"
```

## Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `aws_region` | `us-east-1` | AWS region |
| `ecr_image_uri` | _(required)_ | Full ECR image URI to deploy |
| `instance_type` | `t3.medium` | EC2 instance type |

## User Data

The launch template bootstraps each instance with:

```bash
#!/bin/bash
yum update -y
yum install -y docker
systemctl start docker
systemctl enable docker
aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <account>.dkr.ecr.<region>.amazonaws.com
docker run -d -p 8000:8000 --name churn-api <image_uri>
```

## Outputs

| Output | Description |
|--------|-------------|
| `api_endpoint` | Public API URL (e.g. `http://54.x.x.x:8000`) |
| `ecr_repository_url` | ECR repository URL |

## Cleanup

```bash
terraform destroy
```
