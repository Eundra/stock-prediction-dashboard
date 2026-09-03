import { useState, useEffect } from 'react';

const STORAGE_KEY = 'prediction_history';

function loadHistory() {
  try {
    const data = localStorage.getItem(STORAGE_KEY);
    return data ? JSON.parse(data) : [];
  } catch {
    return [];
  }
}

function saveHistory(history) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(history));
}

export function usePredictionHistory() {
  const [history, setHistory] = useState(loadHistory);

  useEffect(() => {
    saveHistory(history);
  }, [history]);

  function addPrediction(item) {
    setHistory((prev) => [
      { ...item, timestamp: new Date().toISOString() },
      ...prev,
    ]);
  }

  function clearHistory() {
    setHistory([]);
  }

  return { history, addPrediction, clearHistory };
}
