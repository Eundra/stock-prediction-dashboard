"""Turunkan fitur model dari OHLCV mentah.

File ini dipakai DUA kali: saat training dan saat API melayani prediksi.
Jangan pernah menyalin rumusnya ke tempat lain — kalau suatu saat berbeda,
model akan menerima input yang tidak sama dengan waktu dilatih, dan tidak
akan ada error apa pun yang memberitahumu.
"""

from __future__ import annotations

import pandas as pd

from ml.src.config import (
    FEATURE_COLS,
    MA_WINDOW,
    TARGET_COL,
    VOLATILITY_WINDOW,
    WINDOW_SIZE,
)


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    """Hitung return, volatility, dan ma; buang baris pemanasan.

    Mengembalikan DataFrame berisi kolom target diikuti FEATURE_COLS
    sesuai urutan di config — urutan ini adalah kontrak dengan model.
    """
    out = df.copy()

    out["return"] = out["close"].pct_change().shift(1)
    out["volatility"] = out["return"].rolling(window=VOLATILITY_WINDOW).std()
    out["ma"] = out["close"].shift(1).rolling(window=MA_WINDOW).mean()

    out = out.dropna()
    return out[[TARGET_COL] + FEATURE_COLS]


def min_raw_rows() -> int:
    """Jumlah baris mentah minimum untuk menghasilkan satu window utuh.

    MA_WINDOW baris pertama hilang saat pemanasan fitur, lalu WINDOW_SIZE
    baris dipakai sebagai input model. Dipakai API untuk memutuskan berapa
    banyak data historis yang perlu dibaca.
    """
    return WINDOW_SIZE + MA_WINDOW
