import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));

export default {
  root: resolve(__dirname, 'src/main/webapp'),
  build: {
    rollupOptions: {
      // input: {
      //   main: resolve(__dirname, 'src/main/index.html'),
      //   dots: resolve(__dirname, 'src/dots/index.html'),
      // },
    },
    outDir: resolve(__dirname, 'dist'),
    emptyOutDir: true,
    // minify: true,
  },
};