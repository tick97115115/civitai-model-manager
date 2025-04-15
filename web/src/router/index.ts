import { createRouter, createWebHistory } from 'vue-router'
import Layout from '@/Layout/index.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '',
      name: 'Layout',
      component: Layout,
    },

  ],
})

export default router
