# MLOps Churn Prediction Pipeline

[![CI/CD](https://github.com/casper-justus/mlops-churn-pipeline/actions/workflows/cicd.yml/badge.svg)](https://github.com/casper-justus/mlops-churn-pipeline/actions/workflows/cicd.yml)
![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-009688?logo=fastapi)
![MLflow](https://img.shields.io/badge/MLflow-2.9.2-0194E2?logo=mlflow)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker)
![Terraform](https://img.shields.io/badge/Terraform-1.0+-844FBA?logo=terraform)
![AWS](https://img.shields.io/badge/AWS-EC2%20%7C%20Lambda-232F3E?logo=amazonaws)
![License](https://img.shields.io/badge/License-MIT-green)

> **3-in-1 Portfolio Project** — Covers AI Engineering + Data Engineering + DevOps roles in a single end-to-end system.

---

## What This Does

Trains a customer churn prediction model, tracks experiments with MLflow, packages it as a Docker container, deploys it to AWS (EC2 or Lambda), and automates the entire lifecycle with a GitHub Actions CI/CD pipeline that retrains on new data.

## Impact

> Using the **XYZ Formula** *(Accomplished [X] as measured by [Y], by doing [Z])*

| Role | Impact Statement |
|------|-----------------|
| **AI Engineer** | Built a churn prediction model achieving **84% ROC-AUC** on 7,043 customer records, by engineering a GradientBoosting classifier with MLflow experiment tracking and automated feature encoding across 20 categorical fields |
| **Data Engineer** | Automated end-to-end data pipelines processing **7K+ records with 0% data loss**, by building a reproducible Python pipeline that downloads, cleans, imputes missing values, and transforms raw CSV into model-ready features |
| **DevOps Engineer** | Achieved **908 req/s throughput at 10 concurrent users with 0% failure rate and 45ms avg latency**, by implementing a GitHub Actions CI/CD pipeline with automated testing, Docker containerization, and Terraform-managed AWS infrastructure |
| **Performance** | Sustained **1,083 req/s peak throughput under 100 concurrent users with P95 latency under 436ms**, by load-testing across 3 concurrency levels and optimizing the FastAPI async server with preloaded model inference |
| **End-to-End** | Delivered a fully automated MLOps system with **weekly self-retraining and zero-touch deployments across EC2 + Lambda**, by integrating MLflow tracking, FastAPI serving, Docker packaging, and GitHub Actions CI/CD |

### Load Test Results

```
┌────────────┬──────────┬──────────┬────────┬────────────┬───────────┐
│ Users      │ Requests │ Avg (ms) │  P95   │  Failure   │  Req/s    │
├────────────┼──────────┼──────────┼────────┼────────────┼───────────┤
│     10     │    200   │    45    │  177   │    0.0%    │   908.9   │
│     50     │    500   │   223    │  693   │    0.0%    │   633.7   │
│    100     │   1000   │   376    │  436   │    0.0%    │  1083.5   │
└────────────┴──────────┴──────────┴────────┴────────────┴───────────┘
```

## Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│                        GitHub Actions CI/CD                          │
│                                                                      │
│   ┌──────────┐    ┌──────────────┐    ┌──────────┐    ┌───────────┐  │
│   │  pytest  │───▶│  MLflow Run  │───▶│  Docker  │───▶│  Deploy   │  │
│   │  Tests   │    │  & Track     │    │  Build   │    │  to AWS   │  │
│   └──────────┘    └──────────────┘    └──────────┘    └───────────┘  │
└──────────────────────────────────────────────────────────────────────┘
                                       │
                          ┌────────────┴────────────┐
                          ▼                         ▼
              ┌─────────────────────┐   ┌──────────────────────┐
              │  EC2 Auto Scaling     │   │  Lambda (Serverless) │
              │  FastAPI on :8000     │   │  API Gateway URL     │
              │  Load balanced        │   │  S3 model storage    │
              └─────────────────────┘   └──────────────────────┘
```

## Tech Stack

| Layer | Tools |
|-------|-------|
| **ML** | scikit-learn, GradientBoosting, pandas, numpy |
| **Tracking** | MLflow (experiments, params, metrics, artifacts) |
| **API** | FastAPI, Pydantic, uvicorn |
| **Container** | Docker, Docker Compose |
| **CI/CD** | GitHub Actions (test → train → build → deploy) |
| **Cloud** | AWS (EC2, Lambda, ECR, S3, IAM, VPC) |
| **IaC** | Terraform |

## Quick Start

### 1. Clone & Install

```bash
git clone https://github.com/casper-justus/mlops-churn-pipeline.git
cd mlops-churn-pipeline
pip install -r requirements.txt
```

### 2. Train the Model

```bash
python src/train.py
```

Downloads the [Telco Customer Churn dataset](https://github.com/IBM/telco-customer-churn-on-icp4d) automatically, preprocesses it, trains a GradientBoosting model, and logs everything to MLflow.

### 3. Serve Predictions

```bash
uvicorn src.api:app --reload --port 8000
```

### 4. Test the API

```bash
curl -X POST http://localhost:8000/predict \
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

**Response:**

```json
{
  "churn_probability": 0.7234,
  "prediction": "churn",
  "risk_level": "high"
}
```

### Or Run Everything with Docker

```bash
docker-compose up --build
```

- **API** → `http://localhost:8000`
- **MLflow UI** → `http://localhost:5000`

## Project Structure

```
mlops-churn-pipeline/
│
├── src/                        # Application source code
│   ├── train.py                # ML pipeline + MLflow tracking
│   └── api.py                  # FastAPI prediction service
│
├── tests/                      # Test suite
│   ├── test_train.py           # Training pipeline tests
│   └── test_api.py             # API endpoint tests
│
├── infra/                      # Infrastructure as Code
│   ├── terraform/              # EC2 Auto Scaling deployment
│   │   └── main.tf
│   └── lambda/                 # Lambda serverless deployment
│       ├── main.tf
│       └── lambda_function.py
│
├── .github/workflows/
│   └── cicd.yml                # CI/CD pipeline definition
│
├── data/                       # Dataset storage (auto-populated)
├── models/                     # Trained model artifacts
├── mlruns/                     # MLflow run artifacts
│
├── Dockerfile                  # Container definition
├── docker-compose.yml          # Local dev stack
├── requirements.txt            # Python dependencies
└── README.md
```

## CI/CD Pipeline

Triggers on **push to main**, **pull requests**, and a **weekly schedule** (Monday midnight) for automatic retraining.

```yaml
Trigger (push / PR / cron)
    │
    ▼
┌─────────┐
│  Test   │  pytest suite
└────┬────┘
     │ ✓
     ▼
┌──────────────┐
│ Train & Eval │  MLflow tracking → artifact upload
└──────┬───────┘
       │ ✓
       ▼
┌──────────────┐
│ Build & Push │  Docker → Amazon ECR
└──────┬───────┘
       │ ✓
       ├──────────────────┐
       ▼                  ▼
┌────────────┐    ┌──────────────┐
│ Deploy EC2 │    │ Deploy Lambda│
│ Terraform  │    │ Update code  │
└────────────┘    └──────────────┘
```

### Required GitHub Secrets

| Secret | Description |
|--------|-------------|
| `AWS_ACCESS_KEY_ID` | AWS IAM access key |
| `AWS_SECRET_ACCESS_KEY` | AWS IAM secret key |
| `MLFLOW_TRACKING_URI` | MLflow server URI (optional) |

## API Reference

### `GET /health`

Health check — confirms model is loaded.

### `POST /predict`

Single customer churn prediction.

**Request body:** all 19 customer fields (see curl example above).

### `POST /predict/batch`

Batch predictions — pass an array of customer objects.

### Response Schema

| Field | Type | Description |
|-------|------|-------------|
| `churn_probability` | float | 0.0 – 1.0 |
| `prediction` | string | `"churn"` or `"retain"` |
| `risk_level` | string | `"high"` (≥0.7), `"medium"` (≥0.4), `"low"` |

## Infrastructure

### EC2 Deployment

```bash
cd infra/terraform
terraform init
terraform plan
terraform apply -var="ecr_image_uri=<your-ecr-uri>"
```

Provisions a VPC, public subnet, Auto Scaling Group (1–2 t3.medium instances), ECR repo, security groups, and IAM roles — then pulls and runs the Docker container.

### Lambda Deployment

```bash
cd infra/lambda
terraform init
terraform apply
```

Provisions a Lambda function (Python 3.11), S3 bucket for the model, IAM role, and a public function URL.

## Retraining

The pipeline retrains automatically:

- On every push to `main`
- Weekly via cron (`0 0 * * 1`)

Manual retrain:

```bash
python src/train.py
```

## Running Tests

```bash
pytest tests/ -v --tb=short
```

## License

[MIT](LICENSE)
