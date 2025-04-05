// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import DestinationSearch from '../views/DestinationSearch.vue'
import RoutePlanner from '../views/RoutePlanner.vue'

const routes = [
  { path: '/', name: 'DestinationSearch', component: DestinationSearch },
  { path: '/route', name: 'RoutePlanner', component: RoutePlanner },
]

export const router = createRouter({
  history: createWebHistory(),
  routes,
})
