<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import { inventoryService } from '@/services/inventoryService.js';
import { useToast } from 'vue-toastification';

const toast = useToast();

const inventory = ref([]);
const loading = ref(false);
const searchQuery = ref('');
const selectedCategory = ref('all');
const stockFilter = ref('all');
const showUpdateModal = ref(false);
const selectedItem = ref(null);
const updateQuantity = ref(0);

// Pagination - same pattern as products and POS components
const currentPage = ref(1);
const totalPages = ref(1);
const totalInventory = ref(0);
const hasNext = ref(false);
const hasPrevious = ref(false);

// Computed properties
const filteredInventory = computed(() => {
  // Since we're handling filtering on the backend through the API,
  // we can just return all inventory items that were already filtered
  return inventory.value;
});

const lowStockItems = computed(() => {
  return inventory.value.filter(item => item.stock_quantity <= 10);
});

const totalValue = computed(() => {
  return inventory.value.reduce((total, item) => {
    return total + (item.stock * parseFloat(item.price || 0));
  }, 0);
});

const categories = computed(() => {
  const uniqueCategories = [...new Set(inventory.value.map(item => item.category_name))];
  return uniqueCategories.filter(cat => cat);
});

// Pagination computed properties - same as products component
const paginationStart = computed(() => {
  if (totalInventory.value === 0) return 0;
  return (currentPage.value - 1) * 10 + 1; // Backend uses 10 items per page by default
});

const paginationEnd = computed(() => {
  const end = currentPage.value * 10;
  return Math.min(end, totalInventory.value);
});

// Methods
const loadInventory = async (page = 1) => {
  try {
    loading.value = true;
    const params = {
      page,
      search: searchQuery.value,
      category: selectedCategory.value !== 'all' ? selectedCategory.value : '',
      stock_status: stockFilter.value !== 'all' ? stockFilter.value : '',
      ordering: '-created_at'
    };

    // Remove empty parameters
    Object.keys(params).forEach(key => {
      if (params[key] === '' || params[key] === null || params[key] === undefined) {
        delete params[key];
      }
    });

    const response = await inventoryService.getInventoryItems(params);
    
    // Handle paginated response - same as products component
    if (response.data.results) {
      inventory.value = response.data.results;
      currentPage.value = response.data.current_page || page;
      totalPages.value = response.data.num_pages || 1;
      totalInventory.value = response.data.count || 0;
      hasNext.value = response.data.has_next || false;
      hasPrevious.value = response.data.has_previous || false;
    } else {
      // Handle non-paginated response (array)
      inventory.value = response.data;
      totalPages.value = 1;
      totalInventory.value = response.data.length;
      hasNext.value = false;
      hasPrevious.value = false;
    }
  } catch (error) {
    toast.error('Failed to load inventory');
    console.error('Error loading inventory:', error);
    inventory.value = [];
  } finally {
    loading.value = false;
  }
};

// Pagination functions - same as products component
const goToPage = async (page) => {
  await loadInventory(page);
};

const nextPage = async () => {
  if (hasNext.value) {
    await loadInventory(currentPage.value + 1);
  }
};

const previousPage = async () => {
  if (hasPrevious.value) {
    await loadInventory(currentPage.value - 1);
  }
};

const openUpdateModal = (item) => {
  selectedItem.value = item;
  updateQuantity.value = item.stock_quantity;
  showUpdateModal.value = true;
};

const updateStock = async () => {
  if (!selectedItem.value) return;
  
  try {
    loading.value = true;
    await inventoryService.updateInventoryItem(selectedItem.value.id, {
      stock_quantity: updateQuantity.value
    });
    
    // Update local data
    const index = inventory.value.findIndex(item => item.id === selectedItem.value.id);
    if (index !== -1) {
      inventory.value[index].stock_quantity = updateQuantity.value;
    }
    
    showUpdateModal.value = false;
    selectedItem.value = null;
    toast.success('Stock updated successfully');
  } catch (error) {
    toast.error('Failed to update stock');
    console.error('Error updating stock:', error);
  } finally {
    loading.value = false;
  }
};

const getStockStatusClass = (quantity) => {
  if (quantity === 0) return 'bg-red-100 text-red-800';
  if (quantity <= 10) return 'bg-yellow-100 text-yellow-800';
  return 'bg-green-100 text-green-800';
};

const getStockStatusText = (quantity) => {
  if (quantity === 0) return 'Out of Stock';
  if (quantity <= 10) return 'Low Stock';
  return 'In Stock';
};

const formatCurrency = (amount) => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'GHS'
  }).format(amount || 0);
};

// Watch for search and filter changes - same as products component
watch([searchQuery, selectedCategory, stockFilter], async () => {
  await loadInventory(1);
});

// Lifecycle
onMounted(() => {
  loadInventory();
});
</script>

<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex justify-between items-center">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Inventory Management</h1>
        <p class="text-gray-600">Track and manage product stock levels</p>
      </div>
      <button
        @click="loadInventory(currentPage)"
        class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg flex items-center space-x-2"
      >
        <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
        </svg>
        <span>Refresh</span>
      </button>
    </div>

    <!-- Stats Cards -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
      <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <div class="w-8 h-8 bg-blue-500 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
              </svg>
            </div>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-600">Total Items</p>
            <p class="text-2xl font-semibold text-gray-900">{{ totalInventory }}</p>
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
            <p class="text-sm font-medium text-gray-600">Total Value</p>
            <p class="text-2xl font-semibold text-gray-900">{{ formatCurrency(totalValue) }}</p>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <div class="w-8 h-8 bg-yellow-500 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
              </svg>
            </div>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-600">Low Stock Alerts</p>
            <p class="text-2xl font-semibold text-gray-900">{{ lowStockItems.length }}</p>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <div class="w-8 h-8 bg-red-500 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </div>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-600">Out of Stock</p>
            <p class="text-2xl font-semibold text-gray-900">
              {{ inventory.filter(item => item.stock_quantity === 0).length }}
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Filters -->
    <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Search</label>
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Product name or SKU..."
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Category</label>
          <select
            v-model="selectedCategory"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
          >
            <option value="all">All Categories</option>
            <option v-for="category in categories" :key="category" :value="category">
              {{ category }}
            </option>
          </select>
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Stock Status</label>
          <select
            v-model="stockFilter"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
          >
            <option value="all">All Items</option>
            <option value="good">In Stock</option>
            <option value="low">Low Stock</option>
            <option value="out">Out of Stock</option>
          </select>
        </div>
        
        <div class="flex items-end">
          <button
            @click="searchQuery = ''; selectedCategory = 'all'; stockFilter = 'all'; loadInventory(1)"
            class="w-full bg-gray-100 hover:bg-gray-200 text-gray-700 px-4 py-2 rounded-md"
          >
            Clear Filters
          </button>
        </div>
      </div>
    </div>

    <!-- Inventory Table -->
    <div class="bg-white rounded-lg shadow-sm border border-gray-200">
      <div class="p-6 border-b border-gray-200">
        <h3 class="text-lg font-semibold text-gray-900">
          Inventory Items ({{ totalInventory }})
        </h3>
      </div>
      
      <div v-if="loading" class="p-8 text-center">
        <div class="inline-flex items-center space-x-2">
          <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-500"></div>
          <span>Loading inventory...</span>
        </div>
      </div>
      
      <div v-else-if="filteredInventory.length === 0" class="p-8 text-center text-gray-500">
        <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
        </svg>
        <p class="mt-2">No inventory items found</p>
        <p class="text-sm">Check your filters or add products</p>
      </div>
      
      <div v-else class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Product
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Category
              </th>
              <!-- <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Size/Color
              </th> -->
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Price
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Stock
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Status
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Actions
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="item in filteredInventory" :key="item.id" class="hover:bg-gray-50">
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center">
                  <div>
                    <div class="text-sm font-medium text-gray-900">{{ item.product_name }}</div>
                    <div class="text-sm text-gray-500">{{ item.sku }}</div>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ item.category_name }}
              </td>
              <!-- <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ item.size }} - {{ item.color }}
              </td> -->
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                {{ formatCurrency(item.price) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                {{ item.stock_quantity }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span
                  class="inline-flex px-2 py-1 text-xs font-semibold rounded-full"
                  :class="getStockStatusClass(item.stock_quantity)"
                >
                  {{ getStockStatusText(item.stock_quantity) }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                <button
                  @click="openUpdateModal(item)"
                  class="text-blue-600 hover:text-blue-900 font-medium"
                >
                  Update Stock
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination - same as products component -->
      <div v-if="inventory.length > 0" class="bg-white px-4 py-3 flex items-center justify-between border-t border-gray-200 sm:px-6">
        <div class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
          <div>
            <p class="text-sm text-gray-700">
              Showing
              <span class="font-medium">{{ paginationStart }}</span>
              to
              <span class="font-medium">{{ paginationEnd }}</span>
              of
              <span class="font-medium">{{ totalInventory }}</span>
              results
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
                :class="{
                  'opacity-50 cursor-not-allowed': !hasPrevious,
                }"
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
                v-for="page in totalPages"
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
                :class="{
                  'opacity-50 cursor-not-allowed': !hasNext,
                }"
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

    <!-- Update Stock Modal -->
    <div v-if="showUpdateModal" class="fixed inset-0 z-50 overflow-y-auto">
      <div class="flex items-center justify-center min-h-screen px-4">
        <div class="fixed inset-0 bg-black opacity-25" @click="showUpdateModal = false"></div>
        <div class="relative bg-white rounded-lg max-w-md w-full">
          <div class="p-6 border-b border-gray-200">
            <div class="flex justify-between items-center">
              <h3 class="text-lg font-semibold text-gray-900">Update Stock</h3>
              <button
                @click="showUpdateModal = false"
                class="text-gray-400 hover:text-gray-600"
              >
                <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          </div>
          
          <form @submit.prevent="updateStock" class="p-6">
            <div v-if="selectedItem" class="mb-4">
              <div class="flex items-center space-x-3 mb-4">
                <img
                  :src="selectedItem.image || '/api/placeholder/40/40'"
                  :alt="selectedItem.product_name"
                  class="h-10 w-10 rounded object-cover"
                />
                <div>
                  <p class="font-medium text-gray-900">{{ selectedItem.product_name }}</p>
                  <p class="text-sm text-gray-500">{{ selectedItem.size }} - {{ selectedItem.color }}</p>
                </div>
              </div>
              
              <div class="mb-4">
                <label class="block text-sm font-medium text-gray-700 mb-1">
                  Current Stock: {{ selectedItem.stock_quantity }}
                </label>
                <input
                  v-model.number="updateQuantity"
                  type="number"
                  min="0"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="Enter new quantity"
                  required
                />
              </div>
            </div>
            
            <div class="flex justify-end space-x-3">
              <button
                type="button"
                @click="showUpdateModal = false"
                class="px-4 py-2 text-gray-700 bg-gray-200 hover:bg-gray-300 rounded-md"
              >
                Cancel
              </button>
              <button
                type="submit"
                :disabled="loading"
                class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-md disabled:opacity-50"
              >
                <span v-if="loading">Updating...</span>
                <span v-else>Update Stock</span>
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>
