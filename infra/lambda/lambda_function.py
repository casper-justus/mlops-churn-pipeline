import json
import joblib
import os
import pandas as pd
import boto3
from io import BytesIO

CATEGORICAL_ENCODINGS = {
    "gender": {"Male": 0, "Female": 1},
    "Partner": {"No": 0, "Yes": 1},
    "Dependents": {"No": 0, "Yes": 1},
    "PhoneService": {"No": 0, "Yes": 1},
    "MultipleLines": {"No phone service": 0, "No": 1, "Yes": 2},
    "InternetService": {"No": 0, "DSL": 1, "Fiber optic": 2},
    "OnlineSecurity": {"No internet service": 0, "No": 1, "Yes": 2},
    "OnlineBackup": {"No internet service": 0, "No": 1, "Yes": 2},
    "DeviceProtection": {"No internet service": 0, "No": 1, "Yes": 2},
    "TechSupport": {"No internet service": 0, "No": 1, "Yes": 2},
    "StreamingTV": {"No internet service": 0, "No": 1, "Yes": 2},
    "StreamingMovies": {"No internet service": 0, "No": 1, "Yes": 2},
    "Contract": {"Month-to-month": 0, "One year": 1, "Two year": 2},
    "PaperlessBilling": {"No": 0, "Yes": 1},
    "PaymentMethod": {
        "Electronic check": 0,
        "Mailed check": 1,
        "Bank transfer (automatic)": 2,
        "Credit card (automatic)": 3,
    },
}

FEATURE_COLUMNS = [
    "gender", "SeniorCitizen", "Partner", "Dependents", "tenure",
    "PhoneService", "MultipleLines", "InternetService", "OnlineSecurity",
    "OnlineBackup", "DeviceProtection", "TechSupport", "StreamingTV",
    "StreamingMovies", "Contract", "PaperlessBilling", "PaymentMethod",
    "MonthlyCharges", "TotalCharges",
]

model = None


def get_model():
    global model
    if model is None:
        s3 = boto3.client("s3")
        bucket = os.environ.get("MODEL_BUCKET", "churn-models")
        key = os.environ.get("MODEL_KEY", "churn_model.pkl")
        response = s3.get_object(Bucket=bucket, Key=key)
        model = joblib.load(BytesIO(response["Body"].read()))
    return model


def encode_input(data: dict) -> pd.DataFrame:
    encoded = {}
    for col, value in data.items():
        if col in CATEGORICAL_ENCODINGS:
            encoded[col] = CATEGORICAL_ENCODINGS[col].get(value, 0)
        else:
            encoded[col] = value
    return pd.DataFrame([encoded])[FEATURE_COLUMNS]


def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body", "{}"))

        model = get_model()
        X = encode_input(body)
        proba = model.predict_proba(X)[0][1]
        prediction = int(proba >= 0.5)
        risk = "high" if proba >= 0.7 else "medium" if proba >= 0.4 else "low"

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "churn_probability": round(float(proba), 4),
                "prediction": "churn" if prediction == 1 else "retain",
                "risk_level": risk,
            }),
        }
    except Exception as e:
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": str(e)}),
        }
