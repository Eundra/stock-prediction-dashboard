"""Logika endpoint /predict — mengambil data terbaru lalu memanggil model."""

from datetime import date, timedelta

import pandas as pd

from ml.src.config import raw_path
from ml.src.features import min_raw_rows
from ml.src.ingest import fetch_live_price
from api.app.model_loader import get_predictor
from api.app.schemas import PredictResponse


def _next_trading_day(d: date) -> date:
    """Lompat ke hari kerja berikutnya (skip Sabtu/Minggu)."""
    nd = d + timedelta(days=1)
    while nd.weekday() >= 5:  # 5=Sabtu, 6=Minggu
        nd += timedelta(days=1)
    return nd


def predict_next_day(ticker: str = "TLKM.JK") -> PredictResponse:
    predictor = get_predictor()

    raw = pd.read_csv(raw_path(ticker), index_col="date", parse_dates=["date"])
    recent = raw.tail(min_raw_rows() + 10)  # buffer aman

    price = predictor.predict(recent)
    next_date = _next_trading_day(raw.index[-1].date())

    staleness_days = (date.today() - raw.index[-1].date()).days
    if staleness_days > 3:
        print(
            f"[WARNING] Data {ticker} terakhir {raw.index[-1].date()} "
            f"({staleness_days} hari lalu). Jalankan `python -m ml.src.ingest`."
        )

    return PredictResponse(
        ticker=ticker,
        predicted_close=round(price, 2),
        predicted_date=next_date.isoformat(),
        model_version=predictor.manifest["version"],
    )


def backtest(ticker: str, days: int = 5) -> list[dict]:
    raw = pd.read_csv(raw_path(ticker), index_col="date", parse_dates=["date"])
    predictor = get_predictor()
    results = []

    for d in raw.index[-days:]:
        raw_upto = raw[raw.index < d]
        pred = predictor.predict(raw_upto)
        results.append({
            "date": d.date().isoformat(),
            "actual": float(raw.loc[d, "close"]),
            "actual_provisional": None,
            "predicted": round(pred, 2),
            "is_pending": False,
        })

    # Selalu tampilkan prediksi untuk hari kerja setelah data terakhir —
    # begitu data terakhir final, langsung maju. Tidak menunggu kalender
    # berganti, karena data yang dibutuhkan untuk prediksi ini sudah lengkap.
    next_date = _next_trading_day(raw.index.max().date())
    pred_next = predictor.predict(raw)
    is_today = next_date == date.today()
    results.append({
        "date": next_date.isoformat(),
        "actual": None,
        "actual_provisional": fetch_live_price(ticker) if is_today else None,
        "predicted": round(pred_next, 2),
        "is_pending": True,
    })

    return results
