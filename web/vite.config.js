import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import { defineConfig } from 'vite'

export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    proxy: {
      '/tickers': 'http://127.0.0.1:8000',
      '/predict': 'http://127.0.0.1:8000',
      '/metrics': 'http://127.0.0.1:8000',
      '/history': 'http://127.0.0.1:8000',
      '/backtest': 'http://127.0.0.1:8000',
      '/model-info': 'http://127.0.0.1:8000',
    },
  },
})
