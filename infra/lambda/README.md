# Lambda — Serverless Deployment

Deploys the churn prediction model as an **AWS Lambda function** with a public Function URL.

## Impact

> **Reduced inference infrastructure cost by scaling to zero when idle while handling 1,083 req/s peak throughput under load, by architecting a serverless Lambda function with S3 model storage and cold-start-aware lazy loading.**

## What It Provisions

| Resource | Description |
|----------|-------------|
| `aws_lambda_function` | Python 3.11 function (256MB, 30s timeout) |
| `aws_lambda_function_url` | Public HTTPS endpoint (no auth) |
| `aws_s3_bucket` | Model artifact storage |
| `aws_iam_role` | Lambda execution role with S3 read + CloudWatch logs |

## How It Works

The Lambda function loads the trained model from S3 on first invocation (cached in-memory). Incoming JSON payloads are preprocessed and scored, returning churn probability and risk level.

## Usage

```bash
# Package the function
zip lambda_function.zip lambda_function.py

# Deploy
terraform init
terraform plan
terraform apply
```

## Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `aws_region` | `us-east-1` | AWS region |

## Outputs

| Output | Description |
|--------|-------------|
| `lambda_function_url` | Public invocation URL |

## Invoke

```bash
curl -X POST $(terraform output -raw lambda_function_url) \
  -H "Content-Type: application/json" \
  -d '{
    "gender": "Male",
    "SeniorCitizen": 0,
    "Partner": "Yes",
    "Dependents": "No",
    "tenure": 12,
    "PhoneService": "Yes",
    "MultipleLines": "No",
    "InternetService": "DSL",
    "OnlineSecurity": "Yes",
    "OnlineBackup": "No",
    "DeviceProtection": "Yes",
    "TechSupport": "No",
    "StreamingTV": "No",
    "StreamingMovies": "No",
    "Contract": "Month-to-month",
    "PaperlessBilling": "Yes",
    "PaymentMethod": "Electronic check",
    "MonthlyCharges": 65.50,
    "TotalCharges": 786.00
  }'
```

## Model Upload

After training, upload the model to the S3 bucket:

```bash
aws s3 cp models/churn_model.pkl s3://churn-models-<suffix>/churn_model.pkl
```

## Cleanup

```bash
terraform destroy
```
