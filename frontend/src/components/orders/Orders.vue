<template>
  <div class="p-6">
    <div class="mb-6">
      <h1 class="text-2xl font-bold text-gray-900 mb-4">Orders Management</h1>

      <!-- Search and Filters -->
      <div class="flex flex-wrap gap-4 mb-4">
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
    <div class="bg-white shadow rounded-lg overflow-hidden">
      <div class="px-6 py-4 border-b border-gray-200">
        <h2 class="text-lg font-medium text-gray-900">Orders List</h2>
        <p class="text-sm text-gray-500">Manage and track all orders</p>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="flex justify-center py-8">
        <div
          class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"
        ></div>
      </div>

      <!-- Empty State -->
      <div v-else-if="orders.length === 0" class="text-center py-8">
        <svg
          class="mx-auto h-12 w-12 text-gray-400"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
          />
        </svg>
        <p class="mt-2 text-gray-500">No orders found</p>
        <p class="text-sm text-gray-400">
          Orders will appear here once customers make purchases
        </p>
      </div>

      <!-- Orders Table -->
      <div v-else class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                Order Details
              </th>
              <th
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                Customer
              </th>
              <th
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                Items
              </th>
              <th
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                Total
              </th>
              <th
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                Status
              </th>
              <th
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                Payment
              </th>
              <th
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                Date
              </th>
              <th
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                Actions
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr
              v-for="order in orders"
              :key="order.id"
              class="hover:bg-gray-50"
            >
              <td class="px-6 py-4 whitespace-nowrap">
                <div>
                  <div class="text-sm font-medium text-gray-900">
                    {{ order.order_number }}
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
                  ₵{{ parseFloat(order.total || 0).toFixed(2) }}
                </div>
                <div
                  v-if="order.discount_amount > 0"
                  class="text-xs text-gray-500"
                >
                  Discount: ₵{{ parseFloat(order.discount_amount).toFixed(2) }}
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

    <!-- Order Details Modal -->
    <div
      v-if="showOrderModal"
      class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50"
      @click="closeOrderModal"
    >
      <div
        class="relative top-20 mx-auto p-5 border w-11/12 md:w-3/4 lg:w-1/2 shadow-lg rounded-md bg-white"
        @click.stop
      >
        <div class="mt-3">
          <div class="flex justify-between items-center mb-4">
            <h3 class="text-lg font-medium text-gray-900">Order Details</h3>
            <button
              @click="closeOrderModal"
              class="text-gray-400 hover:text-gray-600"
            >
              <svg
                class="w-6 h-6"
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

          <div v-if="selectedOrder" class="space-y-4">
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700"
                  >Order Number</label
                >
                <p class="mt-1 text-sm text-gray-900">
                  {{ selectedOrder.order_number }}
                </p>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700"
                  >Customer</label
                >
                <p class="mt-1 text-sm text-gray-900">
                  {{ selectedOrder.customer_name || "Walk-in Customer" }}
                </p>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700"
                  >Status</label
                >
                <span
                  class="mt-1 px-2 inline-flex text-xs leading-5 font-semibold rounded-full"
                  :class="getStatusClass(selectedOrder.status)"
                >
                  {{ selectedOrder.status_display || selectedOrder.status }}
                </span>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700"
                  >Payment Method</label
                >
                <p class="mt-1 text-sm text-gray-900">
                  {{
                    selectedOrder.payment_method_display ||
                    selectedOrder.payment_method
                  }}
                </p>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700"
                  >Total Amount</label
                >
                <p class="mt-1 text-sm font-medium text-gray-900">
                  ₵{{ parseFloat(selectedOrder.total || 0).toFixed(2) }}
                </p>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700"
                  >Created Date</label
                >
                <p class="mt-1 text-sm text-gray-900">
                  {{ formatDate(selectedOrder.created_at) }}
                  {{ formatTime(selectedOrder.created_at) }}
                </p>
              </div>
            </div>

            <div v-if="selectedOrder.items && selectedOrder.items.length > 0">
              <label class="block text-sm font-medium text-gray-700 mb-2"
                >Order Items</label
              >
              <div class="border border-gray-200 rounded-md">
                <table class="min-w-full divide-y divide-gray-200">
                  <thead class="bg-gray-50">
                    <tr>
                      <th
                        class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase"
                      >
                        Product
                      </th>
                      <th
                        class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase"
                      >
                        Quantity
                      </th>
                      <th
                        class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase"
                      >
                        Price
                      </th>
                      <th
                        class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase"
                      >
                        Total
                      </th>
                    </tr>
                  </thead>
                  <tbody class="divide-y divide-gray-200">
                    <tr v-for="item in selectedOrder.items" :key="item.id">
                      <td class="px-4 py-2 text-sm text-gray-900">
                        {{ item.product_name }}
                      </td>
                      <td class="px-4 py-2 text-sm text-gray-900">
                        {{ item.quantity }}
                      </td>
                      <td class="px-4 py-2 text-sm text-gray-900">
                        ₵{{ parseFloat(item.price || 0).toFixed(2) }}
                      </td>
                      <td class="px-4 py-2 text-sm font-medium text-gray-900">
                        ₵{{
                          parseFloat(
                            item.line_total || item.quantity * item.price
                          ).toFixed(2)
                        }}
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>

            <div v-if="selectedOrder.notes" class="mt-4">
              <label class="block text-sm font-medium text-gray-700"
                >Notes</label
              >
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

<script setup>
  import { ref, onMounted, computed, watch } from "vue";
  import { orderService } from "@/services/orderService.js";
  import { useToast } from "vue-toastification";

  const toast = useToast();

  // Reactive data
  const orders = ref([]);
  const loading = ref(false);
  const searchQuery = ref("");
  const selectedStatus = ref("");
  const selectedPaymentMethod = ref("");
  const dateFilter = ref("");

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
        pages.push("...");
        pages.push(total);
      } else if (current >= total - 3) {
        pages.push(1);
        pages.push("...");
        for (let i = total - 4; i <= total; i++) pages.push(i);
      } else {
        pages.push(1);
        pages.push("...");
        for (let i = current - 1; i <= current + 1; i++) pages.push(i);
        pages.push("...");
        pages.push(total);
      }
    }

    return pages.filter(
      (page) =>
        page !== "..." || pages.indexOf(page) === pages.lastIndexOf(page)
    );
  });

  // Methods
  const loadOrders = async (page = 1) => {
    try {
      loading.value = true;
      const params = {
        page,
        page_size: pageSize.value,
        ordering: "-created_at",
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

      console.log("Loading orders with params:", params);
      const response = await orderService.getOrders(params);
      console.log("Orders API response:", response);

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

        console.log("Set orders from results:", orders.value.length, "orders");
        console.log("Pagination info:", {
          currentPage: currentPage.value,
          totalPages: totalPages.value,
          totalOrders: totalOrders.value,
          hasNext: hasNext.value,
          hasPrevious: hasPrevious.value,
        });
      } else {
        orders.value = Array.isArray(response) ? response : [];
        totalPages.value = 1;
        totalOrders.value = orders.value.length;
        hasNext.value = false;
        hasPrevious.value = false;
        console.log("Set orders from array:", orders.value.length, "orders");
      }
      console.log("Final orders state:", orders.value);
    } catch (error) {
      console.error("Error loading orders:", error);
      console.error("Error response:", error.response);

      if (error.response?.status === 401) {
        toast.error("Authentication required. Please log in.");
      } else if (error.response?.status === 403) {
        toast.error("Access denied. Insufficient permissions.");
      } else {
        toast.error(
          "Failed to load orders: " + (error.message || "Unknown error")
        );
      }

      orders.value = [];
    } finally {
      loading.value = false;
    }
  };

  const goToPage = async (page) => {
    if (page !== "..." && page !== currentPage.value) {
      await loadOrders(page);
    }
  };

  const nextPage = async () => {
    if (hasNext.value) {
      await loadOrders(currentPage.value + 1);
    }
  };

  const previousPage = async () => {
    if (hasPrevious.value) {
      await loadOrders(currentPage.value - 1);
    }
  };

  const viewOrder = async (order) => {
    try {
      const fullOrder = await orderService.getOrder(order.id);
      selectedOrder.value = fullOrder;
      showOrderModal.value = true;
    } catch (error) {
      toast.error("Failed to load order details");
      console.error("Error loading order details:", error);
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
        status: "completed",
        payment_status: "paid",
      });
      toast.success("Order marked as completed");
      await loadOrders(currentPage.value);
    } catch (error) {
      toast.error("Failed to complete order");
      console.error("Error completing order:", error);
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
        status: "cancelled",
      });
      toast.success("Order cancelled successfully");
      closeCancelModal();
      await loadOrders(currentPage.value);
    } catch (error) {
      toast.error("Failed to cancel order");
      console.error("Error cancelling order:", error);
    } finally {
      loading.value = false;
    }
  };

  const getStatusClass = (status) => {
    const classes = {
      pending: "bg-yellow-100 text-yellow-800",
      processing: "bg-blue-100 text-blue-800",
      completed: "bg-green-100 text-green-800",
      cancelled: "bg-red-100 text-red-800",
      refunded: "bg-purple-100 text-purple-800",
    };
    return classes[status] || "bg-gray-100 text-gray-800";
  };

  const getPaymentStatusClass = (status) => {
    const classes = {
      pending: "bg-yellow-100 text-yellow-800",
      paid: "bg-green-100 text-green-800",
      partially_paid: "bg-orange-100 text-orange-800",
      failed: "bg-red-100 text-red-800",
      refunded: "bg-purple-100 text-purple-800",
    };
    return classes[status] || "bg-gray-100 text-gray-800";
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString();
  };

  const formatTime = (dateString) => {
    return new Date(dateString).toLocaleTimeString();
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
    console.log("Orders component mounted");
    console.log(
      "Access token:",
      localStorage.getItem("accessToken") ? "Present" : "Missing"
    );
    console.log("User:", localStorage.getItem("user"));
    await loadOrders();
  });
</script>
