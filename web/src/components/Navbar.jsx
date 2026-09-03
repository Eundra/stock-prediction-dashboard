import clsx from 'clsx';

export default function Navbar({ tickers, ticker, onTickerChange }) {
  return (
    <nav className="bg-surface border-b border-border px-6 py-4">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        <h1 className="text-xl font-semibold text-text">
          Stock Prediction Dashboard
        </h1>
        <select
          value={ticker}
          onChange={(e) => onTickerChange(e.target.value)}
          className={clsx(
            'bg-bg border border-border rounded-lg px-4 py-2',
            'text-text text-sm font-medium',
            'focus:outline-none focus:ring-2 focus:ring-accent-brand focus:border-transparent',
            'cursor-pointer'
          )}
        >
          {tickers.map((t) => (
            <option key={t} value={t}>
              {t}
            </option>
          ))}
        </select>
      </div>
    </nav>
  );
}
