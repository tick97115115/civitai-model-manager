import { fileURLToPath, URL } from "node:url";
import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import vueDevTools from "vite-plugin-vue-devtools";

// https://vite.dev/config/
export default defineConfig({
    plugins: [vue(), vueDevTools()],
    resolve: {
        alias: {
            "@": fileURLToPath(new URL("./src", import.meta.url)),
        },
    },
    // server: {
    //     proxy: {
    //         "/api/v1/models": {
    //             target: "https://civitai.com",
    //             changeOrigin: true,
    //         },
    //     },
    // },
    server: {
        cors: true,
        headers: {
            "Access-Control-Allow-Origin": "*", // 允许所有来源
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization",
        },
    },
});
