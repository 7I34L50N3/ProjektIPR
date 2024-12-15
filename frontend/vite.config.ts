import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': '/src', // Alias do katalogu src
    },
  },
  server: {
    port: 8080, // Port development serwera
  },
});