// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import Homepage from '../views/Homepage.vue'
import Navigation from '../views/Navigation.vue'

const routes = [
  { 
    path: '/', 
    name: 'Homepage', 
    component: Homepage 
  },
  { 
    path: '/route', 
    name: 'Navigation', 
    component: Navigation 
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
