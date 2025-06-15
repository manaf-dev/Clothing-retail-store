import { BaseRequests } from './requests.js';

export class CustomerService extends BaseRequests {
  static BASE_URL = 'customers';

  /**
   * Get all customers with pagination and filtering
   * @param {Object} params - Query parameters
   * @param {number} params.page - Page number
   * @param {string} params.search - Search query
   * @param {string} params.status - Customer status filter
   * @param {string} params.ordering - Field to order by
   * @returns {Promise<Object>} Response with customers, pagination, and metadata
   */
  static async getAllCustomers(params = {}) {
    return await this.get(`${this.BASE_URL}/`, params);
  }

  /**
   * Get a single customer by ID
   * @param {string} customerId - Customer UUID
   * @returns {Promise<Object>} Customer data
   */
  static async getCustomer(customerId) {
    return await this.get(`${this.BASE_URL}/${customerId}/`);
  }

  /**
   * Create a new customer
   * @param {Object} customerData - Customer data
   * @param {string} customerData.name - Customer name
   * @param {string} customerData.email - Customer email
   * @param {string} customerData.phone - Customer phone
   * @param {string} customerData.address - Customer address
   * @returns {Promise<Object>} Created customer data
   */
  static async createCustomer(customerData) {
    return await this.post(`${this.BASE_URL}/`, customerData);
  }

  /**
   * Update an existing customer
   * @param {string} customerId - Customer UUID
   * @param {Object} customerData - Updated customer data
   * @returns {Promise<Object>} Updated customer data
   */
  static async updateCustomer(customerId, customerData) {
    return await this.put(`${this.BASE_URL}/${customerId}/`, customerData);
  }

  /**
   * Delete a customer
   * @param {string} customerId - Customer UUID
   * @returns {Promise<Object>} Deletion confirmation
   */
  static async deleteCustomer(customerId) {
    return await this.del(`${this.BASE_URL}/${customerId}/`);
  }

  /**
   * Search customers with advanced filtering
   * @param {Object} filters - Search and filter parameters
   * @returns {Promise<Object>} Filtered customers with pagination
   */
  static async searchCustomers(filters) {
    const params = {
      search: filters.search || '',
      status: filters.status || '',
      ordering: filters.ordering || 'name',
      page: filters.page || 1
    };

    // Remove empty parameters
    Object.keys(params).forEach(key => {
      if (params[key] === '' || params[key] === null || params[key] === undefined) {
        delete params[key];
      }
    });

    return await this.getAllCustomers(params);
  }

  /**
   * Transform backend customer data to frontend format
   * @param {Object} backendCustomer - Customer data from backend
   * @returns {Object} Frontend-formatted customer data
   */
  static transformToFrontend(backendCustomer) {
    return {
      id: backendCustomer.id,
      name: backendCustomer.name,
      email: backendCustomer.email,
      phone: backendCustomer.phone,
      address: backendCustomer.address,
      status: backendCustomer.status || 'active',
      totalOrders: backendCustomer.total_orders || 0,
      totalSpent: parseFloat(backendCustomer.total_spent || 0),
      lastOrder: backendCustomer.last_order_date,
      joinDate: backendCustomer.created_at?.split('T')[0], // Extract date part
      gender: backendCustomer.gender || '',
      dateOfBirth: backendCustomer.date_of_birth || '',
      createdAt: backendCustomer.created_at,
      updatedAt: backendCustomer.updated_at
    };
  }

  /**
   * Transform multiple backend customers to frontend format
   * @param {Array} backendCustomers - Array of backend customers
   * @returns {Array} Array of frontend-formatted customers
   */
  static transformMultipleToFrontend(backendCustomers) {
    return backendCustomers.map(customer => this.transformToFrontend(customer));
  }

  /**
   * Transform frontend customer data to backend format
   * @param {Object} frontendCustomer - Customer data from frontend
   * @returns {Object} Backend-formatted customer data
   */
  static transformToBackend(frontendCustomer) {
    return {
      name: frontendCustomer.name,
      email: frontendCustomer.email,
      phone: frontendCustomer.phone,
      address: frontendCustomer.address,
      status: frontendCustomer.status || 'active',
      gender: frontendCustomer.gender || '',
      date_of_birth: frontendCustomer.dateOfBirth || frontendCustomer.date_of_birth || null
    };
  }
}
