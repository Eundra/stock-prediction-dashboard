# Stock Prediction Dashboard v2

Upgrade dari model LSTM skripsi (awalnya cuma eksperimen di notebook) menjadi sistem ML end-to-end yang benar-benar bisa dijalankan: data saham → training model → API → web dashboard.

Fokus project ini **bukan** akurasi prediksi saham, melainkan menunjukkan kemampuan mengurus seluruh rantai ML sebagai service — evaluasi yang jujur, kontrak model↔API yang rapi, dan sistem yang bisa dijalankan ulang kapan saja. **Ini bukan sistem rekomendasi beli/jual saham.**

## Stack

| Lapisan | Teknologi |
|---|---|
| Model | LSTM Bidirectional (TensorFlow/Keras), dilatih di Google Colab |
| Data | yfinance (Yahoo Finance) — TLKM.JK |
| API | FastAPI + Uvicorn |
| Frontend | React + Vite + Tailwind CSS + Recharts |
| Deploy | Docker Compose, server rumah (rencana) |

## Arsitektur

```
Yahoo Finance
     │  ml/src/ingest.py
     ▼
ml/data/raw/TLKM.JK.csv
     │  ml/src/train.py (features → preprocessing → LSTM → evaluate)
     ▼
ml/models/TLKM.JK/v1/  (model.keras, scaler, manifest.json, metrics.json)
     │  ml/src/inference.py
     ▼
FastAPI (api/)  →  React Dashboard (web/)
```

Logika ML hanya ada di satu tempat (`ml/src/`). API dan training memakai fungsi yang sama untuk preprocessing/inference — mencegah model dan API diam-diam tidak sinkron.

## Menjalankan lokal

**ML**
```bash
pip install -r ml/requirements.txt
python -m ml.src.ingest   # ambil data terbaru
python -m ml.src.train    # latih ulang model (opsional, model v1 sudah ada)
```

**API**
```bash
pip install -r api/requirements.txt
uvicorn api.app.main:app --reload
# buka http://127.0.0.1:8000/docs
```

**Web**
```bash
cd web
npm install
npm run dev
# buka http://localhost:5173
```

## Hasil model (`v1`)

Test set 2025-03 s.d. sekarang:

| Metrik | Nilai |
|---|---|
| RMSE | 93.79 |
| MAPE | 2.25% |
| R² | 0.94 |
| Directional accuracy | 44.07% |

Directional accuracy di bawah 50% menunjukkan model baik melacak level harga, tapi tidak bisa diandalkan untuk menebak arah pergerakan harian — sesuai dengan scoping project ini yang memang bukan sinyal trading.

## Keterbatasan yang diketahui

- Model final (`v1`) dipilih dari 3 run training berdasarkan RMSE test terbaik — idealnya seleksi memakai validation loss, bukan test set, supaya angka test tetap netral.
- Baseline naif (`besok = harga hari ini`) belum dihitung sebagai pembanding directional accuracy.
- Baru mendukung satu ticker (TLKM.JK).
- Fase deployment (Docker Compose ke server rumah) belum dikerjakan.

## Struktur folder

```
ml/          pipeline data & model (ingest, features, preprocessing, train, inference)
api/         FastAPI backend
web/         React dashboard
deployment/  Docker Compose, Nginx config (belum diisi)
docs/        dokumentasi & screenshot
```
