import { BaseRequests } from './requests.js';

export class AnalyticsService extends BaseRequests {
  static BASE_URL = 'orders/sales/analytics';

  /**
   * Get comprehensive dashboard analytics data
   * @param {string} period - Period filter (today, week, month)
   * @returns {Promise<Object>} Dashboard analytics data
   */
  static async getDashboardAnalytics(period = 'month') {
    return await this.get(`${this.BASE_URL}/dashboard/`, { period });
  }

  /**
   * Get sales trends over time
   * @param {Object} params - Query parameters
   * @param {string} params.period - Period type (daily, weekly, monthly)
   * @param {number} params.days - Number of days to include
   * @returns {Promise<Object>} Sales trends data
   */
  static async getSalesTrends(params = {}) {
    const queryParams = {
      period: params.period || 'daily',
      days: params.days || 30
    };
    return await this.get(`${this.BASE_URL}/trends/`, queryParams);
  }

  /**
   * Get top selling products
   * @param {Object} params - Query parameters
   * @param {string} params.period - Period filter (day, week, month, year)
   * @param {number} params.limit - Number of products to return
   * @returns {Promise<Array>} Top products data
   */
  static async getTopProducts(params = {}) {
    const queryParams = {
      period: params.period || 'month',
      limit: params.limit || 10
    };
    return await this.get(`${this.BASE_URL}/top_products/`, queryParams);
  }

  /**
   * Get payment method breakdown
   * @param {Object} params - Query parameters
   * @param {string} params.start_date - Start date (YYYY-MM-DD)
   * @param {string} params.end_date - End date (YYYY-MM-DD)
   * @returns {Promise<Array>} Payment method statistics
   */
  static async getPaymentMethodStats(params = {}) {
    // If no dates provided, use current month by default
    if (!params.start_date || !params.end_date) {
      const today = new Date();
      const firstDay = new Date(today.getFullYear(), today.getMonth(), 1);
      const lastDay = new Date(today.getFullYear(), today.getMonth() + 1, 0);
      
      params = {
        start_date: firstDay.toISOString().split('T')[0],
        end_date: lastDay.toISOString().split('T')[0],
        ...params
      };
    }
    return await this.get(`${this.BASE_URL}/payment_methods/`, params);
  }

  /**
   * Get daily sales report
   * @param {Object} params - Query parameters
   * @param {string} params.start_date - Start date (YYYY-MM-DD)
   * @param {string} params.end_date - End date (YYYY-MM-DD)
   * @returns {Promise<Array>} Daily sales report data
   */
  static async getDailySalesReport(params = {}) {
    return await this.get(`${this.BASE_URL}/daily_report/`, params);
  }

  /**
   * Get weekly sales report
   * @param {Object} params - Query parameters
   * @param {string} params.start_date - Start date (YYYY-MM-DD)
   * @param {string} params.end_date - End date (YYYY-MM-DD)
   * @returns {Promise<Array>} Weekly sales report data
   */
  static async getWeeklySalesReport(params = {}) {
    return await this.get(`${this.BASE_URL}/weekly_report/`, params);
  }

  /**
   * Get monthly sales report
   * @param {Object} params - Query parameters
   * @param {string} params.start_date - Start date (YYYY-MM-DD)
   * @param {string} params.end_date - End date (YYYY-MM-DD)
   * @returns {Promise<Array>} Monthly sales report data
   */
  static async getMonthlySalesReport(params = {}) {
    return await this.get(`${this.BASE_URL}/monthly_report/`, params);
  }

  /**
   * Get customer-related statistics
   * @param {Object} params - Query parameters
   * @param {string} params.period - Period filter (day, week, month, year)
   * @returns {Promise<Object>} Customer statistics
   */
  static async getCustomerStats(params = {}) {
    const queryParams = {
      period: params.period || 'month'
    };
    return await this.get(`${this.BASE_URL}/customer_stats/`, queryParams);
  }

  /**
   * Calculate period comparison for metrics
   * @param {number} current - Current period value
   * @param {number} previous - Previous period value
   * @returns {number} Percentage change
   */
  static calculatePercentageChange(current, previous) {
    if (previous === 0) return current > 0 ? 100 : 0;
    return ((current - previous) / previous) * 100;
  }

  /**
   * Get date range for period
   * @param {string} period - Period type (today, week, month, quarter, year)
   * @returns {Object} Start and end dates
   */
  static getDateRangeForPeriod(period) {
    const now = new Date();
    const startDate = new Date();
    const endDate = new Date();

    switch (period) {
      case 'today':
        startDate.setHours(0, 0, 0, 0);
        endDate.setHours(23, 59, 59, 999);
        break;
      case 'week':
        startDate.setDate(now.getDate() - now.getDay()); // Start of week (Sunday)
        startDate.setHours(0, 0, 0, 0);
        endDate.setDate(startDate.getDate() + 6); // End of week (Saturday)
        endDate.setHours(23, 59, 59, 999);
        break;
      case 'month':
        startDate.setDate(1);
        startDate.setHours(0, 0, 0, 0);
        endDate.setMonth(startDate.getMonth() + 1, 0); // Last day of month
        endDate.setHours(23, 59, 59, 999);
        break;
      case 'quarter':
        const quarterStart = Math.floor(now.getMonth() / 3) * 3;
        startDate.setMonth(quarterStart, 1);
        startDate.setHours(0, 0, 0, 0);
        endDate.setMonth(quarterStart + 3, 0); // Last day of quarter
        endDate.setHours(23, 59, 59, 999);
        break;
      case 'year':
        startDate.setMonth(0, 1);
        startDate.setHours(0, 0, 0, 0);
        endDate.setMonth(11, 31);
        endDate.setHours(23, 59, 59, 999);
        break;
      default:
        // Default to current month
        startDate.setDate(1);
        startDate.setHours(0, 0, 0, 0);
        endDate.setMonth(startDate.getMonth() + 1, 0);
        endDate.setHours(23, 59, 59, 999);
    }

    return {
      start_date: startDate.toISOString().split('T')[0],
      end_date: endDate.toISOString().split('T')[0]
    };
  }

  /**
   * Transform backend analytics data to frontend format
   * @param {Object} backendData - Analytics data from backend
   * @returns {Object} Frontend-formatted analytics data
   */
  static transformAnalyticsData(backendData) {
    return {
      totalRevenue: parseFloat(backendData.total_revenue || 0),
      totalOrders: parseInt(backendData.total_orders || 0),
      averageOrderValue: parseFloat(backendData.average_order_value || 0),
      productsSold: parseInt(backendData.products_sold || 0),
      totalCustomers: parseInt(backendData.total_customers || 0),
      returningCustomers: parseInt(backendData.returning_customers || 0),
      newCustomers: parseInt(backendData.new_customers || 0),
      revenueGrowth: parseFloat(backendData.revenue_growth || 0),
      orderGrowth: parseFloat(backendData.order_growth || 0),
      customerGrowth: parseFloat(backendData.customer_growth || 0)
    };
  }

  /**
   * Export analytics data to CSV
   * @param {Array} data - Data to export
   * @param {string} filename - Filename for the export
   * @param {Array} columns - Column definitions
   */
  static exportToCSV(data, filename, columns) {
    const csvContent = [
      columns.map(col => col.header).join(','),
      ...data.map(row => 
        columns.map(col => {
          const value = col.accessor ? row[col.accessor] : row[col.key];
          return typeof value === 'string' && value.includes(',') 
            ? `"${value}"` 
            : value;
        }).join(',')
      )
    ].join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    window.URL.revokeObjectURL(url);
  }
}
