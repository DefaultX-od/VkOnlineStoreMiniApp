import { fileURLToPath, URL } from 'node:url'

import path from 'path';
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
  ],
  base: '/',
  build: {
    outDir: path.resolve(__dirname, '../backend/dist'), // куда кладём сборку
    emptyOutDir: true,
    assetsDir: 'assets', // подкаталог для JS/CSS/картинок
    manifest: true, 
  },
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  server: {
    // Vite будет работать на http://localhost:5173 (по умолчанию)
    // Когда фронтенд делает запрос на /api/..., Vite перенаправит его на http://127.0.0.1:5000
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:5000', // Адрес вашего Flask-сервера
        changeOrigin: true, // Нужно для правильной работы с хостами
        // rewrite: (path) => path.replace(/^\/api/, ''), // Если нужно убрать /api из пути на бэкенде
      },
    },
  },
})
