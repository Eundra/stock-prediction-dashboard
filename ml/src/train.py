"""Latih LSTM dan simpan seluruh artefak ke ml/models/{TICKER}/{VERSION}/.

Jalankan: python -m ml.src.train
"""

from __future__ import annotations

import json
from datetime import date

import joblib
import numpy as np
import pandas as pd
import sklearn
import tensorflow as tf
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from tensorflow.keras.layers import Bidirectional, Dense, Dropout, Input, LSTM
from tensorflow.keras.metrics import RootMeanSquaredError
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam

from ml.src import config
from ml.src.evaluate import compute_metrics
from ml.src.features import build_features
from ml.src.preprocessing import Dataset, prepare

SEED = 42


def build_model(n_features: int) -> Sequential:
    """Arsitektur hasil tuning skripsi — jangan diubah tanpa alasan."""
    model = Sequential(
        [
            Input(shape=(config.WINDOW_SIZE, n_features)),
            Bidirectional(LSTM(config.LSTM_UNITS, return_sequences=False)),
            Dropout(config.DROPOUT_RATE),
            Dense(config.DENSE_UNITS, activation="relu"),
            Dense(1),
        ]
    )
    model.compile(
        optimizer=Adam(learning_rate=config.LEARNING_RATE),
        loss="mse",
        metrics=["mae", RootMeanSquaredError()],
    )
    return model


def fit(model: Sequential, data: Dataset):
    """Latih model. shuffle=False wajib untuk data deret waktu."""
    callbacks = [
        EarlyStopping(
            monitor="val_loss",
            patience=config.EARLY_STOPPING_PATIENCE,
            restore_best_weights=True,
        ),
        ReduceLROnPlateau(monitor="val_loss", factor=0.5, patience=5, min_lr=1e-5),
    ]
    return model.fit(
        data.X_train,
        data.y_train,
        validation_data=(data.X_val, data.y_val),
        epochs=config.EPOCHS,
        batch_size=config.BATCH_SIZE,
        shuffle=False,
        callbacks=callbacks,
        verbose=1,
    )


def save_artifacts(model, data: Dataset, metrics: dict, raw: pd.DataFrame) -> None:
    """Tulis 5 artefak yang nanti dibaca oleh inference.py dan API."""
    out = config.model_dir()
    out.mkdir(parents=True, exist_ok=True)

    model.save(out / "model.keras")
    joblib.dump(data.scaler_x, out / "scaler_x.pkl")
    joblib.dump(data.scaler_y, out / "scaler_y.pkl")

    manifest = {
        "ticker": config.TICKER,
        "version": config.MODEL_VERSION,
        "trained_at": date.today().isoformat(),
        "window_size": config.WINDOW_SIZE,
        "features": config.FEATURE_COLS,
        "target": config.TARGET_COL,
        "volatility_window": config.VOLATILITY_WINDOW,
        "ma_window": config.MA_WINDOW,
        "scaler_range": list(config.SCALER_RANGE),
        "split": {"train": config.TRAIN_RATIO, "val": config.VAL_RATIO},
        "hyperparams": {
            "lstm_units": config.LSTM_UNITS,
            "dense_units": config.DENSE_UNITS,
            "dropout_rate": config.DROPOUT_RATE,
            "learning_rate": config.LEARNING_RATE,
            "batch_size": config.BATCH_SIZE,
            "epochs": config.EPOCHS,
        },
        "data_range": [
            str(raw.index.min().date()),
            str(raw.index.max().date()),
        ],
        "n_rows_raw": int(len(raw)),
        "versions": {
            "tensorflow": tf.__version__,
            "sklearn": sklearn.__version__,
        },
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2))
    (out / "metrics.json").write_text(json.dumps(metrics, indent=2))

    print(f"\nArtefak tersimpan di {out}")


def main() -> None:
    np.random.seed(SEED)
    tf.random.set_seed(SEED)

    raw = pd.read_csv(config.raw_path(), index_col="date", parse_dates=["date"])
    data = prepare(build_features(raw))

    print(f"train {data.X_train.shape} | val {data.X_val.shape} | test {data.X_test.shape}")

    model = build_model(n_features=len(config.FEATURE_COLS))
    model.summary()
    fit(model, data)

    # evaluasi di test set, dikembalikan ke rupiah dulu
    y_pred_scaled = model.predict(data.X_test, verbose=0)
    y_pred = data.scaler_y.inverse_transform(y_pred_scaled)
    y_true = data.scaler_y.inverse_transform(data.y_test)

    metrics = {
        "test": compute_metrics(y_true, y_pred),
        "test_period": [
            str(data.dates_test[0].date()),
            str(data.dates_test[-1].date()),
        ],
    }
    print("\nMetrik test:", json.dumps(metrics["test"], indent=2))

    save_artifacts(model, data, metrics, raw)


if __name__ == "__main__":
    main()
