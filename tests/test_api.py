from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200


def test_predict_valid():
    r = client.post(
        "/predict",
        json={"amount": 500, "card_id": "c1", "merchant_id": "m1", "txn_hour": 14},
    )
    assert r.status_code == 200
    assert "fraud_probability" in r.json()


def test_predict_negative_amount_rejected():
    r = client.post(
        "/predict",
        json={"amount": -5, "card_id": "c1", "merchant_id": "m1", "txn_hour": 14},
    )
    assert r.status_code == 422


def test_predict_missing_field_rejected():
    r = client.post("/predict", json={"amount": 100})
    assert r.status_code == 422
