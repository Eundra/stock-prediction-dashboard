import { formatRupiah, formatTanggal } from '../utils/formatters';

export default function PredictionHistory({ history, onClear }) {
  if (history.length === 0) return null;

  return (
    <div className="bg-surface border border-border rounded-xl p-5">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-text font-semibold">Riwayat Prediksi</h3>
        <button
          onClick={onClear}
          className="text-text-secondary text-sm hover:text-accent-down transition-colors"
        >
          Hapus Riwayat
        </button>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-border">
              <th className="text-left text-text-secondary font-medium py-2 px-3">Waktu</th>
              <th className="text-left text-text-secondary font-medium py-2 px-3">Ticker</th>
              <th className="text-left text-text-secondary font-medium py-2 px-3">Tanggal</th>
              <th className="text-right text-text-secondary font-medium py-2 px-3">Aktual</th>
              <th className="text-right text-text-secondary font-medium py-2 px-3">Prediksi</th>
            </tr>
          </thead>
          <tbody>
            {history.map((item, idx) => (
              <tr key={idx} className="border-b border-border/50">
                <td className="py-2 px-3 text-text-secondary text-xs">
                  {new Date(item.timestamp).toLocaleString('id-ID')}
                </td>
                <td className="py-2 px-3 text-text">{item.ticker}</td>
                <td className="py-2 px-3 text-text">{formatTanggal(item.date)}</td>
                <td className="py-2 px-3 text-right tabular-nums">
                  {item.actual != null ? formatRupiah(item.actual) : <span className="text-text-secondary italic">-</span>}
                </td>
                <td className="py-2 px-3 text-right tabular-nums text-accent-brand">
                  {formatRupiah(item.predicted)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
