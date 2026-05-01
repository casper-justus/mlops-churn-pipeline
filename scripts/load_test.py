#!/usr/bin/env python3
"""Load test for Churn Prediction API using only stdlib."""

import subprocess
import time
import json
import statistics
import concurrent.futures
import argparse
from datetime import datetime
from urllib.request import urlopen, Request
from urllib.error import URLError
import os

BASE_URL = os.environ.get("API_URL", "http://localhost:8000")

CUSTOMERS = [
    {"gender": "Male", "SeniorCitizen": 0, "Partner": "Yes", "Dependents": "No", "tenure": 12, "PhoneService": "Yes", "MultipleLines": "No", "InternetService": "DSL", "OnlineSecurity": "Yes", "OnlineBackup": "No", "DeviceProtection": "Yes", "TechSupport": "No", "StreamingTV": "No", "StreamingMovies": "No", "Contract": "Month-to-month", "PaperlessBilling": "Yes", "PaymentMethod": "Electronic check", "MonthlyCharges": 65.50, "TotalCharges": 786.00},
    {"gender": "Female", "SeniorCitizen": 1, "Partner": "No", "Dependents": "No", "tenure": 1, "PhoneService": "Yes", "MultipleLines": "Yes", "InternetService": "Fiber optic", "OnlineSecurity": "No", "OnlineBackup": "No", "DeviceProtection": "No", "TechSupport": "No", "StreamingTV": "Yes", "StreamingMovies": "Yes", "Contract": "Month-to-month", "PaperlessBilling": "Yes", "PaymentMethod": "Electronic check", "MonthlyCharges": 100.75, "TotalCharges": 100.75},
    {"gender": "Male", "SeniorCitizen": 0, "Partner": "Yes", "Dependents": "Yes", "tenure": 48, "PhoneService": "Yes", "MultipleLines": "Yes", "InternetService": "Fiber optic", "OnlineSecurity": "Yes", "OnlineBackup": "Yes", "DeviceProtection": "Yes", "TechSupport": "Yes", "StreamingTV": "Yes", "StreamingMovies": "Yes", "Contract": "Two year", "PaperlessBilling": "No", "PaymentMethod": "Bank transfer (automatic)", "MonthlyCharges": 85.30, "TotalCharges": 4094.40},
    {"gender": "Female", "SeniorCitizen": 0, "Partner": "No", "Dependents": "No", "tenure": 24, "PhoneService": "Yes", "MultipleLines": "No", "InternetService": "DSL", "OnlineSecurity": "No", "OnlineBackup": "Yes", "DeviceProtection": "No", "TechSupport": "Yes", "StreamingTV": "No", "StreamingMovies": "No", "Contract": "One year", "PaperlessBilling": "Yes", "PaymentMethod": "Credit card (automatic)", "MonthlyCharges": 55.20, "TotalCharges": 1324.80},
    {"gender": "Male", "SeniorCitizen": 1, "Partner": "No", "Dependents": "No", "tenure": 3, "PhoneService": "No", "MultipleLines": "No phone service", "InternetService": "No", "OnlineSecurity": "No internet service", "OnlineBackup": "No internet service", "DeviceProtection": "No internet service", "TechSupport": "No internet service", "StreamingTV": "No internet service", "StreamingMovies": "No internet service", "Contract": "Month-to-month", "PaperlessBilling": "No", "PaymentMethod": "Mailed check", "MonthlyCharges": 20.15, "TotalCharges": 60.45},
]


def make_request(customer):
    data = json.dumps(customer).encode()
    req = Request(f"{BASE_URL}/predict", data=data, headers={"Content-Type": "application/json"})
    start = time.time()
    try:
        resp = urlopen(req, timeout=10)
        resp.read()
        elapsed_ms = (time.time() - start) * 1000
        return {"status": resp.status, "time_ms": elapsed_ms, "success": True}
    except URLError as e:
        elapsed_ms = (time.time() - start) * 1000
        return {"status": 0, "time_ms": elapsed_ms, "success": False, "error": str(e)}


def run_load_test(concurrent_users, total_requests):
    print(f"Starting load test: {total_requests} requests, {concurrent_users} concurrent users")
    results = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrent_users) as executor:
        futures = []
        for i in range(total_requests):
            customer = CUSTOMERS[i % len(CUSTOMERS)]
            futures.append(executor.submit(make_request, customer))

        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())

    successful = [r for r in results if r["success"]]
    failed = [r for r in results if not r["success"]]
    times = [r["time_ms"] for r in successful]

    if not times:
        print("All requests failed!")
        return None

    sorted_times = sorted(times)
    duration = max(r["time_ms"] for r in results) / 1000
    rps = len(successful) / duration if duration > 0 else 0

    return {
        "total": len(results),
        "successful": len(successful),
        "failed": len(failed),
        "failure_rate": len(failed) / len(results) * 100,
        "avg_ms": statistics.mean(times),
        "median_ms": statistics.median(times),
        "p95_ms": sorted_times[int(len(sorted_times) * 0.95)],
        "p99_ms": sorted_times[int(len(sorted_times) * 0.99)],
        "min_ms": min(times),
        "max_ms": max(times),
        "rps": rps,
        "duration_s": duration,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--users", type=int, default=50, help="Concurrent users")
    parser.add_argument("--requests", type=int, default=500, help="Total requests")
    args = parser.parse_args()

    print(f"\nAPI URL: {BASE_URL}")
    stats = run_load_test(args.users, args.requests)

    if stats:
        print(f"""
{'='*50}
  LOAD TEST SUMMARY
{'='*50}
Total Requests:    {stats['total']}
Successful:        {stats['successful']}
Failed:            {stats['failed']}
Failure Rate:      {stats['failure_rate']:.1f}%
Avg Response Time: {stats['avg_ms']:.0f}ms
Median:            {stats['median_ms']:.0f}ms
P95:               {stats['p95_ms']:.0f}ms
P99:               {stats['p99_ms']:.0f}ms
Min:               {stats['min_ms']:.0f}ms
Max:               {stats['max_ms']:.0f}ms
Throughput:        {stats['rps']:.1f} req/s
Duration:          {stats['duration_s']:.1f}s
{'='*50}
""")

        os.makedirs("load_test_results", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        with open(f"load_test_results/summary_{timestamp}.json", "w") as f:
            json.dump(stats, f, indent=2)
        print(f"Results saved to load_test_results/summary_{timestamp}.json")
