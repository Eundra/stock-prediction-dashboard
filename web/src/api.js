import axios from 'axios';

const client = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
});

export const getTickers = () => client.get('/tickers').then((r) => r.data);

export const getHistory = (ticker, days = 30) =>
  client.get('/history', { params: { ticker, days } }).then((r) => r.data);

export const getMetrics = (ticker) =>
  client.get(`/metrics/${ticker}`).then((r) => r.data);

export const getBacktest = (ticker, days = 5) =>
  client.get('/backtest', { params: { ticker, days } }).then((r) => r.data);

export const getModelInfo = (ticker) =>
  client.get(`/model-info/${ticker}`).then((r) => r.data);

export const getHealth = () => client.get('/health').then((r) => r.data);

export const triggerIngest = (ticker) =>
  client.post(`/ingest/${ticker}`).then((r) => r.data);
