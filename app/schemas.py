from pydantic import BaseModel, Field


class TransactionIn(BaseModel):
    amount: float = Field(gt=0)
    card_id: str
    merchant_id: str
    txn_hour: int = Field(ge=0, le=23)
    country: str = ""


class PredictionOut(BaseModel):
    fraud_probability: float
    decision: str
