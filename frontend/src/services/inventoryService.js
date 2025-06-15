import { apiClient } from './api.js';

export const inventoryService = {
  // Get all inventory items
  getInventoryItems(params = {}) {
    return apiClient.get('/inventory/', { params });
  },

  // Get inventory item by ID
  getInventoryItem(id) {
    return apiClient.get(`/inventory/${id}/`);
  },

  // Update inventory item
  updateInventoryItem(id, inventoryData) {
    return apiClient.put(`/inventory/${id}/`, inventoryData);
  },

  // Bulk update inventory
  bulkUpdateInventory(updates) {
    return apiClient.post('/inventory/bulk-update/', updates);
  },

  // Get low stock alerts
  getLowStockItems(threshold = 10) {
    return apiClient.get('/inventory/', {
      params: { stock_quantity__lte: threshold }
    });
  },

  // Get inventory by product
  getInventoryByProduct(productId) {
    return apiClient.get('/inventory/', {
      params: { product: productId }
    });
  }
};
