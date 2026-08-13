from fastapi import FastAPI

from app.schemas import PredictionOut, TransactionIn
from app.scorer import score

app = FastAPI(title="TRACER Fraud Scoring")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict", response_model=PredictionOut)
def predict(txn: TransactionIn):
    p = score(txn.amount)
    decision = "approve" if p < 0.5 else ("review" if p < 0.8 else "block")
    return PredictionOut(fraud_probability=p, decision=decision)
