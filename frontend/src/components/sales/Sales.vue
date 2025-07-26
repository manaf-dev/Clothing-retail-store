<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import { orderService } from '@/services/orderService.js';
import { useToast } from 'vue-toastification';

const toast = useToast();

// Reactive data
const orders = ref([]);
const loading = ref(false);
const searchQuery = ref('');
const selectedStatus = ref('');
const selectedPaymentMethod = ref('');
const dateFilter = ref('');

// Pagination
const currentPage = ref(1);
const totalPages = ref(1);
const totalOrders = ref(0);
const hasNext = ref(false);
const hasPrevious = ref(false);
const pageSize = ref(10);

// Modals
const showOrderModal = ref(false);
const showCancelOrderModal = ref(false);
const selectedOrder = ref(null);
const orderToCancel = ref(null);

// Computed properties
const totalSales = computed(() => {
  return orders.value.reduce((sum, order) => sum + parseFloat(order.total || 0), 0);
});

const paginationStart = computed(() => {
  if (totalOrders.value === 0) return 0;
  return (currentPage.value - 1) * pageSize.value + 1;
});

const paginationEnd = computed(() => {
  const end = currentPage.value * pageSize.value;
  return Math.min(end, totalOrders.value);
});

const visiblePages = computed(() => {
  const pages = [];
  const total = totalPages.value;
  const current = currentPage.value;

  if (total <= 7) {
    for (let i = 1; i <= total; i++) {
      pages.push(i);
    }
  } else {
    if (current <= 4) {
      for (let i = 1; i <= 5; i++) pages.push(i);
      pages.push('...');
      pages.push(total);
    } else if (current >= total - 3) {
      pages.push(1);
      pages.push('...');
      for (let i = total - 4; i <= total; i++) pages.push(i);
    } else {
      pages.push(1);
      pages.push('...');
      for (let i = current - 1; i <= current + 1; i++) pages.push(i);
      pages.push('...');
      pages.push(total);
    }
  }

  return pages.filter(
    (page) => page !== '...' || pages.indexOf(page) === pages.lastIndexOf(page)
  );
});

// Methods
const loadOrders = async (page = 1) => {
  try {
    loading.value = true;
    const params = {
      page,
      page_size: pageSize.value,
      ordering: '-created_at',
    };

    if (searchQuery.value) {
      params.search = searchQuery.value;
    }

    if (selectedStatus.value) {
      params.status = selectedStatus.value;
    }

    if (selectedPaymentMethod.value) {
      params.payment_method = selectedPaymentMethod.value;
    }

    if (dateFilter.value) {
      params.date = dateFilter.value;
    }

    console.log('Loading orders with params:', params);
    const response = await orderService.getOrders(params);
    console.log('Orders API response:', response);

    if (response.results) {
      orders.value = response.results;
      totalOrders.value = response.count || 0;

      // Calculate pagination info
      const itemsPerPage = pageSize.value;
      totalPages.value = Math.ceil(totalOrders.value / itemsPerPage);
      currentPage.value = page;

      // Check if there are more pages
      hasNext.value = !!response.next;
      hasPrevious.value = !!response.previous;

      console.log('Set orders from results:', orders.value.length, 'orders');
      console.log('Pagination info:', {
        currentPage: currentPage.value,
        totalPages: totalPages.value,
        totalOrders: totalOrders.value,
        hasNext: hasNext.value,
        hasPrevious: hasPrevious.value,
      });
    } else {
      orders.value = response || [];
      totalOrders.value = orders.value.length;
      console.log('Set orders directly:', orders.value.length, 'orders');
    }
  } catch (error) {
    toast.error('Failed to load orders');
    console.error('Error loading orders:', error);
  } finally {
    loading.value = false;
  }
};

const nextPage = async () => {
  if (hasNext.value && currentPage.value < totalPages.value) {
    await loadOrders(currentPage.value + 1);
  }
};

const previousPage = async () => {
  if (hasPrevious.value && currentPage.value > 1) {
    await loadOrders(currentPage.value - 1);
  }
};

const goToPage = async (page) => {
  if (page !== '...' && page !== currentPage.value) {
    await loadOrders(page);
  }
};

const viewOrder = async (order) => {
  try {
    const fullOrder = await orderService.getOrder(order.id);
    selectedOrder.value = fullOrder;
    showOrderModal.value = true;
  } catch (error) {
    toast.error('Failed to load order details');
    console.error('Error loading order details:', error);
  }
};

const closeOrderModal = () => {
  showOrderModal.value = false;
  selectedOrder.value = null;
};

const completeOrder = async (order) => {
  try {
    loading.value = true;
    await orderService.updateOrder(order.id, {
      status: 'completed',
      payment_status: 'paid',
    });
    toast.success('Order marked as completed');
    await loadOrders(currentPage.value);
  } catch (error) {
    toast.error('Failed to complete order');
    console.error('Error completing order:', error);
  } finally {
    loading.value = false;
  }
};

const showCancelModal = (order) => {
  orderToCancel.value = order;
  showCancelOrderModal.value = true;
};

const closeCancelModal = () => {
  showCancelOrderModal.value = false;
  orderToCancel.value = null;
};

const confirmCancelOrder = async () => {
  if (!orderToCancel.value) return;

  try {
    loading.value = true;
    await orderService.updateOrder(orderToCancel.value.id, {
      status: 'cancelled',
    });
    toast.success('Order cancelled successfully');
    closeCancelModal();
    await loadOrders(currentPage.value);
  } catch (error) {
    toast.error('Failed to cancel order');
    console.error('Error cancelling order:', error);
  } finally {
    loading.value = false;
  }
};

const getStatusClass = (status) => {
  const classes = {
    pending: 'bg-yellow-100 text-yellow-800',
    processing: 'bg-blue-100 text-blue-800',
    completed: 'bg-green-100 text-green-800',
    cancelled: 'bg-red-100 text-red-800',
    refunded: 'bg-purple-100 text-purple-800',
  };
  return classes[status] || 'bg-gray-100 text-gray-800';
};

const getPaymentStatusClass = (status) => {
  const classes = {
    pending: 'bg-yellow-100 text-yellow-800',
    paid: 'bg-green-100 text-green-800',
    partially_paid: 'bg-orange-100 text-orange-800',
    failed: 'bg-red-100 text-red-800',
    refunded: 'bg-purple-100 text-purple-800',
  };
  return classes[status] || 'bg-gray-100 text-gray-800';
};

const formatCurrency = (amount) => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'GHS'
  }).format(amount || 0);
};

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  });
};

const formatTime = (dateString) => {
  return new Date(dateString).toLocaleTimeString('en-US', {
    hour: '2-digit',
    minute: '2-digit'
  });
};

const getStatusBadgeClass = (status) => {
  switch (status) {
    case 'completed':
      return 'bg-green-100 text-green-800';
    case 'pending':
      return 'bg-yellow-100 text-yellow-800';
    case 'cancelled':
      return 'bg-red-100 text-red-800';
    default:
      return 'bg-gray-100 text-gray-800';
  }
};

// Watch for filter changes
watch(
  [searchQuery, selectedStatus, selectedPaymentMethod, dateFilter],
  async () => {
    await loadOrders(1);
  },
  { deep: true }
);

// Lifecycle
onMounted(async () => {
  console.log('Sales component mounted');
  console.log(
    'Access token:',
    localStorage.getItem('accessToken') ? 'Present' : 'Missing'
  );
  console.log('User:', localStorage.getItem('user'));
  await loadOrders();
});
</script>

<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex justify-between items-center">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Sales & Orders</h1>
        <p class="text-gray-600">Manage and track all store orders and sales</p>
      </div>
      <div class="flex space-x-3">
        <button
          @click="loadOrders"
          class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg flex items-center space-x-2"
        >
          <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          <span>Refresh</span>
        </button>
        <router-link
          to="/pos"
          class="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg flex items-center space-x-2"
        >
          <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
          </svg>
          <span>New Sale</span>
        </router-link>
      </div>
    </div>

    <!-- Stats Cards -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
      <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <div class="w-8 h-8 bg-blue-500 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l-1 12H6L5 9z" />
              </svg>
            </div>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-600">Total Orders</p>
            <p class="text-2xl font-semibold text-gray-900">{{ totalOrders }}</p>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <div class="w-8 h-8 bg-green-500 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-600">Total Sales</p>
            <p class="text-2xl font-semibold text-gray-900">{{ formatCurrency(totalSales) }}</p>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <div class="w-8 h-8 bg-yellow-500 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-600">Avg. Order Value</p>
            <p class="text-2xl font-semibold text-gray-900">
              {{ formatCurrency(orders.length > 0 ? totalSales / orders.length : 0) }}
            </p>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <div class="w-8 h-8 bg-purple-500 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
            </div>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-600">Completed Today</p>
            <p class="text-2xl font-semibold text-gray-900">
              {{ orders.filter(o => 
                o.status === 'completed' && 
                new Date(o.created_at).toDateString() === new Date().toDateString()
              ).length }}
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Search and Filters -->
    <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <h3 class="text-lg font-semibold text-gray-900 mb-4">Search & Filter Orders</h3>
      <div class="flex flex-wrap gap-4">
        <div class="flex-1 min-w-64">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search orders by customer name or order number..."
            class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>

        <select
          v-model="selectedStatus"
          class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
        >
          <option value="">All Status</option>
          <option value="pending">Pending</option>
          <option value="processing">Processing</option>
          <option value="completed">Completed</option>
          <option value="cancelled">Cancelled</option>
          <option value="refunded">Refunded</option>
        </select>

        <select
          v-model="selectedPaymentMethod"
          class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
        >
          <option value="">All Payment Methods</option>
          <option value="cash">Cash</option>
          <option value="card">Card</option>
          <option value="mobile_money">Mobile Money</option>
          <option value="bank_transfer">Bank Transfer</option>
          <option value="credit">Credit</option>
        </select>

        <input
          v-model="dateFilter"
          type="date"
          class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
        />
      </div>
    </div>

    <!-- Orders Table -->
    <div class="bg-white rounded-lg shadow-sm border border-gray-200">
      <div class="p-6 border-b border-gray-200">
        <h3 class="text-lg font-semibold text-gray-900">All Orders</h3>
        <p class="text-sm text-gray-500">Manage and track all orders with full pagination</p>
      </div>
      
      <div v-if="loading" class="p-8 text-center">
        <div class="inline-flex items-center space-x-2">
          <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-500"></div>
          <span>Loading orders...</span>
        </div>
      </div>
      
      <div v-else-if="orders.length === 0" class="p-8 text-center text-gray-500">
        <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l-1 12H6L5 9z" />
        </svg>
        <p class="mt-2">No orders found</p>
        <p class="text-sm">Start making sales to see orders here</p>
      </div>
      
      <div v-else class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Order Details
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Customer
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Items
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Total
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Status
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Payment
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Date
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Actions
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="order in orders" :key="order.id" class="hover:bg-gray-50">
              <td class="px-6 py-4 whitespace-nowrap">
                <div>
                  <div class="text-sm font-medium text-gray-900">
                    {{ order.order_number || `#${order.id}` }}
                  </div>
                  <div class="text-sm text-gray-500">
                    Served by: {{ order.served_by || "N/A" }}
                  </div>
                </div>
              </td>

              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm text-gray-900">
                  {{ order.customer_name || "Walk-in Customer" }}
                </div>
              </td>

              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                {{ order.item_count || order.total_quantity || 0 }} items
              </td>

              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm font-medium text-gray-900">
                  {{ formatCurrency(order.total) }}
                </div>
                <div
                  v-if="order.discount_amount > 0"
                  class="text-xs text-gray-500"
                >
                  Discount: {{ formatCurrency(order.discount_amount) }}
                </div>
              </td>

              <td class="px-6 py-4 whitespace-nowrap">
                <span
                  class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full"
                  :class="getStatusClass(order.status)"
                >
                  {{ order.status_display || order.status }}
                </span>
              </td>

              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm text-gray-900">
                  {{ order.payment_method_display || order.payment_method }}
                </div>
                <span
                  class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full mt-1"
                  :class="getPaymentStatusClass(order.payment_status)"
                >
                  {{ order.payment_status_display || order.payment_status }}
                </span>
              </td>

              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                <div>{{ formatDate(order.created_at) }}</div>
                <div class="text-xs">{{ formatTime(order.created_at) }}</div>
              </td>

              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                <div class="flex space-x-2">
                  <button
                    @click="viewOrder(order)"
                    class="text-blue-600 hover:text-blue-900"
                    title="View Details"
                  >
                    <svg
                      class="w-4 h-4"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
                      />
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"
                      />
                    </svg>
                  </button>

                  <button
                    v-if="order.status === 'pending'"
                    @click="completeOrder(order)"
                    class="text-green-600 hover:text-green-900"
                    title="Mark as Completed"
                  >
                    <svg
                      class="w-4 h-4"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M5 13l4 4L19 7"
                      />
                    </svg>
                  </button>

                  <button
                    v-if="
                      order.status !== 'cancelled' &&
                      order.status !== 'refunded' &&
                      order.status !== 'completed'
                    "
                    @click="showCancelModal(order)"
                    class="text-red-600 hover:text-red-900"
                    title="Cancel Order"
                  >
                    <svg
                      class="w-4 h-4"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M6 18L18 6M6 6l12 12"
                      />
                    </svg>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination -->
      <div
        v-if="orders.length > 0"
        class="bg-white px-4 py-3 flex items-center justify-between border-t border-gray-200 sm:px-6"
      >
        <div class="flex-1 flex justify-between sm:hidden">
          <button
            @click="previousPage"
            :disabled="!hasPrevious"
            class="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
            :class="{ 'opacity-50 cursor-not-allowed': !hasPrevious }"
          >
            Previous
          </button>
          <button
            @click="nextPage"
            :disabled="!hasNext"
            class="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
            :class="{ 'opacity-50 cursor-not-allowed': !hasNext }"
          >
            Next
          </button>
        </div>
        <div
          class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between"
        >
          <div>
            <p class="text-sm text-gray-700">
              Showing
              <span class="font-medium">{{ paginationStart }}</span>
              to
              <span class="font-medium">{{ paginationEnd }}</span>
              of
              <span class="font-medium">{{ totalOrders }}</span>
              orders
            </p>
          </div>
          <div>
            <nav
              class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px"
              aria-label="Pagination"
            >
              <button
                @click="previousPage"
                :disabled="!hasPrevious"
                class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50"
                :class="{ 'opacity-50 cursor-not-allowed': !hasPrevious }"
              >
                <span class="sr-only">Previous</span>
                <svg
                  class="h-5 w-5"
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                  aria-hidden="true"
                >
                  <path
                    fill-rule="evenodd"
                    d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z"
                    clip-rule="evenodd"
                  />
                </svg>
              </button>

              <button
                v-for="page in visiblePages"
                :key="page"
                @click="goToPage(page)"
                :class="{
                  'relative inline-flex items-center px-4 py-2 border text-sm font-medium': true,
                  'bg-indigo-50 border-indigo-500 text-indigo-600':
                    currentPage === page,
                  'bg-white border-gray-300 text-gray-500 hover:bg-gray-50':
                    currentPage !== page,
                }"
              >
                {{ page }}
              </button>

              <button
                @click="nextPage"
                :disabled="!hasNext"
                class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50"
                :class="{ 'opacity-50 cursor-not-allowed': !hasNext }"
              >
                <span class="sr-only">Next</span>
                <svg
                  class="h-5 w-5"
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                  aria-hidden="true"
                >
                  <path
                    fill-rule="evenodd"
                    d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"
                    clip-rule="evenodd"
                  />
                </svg>
              </button>
            </nav>
          </div>
        </div>
      </div>
    </div>

    <!-- Order Detail Modal -->
    <div v-if="showOrderModal" class="fixed inset-0 z-50 overflow-y-auto">
      <div class="flex items-center justify-center min-h-screen px-4">
        <div class="fixed inset-0 bg-black opacity-25" @click="closeOrderModal"></div>
        <div class="relative bg-white rounded-lg max-w-2xl w-full max-h-screen overflow-y-auto">
          <div class="p-6 border-b border-gray-200">
            <div class="flex justify-between items-center">
              <h3 class="text-lg font-semibold text-gray-900">Order Details</h3>
              <button
                @click="closeOrderModal"
                class="text-gray-400 hover:text-gray-600"
              >
                <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          </div>
          
          <div v-if="selectedOrder" class="p-6">
            <div class="grid grid-cols-2 gap-4 mb-6">
              <div>
                <label class="block text-sm font-medium text-gray-700">Order Number</label>
                <p class="mt-1 text-sm text-gray-900">
                  {{ selectedOrder.order_number || `#${selectedOrder.id}` }}
                </p>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700">Customer</label>
                <p class="mt-1 text-sm text-gray-900">
                  {{ selectedOrder.customer_name || 'Walk-in Customer' }}
                </p>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700">Status</label>
                <span
                  class="mt-1 px-2 inline-flex text-xs leading-5 font-semibold rounded-full"
                  :class="getStatusClass(selectedOrder.status)"
                >
                  {{ selectedOrder.status_display || selectedOrder.status }}
                </span>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700">Payment Method</label>
                <p class="mt-1 text-sm text-gray-900">
                  {{ selectedOrder.payment_method_display || selectedOrder.payment_method }}
                </p>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700">Total Amount</label>
                <p class="mt-1 text-sm font-medium text-gray-900">
                  {{ formatCurrency(selectedOrder.total) }}
                </p>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700">Created Date</label>
                <p class="mt-1 text-sm text-gray-900">
                  {{ formatDate(selectedOrder.created_at) }}
                  {{ formatTime(selectedOrder.created_at) }}
                </p>
              </div>
            </div>
            
            <div v-if="selectedOrder.items && selectedOrder.items.length > 0">
              <label class="block text-sm font-medium text-gray-700 mb-2">Order Items</label>
              <div class="border border-gray-200 rounded-md">
                <table class="min-w-full divide-y divide-gray-200">
                  <thead class="bg-gray-50">
                    <tr>
                      <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">
                        Product
                      </th>
                      <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">
                        Quantity
                      </th>
                      <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">
                        Price
                      </th>
                      <th class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">
                        Total
                      </th>
                    </tr>
                  </thead>
                  <tbody class="divide-y divide-gray-200">
                    <tr v-for="item in selectedOrder.items" :key="item.id">
                      <td class="px-4 py-2 text-sm text-gray-900">
                        {{ item.product_name || `Product #${item.product}` }}
                        <div v-if="item.size || item.color" class="text-xs text-gray-500">
                          {{ item.size }} - {{ item.color }}
                        </div>
                      </td>
                      <td class="px-4 py-2 text-sm text-gray-900">
                        {{ item.quantity }}
                      </td>
                      <td class="px-4 py-2 text-sm text-gray-900">
                        {{ formatCurrency(item.price) }}
                      </td>
                      <td class="px-4 py-2 text-sm font-medium text-gray-900">
                        {{ formatCurrency(item.line_total || item.quantity * item.price) }}
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>

            <div v-if="selectedOrder.notes" class="mt-4">
              <label class="block text-sm font-medium text-gray-700">Notes</label>
              <p class="mt-1 text-sm text-gray-900">
                {{ selectedOrder.notes }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Cancel Order Modal -->
    <div
      v-if="showCancelOrderModal"
      class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50"
      @click="closeCancelModal"
    >
      <div
        class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white"
        @click.stop
      >
        <div class="mt-3 text-center">
          <h3 class="text-lg font-medium text-gray-900">Cancel Order</h3>
          <div class="mt-2 px-7 py-3">
            <p class="text-sm text-gray-500">
              Are you sure you want to cancel this order? This action cannot be
              undone.
            </p>
          </div>
          <div class="flex gap-4 justify-center mt-4">
            <button
              @click="closeCancelModal"
              class="px-4 py-2 bg-gray-300 text-gray-700 rounded-md hover:bg-gray-400"
            >
              Cancel
            </button>
            <button
              @click="confirmCancelOrder"
              :disabled="loading"
              class="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 disabled:opacity-50"
            >
              <span v-if="loading">Cancelling...</span>
              <span v-else>Yes, Cancel Order</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>