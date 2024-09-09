import { createRouter, createWebHistory } from 'vue-router'
import Login from "@/components/Login.vue"

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'main',
      component: Login
    },
  ]
})

export default router
