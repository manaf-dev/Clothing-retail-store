import { apiClient } from './api.js';

export const dashboardService = {
  // Get dashboard overview
  getOverview() {
    return apiClient.get('/dashboard/overview/');
  },

  // Get sales summary
  getSalesSummary() {
    return apiClient.get('/dashboard/sales-summary/');
  },

  // Get inventory alerts
  getInventoryAlerts() {
    return apiClient.get('/dashboard/inventory-alerts/');
  },

  // Get today's sales
  getTodaySales() {
    return apiClient.get('/dashboard/sales-summary/', {
      params: { period: 'today' }
    });
  },

  // Get weekly sales
  getWeeklySales() {
    return apiClient.get('/dashboard/sales-summary/', {
      params: { period: 'week' }
    });
  },

  // Get monthly sales
  getMonthlySales() {
    return apiClient.get('/dashboard/sales-summary/', {
      params: { period: 'month' }
    });
  }
};
