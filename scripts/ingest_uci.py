"""Ingest UCI Credit Card Fraud CSV -> Parquet via the TRACER data layer."""

from pathlib import Path

import pandas as pd

from tracer.data import load_parquet, to_parquet, validate_creditcard_schema

RAW = Path("data/raw/creditcard.csv")
OUT = Path("data/processed/uci_creditcard.parquet")

df = pd.read_csv(RAW)
print(f"rows: {len(df):,}  cols: {len(df.columns)}")
print(f"fraud rate: {df['Class'].mean() * 100:.4f}%")

out = to_parquet(df, OUT)
back = load_parquet(out)
print(f"schema ok: {validate_creditcard_schema(back)}")
print(f"parquet size MB: {out.stat().st_size / 1e6:.1f}")