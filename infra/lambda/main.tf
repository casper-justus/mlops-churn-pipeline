terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

variable "aws_region" {
  default = "us-east-1"
}

resource "aws_iam_role" "lambda_role" {
  name = "churn-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy" "lambda_s3" {
  name = "churn-lambda-s3-policy"
  role = aws_iam_role.lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:ListBucket",
        ]
        Resource = [
          "arn:aws:s3:::churn-models",
          "arn:aws:s3:::churn-models/*",
        ]
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_s3_bucket" "models" {
  bucket = "churn-models-${random_id.suffix.hex}"

  tags = {
    Name = "churn-models"
  }
}

resource "random_id" "suffix" {
  byte_length = 4
}

resource "aws_lambda_function" "churn_predictor" {
  filename         = "lambda_function.zip"
  function_name    = "churn-predictor"
  role             = aws_iam_role.lambda_role.arn
  handler          = "lambda_function.lambda_handler"
  runtime          = "python3.11"
  timeout          = 30
  memory_size      = 256

  environment {
    variables = {
      MODEL_BUCKET = aws_s3_bucket.models.id
      MODEL_KEY    = "churn_model.pkl"
    }
  }

  tags = {
    Name = "churn-predictor"
  }
}

resource "aws_lambda_function_url" "churn_predictor" {
  function_name      = aws_lambda_function.churn_predictor.function_name
  authorization_type = "NONE"
}

output "lambda_function_url" {
  value = aws_lambda_function_url.churn_predictor.function_url
}
