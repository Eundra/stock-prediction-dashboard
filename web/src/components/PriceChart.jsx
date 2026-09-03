import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  CartesianGrid,
  ResponsiveContainer,
} from 'recharts';

const CustomTooltip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null;

  return (
    <div className="bg-surface border border-border rounded-lg p-3 shadow-lg">
      <p className="text-text-secondary text-xs mb-2">{label}</p>
      {payload.map((entry) => (
        <p key={entry.dataKey} className="text-sm" style={{ color: entry.color }}>
          {entry.name}: {entry.value != null ? `Rp${entry.value.toLocaleString('id-ID')}` : '-'}
        </p>
      ))}
    </div>
  );
};

export default function PriceChart({ historyData, backtestData, revealedIndex, predicting }) {
  const chartData = historyData.map((h) => ({
    date: h.date,
    aktual: h.close,
    prediksi: null,
  }));

  const revealedRow = !predicting && revealedIndex !== null ? backtestData[revealedIndex] : null;
  if (revealedRow) {
    const existing = chartData.find((c) => c.date === revealedRow.date);
    if (existing) {
      existing.prediksi = revealedRow.predicted;
    } else {
      chartData.push({
        date: revealedRow.date,
        aktual: revealedRow.actual,
        prediksi: revealedRow.predicted,
      });
    }
  }

  chartData.sort((a, b) => a.date.localeCompare(b.date));

  return (
    <div className="bg-surface border border-border rounded-xl p-5">
      <h3 className="text-text font-semibold mb-4">Grafik Harga</h3>
      <ResponsiveContainer width="100%" height={350}>
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" stroke="#232b3d" />
          <XAxis
            dataKey="date"
            stroke="#94a3b8"
            fontSize={12}
            tickFormatter={(v) => {
              const d = new Date(v + 'T00:00:00');
              return d.toLocaleDateString('id-ID', { day: 'numeric', month: 'short' });
            }}
          />
          <YAxis
            stroke="#94a3b8"
            fontSize={12}
            domain={['auto', 'auto']}
            tickFormatter={(v) => `Rp${(v / 1000).toFixed(0)}k`}
          />
          <Tooltip content={<CustomTooltip />} />
          <Legend />
          <Line
            type="monotone"
            dataKey="aktual"
            name="Aktual"
            stroke="#3b82f6"
            strokeWidth={2}
            dot={false}
          />
          <Line
            type="monotone"
            dataKey="prediksi"
            name="Prediksi"
            stroke="#ef4444"
            strokeWidth={2}
            strokeDasharray="5 5"
            dot={{ r: 4, fill: '#ef4444' }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
