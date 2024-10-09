import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/next_pair': 'http://localhost:8000',
      '/last_pair': 'http://localhost:8000',
      '/record_response': 'http://localhost:8000',
      '/a': 'http://localhost:8000',
      '/b': 'http://localhost:8000',
    },
  },
});
