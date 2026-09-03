import clsx from 'clsx';
import { formatTanggal, formatHari, formatBulan, formatTahun, formatRupiah } from '../utils/formatters';

export default function DataTable({ data, selectedIndex, onRowClick }) {
  return (
    <div className="bg-surface border border-border rounded-xl p-5">
      <h3 className="text-text font-semibold mb-4">Data Prediksi</h3>
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-border">
              <th className="text-left text-text-secondary font-medium py-3 px-3">Tanggal</th>
              <th className="text-left text-text-secondary font-medium py-3 px-3">Hari</th>
              <th className="text-left text-text-secondary font-medium py-3 px-3">Bulan</th>
              <th className="text-left text-text-secondary font-medium py-3 px-3">Tahun</th>
              <th className="text-right text-text-secondary font-medium py-3 px-3">Aktual</th>
              <th className="text-right text-text-secondary font-medium py-3 px-3">Prediksi</th>
            </tr>
          </thead>
          <tbody>
            {data.map((row, idx) => (
              <tr
                key={row.date}
                onClick={() => onRowClick(idx)}
                className={clsx(
                  'border-b border-border/50 cursor-pointer transition-colors',
                  selectedIndex === idx
                    ? 'bg-accent-brand/10'
                    : 'hover:bg-surface/80'
                )}
              >
                <td className="py-3 px-3 text-text">{formatTanggal(row.date)}</td>
                <td className="py-3 px-3 text-text-secondary">{formatHari(row.date)}</td>
                <td className="py-3 px-3 text-text-secondary">{formatBulan(row.date)}</td>
                <td className="py-3 px-3 text-text-secondary">{formatTahun(row.date)}</td>
                <td className="py-3 px-3 text-right tabular-nums font-medium text-text">
                  {row.actual != null ? (
                    formatRupiah(row.actual)
                  ) : row.actual_provisional != null ? (
                    <span className="italic text-text-secondary">
                      {formatRupiah(row.actual_provisional)}*
                    </span>
                  ) : (
                    <span className="text-text-secondary italic">-</span>
                  )}
                </td>
                <td className="py-3 px-3 text-right tabular-nums font-medium text-accent-brand">
                  {formatRupiah(row.predicted)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {data.some((r) => r.actual_provisional != null) && (
        <p className="text-xs text-text-secondary italic mt-3">
          * harga sementara, bursa masih berjalan / belum final
        </p>
      )}
    </div>
  );
}
