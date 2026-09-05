"""Prediksi harga dari data OHLCV mentah — dipakai langsung oleh API.

Satu-satunya pintu masuk untuk inference. API tidak boleh menyusun ulang
preprocessing sendiri — semua logika window/fitur/scaling hanya ada di sini.
"""

from __future__ import annotations

import json

import joblib
import numpy as np
import pandas as pd
from ai_edge_litert.interpreter import Interpreter

from ml.src import config
from ml.src.features import build_features, min_raw_rows


class Predictor:
    """Muat model + scaler + manifest sekali, dipakai berulang untuk tiap request.

    Model disimpan sebagai .tflite (bukan .keras) supaya inference tidak
    butuh TensorFlow penuh — TF wajib AVX, banyak server kecil (mis. Celeron
    lama) tidak punya AVX dan langsung crash (SIGILL) begitu TF di-import.
    """

    def __init__(self, model_dir=None):
        model_dir = model_dir or config.model_dir()

        self.manifest = json.loads((model_dir / "manifest.json").read_text())
        self.interpreter = Interpreter(model_path=str(model_dir / "model.tflite"))
        self.interpreter.allocate_tensors()
        self._input_index = self.interpreter.get_input_details()[0]["index"]
        self._output_index = self.interpreter.get_output_details()[0]["index"]
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
        X = X.reshape(1, self.window, len(self.features)).astype(np.float32)

        self.interpreter.set_tensor(self._input_index, X)
        self.interpreter.invoke()
        y_scaled = self.interpreter.get_tensor(self._output_index)
        y = self.scaler_y.inverse_transform(y_scaled)
        return float(y[0, 0])
