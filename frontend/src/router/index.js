import { createRouter, createWebHistory } from 'vue-router'
import Main from "@/views/Main.vue"
import PersonalAccount from "@/views/PersonalAccount.vue"
import { isAuthenticated, isTokenExpired, logout } from "./auth.js"

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'main',
      component: Main
    },
    {
      path: '/messenger',
      name: 'messenger',
      component: PersonalAccount,
      meta: { requiresAuth: true }
    }
  ]
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('access_token');

  if (to.meta.requiresAuth) {
    if (!isAuthenticated()) {
      next('/login');
    } else if (isTokenExpired(token)) {
      logout();
      next('/login');
    } else {
      next();
    }
  } else {
    next();
  }
})

export default router
