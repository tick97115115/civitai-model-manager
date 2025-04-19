import { createRouter, createWebHistory } from "vue-router";
import ModelsView from "@/views/ModelsView.vue";

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: "/",
            name: "models-view",
            component: ModelsView,
        },
    ],
});

export default router;
