import clsx from 'clsx';
import { formatTanggal } from '../utils/formatters';

export default function ControlPanel({
  backtestData,
  selectedIndex,
  onDateSelect,
  onPredict,
  disabled,
  predicting,
}) {
  return (
    <div className="bg-surface border border-border rounded-xl p-4">
      <div className="flex flex-wrap items-center gap-3">
        <div className="flex gap-2">
          {backtestData.map((item, idx) => (
            <button
              key={item.date}
              onClick={() => onDateSelect(idx)}
              disabled={disabled}
              className={clsx(
                'px-4 py-2 rounded-lg text-sm font-medium transition-all',
                'border',
                selectedIndex === idx
                  ? 'bg-accent-brand text-white border-accent-brand'
                  : 'bg-bg text-text-secondary border-border hover:border-accent-brand hover:text-text',
                disabled && 'opacity-50 cursor-not-allowed'
              )}
            >
              {formatTanggal(item.date)}
            </button>
          ))}
        </div>
        <button
          onClick={onPredict}
          disabled={disabled || selectedIndex === null || predicting}
          className={clsx(
            'ml-auto px-6 py-2 rounded-lg text-sm font-semibold transition-all flex items-center gap-2',
            'bg-accent-brand text-white',
            'hover:bg-blue-600 active:bg-blue-700',
            'disabled:opacity-50 disabled:cursor-not-allowed'
          )}
        >
          {predicting && (
            <span className="w-3.5 h-3.5 border-2 border-white/40 border-t-white rounded-full animate-spin" />
          )}
          {predicting ? 'Memprediksi...' : 'Prediksi'}
        </button>
      </div>
    </div>
  );
}
