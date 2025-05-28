import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from '../views/DashboardView.vue'
import ProductsView from '@/views/ProductsView.vue'
import SalesView from '@/views/SalesView.vue'
import CustomersView from '@/views/CustomersView.vue'
import ReportsView from '@/views/ReportsView.vue'
import InventoryView from '@/views/InventoryView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/dashboard',
      name: 'dashboard',
      component: DashboardView,
    },
    {
      path: '/products',
      name: 'products',
      component: ProductsView,
    },
    {
      path: '/sales',
      name: 'sales',
      component: SalesView,
    },
    {
      path: '/customers',
      name: 'customers',
      component: CustomersView,
    },
    {
      path: '/reports',
      name: 'reports',
      component: ReportsView,
    },
    {
      path: '/inventory',
      name: 'inventory',
      component: InventoryView,
    },
    {
      path: '/:catchAll(.*)',
      name: 'not-found',
      component: () => import('@/views/NotFound.vue'),
    },
  ],
})

export default router
