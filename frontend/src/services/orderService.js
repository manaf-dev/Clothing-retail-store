import { apiClient } from './api.js';

export const orderService = {
  // Get all orders
  getOrders(params = {}) {
    return apiClient.get('/orders/', { params }).then(response => response.data);
  },

  // Get order by ID
  getOrder(id) {
    return apiClient.get(`/orders/${id}/`).then(response => response.data);
  },

  // Create new order
  createOrder(orderData) {
    return apiClient.post('/orders/', orderData).then(response => response.data);
  },

  // Update order
  updateOrder(id, orderData) {
    return apiClient.put(`/orders/${id}/`, orderData).then(response => response.data);
  },

  // Delete order
  deleteOrder(id) {
    return apiClient.delete(`/orders/${id}/`).then(response => response.data);
  },

  // Get order items
  getOrderItems(orderId) {
    return apiClient.get(`/orders/${orderId}/items/`).then(response => response.data);
  },

  // Add item to order
  addOrderItem(orderItemData) {
    return apiClient.post('/order-items/', orderItemData).then(response => response.data);
  },

  // Update order item
  updateOrderItem(id, orderItemData) {
    return apiClient.put(`/order-items/${id}/`, orderItemData).then(response => response.data);
  },

  // Remove item from order
  removeOrderItem(id) {
    return apiClient.delete(`/order-items/${id}/`).then(response => response.data);
  }
};
