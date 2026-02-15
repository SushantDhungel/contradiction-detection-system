# backend

A project created with FastAPI CLI.

## Quick Start

### Start the development server

```bash
uv run fastapi dev
```

Visit <http://localhost:8000>

### Deploy to FastAPI Cloud

> FastAPI Cloud is currently in private beta. Join the waitlist at <https://fastapicloud.com>

```bash
uv run fastapi login
uv run fastapi deploy
```

## Project Structure

- `main.py` - Your FastAPI application
- `pyproject.toml` - Project dependencies

## Learn More

- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [FastAPI Cloud](https://fastapicloud.com)

## Healthcare Self-Report vs Metrics

Dataset:

Heart Disease UCI Dataset

On UCI Machine Learning Repository

Also mirrored on Kaggle

You simulate:

Patient-reported symptoms (text input)

Clinical features (cholesterol, BP, age)

Your AI detects mismatch risk.

## Tasks

### Backend (FastAPI)

Endpoints:

Upload text

Upload CSV

Return mismatch score

Return explanation

