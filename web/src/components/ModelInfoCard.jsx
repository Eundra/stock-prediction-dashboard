export default function ModelInfoCard({ modelInfo }) {
  if (!modelInfo) return null;

  return (
    <div className="bg-surface border border-border rounded-xl p-5">
      <h3 className="text-text font-semibold mb-4">Informasi Model</h3>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="space-y-3">
          <InfoRow label="Ticker" value={modelInfo.ticker} />
          <InfoRow label="Versi" value={modelInfo.version} />
          <InfoRow label="Tanggal Training" value={modelInfo.trained_at} />
          <InfoRow label="Window Size" value={modelInfo.window_size} />
          <InfoRow label="Target" value={modelInfo.target} />
          <InfoRow
            label="Data Range"
            value={`${modelInfo.data_range[0]} — ${modelInfo.data_range[1]}`}
          />
          <InfoRow label="Jumlah Data" value={`${modelInfo.n_rows_raw.toLocaleString('id-ID')} baris`} />
        </div>
        <div className="space-y-3">
          <p className="text-text-secondary text-xs uppercase tracking-wide">Features</p>
          <div className="flex flex-wrap gap-2">
            {modelInfo.features.map((f) => (
              <span
                key={f}
                className="bg-bg border border-border rounded-md px-2 py-1 text-xs text-text"
              >
                {f}
              </span>
            ))}
          </div>
          <p className="text-text-secondary text-xs uppercase tracking-wide mt-4">Hyperparams</p>
          <div className="space-y-2">
            {Object.entries(modelInfo.hyperparams).map(([key, val]) => (
              <InfoRow key={key} label={key} value={val} />
            ))}
          </div>
          <p className="text-text-secondary text-xs uppercase tracking-wide mt-4">Dependencies</p>
          {Object.entries(modelInfo.versions).map(([key, val]) => (
            <InfoRow key={key} label={key} value={`v${val}`} />
          ))}
        </div>
      </div>
    </div>
  );
}

function InfoRow({ label, value }) {
  return (
    <div className="flex justify-between items-center">
      <span className="text-text-secondary text-sm">{label}</span>
      <span className="text-text text-sm font-medium tabular-nums">{value}</span>
    </div>
  );
}
