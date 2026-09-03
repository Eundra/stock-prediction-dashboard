import { useEffect, useState } from 'react';
import { getTickers, getHistory, getBacktest, getMetrics, getModelInfo, triggerIngest } from './api';
import { usePredictionHistory } from './hooks/usePredictionHistory';
import Navbar from './components/Navbar';
import ControlPanel from './components/ControlPanel';
import ResultCards from './components/ResultCards';
import PriceChart from './components/PriceChart';
import DataTable from './components/DataTable';
import PredictionHistory from './components/PredictionHistory';
import ModelInfoCard from './components/ModelInfoCard';

export default function App() {
  const [tickers, setTickers] = useState([]);
  const [ticker, setTicker] = useState('TLKM.JK');
  const [backtestData, setBacktestData] = useState([]);
  const [historyData, setHistoryData] = useState([]);
  const [metrics, setMetrics] = useState(null);
  const [modelInfo, setModelInfo] = useState(null);
  const [selectedIndex, setSelectedIndex] = useState(null);
  const [revealedIndex, setRevealedIndex] = useState(null);
  const [loading, setLoading] = useState(true);
  const [predicting, setPredicting] = useState(false);
  const [error, setError] = useState(null);

  const { history, addPrediction, clearHistory } = usePredictionHistory();

  useEffect(() => {
    getTickers()
      .then((d) => setTickers(d.tickers))
      .catch(() => setError('API tidak bisa dihubungi'));
  }, []);

  useEffect(() => {
    if (!ticker) return;

    let cancelled = false;

    Promise.all([
      getBacktest(ticker, 5),
      getHistory(ticker, 30),
      getMetrics(ticker),
      getModelInfo(ticker),
    ])
      .then(([bt, hist, met, info]) => {
        if (!cancelled) {
          setBacktestData(bt);
          setHistoryData(hist);
          setMetrics(met);
          setModelInfo(info);
        }
      })
      .catch(() => {
        if (!cancelled) setError('Gagal memuat data — cek apakah API menyala');
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });

    return () => { cancelled = true; };
  }, [ticker]);

  function handleTickerChange(newTicker) {
    setLoading(true);
    setError(null);
    setSelectedIndex(null);
    setRevealedIndex(null);
    setTicker(newTicker);
  }

  function handleDateSelect(idx) {
    setSelectedIndex(idx);
    setRevealedIndex(null); // sembunyikan hasil lama sampai tombol Prediksi ditekan lagi
  }

  async function handlePredict() {
    if (selectedIndex === null) return;
    const targetDate = backtestData[selectedIndex]?.date;

    setPredicting(true);
    setError(null);
    try {
      await triggerIngest(ticker);
      const fresh = await getBacktest(ticker, 5);
      setBacktestData(fresh);

      const idx = fresh.findIndex((r) => r.date === targetDate);
      const finalIdx = idx !== -1 ? idx : fresh.length - 1;
      setSelectedIndex(finalIdx);
      setRevealedIndex(finalIdx);

      const row = fresh[finalIdx];
      addPrediction({ date: row.date, ticker, actual: row.actual, predicted: row.predicted });
    } catch {
      setError('Gagal memperbarui data — cek apakah API menyala');
    } finally {
      setPredicting(false);
    }
  }

  const selectedRow = revealedIndex !== null ? backtestData[revealedIndex] : null;

  return (
    <div className="min-h-screen bg-bg">
      <Navbar tickers={tickers} ticker={ticker} onTickerChange={handleTickerChange} />

      <main className="max-w-7xl mx-auto px-4 sm:px-6 py-6 space-y-6">
        {error && (
          <div className="bg-accent-down/10 border border-accent-down/30 rounded-xl p-4 text-accent-down text-sm">
            {error}
          </div>
        )}

        <ControlPanel
          backtestData={backtestData}
          selectedIndex={selectedIndex}
          onDateSelect={handleDateSelect}
          onPredict={handlePredict}
          disabled={loading}
          predicting={predicting}
        />

        {loading ? (
          <div className="text-center py-12 text-text-secondary">Memuat data...</div>
        ) : (
          <>
            <ResultCards selectedRow={selectedRow} metrics={metrics} />

            <PriceChart
              historyData={historyData}
              backtestData={backtestData}
              revealedIndex={revealedIndex}
              predicting={predicting}
            />

            <DataTable
              data={backtestData}
              selectedIndex={selectedIndex}
              onRowClick={handleDateSelect}
            />

            <PredictionHistory history={history} onClear={clearHistory} />

            <ModelInfoCard modelInfo={modelInfo} />

            <p className="text-center text-text-secondary text-xs py-4">
              Disclaimer: demonstrasi teknis pipeline ML, bukan saran investasi.
            </p>
          </>
        )}
      </main>
    </div>
  );
}
