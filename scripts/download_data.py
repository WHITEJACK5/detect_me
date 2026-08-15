"""
TRACER — Dataset download & Parquet conversion.

Pulls three datasets from Kaggle and converts each to Parquet under data/raw/:
  1. UCI Credit Card Fraud     -> data/raw/uci_creditcard.parquet
  2. IEEE-CIS Fraud Detection  -> data/raw/ieee_cis_train.parquet (+ identity)
  3. PaySim Synthetic Financial -> data/raw/paysim.parquet

Run:
  poetry run python scripts/download_data.py
  poetry run python scripts/download_data.py --only uci        # just one dataset
  poetry run python scripts/download_data.py --skip-download   # re-convert existing CSVs only
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

import pandas as pd

RAW_DIR = Path("data/raw")
DOWNLOAD_DIR = Path("data/_kaggle_downloads")

DATASETS = {
    "uci": {
        "kind": "dataset",
        "ref": "mlg-ulb/creditcardfraud",
        "csv_names": ["creditcard.csv"],
        "parquet_out": "uci_creditcard.parquet",
    },
    "ieee": {
        "kind": "competition",
        "ref": "ieee-fraud-detection",
        "csv_names": ["train_transaction.csv", "train_identity.csv"],
        "parquet_out": None,
    },
    "paysim": {
        "kind": "dataset",
        "ref": "ealaxi/paysim1",
        "csv_names": ["PS_20174392719_1491204439457_log.csv"],
        "parquet_out": "paysim.parquet",
    },
}


def run(cmd: list[str]) -> None:
    print(f"$ {' '.join(cmd)}")
    subprocess.run(cmd, check=True)


def check_kaggle_cli() -> None:
    if shutil.which("kaggle") is None:
        sys.exit(
            "ERROR: `kaggle` CLI not found on PATH.\n"
            "Install it with: poetry add --group dev kaggle"
        )
    kaggle_json = Path.home() / ".kaggle" / "kaggle.json"
    access_token = Path.home() / ".kaggle" / "access_token"
    if not kaggle_json.exists() and not access_token.exists():
        sys.exit(
            f"ERROR: neither {kaggle_json} nor {access_token} found.\n"
            "Create an API token at https://www.kaggle.com/settings and place it there."
        )


def download(key: str) -> Path:
    spec = DATASETS[key]
    target = DOWNLOAD_DIR / key
    target.mkdir(parents=True, exist_ok=True)

    if spec["kind"] == "dataset":
        run(["kaggle", "datasets", "download", "-d", spec["ref"], "-p", str(target), "--force"])
    else:
        run(["kaggle", "competitions", "download", "-c", spec["ref"], "-p", str(target), "--force"])

    for zf in target.glob("*.zip"):
        print(f"Unzipping {zf.name} ...")
        with zipfile.ZipFile(zf) as z:
            z.extractall(target)

    return target


def convert(key: str, folder: Path) -> None:
    spec = DATASETS[key]
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    if key == "ieee":
        tx_csv = folder / "train_transaction.csv"
        id_csv = folder / "train_identity.csv"
        if not tx_csv.exists():
            print(f"WARNING: {tx_csv} not found, skipping IEEE conversion.")
            return
        tx = pd.read_csv(tx_csv)
        tx_out = RAW_DIR / "ieee_cis_train_transaction.parquet"
        tx.to_parquet(tx_out, index=False)
        print(f"Wrote {tx_out} ({len(tx):,} rows)")

        if id_csv.exists():
            ident = pd.read_csv(id_csv)
            id_out = RAW_DIR / "ieee_cis_train_identity.parquet"
            ident.to_parquet(id_out, index=False)
            print(f"Wrote {id_out} ({len(ident):,} rows)")
        else:
            print(f"NOTE: {id_csv} not present.")
        return

    csv_path = folder / spec["csv_names"][0]
    if not csv_path.exists():
        candidates = list(folder.glob("*.csv"))
        if len(candidates) == 1:
            csv_path = candidates[0]
        else:
            print(f"WARNING: expected {csv_path} not found and folder has {len(candidates)} CSVs, skipping.")
            return

    df = pd.read_csv(csv_path)
    out_path = RAW_DIR / spec["parquet_out"]
    df.to_parquet(out_path, index=False)
    print(f"Wrote {out_path} ({len(df):,} rows, {len(df.columns)} cols)")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--only", choices=list(DATASETS), help="Only process this one dataset")
    parser.add_argument(
        "--skip-download",
        action="store_true",
        help="Skip download, just convert existing CSVs under data/_kaggle_downloads/",
    )
    args = parser.parse_args()

    keys = [args.only] if args.only else list(DATASETS)

    if not args.skip_download:
        check_kaggle_cli()

    for key in keys:
        print(f"\n=== {key} ===")
        folder = DOWNLOAD_DIR / key
        if not args.skip_download:
            folder = download(key)
        elif not folder.exists():
            print(f"WARNING: {folder} doesn't exist and --skip-download was set, skipping.")
            continue
        convert(key, folder)

    print("\nDone. Parquet files are in data/raw/")


if __name__ == "__main__":
    main()

