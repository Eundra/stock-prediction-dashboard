"""Entry point FastAPI — definisi seluruh endpoint."""

import json

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from ml.src.config import TICKER, model_dir
from api.app.model_loader import get_predictor
from api.app.predict import backtest, predict_next_day
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

@app.get("/history")
def history(ticker: str = TICKER, days: int = 180):
    if ticker != TICKER:
        raise HTTPException(404, f"Ticker {ticker!r} tidak didukung")
    import pandas as pd
    from ml.src.config import raw_path
    raw = pd.read_csv(raw_path(ticker), index_col="date", parse_dates=["date"])
    recent = raw.tail(days)
    return [
        {"date": str(idx.date()), "close": float(row["close"])}
        for idx, row in recent.iterrows()
    ]

@app.get("/backtest")
def backtest_endpoint(ticker: str = TICKER, days: int = 5):
    if ticker != TICKER:
        raise HTTPException(404, f"Ticker {ticker!r} tidak didukung")
    return backtest(ticker, days)

@app.get("/model-info/{ticker}")
def model_info(ticker: str):
    if ticker != TICKER:
        raise HTTPException(404, f"Ticker {ticker!r} tidak didukung")
    path = model_dir(ticker) / "manifest.json"
    return json.loads(path.read_text())


@app.post("/ingest/{ticker}")
def ingest_endpoint(ticker: str):
    if ticker != TICKER:
        raise HTTPException(404, f"Ticker {ticker!r} tidak didukung")
    from ml.src.ingest import update
    df = update(ticker)
    return {"ticker": ticker, "rows": len(df), "last_date": str(df.index.max().date())}

