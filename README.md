# TRACER — Fraud Detection ML Platform

Production-grade fraud detection system: FastAPI scoring API, gradient-boosted detector (XGBoost/LightGBM/CatBoost), graph-based AML mule detection (GraphSAGE), and red-team adversarial hardening.

## 24-Week Plan

| Phase | Weeks | Deliverable |
|-------|-------|-------------|
| 0 | Day 1–3 | Environment, tooling, repo, CI |
| 1 | W1–4 | FastAPI scoring API + MLflow + live demo |
| 2 | W5–8 | Detector, AUPRC >= 0.85 on UCI fraud |
| 3 | W9–12 | Kaggle IEEE-CIS top-10% notebook |
| 4 | W13–18 | GraphSAGE mule detection (Neo4j/DuckDB) |
| 5 | W19–20 | Synthetic-identity red-team hardening |
| 6 | W21–24 | Paper, articles, talk, portfolio lock |

## Stack

FastAPI, MLflow, XGBoost, LightGBM, CatBoost, PyTorch, Polars, pytest, Docker Compose, GitHub Actions.

## Setup

```bash
poetry install
poetry run pytest
```
