"""Bentuk data request/response — divalidasi otomatis oleh FastAPI."""

from pydantic import BaseModel


class PredictRequest(BaseModel):
    ticker: str = "TLKM.JK"

class PredictResponse(BaseModel):
    model_config = {"protected_namespaces": ()}

    ticker: str
    predicted_close: float
    predicted_date: str
    model_version: str

class HistoryPoint(BaseModel):
    date: str
    close: float


class HealthResponse(BaseModel):
    status: str
    models_loaded: list[str]
