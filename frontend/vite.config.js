import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path' // Ensure path module is imported for alias resolution

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
      '@': path.resolve(__dirname, './src'), // Ensure absolute path resolution
    },
  },
  server: {
    host: '0.0.0.0', // Expose to the network
    port: 5173, // Default Vite port
    proxy: {
      '/api': {
        target: 'https://careconnected-backend-v1-0.onrender.com', // Local backend URL
        changeOrigin: true, // Rewrite the host header
        secure: true, // false for development (useful for development)
        rewrite: (path) => path.replace(/^\/api/, '/api'),
      },
    },
  },
  plugins: [vue()],
})
