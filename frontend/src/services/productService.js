import { BaseRequests } from './requests.js';

export class ProductService extends BaseRequests {
  static BASE_URL = 'products';

  /**
   * Get all products with pagination and filtering
   * @param {Object} params - Query parameters
   * @param {number} params.page - Page number
   * @param {string} params.search - Search query
   * @param {string} params.category - Category ID to filter by
   * @param {string} params.stock_status - Stock status filter (in_stock, low_stock, out_of_stock)
   * @param {string} params.status - Product status filter (active, inactive)
   * @param {number} params.min_price - Minimum price filter
   * @param {number} params.max_price - Maximum price filter
   * @param {string} params.ordering - Field to order by (e.g., 'name', '-created_at')
   * @returns {Promise<Object>} Response with products, pagination, and metadata
   */
  static async getAllProducts(params = {}) {
    return await this.get(`${this.BASE_URL}/`, params);
  }

  /**
   * Get a single product by ID
   * @param {string} productId - Product UUID
   * @returns {Promise<Object>} Product data
   */
  static async getProduct(productId) {
    return await this.get(`${this.BASE_URL}/${productId}/`);
  }

  /**
   * Create a new product
   * @param {Object} productData - Product data
   * @param {string} productData.name - Product name
   * @param {string} productData.description - Product description
   * @param {string} productData.price - Product price
   * @param {string} productData.sale_price - Sale price (optional)
   * @param {number} productData.stock - Stock quantity
   * @param {number} productData.min_stock - Minimum stock level
   * @param {string} productData.category_id - Category UUID
   * @param {string} productData.status - Product status (active/inactive)
   * @returns {Promise<Object>} Created product data
   */
  static async createProduct(productData) {
    // Transform frontend data to backend format
    const backendData = {
      name: productData.name,
      description: productData.description || '',
      price: parseFloat(productData.price),
      sale_price: productData.sale_price ? parseFloat(productData.sale_price) : null,
      stock: parseInt(productData.stock),
      min_stock: parseInt(productData.min_stock || productData.minStock || 0),
      category_id: productData.category_id || productData.category,
      status: productData.status || 'active'
    };

    return await this.post(`${this.BASE_URL}/`, backendData);
  }

  /**
   * Update an existing product
   * @param {string} productId - Product UUID
   * @param {Object} productData - Updated product data
   * @returns {Promise<Object>} Updated product data
   */
  static async updateProduct(productId, productData) {
    // Transform frontend data to backend format
    const backendData = {
      name: productData.name,
      description: productData.description || '',
      price: parseFloat(productData.price),
      sale_price: productData.sale_price ? parseFloat(productData.sale_price) : null,
      stock: parseInt(productData.stock),
      min_stock: parseInt(productData.min_stock || productData.minStock || 0),
      category_id: productData.category_id || productData.category,
      status: productData.status || 'active'
    };

    return await this.put(`${this.BASE_URL}/${productId}/`, backendData);
  }

  /**
   * Partially update a product
   * @param {string} productId - Product UUID
   * @param {Object} updates - Partial product data
   * @returns {Promise<Object>} Updated product data
   */
  static async patchProduct(productId, updates) {
    return await this.patch(`${this.BASE_URL}/${productId}/`, updates);
  }

  /**
   * Delete a product
   * @param {string} productId - Product UUID
   * @returns {Promise<void>}
   */
  static async deleteProduct(productId) {
    return await this.del(`${this.BASE_URL}/${productId}/`);
  }

  /**
   * Get products with low stock
   * @returns {Promise<Array>} Array of low stock products
   */
  static async getLowStockProducts() {
    return await this.get(`${this.BASE_URL}/low_stock/`);
  }

  /**
   * Get products that are out of stock
   * @returns {Promise<Array>} Array of out of stock products
   */
  static async getOutOfStockProducts() {
    return await this.get(`${this.BASE_URL}/out_of_stock/`);
  }

  /**
   * Bulk update stock for multiple products
   * @param {Array} updates - Array of {product_id, stock} objects
   * @returns {Promise<Object>} Bulk update result
   */
  static async bulkUpdateStock(updates) {
    return await this.post(`${this.BASE_URL}/bulk_stock_update/`, { updates });
  }

  /**
   * Bulk update status for multiple products
   * @param {Array} productIds - Array of product UUIDs
   * @param {string} status - New status (active/inactive)
   * @returns {Promise<Object>} Bulk update result
   */
  static async bulkUpdateStatus(productIds, status) {
    return await this.post(`${this.BASE_URL}/bulk_status_update/`, {
      product_ids: productIds,
      status
    });
  }

  /**
   * Get all categories for product creation/editing
   * @returns {Promise<Array>} Array of categories
   */
  static async getCategories() {
    return await this.get('products/categories/');
  }

  /**
   * Search products with advanced filtering
   * @param {Object} filters - Search and filter parameters
   * @returns {Promise<Object>} Filtered products with pagination
   */
  static async searchProducts(filters) {
    const params = {
      search: filters.search || '',
      category: filters.category || '',
      stock_status: filters.stockStatus || filters.stock_status || '',
      status: filters.status || '',
      min_price: filters.minPrice || filters.min_price || '',
      max_price: filters.maxPrice || filters.max_price || '',
      ordering: filters.ordering || '-created_at',
      page: filters.page || 1
    };

    // Remove empty parameters
    Object.keys(params).forEach(key => {
      if (params[key] === '' || params[key] === null || params[key] === undefined) {
        delete params[key];
      }
    });

    return await this.getAllProducts(params);
  }

  /**
   * Transform backend product data to frontend format
   * @param {Object} backendProduct - Product data from backend
   * @returns {Object} Frontend-formatted product data
   */
  static transformToFrontend(backendProduct) {
    return {
      id: backendProduct.id,
      name: backendProduct.name,
      description: backendProduct.description,
      price: parseFloat(backendProduct.price),
      sale_price: backendProduct.sale_price ? parseFloat(backendProduct.sale_price) : null,
      stock: backendProduct.stock,
      min_stock: backendProduct.min_stock,
      minStock: backendProduct.min_stock, // Alternative naming for compatibility
      category: backendProduct.category?.id || '',
      category_id: backendProduct.category?.id || '',
      category_name: backendProduct.category?.name || '',
      status: backendProduct.status,
      stock_status: backendProduct.stock_status,
      is_on_sale: backendProduct.is_on_sale,
      effective_price: parseFloat(backendProduct.effective_price),
      created_at: backendProduct.created_at,
      updated_at: backendProduct.updated_at
    };
  }

  /**
   * Transform multiple backend products to frontend format
   * @param {Array} backendProducts - Array of backend products
   * @returns {Array} Array of frontend-formatted products
   */
  static transformMultipleToFrontend(backendProducts) {
    return backendProducts.map(product => this.transformToFrontend(product));
  }
}

// Export both the class and an instance for different import styles
export const productService = ProductService;
