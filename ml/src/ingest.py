"""Unduh dan perbarui data OHLCV dari Yahoo Finance ke CSV."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import yfinance as yf

from ml.src.config import BASE_COLS, RAW_DIR, START_DATE, TICKER, raw_path


def _normalize(df: pd.DataFrame) -> pd.DataFrame:
    """Seragamkan bentuk DataFrame dari yfinance.

    - ratakan kolom MultiIndex (muncul di yfinance versi baru)
    - nama kolom jadi huruf kecil, sesuai notebook skripsi
    - index tanggal urut naik, tanpa duplikat
    """
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df.columns = [str(c).lower() for c in df.columns]

    missing = [c for c in BASE_COLS if c not in df.columns]
    if missing:
        raise ValueError(f"Kolom tidak ditemukan pada data yfinance: {missing}")

    df = df[BASE_COLS].copy()
    df.index = pd.to_datetime(df.index)
    df.index.name = "date"
    df = df.sort_index()
    df = df[~df.index.duplicated(keep="last")]
    df = df.dropna(subset=["close"])
    return df


def fetch(ticker: str = TICKER, start: str = START_DATE, end: str | None = None) -> pd.DataFrame:
    """Ambil OHLCV dari Yahoo Finance. Error kalau hasilnya kosong."""
    df = yf.download(ticker, start=start, end=end, auto_adjust=False, progress=False)

    if df is None or df.empty:
        raise ValueError(
            f"yfinance mengembalikan data kosong untuk {ticker!r} sejak {start}. "
            "Cek koneksi internet atau penulisan ticker."
        )

    return _normalize(df)


def save(df: pd.DataFrame, ticker: str = TICKER) -> Path:
    """Tulis ke ml/data/raw/{TICKER}.csv."""
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    path = raw_path(ticker)
    df.to_csv(path)
    return path


def update(ticker: str = TICKER) -> pd.DataFrame:
    """Tambah baris baru saja kalau file CSV sudah ada."""
    path = raw_path(ticker)

    if not path.exists():
        df = fetch(ticker)
        save(df, ticker)
        return df

    existing = pd.read_csv(path, index_col="date", parse_dates=["date"])
    last_date = existing.index.max()

    fresh = fetch(ticker, start=last_date.strftime("%Y-%m-%d"))

    combined = pd.concat([existing, fresh])
    combined = combined[~combined.index.duplicated(keep="last")]
    combined = combined.sort_index()

    save(combined, ticker)
    return combined


def main() -> None:
    df = update()
    print(
        f"{TICKER}: {len(df):,} baris | "
        f"{df.index.min().date()} - {df.index.max().date()}"
    )


if __name__ == "__main__":
    main()
