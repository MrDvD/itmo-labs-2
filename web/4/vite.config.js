import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { svelte } from '@sveltejs/vite-plugin-svelte';

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = resolve(__dirname, 'src', 'main', 'webapp');

export default {
  root,
  appType: 'mpa',
  build: {
    outDir: resolve(__dirname, 'dist'),
    emptyOutDir: true,
    minify: true,
  },
  plugins: [svelte()],
  resolve: {
    alias: {
      'lib': resolve(root, 'lib'),
    }
  },
};