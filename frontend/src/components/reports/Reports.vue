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
        <button @click="exportReport" class="export-btn">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
          </svg>
          Export CSV
        </button>
      </div>
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
          <h3>Sales Trend</h3>
          <div class="chart-placeholder">
            <canvas ref="salesChart" width="400" height="200"></canvas>
          </div>
        </div>

        <div class="chart-container">
          <h3>Top Products</h3>
          <div class="top-products-list">
            <div v-for="(product, index) in topProducts" :key="product.id" class="product-item">
              <span class="rank">{{ index + 1 }}</span>
              <div class="product-info">
                <span class="product-name">{{ product.name }}</span>
                <span class="product-sales">{{ product.quantity_sold }} sold</span>
              </div>
              <span class="product-revenue">${{ formatNumber(product.revenue) }}</span>
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
                <td>#{{ order.id }}</td>
                <td>{{ order.customer_name || 'Walk-in Customer' }}</td>
                <td>{{ order.items.length }}</td>
                <td>${{ formatNumber(order.total) }}</td>
                <td>
                  <span class="status-badge" :class="order.status.toLowerCase()">
                    {{ order.status }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, nextTick } from 'vue'
import { orderService } from '@/services/orderService'
import { dashboardService } from '@/services/dashboardService'

export default {
  name: 'Reports',
  setup() {
    const loading = ref(true)
    const selectedPeriod = ref('month')
    const salesChart = ref(null)
    
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

    const loadReports = async () => {
      try {
        loading.value = true
        
        // Load dashboard data
        const dashboardData = await dashboardService.getOverview()
        metrics.value = {
          totalRevenue: dashboardData.total_revenue || 0,
          totalOrders: dashboardData.total_orders || 0,
          averageOrderValue: dashboardData.average_order_value || 0,
          productsSold: dashboardData.products_sold || 0,
          revenueChange: Math.random() * 20 - 10, // Mock change percentage
          ordersChange: Math.random() * 15 - 7,
          aovChange: Math.random() * 12 - 6,
          productsChange: Math.random() * 18 - 9
        }
        
        // Load orders
        const ordersData = await orderService.getOrders()
        detailedOrders.value = ordersData.results || []
        
        // Calculate top products from orders
        const productSales = {}
        detailedOrders.value.forEach(order => {
          order.items.forEach(item => {
            if (!productSales[item.product_id]) {
              productSales[item.product_id] = {
                id: item.product_id,
                name: item.product_name,
                quantity_sold: 0,
                revenue: 0
              }
            }
            productSales[item.product_id].quantity_sold += item.quantity
            productSales[item.product_id].revenue += item.price * item.quantity
          })
        })
        
        topProducts.value = Object.values(productSales)
          .sort((a, b) => b.revenue - a.revenue)
          .slice(0, 5)
        
        // Generate mock sales trend data
        generateSalesChart()
        
      } catch (error) {
        console.error('Error loading reports:', error)
      } finally {
        loading.value = false
      }
    }

    const generateSalesChart = async () => {
      await nextTick()
      if (!salesChart.value) return

      const ctx = salesChart.value.getContext('2d')
      const days = []
      const revenues = []
      
      // Generate last 7 days data
      for (let i = 6; i >= 0; i--) {
        const date = new Date()
        date.setDate(date.getDate() - i)
        days.push(date.toLocaleDateString('en-US', { weekday: 'short' }))
        revenues.push(Math.random() * 2000 + 500)
      }
      
      // Simple canvas chart
      ctx.clearRect(0, 0, salesChart.value.width, salesChart.value.height)
      ctx.strokeStyle = '#3B82F6'
      ctx.lineWidth = 2
      ctx.fillStyle = 'rgba(59, 130, 246, 0.1)'
      
      const width = salesChart.value.width
      const height = salesChart.value.height
      const padding = 40
      const chartWidth = width - 2 * padding
      const chartHeight = height - 2 * padding
      
      const maxRevenue = Math.max(...revenues)
      const minRevenue = Math.min(...revenues)
      
      // Draw chart
      ctx.beginPath()
      revenues.forEach((revenue, index) => {
        const x = padding + (index * chartWidth) / (revenues.length - 1)
        const y = padding + chartHeight - ((revenue - minRevenue) / (maxRevenue - minRevenue)) * chartHeight
        
        if (index === 0) {
          ctx.moveTo(x, y)
        } else {
          ctx.lineTo(x, y)
        }
      })
      ctx.stroke()
      
      // Draw points
      ctx.fillStyle = '#3B82F6'
      revenues.forEach((revenue, index) => {
        const x = padding + (index * chartWidth) / (revenues.length - 1)
        const y = padding + chartHeight - ((revenue - minRevenue) / (maxRevenue - minRevenue)) * chartHeight
        
        ctx.beginPath()
        ctx.arc(x, y, 4, 0, 2 * Math.PI)
        ctx.fill()
      })
    }

    const exportReport = () => {
      const csvContent = [
        ['Date', 'Order ID', 'Customer', 'Items', 'Total', 'Status'],
        ...detailedOrders.value.map(order => [
          formatDate(order.created_at),
          `#${order.id}`,
          order.customer_name || 'Walk-in Customer',
          order.items.length,
          order.total,
          order.status
        ])
      ].map(row => row.join(',')).join('\n')
      
      const blob = new Blob([csvContent], { type: 'text/csv' })
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `sales-report-${selectedPeriod.value}-${new Date().toISOString().split('T')[0]}.csv`
      a.click()
      window.URL.revokeObjectURL(url)
    }

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
    })

    return {
      loading,
      selectedPeriod,
      metrics,
      topProducts,
      detailedOrders,
      salesChart,
      loadReports,
      exportReport,
      formatNumber,
      formatDate
    }
  }
}
</script>

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

.export-btn:hover {
  background: #2563eb;
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

.chart-placeholder canvas {
  width: 100%;
  height: 200px;
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
</style>