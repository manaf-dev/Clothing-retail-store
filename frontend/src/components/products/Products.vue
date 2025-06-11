<script setup>
import { ref, computed, onMounted, watch } from "vue";
import GridLoader from "vue-spinner/src/GridLoader.vue";
import { useToast } from "vue-toastification";
import ProductFormModal from "./ProductFormModal.vue";
import DeleteConfirmModal from "./DeleteConfirmModal.vue";
import { ProductService } from "@/services/productService.js";
import { Formatters } from "@/utils/formatters.js";

const toast = useToast();

const products = ref([]);
const categories = ref([]);
const loading = ref(false);
const showProductModal = ref(false);
const showDeleteModal = ref(false);
const editingProduct = ref(false);
const currentProduct = ref({
  id: null,
  name: "",
  category: "",
  price: 0,
  sale_price: null,
  stock: 0,
  min_stock: 0,
  description: "",
});
const productToDelete = ref(null);

// Pagination
const currentPage = ref(1);
const totalPages = ref(1);
const totalProducts = ref(0);
const hasNext = ref(false);
const hasPrevious = ref(false);

// Filters and search
const searchQuery = ref("");
const filters = ref({
  category: "",
  stockStatus: "",
  minPrice: "",
  maxPrice: "",
  status: "active",
});

// Load products from backend
const loadProducts = async (page = 1) => {
  try {
    loading.value = true;
    const params = {
      page,
      search: searchQuery.value,
      category: filters.value.category,
      stock_status: filters.value.stockStatus,
      status: filters.value.status,
      min_price: filters.value.minPrice,
      max_price: filters.value.maxPrice,
      ordering: '-created_at'
    };

    const response = await ProductService.searchProducts(params);
    
    // Handle paginated response
    if (response.results) {
      products.value = ProductService.transformMultipleToFrontend(response.results);
      currentPage.value = response.current_page || page;
      totalPages.value = response.num_pages || 1;
      totalProducts.value = response.count || 0;
      hasNext.value = response.has_next || false;
      hasPrevious.value = response.has_previous || false;
    } else {
      // Handle non-paginated response (array)
      products.value = ProductService.transformMultipleToFrontend(response);
    }
  } catch (error) {
    console.error("Failed to load products:", error);
    toast.error("Failed to load products. Please try again.");
    products.value = [];
  } finally {
    loading.value = false;
  }
};

// Load categories
const loadCategories = async () => {
  try {
    const response = await ProductService.getCategories();
    categories.value = response;
  } catch (error) {
    console.error("Failed to load categories:", error);
    toast.error("Failed to load categories.");
  }
};

const openAddProduct = () => {
  currentProduct.value = {
    id: null,
    name: "",
    category: "",
    price: 0,
    sale_price: null,
    stock: 0,
    min_stock: 0,
    description: "",
  };
  editingProduct.value = false;
  showProductModal.value = true;
};

const closeProductModal = () => {
  showProductModal.value = false;
  currentProduct.value = {
    id: null,
    name: "",
    category: "",
    price: 0,
    sale_price: null,
    stock: 0,
    min_stock: 0,
    description: "",
  };
  editingProduct.value = false;
};

const openEditProduct = (product) => {
  currentProduct.value = { ...product };
  editingProduct.value = true;
  showProductModal.value = true;
};

const saveProduct = async (productData) => {
  try {
    loading.value = true;
    
    if (editingProduct.value) {
      // Update existing product
      const updatedProduct = await ProductService.updateProduct(
        currentProduct.value.id,
        productData
      );
      
      // Update the product in the local array
      const index = products.value.findIndex(p => p.id === updatedProduct.id);
      if (index !== -1) {
        products.value[index] = ProductService.transformToFrontend(updatedProduct);
      }
      
      toast.success("Product updated successfully!");
    } else {
      // Create new product
      const newProduct = await ProductService.createProduct(productData);
      
      // Add to local array (or reload to maintain pagination)
      await loadProducts(currentPage.value);
      
      toast.success("Product added successfully!");
    }
    
    closeProductModal();
  } catch (error) {
    console.error("API Error:", error);
    
    // Extract error message from response
    let errorMessage = "Failed to save product.";
    if (error.response?.data) {
      if (typeof error.response.data === 'string') {
        errorMessage = error.response.data;
      } else if (error.response.data.detail) {
        errorMessage = error.response.data.detail;
      } else if (error.response.data.error) {
        errorMessage = error.response.data.error;
      } else {
        // Handle field validation errors
        const errors = Object.values(error.response.data).flat();
        if (errors.length > 0) {
          errorMessage = errors.join(', ');
        }
      }
    }
    
    toast.error(errorMessage);
  } finally {
    loading.value = false;
  }
};

const confirmDeleteProduct = (product) => {
  productToDelete.value = product;
  showDeleteModal.value = true;
};

const closeDeleteModal = () => {
  showDeleteModal.value = false;
  productToDelete.value = null;
};

const deleteProduct = async () => {
  try {
    loading.value = true;
    await ProductService.deleteProduct(productToDelete.value.id);
    
    // Remove from local array
    const index = products.value.findIndex(p => p.id === productToDelete.value.id);
    if (index !== -1) {
      products.value.splice(index, 1);
    }
    
    // If current page becomes empty and there are previous pages, go back
    if (products.value.length === 0 && currentPage.value > 1) {
      await loadProducts(currentPage.value - 1);
    } else if (products.value.length === 0) {
      // Reload current page to get fresh data
      await loadProducts(currentPage.value);
    }
    
    toast.success("Product deleted successfully!");
    closeDeleteModal();
  } catch (error) {
    console.error("Delete error:", error);
    toast.error("Failed to delete product. Please try again.");
  } finally {
    loading.value = false;
  }
};

// Pagination functions
const goToPage = async (page) => {
  await loadProducts(page);
};

const nextPage = async () => {
  if (hasNext.value) {
    await loadProducts(currentPage.value + 1);
  }
};

const previousPage = async () => {
  if (hasPrevious.value) {
    await loadProducts(currentPage.value - 1);
  }
};

// Filter functions
const clearFilters = async () => {
  filters.value = {
    category: "",
    stockStatus: "",
    minPrice: "",
    maxPrice: "",
    status: "active",
  };
  searchQuery.value = "";
  await loadProducts(1);
};

// Watch for filter changes
watch([searchQuery, filters], async () => {
  await loadProducts(1);
}, { deep: true });

// Computed properties for display
const displayedProducts = computed(() => products.value);

const stockStatusOptions = [
  { value: "", label: "All Stock Status" },
  { value: "in_stock", label: "In Stock" },
  { value: "low_stock", label: "Low Stock" },
  { value: "out_of_stock", label: "Out of Stock" },
];

const productStatusOptions = [
  { value: "active", label: "Active" },
  { value: "inactive", label: "Inactive" },
];

// Pagination computed properties
const paginationStart = computed(() => {
  if (totalProducts.value === 0) return 0;
  return (currentPage.value - 1) * 10 + 1;
});

const paginationEnd = computed(() => {
  const end = currentPage.value * 10;
  return Math.min(end, totalProducts.value);
});

// Methods
const getStockStatus = (stock) => {
  if (stock > 10) return "In Stock";
  if (stock > 0) return "Low Stock";
  return "Out of Stock";
};

onMounted(async () => {
  
  await loadProducts();
  await loadCategories();
});
</script>

<template>
  <div>
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-semibold text-gray-800">Products</h1>
      <button
        @click="openAddProduct"
        class="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 flex items-center"
      >
        <svg
          class="h-5 w-5 mr-2"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M12 6v6m0 0v6m0-6h6m-6 0H6"
          />
        </svg>
        Add Product
      </button>
    </div>

    <!-- Filter & Search -->
    <div class="bg-white rounded-lg shadow mb-6 p-4">
      <div
        class="flex flex-col md:flex-row md:items-center md:justify-between space-y-4 md:space-y-0"
      >
        <div
          class="flex flex-col md:flex-row md:space-x-4 space-y-2 md:space-y-0"
        >
          <!-- Category Filter -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1"
              >Category</label
            >
            <select
              v-model="filters.category"
              class="border border-gray-300 rounded-md shadow-sm px-4 py-2 focus:ring-indigo-500 focus:border-indigo-500"
            >
              <option value="">All Categories</option>
              <option v-for="category in categories" :key="category.id" :value="category.id">
                {{ category.name }}
              </option>
            </select>
          </div>

          <!-- Stock Filter -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1"
              >Stock Status</label
            >
            <select
              v-model="filters.stockStatus"
              class="border border-gray-300 rounded-md shadow-sm px-4 py-2 focus:ring-indigo-500 focus:border-indigo-500"
            >
              <option v-for="option in stockStatusOptions" :key="option.value" :value="option.value">
                {{ option.label }}
              </option>
            </select>
          </div>

          <!-- Price Range Filter -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1"
              >Price Range</label
            >
            <div class="flex items-center space-x-2">
              <input
                v-model="filters.minPrice"
                type="number"
                placeholder="Min"
                class="border border-gray-300 rounded-md shadow-sm px-4 py-2 w-20 focus:ring-indigo-500 focus:border-indigo-500"
              />
              <span>to</span>
              <input
                v-model="filters.maxPrice"
                type="number"
                placeholder="Max"
                class="border border-gray-300 rounded-md shadow-sm px-4 py-2 w-20 focus:ring-indigo-500 focus:border-indigo-500"
              />
            </div>
          </div>
        </div>

        <!-- Search -->
        <div class="flex items-center space-x-4">
          <div class="relative">
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Search products..."
              class="border border-gray-300 rounded-md shadow-sm px-10 py-2 w-full md:w-64 focus:ring-indigo-500 focus:border-indigo-500"
            />
            <div class="absolute left-3 top-2.5 text-gray-400">
              <svg
                class="h-5 w-5"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                />
              </svg>
            </div>
          </div>
          
          <!-- Clear Filters Button -->
          <button
            @click="clearFilters"
            class="px-4 py-2 text-gray-600 border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          >
            Clear Filters
          </button>
        </div>
      </div>
    </div>

    <!-- Products Table -->
    <div v-if="loading" class="flex justify-center items-center h-64">
      <GridLoader :loading="loading" color="#4F46E5" />
    </div>
    <div v-else>
      <div
        v-if="products.length"
        class="bg-white rounded-lg shadow overflow-hidden"
      >
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th
                  class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Product
                </th>
                <th
                  class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Category
                </th>
                <th
                  class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Price
                </th>
                <th
                  class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Stock
                </th>
                <th
                  class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Status
                </th>
                <th
                  class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  Actions
                </th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="product in displayedProducts" :key="product.id">
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="flex items-center">
                    <div class="text-sm font-medium text-gray-900">
                      {{ product.name }}
                    </div>
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="text-sm text-gray-900">
                    {{ product.category_name }}
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="text-sm text-gray-900">
                    {{ Formatters.formatCurrency(product.effective_price) }}
                  </div>
                  <div v-if="product.is_on_sale" class="text-sm text-red-600">
                    Sale: {{ Formatters.formatCurrency(product.sale_price) }}
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {{ product.stock }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span
                    :class="{
                      'px-2 inline-flex text-xs leading-5 font-semibold rounded-full': true,
                      'bg-green-100 text-green-800': product.stock_status === 'In Stock',
                      'bg-yellow-100 text-yellow-800': product.stock_status === 'Low Stock',
                      'bg-red-100 text-red-800': product.stock_status === 'Out of Stock',
                    }"
                  >
                    {{ product.stock_status }}
                  </span>
                </td>
                <td
                  class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium"
                >
                  <button
                    @click="openEditProduct(product)"
                    class="text-indigo-600 hover:text-indigo-900 mr-4"
                  >
                    Edit
                  </button>
                  <button
                    @click="confirmDeleteProduct(product)"
                    class="text-red-600 hover:text-red-900"
                  >
                    Delete
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Pagination -->
        <div
          class="bg-white px-4 py-3 flex items-center justify-between border-t border-gray-200 sm:px-6"
        >
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
                <span class="font-medium">{{ totalProducts }}</span>
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
      <div v-else class="text-center text-gray-500 py-6">
        No products found.
      </div>
    </div>

    <!-- Add/Edit Product Modal -->
    <ProductFormModal
      :is-open="showProductModal"
      :product="currentProduct"
      :is-editing="editingProduct"
      @close="closeProductModal"
      @save="saveProduct"
    />

    <!-- Delete Confirmation Modal -->
    <DeleteConfirmModal
      :is-open="showDeleteModal"
      :product="productToDelete"
      @close="closeDeleteModal"
      @confirm="deleteProduct"
    />
  </div>
</template>
