import { defineConfig } from 'vite'

export default defineConfig({
  server: {
    port: 20003,
    host: '0.0.0.0',
    proxy: {
      '/api': {
        target: 'http://localhost:20004',
        changeOrigin: true,
      },
      '/media': {
        target: 'http://localhost:20004',
        changeOrigin: true,
      },
      '/static': {
        target: 'http://localhost:20004',
        changeOrigin: true,
      }
    }
  },
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
  }
})
