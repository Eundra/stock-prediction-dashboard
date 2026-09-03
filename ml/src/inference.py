"""Prediksi harga dari data OHLCV mentah — dipakai langsung oleh API.

Satu-satunya pintu masuk untuk inference. API tidak boleh menyusun ulang
preprocessing sendiri — semua logika window/fitur/scaling hanya ada di sini.
"""

from __future__ import annotations

import json

import joblib
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model

from ml.src import config
from ml.src.features import build_features, min_raw_rows


class Predictor:
    """Muat model + scaler + manifest sekali, dipakai berulang untuk tiap request."""

    def __init__(self, model_dir=None):
        model_dir = model_dir or config.model_dir()

        self.manifest = json.loads((model_dir / "manifest.json").read_text())
        self.model = load_model(model_dir / "model.keras")
        self.scaler_x = joblib.load(model_dir / "scaler_x.pkl")
        self.scaler_y = joblib.load(model_dir / "scaler_y.pkl")

        # baca kontrak dari manifest, BUKAN dari config — supaya kalau nanti
        # ada v2 dengan window beda, kode ini tidak perlu diubah
        self.window = self.manifest["window_size"]
        self.features = self.manifest["features"]

    def predict(self, raw_df: pd.DataFrame) -> float:
        """raw_df: OHLCV mentah, minimal min_raw_rows() baris terakhir."""
        if len(raw_df) < min_raw_rows():
            raise ValueError(
                f"Butuh minimal {min_raw_rows()} baris data mentah, dapat {len(raw_df)}"
            )

        feat = build_features(raw_df)
        window = feat[self.features].values[-self.window:]

        if len(window) < self.window:
            raise ValueError(
                f"Setelah feature engineering, tersisa {len(window)} baris, "
                f"butuh {self.window}"
            )

        X = self.scaler_x.transform(window)
        X = X.reshape(1, self.window, len(self.features))

        y_scaled = self.model.predict(X, verbose=0)
        y = self.scaler_y.inverse_transform(y_scaled)
        return float(y[0, 0])
