<script setup>
import { ref, onMounted, onUnmounted, nextTick, watch } from 'vue'
import { orderService } from '@/services/orderService'
import { AnalyticsService } from '@/services/analyticsService'

const loading = ref(true)
const selectedPeriod = ref('month')
const salesChart = ref(null)
const error = ref(null)

const metrics = ref({
  totalRevenue: 0,
  totalOrders: 0,
  averageOrderValue: 0,
  productsSold: 0,
  revenueChange: 0,
  ordersChange: 0,
  aovChange: 0,
  productsChange: 0
})

const topProducts = ref([])
const detailedOrders = ref([])
const salesData = ref([])
const trendsData = ref([])

const loadReports = async () => {
  try {
    loading.value = true
    error.value = null

    // Load analytics data from backend
    const [dashboardResponse, topProductsResponse, trendsResponse, ordersResponse] = await Promise.all([
      AnalyticsService.getDashboardAnalytics(selectedPeriod.value),
      AnalyticsService.getTopProducts({ period: selectedPeriod.value, limit: 5 }),
      AnalyticsService.getSalesTrends({ period: 'daily', days: 7 }),
      orderService.getOrders({ page: 1, page_size: 20, ordering: '-created_at' })
    ])

    // Process dashboard metrics - handle both direct data and nested response structure
    const dashboardData = dashboardResponse.data || dashboardResponse;
    const currentMetrics = dashboardData[selectedPeriod.value === 'today' ? 'today' : 
                                        selectedPeriod.value === 'week' ? 'this_week' : 
                                        'this_month'] || dashboardData.this_month || dashboardData || {}

    metrics.value = {
      totalRevenue: parseFloat(currentMetrics.total_revenue || 0),
      totalOrders: parseInt(currentMetrics.total_orders || 0),
      averageOrderValue: parseFloat(currentMetrics.average_order_value || 0),
      productsSold: parseInt(currentMetrics.products_sold || 0),
      revenueChange: parseFloat(currentMetrics.revenue_growth || 0),
      ordersChange: parseFloat(currentMetrics.order_growth || 0),
      aovChange: parseFloat(currentMetrics.aov_growth || 0),
      productsChange: parseFloat(currentMetrics.products_growth || 0)
    }

    // Process top products - handle both direct array and nested response
    const topProductsData = topProductsResponse.data || topProductsResponse;
    topProducts.value = (Array.isArray(topProductsData) ? topProductsData : []).map(product => ({
      id: product.product_id,
      name: product.product_name,
      quantity_sold: product.total_quantity,
      revenue: parseFloat(product.total_revenue || 0)
    }))

    // Process trends data - handle both direct array and nested response
    const trendsData_raw = trendsResponse.data || trendsResponse;
    trendsData.value = Array.isArray(trendsData_raw) ? trendsData_raw : []

    // Load recent orders - handle both direct array and paginated response
    const ordersData = ordersResponse.data || ordersResponse;
    detailedOrders.value = ordersData.results || ordersData || []

    // Generate sales chart with real data
    await generateSalesChart()
  } catch (err) {
    error.value = 'Failed to load reports data. Please try again.'
  } finally {
    loading.value = false
  }
}

watch([trendsData, loading], async () => {
  if (!loading.value && trendsData.value) {
    await generateSalesChart();
  }
});

const generateSalesChart = async () => {
  try {
    await nextTick()
    await new Promise(resolve => setTimeout(resolve, 150))

    if (!salesChart.value) return

    const container = salesChart.value.parentElement;
    if (!container) return

    const containerWidth = container.clientWidth;
    const containerHeight = 200;

    if (containerWidth === 0) {
      setTimeout(generateSalesChart, 300);
      return
    }

    const dpr = window.devicePixelRatio || 1;
    const actualWidth = containerWidth * dpr;
    const actualHeight = containerHeight * dpr;

    salesChart.value.width = actualWidth;
    salesChart.value.height = actualHeight;
    salesChart.value.style.width = containerWidth + 'px';
    salesChart.value.style.height = containerHeight + 'px';

    const ctx = salesChart.value.getContext('2d');
    if (!ctx) return;

    ctx.scale(dpr, dpr);
    ctx.clearRect(0, 0, containerWidth, containerHeight);
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';

    let chartData = [];
    if (trendsData.value && trendsData.value.length > 0) {
      chartData = trendsData.value.map(item => ({
        label: new Date(item.date).toLocaleDateString('en-US', { weekday: 'short' }),
        value: parseFloat(item.total_revenue || 0)
      }));
    } else {
      const days = [];
      for (let i = 6; i >= 0; i--) {
        const date = new Date();
        date.setDate(date.getDate() - i);
        days.push({
          label: date.toLocaleDateString('en-US', { weekday: 'short' }),
          value: Math.random() * 1500 + 200
        });
      }
      chartData = days;
    }

    if (chartData.length === 0) {
      ctx.fillStyle = '#6b7280';
      ctx.font = '16px Arial, sans-serif';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText('No data available', containerWidth / 2, containerHeight / 2);
      return;
    }

    const padding = 40;
    const chartWidth = containerWidth - 2 * padding;
    const chartHeight = containerHeight - 2 * padding;

    const values = chartData.map(item => item.value);
    const maxValue = Math.max(...values, 1);
    const minValue = Math.min(...values, 0);
    const range = maxValue - minValue || 1;

    ctx.strokeStyle = '#f3f4f6';
    ctx.lineWidth = 1;
    for (let i = 1; i < 4; i++) {
      const y = padding + (i * chartHeight / 4);
      ctx.beginPath();
      ctx.moveTo(padding, y);
      ctx.lineTo(padding + chartWidth, y);
      ctx.stroke();
    }

    ctx.strokeStyle = '#3B82F6';
    ctx.lineWidth = 3;
    ctx.beginPath();

    let hasValidPoints = false;
    values.forEach((value, index) => {
      const x = padding + (index * chartWidth) / Math.max(values.length - 1, 1);
      const y = padding + chartHeight - ((value - minValue) / range) * chartHeight;
      if (index === 0) {
        ctx.moveTo(x, y);
      } else {
        ctx.lineTo(x, y);
      }
      hasValidPoints = true;
    });

    if (hasValidPoints) {
      ctx.stroke();
    }

    ctx.fillStyle = '#3B82F6';
    values.forEach((value, index) => {
      const x = padding + (index * chartWidth) / Math.max(values.length - 1, 1);
      const y = padding + chartHeight - ((value - minValue) / range) * chartHeight;
      ctx.beginPath();
      ctx.arc(x, y, 5, 0, 2 * Math.PI);
      ctx.fill();
      ctx.strokeStyle = '#ffffff';
      ctx.lineWidth = 2;
      ctx.stroke();
      ctx.strokeStyle = '#3B82F6';
    });

    ctx.fillStyle = '#6b7280';
    ctx.font = '12px Arial, sans-serif';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'top';
    chartData.forEach((item, index) => {
      const x = padding + (index * chartWidth) / Math.max(values.length - 1, 1);
      ctx.fillText(item.label, x, containerHeight - 25);
    });

    ctx.textAlign = 'right';
    ctx.textBaseline = 'middle';
    const steps = 4;
    for (let i = 0; i <= steps; i++) {
      const value = minValue + (range * i / steps);
      const y = padding + chartHeight - (i * chartHeight / steps);
      const label = value >= 1000 ? '$' + (value / 1000).toFixed(1) + 'k' : '$' + Math.round(value);
      ctx.fillText(label, padding - 10, y);
    }
  } catch (err) {
    if (salesChart.value) {
      const ctx = salesChart.value.getContext('2d');
      if (ctx) {
        ctx.fillStyle = '#ef4444';
        ctx.font = '14px Arial, sans-serif';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        const container = salesChart.value.parentElement;
        const width = container ? container.clientWidth : 400;
        const height = 200;
        ctx.fillText('Error rendering chart', width / 2, height / 2);
      }
    }
  }
}

const exportReport = async () => {
  try {
    if (!detailedOrders.value || detailedOrders.value.length === 0) {
      error.value = 'No data available to export for the selected period'
      return
    }
    const csvContent = [
      ['Date', 'Order ID', 'Customer', 'Items', 'Total', 'Status', 'Payment Method'],
      ...detailedOrders.value.map(order => [
        formatDate(order.created_at),
        `#${order.order_number || order.id}`,
        order.customer_name || order.customer?.name || 'Walk-in Customer',
        order.items?.length || order.item_count || 0,
        order.total,
        order.status || 'Pending',
        order.payment_method || 'N/A'
      ])
    ].map(row => row.join(',')).join('\n')

    const blob = new Blob([csvContent], { type: 'text/csv' })
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `sales-report-${selectedPeriod.value}-${new Date().toISOString().split('T')[0]}.csv`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    window.URL.revokeObjectURL(url)
  } catch (err) {
    error.value = 'Failed to export report. Please try again.'
  }
}

const refreshReports = async () => {
  await loadReports()
}

const testApiEndpoints = async () => {
  try {
    // For debugging only
    const dashboardUrl = '/api/orders/sales/analytics/dashboard/?period=month';
    const trendsUrl = '/api/orders/sales/analytics/trends/?period=daily&days=7';
    // You can log or test endpoints here if needed
  } catch (err) {}
};

const debugChartState = () => {
  // For debugging only
  if (salesChart.value) {
    const container = salesChart.value.parentElement;
    const ctx = salesChart.value.getContext('2d');
  }
};

const formatNumber = (num) => {
  return new Intl.NumberFormat('en-US', {
    minimumFractionDigits: 0,
    maximumFractionDigits: 2
  }).format(num)
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

onMounted(() => {
  loadReports()
  let resizeObserver
  if (window.ResizeObserver && salesChart.value) {
    resizeObserver = new ResizeObserver(() => {
      if (!loading.value) {
        generateSalesChart()
      }
    })
    const container = salesChart.value.parentElement
    if (container) {
      resizeObserver.observe(container)
    }
  }
  onUnmounted(() => {
    if (resizeObserver) resizeObserver.disconnect()
  })
})
</script>


<template>
  <div class="reports-container">
    <div class="reports-header">
      <h2>Reports & Analytics</h2>
      <div class="header-actions">
        <select v-model="selectedPeriod" @change="loadReports" class="period-select">
          <option value="today">Today</option>
          <option value="week">This Week</option>
          <option value="month">This Month</option>
          <option value="quarter">This Quarter</option>
          <option value="year">This Year</option>
        </select>
        <button @click="refreshReports" class="refresh-btn" :disabled="loading">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
          </svg>
          Refresh
        </button>
        <button @click="exportReport" class="export-btn" :disabled="loading">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
          </svg>
          Export CSV
        </button>
      </div>
    </div>

    <!-- Error State -->
    <div v-if="error" class="error-container">
      <div class="error-message">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
        </svg>
        {{ error }}
      </div>
      <button @click="refreshReports" class="retry-btn">Try Again</button>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading-container">
      <div class="loading-spinner"></div>
      <p>Loading reports...</p>
    </div>

    <!-- Reports Content -->
    <div v-else class="reports-content">
      <!-- Key Metrics -->
      <div class="metrics-grid">
        <div class="metric-card">
          <div class="metric-icon revenue">
            <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1"></path>
            </svg>
          </div>
          <div class="metric-content">
            <h3>Total Revenue</h3>
            <p class="metric-value">${{ formatNumber(metrics.totalRevenue) }}</p>
            <span class="metric-change" :class="{ positive: metrics.revenueChange >= 0, negative: metrics.revenueChange < 0 }">
              {{ metrics.revenueChange >= 0 ? '+' : '' }}{{ metrics.revenueChange.toFixed(1) }}%
            </span>
          </div>
        </div>

        <div class="metric-card">
          <div class="metric-icon orders">
            <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"></path>
            </svg>
          </div>
          <div class="metric-content">
            <h3>Total Orders</h3>
            <p class="metric-value">{{ formatNumber(metrics.totalOrders) }}</p>
            <span class="metric-change" :class="{ positive: metrics.ordersChange >= 0, negative: metrics.ordersChange < 0 }">
              {{ metrics.ordersChange >= 0 ? '+' : '' }}{{ metrics.ordersChange.toFixed(1) }}%
            </span>
          </div>
        </div>

        <div class="metric-card">
          <div class="metric-icon average">
            <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
            </svg>
          </div>
          <div class="metric-content">
            <h3>Average Order Value</h3>
            <p class="metric-value">${{ formatNumber(metrics.averageOrderValue) }}</p>
            <span class="metric-change" :class="{ positive: metrics.aovChange >= 0, negative: metrics.aovChange < 0 }">
              {{ metrics.aovChange >= 0 ? '+' : '' }}{{ metrics.aovChange.toFixed(1) }}%
            </span>
          </div>
        </div>

        <div class="metric-card">
          <div class="metric-icon products">
            <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"></path>
            </svg>
          </div>
          <div class="metric-content">
            <h3>Products Sold</h3>
            <p class="metric-value">{{ formatNumber(metrics.productsSold) }}</p>
            <span class="metric-change" :class="{ positive: metrics.productsChange >= 0, negative: metrics.productsChange < 0 }">
              {{ metrics.productsChange >= 0 ? '+' : '' }}{{ metrics.productsChange.toFixed(1) }}%
            </span>
          </div>
        </div>
      </div>

      <!-- Charts Section -->
      <div class="charts-section">
        <div class="chart-container">
          <div class="chart-header">
            <h3>Sales Trend</h3>
            <button @click="generateSalesChart" class="regenerate-chart-btn" :disabled="loading">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
              </svg>
              Regenerate Chart
            </button>
          </div>
          <div class="chart-placeholder">
            <canvas ref="salesChart" width="400" height="200"></canvas>
            <div v-if="loading" class="chart-loading">
              <div class="loading-spinner"></div>
              <p>Loading chart data...</p>
            </div>
            <div v-else-if="!trendsData.length" class="chart-error">
              <p>No chart data available</p>
            </div>
          </div>
        </div>

        <div class="chart-container">
          <h3>Top Products</h3>
          <div class="top-products-list">
            <div v-if="topProducts.length > 0">
              <div v-for="(product, index) in topProducts" :key="product.id" class="product-item">
                <span class="rank">{{ index + 1 }}</span>
                <div class="product-info">
                  <span class="product-name">{{ product.name }}</span>
                  <span class="product-sales">{{ product.quantity_sold }} sold</span>
                </div>
                <span class="product-revenue">${{ formatNumber(product.revenue) }}</span>
              </div>
            </div>
            <div v-else class="no-data">
              <p>No product sales data available for the selected period</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Detailed Reports Table -->
      <div class="detailed-reports">
        <h3>Detailed Sales Report</h3>
        <div class="table-container">
          <table class="reports-table">
            <thead>
              <tr>
                <th>Date</th>
                <th>Order ID</th>
                <th>Customer</th>
                <th>Items</th>
                <th>Total</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="order in detailedOrders" :key="order.id">
                <td>{{ formatDate(order.created_at) }}</td>
                <td>#{{ order.order_number || order.id }}</td>
                <td>{{ order.customer_name || order.customer?.name || 'Walk-in Customer' }}</td>
                <td>{{ order.items?.length || order.item_count || 0 }}</td>
                <td>${{ formatNumber(order.total) }}</td>
                <td>
                  <span class="status-badge" :class="(order.status || 'pending').toLowerCase()">
                    {{ order.status || 'Pending' }}
                  </span>
                </td>
              </tr>
              <tr v-if="detailedOrders.length === 0">
                <td colspan="6" style="text-align: center; padding: 20px; color: #6b7280;">
                  No orders found for the selected period
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>



<style scoped>
.reports-container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.reports-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.reports-header h2 {
  color: #1f2937;
  font-size: 24px;
  font-weight: 600;
  margin: 0;
}

.header-actions {
  display: flex;
  gap: 15px;
  align-items: center;
}

.period-select {
  padding: 8px 12px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  background: white;
  color: #374151;
  font-size: 14px;
}

.export-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.2s;
}

.export-btn:hover:not(:disabled) {
  background: #2563eb;
}

.export-btn:disabled {
  background: #9ca3af;
  cursor: not-allowed;
}

.refresh-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: #10b981;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.2s;
}

.refresh-btn:hover:not(:disabled) {
  background: #059669;
}

.refresh-btn:disabled {
  background: #9ca3af;
  cursor: not-allowed;
}

.error-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 8px;
  margin-bottom: 20px;
}

.error-message {
  display: flex;
  align-items: center;
  gap: 12px;
  color: #dc2626;
  font-size: 16px;
  margin-bottom: 16px;
}

.retry-btn {
  padding: 8px 16px;
  background: #dc2626;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.2s;
}

.retry-btn:hover {
  background: #b91c1c;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  color: #6b7280;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #f3f4f6;
  border-top: 3px solid #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.metric-card {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 16px;
}

.metric-icon {
  width: 48px;
  height: 48px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.metric-icon.revenue { background: #10b981; }
.metric-icon.orders { background: #3b82f6; }
.metric-icon.average { background: #8b5cf6; }
.metric-icon.products { background: #f59e0b; }

.metric-content h3 {
  color: #6b7280;
  font-size: 14px;
  font-weight: 500;
  margin: 0 0 4px 0;
}

.metric-value {
  color: #1f2937;
  font-size: 24px;
  font-weight: 600;
  margin: 0 0 4px 0;
}

.metric-change {
  font-size: 12px;
  font-weight: 500;
}

.metric-change.positive { color: #10b981; }
.metric-change.negative { color: #ef4444; }

.charts-section {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 20px;
  margin-bottom: 30px;
}

.chart-container {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.chart-container h3 {
  color: #1f2937;
  font-size: 18px;
  font-weight: 600;
  margin: 0 0 20px 0;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.chart-header h3 {
  margin: 0;
}

.regenerate-chart-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  background: #f3f4f6;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  color: #374151;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.2s;
}

.regenerate-chart-btn:hover:not(:disabled) {
  background: #e5e7eb;
  border-color: #9ca3af;
}

.regenerate-chart-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.chart-placeholder {
  width: 100%;
  height: 200px;
  border: 1px solid #e5e7eb;
  border-radius: 4px;
  overflow: hidden;
  position: relative;
}

.chart-placeholder canvas {
  display: block;
  max-width: 100%;
  height: 200px;
  border: none;
  background: #ffffff;
}

.chart-error {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: #6b7280;
  font-style: italic;
  text-align: center;
}

.chart-loading {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  color: #6b7280;
}

.chart-loading .loading-spinner {
  width: 24px;
  height: 24px;
  border: 2px solid #f3f4f6;
  border-top: 2px solid #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.top-products-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.product-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: #f9fafb;
  border-radius: 6px;
}

.rank {
  width: 24px;
  height: 24px;
  background: #3b82f6;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 600;
}

.product-info {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.product-name {
  color: #1f2937;
  font-weight: 500;
  font-size: 14px;
}

.product-sales {
  color: #6b7280;
  font-size: 12px;
}

.product-revenue {
  color: #1f2937;
  font-weight: 600;
  font-size: 14px;
}

.no-data {
  text-align: center;
  padding: 20px;
  color: #6b7280;
  font-style: italic;
}

.detailed-reports {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.detailed-reports h3 {
  color: #1f2937;
  font-size: 18px;
  font-weight: 600;
  margin: 0 0 20px 0;
}

.table-container {
  overflow-x: auto;
}

.reports-table {
  width: 100%;
  border-collapse: collapse;
}

.reports-table th {
  background: #f9fafb;
  color: #374151;
  font-weight: 600;
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #e5e7eb;
}

.reports-table td {
  padding: 12px;
  border-bottom: 1px solid #f3f4f6;
  color: #1f2937;
}

.status-badge {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
  text-transform: uppercase;
}

.status-badge.completed {
  background: #d1fae5;
  color: #065f46;
}

.status-badge.pending {
  background: #fef3c7;
  color: #92400e;
}

.status-badge.processing {
  background: #dbeafe;
  color: #1e40af;
}

@media (max-width: 768px) {
  .charts-section {
    grid-template-columns: 1fr;
  }
  
  .metrics-grid {
    grid-template-columns: 1fr;
  }
  
  .header-actions {
    flex-direction: column;
    gap: 10px;
  }
}

.test-btn {
  background: #8b5cf6;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.2s;
}

.test-btn:hover {
  background: #7c3aed;
}
</style>