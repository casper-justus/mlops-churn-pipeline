# Contributing

Thank you for your interest in contributing! Contributions are welcome in the form of bug reports, model improvements, pipeline enhancements, and documentation fixes.

## Getting Started

1. **Fork** the repository and create a new branch from `main`:
   ```bash
   git checkout -b feat/your-feature-name
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and configure your MLflow tracking URI and AWS credentials.
4. Open a **Pull Request** against `main` with a clear description of what changed and why.

## What You Can Contribute

- 🧠 **Model improvements** — new algorithms, hyperparameter tuning, feature engineering
- 🔄 **Pipeline enhancements** — better data preprocessing, retraining triggers, drift detection
- ☁️ **AWS deployment** — SageMaker integration, Lambda inference, ECS improvements
- 📊 **Experiment tracking** — better MLflow logging, model registry usage, artifact management
- 📚 **Documentation** — pipeline diagrams, model cards, deployment guides

## Pull Request Guidelines

- Keep PRs focused — one change per PR
- Use clear commit messages (e.g. `feat: add XGBoost model variant`)
- Log all experiments to MLflow before submitting model changes
- Never commit AWS credentials or `.env` files

## Reporting Issues

When reporting a bug, please include:
- The pipeline stage where the failure occurred
- Relevant error messages or MLflow run IDs
- Your Python version and relevant package versions

## Code of Conduct

Be respectful and constructive. Everyone is welcome regardless of experience level.
