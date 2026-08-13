import pandas as pd

from tracer.data import CREDITCARD_COLUMNS, load_parquet, to_parquet, validate_creditcard_schema


def make_fixture_creditcard(n_rows: int = 100) -> pd.DataFrame:
    """Synthetic UCI-schema fixture for tests."""
    df = pd.DataFrame(0.0, index=range(n_rows), columns=CREDITCARD_COLUMNS)
    df["Class"] = 0
    df.loc[df.index[:5], "Class"] = 1
    return df


def test_roundtrip_parquet(tmp_path):
    df = make_fixture_creditcard()
    out = to_parquet(df, tmp_path / "creditcard.parquet")
    assert out.exists()
    back = load_parquet(out)
    assert back.shape == df.shape


def test_schema_validation():
    assert validate_creditcard_schema(make_fixture_creditcard())


def test_schema_rejects_missing_column():
    df = make_fixture_creditcard().drop(columns=["V28"])
    assert not validate_creditcard_schema(df)


def test_class_imbalance_visible():
    df = make_fixture_creditcard()
    fraud_rate = df["Class"].mean()
    assert 0 < fraud_rate < 0.5
