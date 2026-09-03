"""Entry point FastAPI — definisi seluruh endpoint."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from ml.src.config import TICKER, model_dir
from api.app.model_loader import get_predictor
from api.app.predict import predict_next_day
from api.app.schemas import HealthResponse, PredictResponse

app = FastAPI(title="Stock Prediction API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # nanti dipersempit ke domain dashboard saat deploy
    allow_methods=["GET", "POST"],
)

@app.get("/")
def root():
    return {"message": "Stock Prediction API", "docs": "/docs"}

@app.get("/health", response_model=HealthResponse)
def health():
    try:
        get_predictor()
        loaded = [TICKER]
    except Exception:
        loaded = []
    return HealthResponse(status="ok" if loaded else "degraded", models_loaded=loaded)


@app.get("/tickers")
def tickers():
    return {"tickers": [TICKER]}


@app.post("/predict", response_model=PredictResponse)
def predict(ticker: str = TICKER):
    if ticker != TICKER:
        raise HTTPException(404, f"Ticker {ticker!r} tidak didukung")
    return predict_next_day(ticker)


@app.get("/metrics/{ticker}")
def metrics(ticker: str):
    if ticker != TICKER:
        raise HTTPException(404, f"Ticker {ticker!r} tidak didukung")
    import json
    path = model_dir(ticker) / "metrics.json"
    return json.loads(path.read_text())
