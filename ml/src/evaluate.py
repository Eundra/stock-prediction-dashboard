"""Metrik evaluasi — selalu dihitung dalam satuan rupiah, bukan nilai ter-scale.

Angka ter-scale tidak bisa ditafsirkan manusia. RMSE 0.04 tidak berarti apa-apa;
RMSE 87 rupiah bisa langsung dinilai bagus atau tidak.
"""

from __future__ import annotations

import numpy as np


def rmse(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    return float(np.sqrt(np.mean((y_true - y_pred) ** 2)))


def mae(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    return float(np.mean(np.abs(y_true - y_pred)))


def mape(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Rata-rata galat relatif dalam persen."""
    return float(np.mean(np.abs((y_true - y_pred) / y_true)) * 100)


def r_squared(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Koefisien determinasi — metrik yang sama dipakai di skripsi."""
    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
    return float(1 - ss_res / ss_tot)


def directional_accuracy(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Persentase arah gerak (naik/turun) yang ditebak benar.

    Untuk saham ini sering lebih informatif daripada RMSE: model bisa saja
    galatnya kecil tapi arahnya salah terus.
    """
    true_dir = np.sign(np.diff(y_true.ravel()))
    pred_dir = np.sign(np.diff(y_pred.ravel()))
    return float(np.mean(true_dir == pred_dir) * 100)


def compute_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> dict:
    """Semua metrik sekaligus, siap ditulis ke metrics.json."""
    y_true = np.asarray(y_true).ravel()
    y_pred = np.asarray(y_pred).ravel()
    return {
        "rmse": round(rmse(y_true, y_pred), 4),
        "mae": round(mae(y_true, y_pred), 4),
        "mape": round(mape(y_true, y_pred), 4),
        "r_squared": round(r_squared(y_true, y_pred), 4),
        "directional_accuracy": round(directional_accuracy(y_true, y_pred), 4),
        "n": int(len(y_true)),
    }
