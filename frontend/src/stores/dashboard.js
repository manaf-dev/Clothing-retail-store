import { defineStore } from 'pinia';
import { dashboardService } from '@/services/dashboardService.js';

export const useDashboardStore = defineStore('dashboard', {
  state: () => ({
    overview: {
      totalSales: 0,
      totalOrders: 0,
      totalProducts: 0,
      lowStockItems: 0
    },
    salesSummary: {
      today: { sales: 0, orders: 0 },
      week: { sales: 0, orders: 0 },
      month: { sales: 0, orders: 0 }
    },
    inventoryAlerts: [],
    loading: false,
    error: null
  }),

  actions: {
    async fetchOverview() {
      this.loading = true;
      try {
        const response = await dashboardService.getOverview();
        this.overview = response.data;
      } catch (error) {
        this.error = error.message;
        console.error('Error fetching overview:', error);
      } finally {
        this.loading = false;
      }
    },

    async fetchSalesSummary() {
      try {
        const [todayRes, weekRes, monthRes] = await Promise.all([
          dashboardService.getTodaySales(),
          dashboardService.getWeeklySales(),
          dashboardService.getMonthlySales()
        ]);

        this.salesSummary = {
          today: todayRes.data,
          week: weekRes.data,
          month: monthRes.data
        };
      } catch (error) {
        this.error = error.message;
        console.error('Error fetching sales summary:', error);
      }
    },

    async fetchInventoryAlerts() {
      try {
        const response = await dashboardService.getInventoryAlerts();
        this.inventoryAlerts = response.data;
      } catch (error) {
        this.error = error.message;
        console.error('Error fetching inventory alerts:', error);
      }
    },

    async refreshDashboard() {
      await Promise.all([
        this.fetchOverview(),
        this.fetchSalesSummary(),
        this.fetchInventoryAlerts()
      ]);
    }
  }
});
