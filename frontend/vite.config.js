import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  css: {
    preprocessorOptions: {
      scss: {
        api: 'modern-compiler',
      },
    },
  },
  resolve: {
    alias: {
      '@': 'src', // Maps `@` to the `src` directory
    },
  },
  server: {
    proxy: {
      '/api': {
        target: 'https://backendcareconnected.onrender.com', // Use the service name "backend"
        changeOrigin: true,
      },
    },
  },
  plugins: [vue()],
})

