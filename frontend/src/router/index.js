import { createRouter, createWebHistory } from 'vue-router'
import { userRoutes } from './userRoutes' // ваш файл

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: []
})

export default router