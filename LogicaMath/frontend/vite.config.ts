/// <reference types="vitest" />
import path from 'path';
import { fileURLToPath } from 'node:url';
import { defineConfig, loadEnv } from 'vite';
import react from '@vitejs/plugin-react';
import tailwindcss from '@tailwindcss/vite';

const projectDir = path.dirname(fileURLToPath(import.meta.url));

export default defineConfig(({ mode }) => {
    const env = loadEnv(mode, '.', '');
    return {
      server: {
        port: 3000,
        host: '0.0.0.0',
      },
      plugins: [react(), tailwindcss()],
      test: {
        globals: true,
        environment: 'jsdom',
        include: ['components/**/*.test.{ts,tsx}', 'services/**/*.test.{ts,tsx}', 'tests/**/*.test.{ts,tsx}'],
        exclude: ['**/node_modules/**', '**/dist/**', '**/*.spec.ts']
      },
      resolve: {
        alias: {
          '@': path.resolve(projectDir, '.'),
        }
      },
      build: {
        rollupOptions: {
          output: {
            manualChunks: {
              'vendor-three': ['three'],
              'vendor-fabric': ['fabric'],
              'vendor-recharts': ['recharts'],
              'vendor-motion': ['framer-motion'],
              'vendor-react': ['react', 'react-dom', 'react-router-dom']
            }
          }
        }
      }
    };
});
