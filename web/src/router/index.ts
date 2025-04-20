import { createRouter, createWebHistory } from "vue-router";
import ModelsView from "@/views/ModelsView.vue";
import DownloadsView from "@/views/DownloadsView.vue";

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: "/",
            name: "models-view",
            component: ModelsView,
        },
        {
            path: "/downloads",
            name: "downloads-view",
            component: DownloadsView,
        },
    ],
});

export default router;
