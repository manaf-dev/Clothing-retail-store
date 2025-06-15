import { apiClient } from './api.js';

export const orderService = {
  // Get all orders
  getOrders(params = {}) {
    return apiClient.get('/orders/', { params });
  },

  // Get order by ID
  getOrder(id) {
    return apiClient.get(`/orders/${id}/`);
  },

  // Create new order
  createOrder(orderData) {
    return apiClient.post('/orders/', orderData);
  },

  // Update order
  updateOrder(id, orderData) {
    return apiClient.put(`/orders/${id}/`, orderData);
  },

  // Delete order
  deleteOrder(id) {
    return apiClient.delete(`/orders/${id}/`);
  },

  // Get order items
  getOrderItems(orderId) {
    return apiClient.get(`/orders/${orderId}/items/`);
  },

  // Add item to order
  addOrderItem(orderItemData) {
    return apiClient.post('/order-items/', orderItemData);
  },

  // Update order item
  updateOrderItem(id, orderItemData) {
    return apiClient.put(`/order-items/${id}/`, orderItemData);
  },

  // Remove item from order
  removeOrderItem(id) {
    return apiClient.delete(`/order-items/${id}/`);
  }
};
