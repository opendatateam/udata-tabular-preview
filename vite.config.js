import { defineConfig } from 'vite';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'url';
import vue from '@vitejs/plugin-vue';
import legacy from '@vitejs/plugin-legacy';
import VueI18nPlugin from '@intlify/unplugin-vue-i18n/vite';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    VueI18nPlugin({
      include: resolve(dirname(fileURLToPath(import.meta.url)), './udata-tabular-preview/locales/**'),
      compositionOnly: false,
      fullInstall: false,
    }),
    legacy({
      targets: "> 0.1%, last 15 versions, Firefox ESR, not dead",
    }),
  ],
  build: {
    outDir: "udata_tabular_preview/static/udata-tabular-preview",
    rollupOptions: {
      input: "udata-tabular-preview/index.js",
      // make sure to externalize deps that shouldn't be bundled
      // into your library
      external: ['vue', 'vue-content-loader'],
      output: {
        entryFileNames: `[name].js`,
        chunkFileNames: `[name].js`,
        assetFileNames: `[name].[ext]`,
        // Provide global variables to use in the UMD build
        // for externalized deps
        globals: {
          vue: "Vue",
          "vue-content-loader": "ContentLoader"
        }
      }
    }
  }
});
