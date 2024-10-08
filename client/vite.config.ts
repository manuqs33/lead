import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [react()],
    server: {
        port: 3000,
        host: true,
        hmr: {
            port: 3000,
            host: 'localhost',
        },
        watch: {
            usePolling: true,
        },
    },
    css: {
        preprocessorOptions: {
          scss: {
            quietDeps: true
          }
        }
      }
})
