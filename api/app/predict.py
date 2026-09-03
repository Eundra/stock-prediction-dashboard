"""Logika endpoint /predict — mengambil data terbaru lalu memanggil model."""

from datetime import date, timedelta

import pandas as pd

from ml.src.config import raw_path
from ml.src.features import min_raw_rows
from api.app.model_loader import get_predictor
from api.app.schemas import PredictResponse


def predict_next_day(ticker: str = "TLKM.JK") -> PredictResponse:
    predictor = get_predictor()

    raw = pd.read_csv(raw_path(ticker), index_col="date", parse_dates=["date"])
    recent = raw.tail(min_raw_rows() + 10)  # buffer aman

    price = predictor.predict(recent)
    next_date = raw.index[-1] + timedelta(days=1)

    staleness_days = (date.today() - raw.index[-1].date()).days
    if staleness_days > 3:
        print(
            f"[WARNING] Data {ticker} terakhir {raw.index[-1].date()} "
            f"({staleness_days} hari lalu). Jalankan `python -m ml.src.ingest`."
        )

    return PredictResponse(
        ticker=ticker,
        predicted_close=round(price, 2),
        predicted_date=next_date.date().isoformat(),
        model_version=predictor.manifest["version"],
    )
