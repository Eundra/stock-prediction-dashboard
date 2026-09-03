"""Muat model sekali saat startup, dipakai berulang di semua request."""

from ml.src.inference import Predictor

_predictor: Predictor | None = None


def get_predictor() -> Predictor:
    global _predictor
    if _predictor is None:
        _predictor = Predictor()
    return _predictor
