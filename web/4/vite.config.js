import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { svelte, vitePreprocess } from '@sveltejs/vite-plugin-svelte';
import { sveltePreprocess } from 'svelte-preprocess';

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = resolve(__dirname, 'src', 'main', 'webapp');

export default {
  root,
  appType: 'mpa',
  build: {
    outDir: resolve(__dirname, 'dist'),
    emptyOutDir: true,
    minify: false,
    rollupOptions: {
      input: {
        main: resolve(root, 'index.html'),
        dots: resolve(resolve(root, "dots"), 'index.html'),
      },
    },
  },
  plugins: [svelte({
    preprocess: vitePreprocess({ typescript: true }),
  })],
  resolve: {
    alias: {
      '@lib': resolve(root, 'lib'),
      "@components": resolve(root, "components"),
    }
  },
};