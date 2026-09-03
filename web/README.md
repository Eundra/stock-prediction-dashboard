# Web — Stock Prediction Dashboard

Frontend React (Vite + Tailwind CSS + Recharts). Lihat [README.md](../README.md) di root untuk gambaran project secara keseluruhan.

## Menjalankan

```bash
npm install
npm run dev
# http://localhost:5173
```

Butuh API (`api/`) sudah jalan di `http://1x7.0.0.1:xxxx` — atur lewat `.env`:

```
VITE_API_BASE_URL=http://1x7.0.0.1:xxxx
```

## Struktur

```
src/
├── App.jsx                    orkestrasi state & layout
├── api.js                     semua panggilan ke backend
├── components/                Navbar, ControlPanel, ResultCards, PriceChart, DataTable, PredictionHistory, ModelInfoCard
├── hooks/usePredictionHistory.js   riwayat prediksi (localStorage)
└── utils/formatters.js        format Rupiah & tanggal (locale id-ID)
```

## Alur

1. Buka halaman → `/backtest` diambil otomatis, isi date selector + tabel
2. Pilih tanggal → tombol **Prediksi** menarik data terbaru (`/ingest`) lalu memprediksi ulang
3. Hasil tampil di card + grafik, tersimpan ke riwayat (browser, tidak ke server)
