"""Konstanta terpusat untuk seluruh pipeline ML.

Semua angka di sini diambil dari notebook skripsi (ml/notebooks/archive/).
Jangan menulis ulang nilai-nilai ini di file lain — impor dari sini.
"""

from pathlib import Path

# ── Data ─────────────────────────────────────────────────
TICKER = "TLKM.JK"
START_DATE = "2011-01-01"

# kolom mentah dari yfinance, sudah di-lowercase agar cocok dengan notebook
BASE_COLS = ["open", "high", "low", "close", "volume"]

# ── Fitur ────────────────────────────────────────────────
# Urutan kolom ini adalah kontrak dengan model — jangan diubah urutannya.
FEATURE_COLS = ["open", "high", "low", "volume", "return", "volatility", "ma"]
TARGET_COL = "close"

VOLATILITY_WINDOW = 5   # return.rolling(5).std()
MA_WINDOW = 10          # close.shift(1).rolling(10).mean()

# ── Windowing & split ────────────────────────────────────
WINDOW_SIZE = 30
TRAIN_RATIO = 0.8
VAL_RATIO = 0.1         # sisanya (0.1) jadi test

SCALER_RANGE = (-1, 1)

# ── Hyperparameter (hasil tuning skripsi, jangan diubah) ─
LSTM_UNITS = 192
DENSE_UNITS = 160
DROPOUT_RATE = 0.2
LEARNING_RATE = 0.005
BATCH_SIZE = 16
EPOCHS = 100
EARLY_STOPPING_PATIENCE = 10

# ── Path (relatif terhadap root repo) ────────────────────
_ROOT = Path(__file__).resolve().parents[2]

RAW_DIR = _ROOT / "ml" / "data" / "raw"
PROCESSED_DIR = _ROOT / "ml" / "data" / "processed"
MODELS_DIR = _ROOT / "ml" / "models"

MODEL_VERSION = "v1"


def raw_path(ticker: str = TICKER) -> Path:
    """Lokasi file CSV data mentah untuk *ticker*."""
    return RAW_DIR / f"{ticker}.csv"


def model_dir(ticker: str = TICKER, version: str = MODEL_VERSION) -> Path:
    """Folder artefak model: ml/models/{TICKER}/{VERSION}/."""
    return MODELS_DIR / ticker / version
