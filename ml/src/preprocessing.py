"""Split kronologis, scaling, dan windowing untuk LSTM.

Urutan operasinya tidak boleh ditukar:
    split  →  fit scaler HANYA di train  →  transform  →  windowing per split
Kalau windowing dilakukan sebelum split, baris akhir train dan baris awal val
akan berbagi data yang sama — evaluasimu jadi terlalu bagus dan tidak jujur.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

from ml.src.config import (
    FEATURE_COLS,
    SCALER_RANGE,
    TARGET_COL,
    TRAIN_RATIO,
    VAL_RATIO,
    WINDOW_SIZE,
)


@dataclass
class Dataset:
    """Hasil akhir preprocessing, siap dipakai train.py."""

    X_train: np.ndarray
    y_train: np.ndarray
    X_val: np.ndarray
    y_val: np.ndarray
    X_test: np.ndarray
    y_test: np.ndarray
    scaler_x: MinMaxScaler
    scaler_y: MinMaxScaler
    dates_test: pd.DatetimeIndex


def to_arrays(df: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
    """Pisahkan DataFrame berfitur jadi matriks X dan vektor target y."""
    X = df[FEATURE_COLS].values
    y = df[[TARGET_COL]].values.reshape(-1, 1)
    return X, y


def split_points(n: int) -> tuple[int, int]:
    """Batas indeks train/val — 80% dan 10% berikutnya, sisanya test."""
    train_end = int(n * TRAIN_RATIO)
    val_end = train_end + int(n * VAL_RATIO)
    return train_end, val_end


def fit_scalers(
    X_train: np.ndarray, y_train: np.ndarray
) -> tuple[MinMaxScaler, MinMaxScaler]:
    """Dua scaler terpisah, di-fit HANYA pada data train.

    scaler_y dipisah supaya prediksi model bisa dikembalikan ke rupiah
    lewat inverse_transform tanpa mencampur statistik kolom fitur lain.
    """
    scaler_x = MinMaxScaler(feature_range=SCALER_RANGE).fit(X_train)
    scaler_y = MinMaxScaler(feature_range=SCALER_RANGE).fit(y_train)
    return scaler_x, scaler_y


def create_windows(
    data: np.ndarray, target: np.ndarray, window_size: int = WINDOW_SIZE
) -> tuple[np.ndarray, np.ndarray]:
    """Geser jendela sepanjang *window_size*; target = nilai hari berikutnya."""
    X_w, y_w = [], []
    for i in range(len(data) - window_size):
        X_w.append(data[i : i + window_size])
        y_w.append(target[i + window_size])
    return np.array(X_w), np.array(y_w)


def prepare(df: pd.DataFrame) -> Dataset:
    """Jalankan seluruh rantai preprocessing pada DataFrame berfitur."""
    X, y = to_arrays(df)
    train_end, val_end = split_points(len(X))

    X_train_raw, y_train_raw = X[:train_end], y[:train_end]
    X_val_raw, y_val_raw = X[train_end:val_end], y[train_end:val_end]
    X_test_raw, y_test_raw = X[val_end:], y[val_end:]

    scaler_x, scaler_y = fit_scalers(X_train_raw, y_train_raw)

    X_train_w, y_train_w = create_windows(
        scaler_x.transform(X_train_raw), scaler_y.transform(y_train_raw)
    )
    X_val_w, y_val_w = create_windows(
        scaler_x.transform(X_val_raw), scaler_y.transform(y_val_raw)
    )
    X_test_w, y_test_w = create_windows(
        scaler_x.transform(X_test_raw), scaler_y.transform(y_test_raw)
    )

    # tanggal untuk tiap prediksi di test set — WINDOW_SIZE baris pertama
    # terpakai sebagai input, jadi tidak punya prediksi sendiri
    dates_test = df.index[val_end:][WINDOW_SIZE:]

    return Dataset(
        X_train=X_train_w,
        y_train=y_train_w,
        X_val=X_val_w,
        y_val=y_val_w,
        X_test=X_test_w,
        y_test=y_test_w,
        scaler_x=scaler_x,
        scaler_y=scaler_y,
        dates_test=dates_test,
    )
