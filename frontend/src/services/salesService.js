import { BaseRequests } from './requests.js';

export class SalesService extends BaseRequests {
  static BASE_URL = 'orders';

  /**
   * Get all orders/sales with pagination and filtering
   * @param {Object} params - Query parameters
   * @param {number} params.page - Page number
   * @param {string} params.search - Search query
   * @param {string} params.status - Order status filter
   * @param {string} params.payment_status - Payment status filter
   * @param {string} params.start_date - Start date filter (YYYY-MM-DD)
   * @param {string} params.end_date - End date filter (YYYY-MM-DD)
   * @param {string} params.customer - Customer ID or name filter
   * @param {string} params.ordering - Field to order by (e.g., '-created_at')
   * @returns {Promise<Object>} Response with orders, pagination, and metadata
   */
  static async getAllOrders(params = {}) {
    return await this.get(`${this.BASE_URL}/`, params);
  }

  /**
   * Get a single order by ID
   * @param {string} orderId - Order UUID
   * @returns {Promise<Object>} Order data with items
   */
  static async getOrder(orderId) {
    return await this.get(`${this.BASE_URL}/${orderId}/`);
  }

  /**
   * Create a new order/sale
   * @param {Object} orderData - Order data
   * @param {string} orderData.customer_id - Customer UUID (optional)
   * @param {Array} orderData.items - Array of order items
   * @param {string} orderData.payment_method - Payment method
   * @param {string} orderData.notes - Order notes (optional)
   * @param {number} orderData.discount_amount - Discount amount (optional)
   * @param {number} orderData.tax_amount - Tax amount (optional)
   * @returns {Promise<Object>} Created order data
   */
  static async createOrder(orderData) {
    // Transform frontend data to backend format
    const backendData = {
      customer: orderData.customer_id || null,
      items: orderData.items.map(item => ({
        product_id: item.product_id,
        quantity: parseInt(item.quantity),
        price: parseFloat(item.price)
      })),
      payment_method: orderData.payment_method,
      notes: orderData.notes || '',
      discount_amount: parseFloat(orderData.discount_amount || 0),
      tax_amount: parseFloat(orderData.tax_amount || 0)
    };

    return await this.post(`${this.BASE_URL}/`, backendData);
  }

  /**
   * Update an existing order
   * @param {string} orderId - Order UUID
   * @param {Object} orderData - Updated order data
   * @returns {Promise<Object>} Updated order data
   */
  static async updateOrder(orderId, orderData) {
    return await this.put(`${this.BASE_URL}/${orderId}/`, orderData);
  }

  /**
   * Cancel an order
   * @param {string} orderId - Order UUID
   * @returns {Promise<Object>} Updated order data
   */
  static async cancelOrder(orderId) {
    return await this.post(`${this.BASE_URL}/${orderId}/cancel/`);
  }

  /**
   * Complete an order
   * @param {string} orderId - Order UUID
   * @returns {Promise<Object>} Updated order data
   */
  static async completeOrder(orderId) {
    return await this.post(`${this.BASE_URL}/${orderId}/complete/`);
  }

  /**
   * Get sales analytics/reports
   * @param {Object} params - Query parameters for analytics
   * @param {string} params.period - Period filter (daily, weekly, monthly)
   * @param {string} params.start_date - Start date (YYYY-MM-DD)
   * @param {string} params.end_date - End date (YYYY-MM-DD)
   * @returns {Promise<Object>} Sales analytics data
   */
  static async getSalesAnalytics(params = {}) {
    return await this.get(`${this.BASE_URL}/analytics/`, params);
  }

  /**
   * Get sales summary (daily, weekly, monthly totals)
   * @returns {Promise<Object>} Sales summary data
   */
  static async getSalesSummary() {
    return await this.get(`${this.BASE_URL}/analytics/summary/`);
  }

  /**
   * Get top selling products
   * @param {Object} params - Query parameters
   * @param {number} params.limit - Number of products to return
   * @param {string} params.period - Period filter (daily, weekly, monthly)
   * @returns {Promise<Array>} Array of top products
   */
  static async getTopProducts(params = {}) {
    return await this.get(`${this.BASE_URL}/analytics/top-products/`, params);
  }

  /**
   * Get payment method analytics
   * @param {Object} params - Query parameters
   * @param {string} params.period - Period filter (daily, weekly, monthly)
   * @returns {Promise<Array>} Payment method statistics
   */
  static async getPaymentMethodAnalytics(params = {}) {
    return await this.get(`${this.BASE_URL}/analytics/payment-methods/`, params);
  }

  /**
   * Search orders with advanced filtering
   * @param {Object} filters - Search and filter parameters
   * @returns {Promise<Object>} Filtered orders with pagination
   */
  static async searchOrders(filters) {
    const params = {
      search: filters.search || '',
      status: filters.status || '',
      payment_status: filters.payment_status || '',
      start_date: filters.start_date || filters.startDate || '',
      end_date: filters.end_date || filters.endDate || '',
      customer: filters.customer || '',
      ordering: filters.ordering || '-created_at',
      page: filters.page || 1
    };

    // Remove empty parameters
    Object.keys(params).forEach(key => {
      if (params[key] === '' || params[key] === null || params[key] === undefined) {
        delete params[key];
      }
    });

    return await this.getAllOrders(params);
  }

  /**
   * Transform backend order data to frontend format
   * @param {Object} backendOrder - Order data from backend
   * @returns {Object} Frontend-formatted order data
   */
  static transformToFrontend(backendOrder) {
    return {
      id: backendOrder.id,
      invoiceNumber: backendOrder.order_number,
      orderNumber: backendOrder.order_number,
      date: new Date(backendOrder.created_at),
      customer: backendOrder.customer ? {
        id: backendOrder.customer.id,
        name: backendOrder.customer.name,
        email: backendOrder.customer.email,
        phone: backendOrder.customer.phone,
        address: backendOrder.customer.address
      } : null,
      items: backendOrder.items?.map(item => ({
        id: item.id,
        product: {
          id: item.product?.id,
          name: item.product_name,
          sku: item.product?.sku || 'N/A'
        },
        quantity: item.quantity,
        price: parseFloat(item.price),
        discount: parseFloat(item.discount || 0),
        total: parseFloat(item.line_total || (item.price * item.quantity))
      })) || [],
      subtotal: parseFloat(backendOrder.subtotal),
      taxAmount: parseFloat(backendOrder.tax_amount),
      tax: parseFloat(backendOrder.tax_amount), // Alternative naming
      discountAmount: parseFloat(backendOrder.discount_amount),
      total: parseFloat(backendOrder.total),
      status: this.formatStatus(backendOrder.status),
      paymentMethod: backendOrder.payment_method,
      paymentStatus: backendOrder.payment_status,
      notes: backendOrder.notes || '',
      servedBy: backendOrder.served_by || '',
      createdAt: backendOrder.created_at,
      updatedAt: backendOrder.updated_at,
      completedAt: backendOrder.completed_at
    };
  }

  /**
   * Transform frontend order data to backend format
   * @param {Object} frontendOrder - Order data from frontend
   * @returns {Object} Backend-formatted order data
   */
  static transformToBackend(frontendOrder) {
    return {
      customer: frontendOrder.customer_id || frontendOrder.customerId,
      items: frontendOrder.items?.map(item => ({
        product_id: item.product_id || item.productId,
        quantity: parseInt(item.quantity),
        price: parseFloat(item.price),
        discount: parseFloat(item.discount || 0)
      })) || [],
      payment_method: frontendOrder.payment_method || frontendOrder.paymentMethod,
      notes: frontendOrder.notes || '',
      discount_amount: parseFloat(frontendOrder.discount_amount || frontendOrder.discountAmount || 0),
      tax_amount: parseFloat(frontendOrder.tax_amount || frontendOrder.taxAmount || 0),
      served_by: frontendOrder.served_by || frontendOrder.servedBy || ''
    };
  }

  /**
   * Format status for display
   * @param {string} status - Backend status
   * @returns {string} Formatted status
   */
  static formatStatus(status) {
    const statusMap = {
      'pending': 'Pending',
      'processing': 'Processing',
      'completed': 'Completed',
      'cancelled': 'Cancelled',
      'refunded': 'Refunded'
    };
    return statusMap[status] || status;
  }

  /**
   * Transform multiple backend orders to frontend format
   * @param {Array} backendOrders - Array of backend orders
   * @returns {Array} Array of frontend-formatted orders
   */
  static transformMultipleToFrontend(backendOrders) {
    return backendOrders.map(order => this.transformToFrontend(order));
  }
}
