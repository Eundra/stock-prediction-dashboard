import clsx from 'clsx';
import { formatRupiah } from '../utils/formatters';

export default function ResultCards({ selectedRow, metrics }) {
  if (!selectedRow) return null;

  const isPending = selectedRow.is_pending;
  const aktual = selectedRow.actual;
  const prediksi = selectedRow.predicted;

  const diff = aktual != null ? prediksi - aktual : null;
  const isUp = diff != null && diff > 0;

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
      <div className="bg-surface border border-border rounded-xl p-5">
        <p className="text-text-secondary text-sm mb-1">Harga Aktual</p>
        {isPending ? (
          selectedRow.actual_provisional != null ? (
            <>
              <p className="text-2xl font-bold tabular-nums">
                {formatRupiah(selectedRow.actual_provisional)}
              </p>
              <p className="text-xs text-text-secondary italic mt-1">
                Harga sementara, belum final
              </p>
            </>
          ) : (
            <p className="text-2xl font-bold text-text-secondary italic">Sementara</p>
          )
        ) : (
          <p className="text-2xl font-bold tabular-nums">{formatRupiah(aktual)}</p>
        )}
      </div>

      <div className="bg-surface border border-border rounded-xl p-5">
        <p className="text-text-secondary text-sm mb-1">Harga Prediksi</p>
        <p className="text-2xl font-bold tabular-nums text-accent-brand">
          {formatRupiah(prediksi)}
        </p>
        {diff != null && (
          <p
            className={clsx(
              'text-sm mt-1 font-medium',
              isUp ? 'text-accent-up' : 'text-accent-down'
            )}
          >
            {isUp ? '▲' : '▼'} {formatRupiah(Math.abs(diff))} dari aktual
          </p>
        )}
      </div>

      <div className="bg-surface border border-border rounded-xl p-5">
        <p className="text-text-secondary text-sm mb-1">Akurasi Model</p>
        {metrics ? (
          <div className="space-y-1">
            <div className="flex justify-between">
              <span className="text-text-secondary text-sm">RMSE</span>
              <span className="text-sm font-medium tabular-nums">
                {metrics.test.rmse}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-text-secondary text-sm">MAPE</span>
              <span className="text-sm font-medium tabular-nums">
                {metrics.test.mape}%
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-text-secondary text-sm">R²</span>
              <span className="text-sm font-medium tabular-nums">
                {metrics.test.r_squared}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-text-secondary text-sm">Directional Acc.</span>
              <span
                className={clsx(
                  'text-sm font-medium tabular-nums',
                  metrics.test.directional_accuracy >= 50
                    ? 'text-accent-up'
                    : 'text-accent-down'
                )}
              >
                {metrics.test.directional_accuracy}%
              </span>
            </div>
          </div>
        ) : (
          <p className="text-text-secondary text-sm italic">Memuat...</p>
        )}
      </div>
    </div>
  );
}
