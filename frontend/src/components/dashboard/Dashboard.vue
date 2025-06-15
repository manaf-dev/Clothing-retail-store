<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { dashboardService } from '@/services/dashboardService'
import { orderService } from '@/services/orderService'
import { inventoryService } from '@/services/inventoryService'

const loading = ref(true)
const metrics = ref({
    month_metrics: {
        total_revenue: 0,
        orders_count: 0,
        items_sold: 0,
        avg_order_value: 0
    },
    today_metrics: {
        total_revenue: 0,
        orders_count: 0,
        items_sold: 0,
        avg_order_value: 0
    },
    recent_orders: [],
    inventory_alerts: []
})


const loadDashboardData = async () => {
    try {
        loading.value = true

        // Load main metrics
        const overview = await dashboardService.getOverview()
        metrics.value = overview.data
        console.log('Dashboard metrics loaded:', metrics.value)
        console.log('Today stats:', metrics.value.today_metrics)
        console.log('Monthly metrics:', metrics.value.month_metrics)

       

    } catch (error) {
        console.error('Error loading dashboard data:', error)

    } finally {
        loading.value = false
    }
}

const refreshData = () => {
    loadDashboardData()
}

const formatNumber = (num) => {
    if (num === null || num === undefined) return '0'
    return new Intl.NumberFormat('en-US', {
        minimumFractionDigits: 0,
        maximumFractionDigits: 2
    }).format(num)
}

const formatTime = (dateString) => {
    const date = new Date(dateString)
    const now = new Date()
    const diffInMinutes = Math.floor((now - date) / (1000 * 60))

    if (diffInMinutes < 1) return 'Just now'
    if (diffInMinutes < 60) return `${diffInMinutes}m ago`
    if (diffInMinutes < 1440) return `${Math.floor(diffInMinutes / 60)}h ago`
    return date.toLocaleDateString()
}

let intervalId
onMounted(() => {
    loadDashboardData()
    // Auto-refresh every 5 minutes
    intervalId = setInterval(loadDashboardData, 5 * 60 * 1000)
})
onUnmounted(() => {
    clearInterval(intervalId)
})
</script>


<template>
  <div class="dashboard-container">
    <div class="dashboard-header">
      <h1>Store Dashboard</h1>
      <div class="header-actions">
        <button @click="refreshData" class="refresh-btn" :disabled="loading">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
          </svg>
          Refresh
        </button>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading-container">
      <div class="loading-spinner"></div>
      <p>Loading dashboard data...</p>
    </div>

    <!-- Dashboard Content -->
    <div v-else class="dashboard-content">
      <!-- Key Metrics Cards -->
      <div class="metrics-grid">
        <div class="metric-card revenue">
          <div class="metric-icon">
            <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1"></path>
            </svg>
          </div>
          <div class="metric-content">
            <h3>Total Revenue</h3>
            <p class="metric-value">₵{{ formatNumber(metrics.month_metrics?.total_revenue) }}</p>
            <span class="metric-label">This month sales</span>
          </div>
        </div>

        <div class="metric-card orders">
          <div class="metric-icon">
            <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"></path>
            </svg>
          </div>
          <div class="metric-content">
            <h3>Total Orders</h3>
            <p class="metric-value">{{ formatNumber(metrics.month_metrics?.orders_count) }}</p>
            <span class="metric-label">This month orders</span>
          </div>
        </div>

        <div class="metric-card products">
          <div class="metric-icon">
            <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"></path>
            </svg>
          </div>
          <div class="metric-content">
            <h3>Products Sold</h3>
            <p class="metric-value">{{ formatNumber(metrics.month_metrics?.items_sold) }}</p>
            <span class="metric-label">Total items sold</span>
          </div>
        </div>

        <div class="metric-card average">
          <div class="metric-icon">
            <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
            </svg>
          </div>
          <div class="metric-content">
            <h3>Average Order Value</h3>
            <p class="metric-value">₵{{ formatNumber(metrics.month_metrics?.avg_order_value) }}</p>
            <span class="metric-label">Per order average</span>
          </div>
        </div>
      </div>

      <!-- Quick Stats Section -->
      <div class="quick-stats">
        <div class="stats-card">
          <h3>Today's Performance</h3>
          <div class="stats-grid">
            <div class="stat-item">
              <span class="stat-label">Today's Sales</span>
              <span class="stat-value">₵{{ formatNumber(metrics.today_metrics?.total_revenue) }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Orders Today</span>
              <span class="stat-value">{{ metrics.today_metrics?.orders_count }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Average Order value</span>
              <span class="stat-value">{{ formatNumber(metrics.today_metrics?.avg_order_value) }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">Items Sold</span>
              <span class="stat-value">{{ metrics.today_metrics?.items_sold }}</span>
            </div>
          </div>
        </div>

        <div class="stats-card">
          <h3>Inventory Alerts</h3>
          <div v-if="metrics.inventory_alerts?.length > 0" class="alert-list">
            <div v-for="item in metrics.inventory_alerts" :key="item.id" class="alert-item">
              <div class="alert-icon">⚠️</div>
              <div class="alert-content">
                <span class="alert-product">{{ item.name }}</span>
                <span class="alert-stock">{{ item.stock }} left</span>
              </div>
            </div>
            <router-link to="/inventory" class="view-all-link">
              View all alerts
            </router-link>
          </div>
          <div v-else class="no-alerts">
            <div class="no-alerts-icon">✅</div>
            <p>All products are well stocked!</p>
          </div>
        </div>
      </div>

      <!-- Recent Activity -->
      <div class="recent-activity">
        <div class="activity-header">
          <h3>Recent Orders</h3>
          <router-link to="/sales" class="view-all-link">View All</router-link>
        </div>
        
        <div v-if="metrics.recent_orders?.length > 0" class="orders-list">
          <div v-for="order in metrics.recent_orders" :key="order.id" class="order-item">
            <div class="order-id">#{{ order.id }}</div>
            <div class="order-details">
              <span class="order-customer">{{ order.customer_name || 'Walk-in Customer' }}</span>
              <span class="order-time">{{ formatTime(order.created_at) }}</span>
            </div>
            <div class="order-total">₵{{ formatNumber(order.total) }}</div>
            <div class="order-status">
              <span class="status-badge" :class="order.status.toLowerCase()">
                {{ order.status }}
              </span>
            </div>
          </div>
        </div>
        <div v-else class="no-orders">
          <p>No recent orders found.</p>
          <router-link to="/pos" class="create-order-btn">Create First Order</router-link>
        </div>
      </div>
    </div>
  </div>
</template>



<style scoped>
.dashboard-container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.dashboard-header h1 {
  color: #1f2937;
  font-size: 28px;
  font-weight: 600;
  margin: 0;
}

.refresh-btn {
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

.refresh-btn:hover:not(:disabled) {
  background: #2563eb;
}

.refresh-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
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
  transition: transform 0.2s, box-shadow 0.2s;
}

.metric-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
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

.metric-card.revenue .metric-icon { background: #10b981; }
.metric-card.orders .metric-icon { background: #3b82f6; }
.metric-card.products .metric-icon { background: #f59e0b; }
.metric-card.average .metric-icon { background: #8b5cf6; }

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

.metric-label {
  color: #9ca3af;
  font-size: 12px;
}

.quick-stats {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 30px;
}

.stats-card {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.stats-card h3 {
  color: #1f2937;
  font-size: 18px;
  font-weight: 600;
  margin: 0 0 16px 0;
}

.stats-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.stat-label {
  color: #6b7280;
  font-size: 12px;
  font-weight: 500;
}

.stat-value {
  color: #1f2937;
  font-size: 18px;
  font-weight: 600;
}

.alert-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.alert-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px;
  background: #fef3c7;
  border-radius: 6px;
  border-left: 3px solid #f59e0b;
}

.alert-icon {
  font-size: 16px;
}

.alert-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.alert-product {
  color: #1f2937;
  font-weight: 500;
  font-size: 14px;
}

.alert-stock {
  color: #92400e;
  font-size: 12px;
}

.no-alerts {
  text-align: center;
  padding: 20px;
  color: #6b7280;
}

.no-alerts-icon {
  font-size: 24px;
  margin-bottom: 8px;
}

.recent-activity {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.activity-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.activity-header h3 {
  color: #1f2937;
  font-size: 18px;
  font-weight: 600;
  margin: 0;
}

.view-all-link {
  color: #3b82f6;
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
}

.view-all-link:hover {
  text-decoration: underline;
}

.orders-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.order-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 12px;
  background: #f9fafb;
  border-radius: 6px;
  transition: background-color 0.2s;
}

.order-item:hover {
  background: #f3f4f6;
}

.order-id {
  color: #1f2937;
  font-weight: 600;
  font-size: 14px;
  min-width: 60px;
}

.order-details {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.order-customer {
  color: #1f2937;
  font-weight: 500;
  font-size: 14px;
}

.order-time {
  color: #6b7280;
  font-size: 12px;
}

.order-total {
  color: #1f2937;
  font-weight: 600;
  font-size: 14px;
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

.no-orders {
  text-align: center;
  padding: 40px 20px;
  color: #6b7280;
}

.create-order-btn {
  display: inline-block;
  margin-top: 16px;
  padding: 8px 16px;
  background: #3b82f6;
  color: white;
  text-decoration: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  transition: background-color 0.2s;
}

.create-order-btn:hover {
  background: #2563eb;
}

@media (max-width: 768px) {
  .quick-stats {
    grid-template-columns: 1fr;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .metrics-grid {
    grid-template-columns: 1fr;
  }
  
  .order-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
}
</style>