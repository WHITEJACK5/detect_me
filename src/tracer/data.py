"""Data layer for TRACER: Parquet-first storage with schema validation."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

CREDITCARD_COLUMNS = ["Time", "V1", "V2", "V3", "V4", "V5", "V6", "V7", "V8", "V9", "V10", "V11", "V12", "V13", "V14", "V15", "V16", "V17", "V18", "V19", "V20", "V21", "V22", "V23", "V24", "V25", "V26", "V27", "V28", "Amount", "Class"]


def to_parquet(df: pd.DataFrame, out_path: Path) -> Path:
    """Persist a DataFrame to Parquet, returning the output path."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(out_path, index=False)
    return out_path


def load_parquet(path: Path) -> pd.DataFrame:
    """Load a Parquet file into a DataFrame."""
    return pd.read_parquet(path)


def validate_creditcard_schema(df: pd.DataFrame) -> bool:
    """Return True if the DataFrame has the full UCI credit card fraud schema."""
    return set(CREDITCARD_COLUMNS).issubset(set(df.columns))
