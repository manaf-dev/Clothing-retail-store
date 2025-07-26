<script setup>
  import { ref, onMounted, computed, watch } from "vue";
  import { usePOSStore } from "@/stores/pos.js";
  import { productService } from "@/services/productService.js";
  import { useToast } from "vue-toastification";

  const posStore = usePOSStore();
  const toast = useToast();

  const products = ref([]);
  const searchQuery = ref("");
  const customerName = ref("");
  const loading = ref(false);
  const selectedCategory = ref("all");
  const categories = ref([]);
  
  // Pagination - same as products component
  const currentPage = ref(1);
  const totalPages = ref(1);
  const totalProducts = ref(0);
  const hasNext = ref(false);
  const hasPrevious = ref(false);
  
  // Payment and pricing
  const paymentMethod = ref("cash");
  const taxRate = ref(0);
  const discountAmount = ref(0);
  const discountType = ref("amount"); // 'amount' or 'percentage'

  // Computed properties
  const filteredProducts = computed(() => {
    // Since we're handling filtering on the backend through the API,
    // we can just return all products that were already filtered
    return products.value;
  });

  const subtotal = computed(() => posStore.cartTotal);
  
  const taxAmount = computed(() => {
    return (subtotal.value * taxRate.value) / 100;
  });
  
  const discountValue = computed(() => {
    if (discountType.value === "percentage") {
      return (subtotal.value * discountAmount.value) / 100;
    }
    return discountAmount.value;
  });
  
  const finalTotal = computed(() => {
    return Math.max(0, subtotal.value + taxAmount.value - discountValue.value);
  });

  const formattedTotal = computed(() => {
    return new Intl.NumberFormat("en-GH", {
      style: "currency",
      currency: "GHS",
    }).format(finalTotal.value);
  });
  
  const paginationStart = computed(() => {
    if (totalProducts.value === 0) return 0;
    return (currentPage.value - 1) * 10 + 1; // Backend uses 10 items per page by default
  });

  const paginationEnd = computed(() => {
    const end = currentPage.value * 10;
    return Math.min(end, totalProducts.value);
  });

  // Methods
  const loadProducts = async (page = 1) => {
    try {
      loading.value = true;
      const params = {
        page,
        search: searchQuery.value,
        category: selectedCategory.value !== 'all' ? selectedCategory.value : '',
        status: 'active',
        ordering: 'name'
      };

      const response = await productService.searchProducts(params);
      
      // Handle paginated response - same as products component
      if (response.results) {
        products.value = productService.transformMultipleToFrontend(response.results);
        currentPage.value = response.current_page || page;
        totalPages.value = response.num_pages || 1;
        totalProducts.value = response.count || 0;
        hasNext.value = response.has_next || false;
        hasPrevious.value = response.has_previous || false;
      } else {
        // Handle non-paginated response (array)
        products.value = productService.transformMultipleToFrontend(response);
        totalPages.value = 1;
        totalProducts.value = response.length;
        hasNext.value = false;
        hasPrevious.value = false;
      }
    } catch (error) {
      toast.error("Failed to load products");
      console.error("Error loading products:", error);
      products.value = [];
    } finally {
      loading.value = false;
    }
  };

  const loadCategories = async () => {
    try {
      const response = await productService.getCategories();
      categories.value = response;
    } catch (error) {
      console.error("Error loading categories:", error);
    }
  };

  // Pagination functions - same as products component
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

  const addToCart = (product) => {
    if (product.stock <= 0) {
      toast.warning("Product is out of stock");
      return;
    }

    posStore.addToCart(product);
    toast.success(`${product.name} added to cart`);
  };

  const removeFromCart = (productId) => {
    posStore.removeFromCart(productId);
    toast.info("Item removed from cart");
  };

  const updateQuantity = (productId, quantity) => {
    posStore.updateCartItemQuantity(productId, quantity);
  };

  const processOrder = async () => {
    if (posStore.cart.length === 0) {
      toast.warning("Cart is empty");
      return;
    }

    try {
      loading.value = true;
      
      const orderData = {
        customer_name: customerName.value,
        payment_method: paymentMethod.value,
        tax_amount: taxAmount.value,
        discount_amount: discountValue.value,
        items: posStore.cart.map(item => ({
          product_id: item.product_id,
          quantity: item.quantity,
          price: item.price
        }))
      };

      await posStore.processOrder(orderData);
      
      // Reset form
      customerName.value = "";
      paymentMethod.value = "cash";
      taxRate.value = 0;
      discountAmount.value = 0;
      discountType.value = "amount";
      
      toast.success("Order processed successfully!");

      // Reload current page to update stock
      await loadProducts(currentPage.value);
    } catch (error) {
      toast.error("Failed to process order");
      console.error("Error processing order:", error);
    } finally {
      loading.value = false;
    }
  };

  const clearCart = () => {
    posStore.clearCart();
    customerName.value = "";
    paymentMethod.value = "cash";
    taxRate.value = 0;
    discountAmount.value = 0;
    discountType.value = "amount";
    toast.info("Cart cleared");
  };

  // Watch for search and category changes - same as products component
  watch([searchQuery, selectedCategory], async () => {
    await loadProducts(1);
  }, { deep: true });

  // Lifecycle
  onMounted(async () => {
    await Promise.all([
      loadProducts(),
      loadCategories()
    ]);
  });
</script>

<template>
  <div class="h-full flex bg-white">
    <!-- Products Grid - Left Side -->
    <div class="flex-1 p-6 overflow-y-auto">
      <div class="mb-6">
        <h1 class="text-2xl font-bold text-gray-900 mb-4">Point of Sale</h1>

        <!-- Search and Filter -->
        <div class="flex gap-4 mb-4">
          <div class="flex-1">
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Search products..."
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <select
            v-model="selectedCategory"
            class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          >
            <option value="all">All Categories</option>
            <option
              v-for="category in categories"
              :key="category.id"
              :value="category.id"
            >
              {{ category.name }}
            </option>
          </select>
        </div>
      </div>

      <!-- Products Grid -->
      <div v-if="loading" class="flex justify-center">
        <div
          class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"
        ></div>
      </div>

      <div v-else-if="filteredProducts.length === 0" class="text-center text-gray-500 py-8">
        <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
        </svg>
        <p class="mt-2">No products found</p>
        <p class="text-sm">Try adjusting your search or filters</p>
      </div>

      <div v-else class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        <div
          v-for="product in filteredProducts"
          :key="product.id"
          class="bg-white border border-gray-200 rounded-lg shadow-sm hover:shadow-md transition-shadow cursor-pointer"
          @click="addToCart(product)"
        >
          <div class="p-4">
            <div class="aspect-w-1 aspect-h-1 mb-3">
              <!-- Product image placeholder - removed since no images -->
              <div class="w-full h-32 bg-gray-100 rounded flex items-center justify-center">
                <img
                  v-if="product.image"
                  :src="product.image"
                  alt="Product Image"
                  class="w-full h-full object-cover rounded"
                />
                <div v-else class="w-8 h-8 flex items-center justify-center text-gray-400">
                  <svg class="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
                  </svg>
                </div>
              </div>
            </div>
            <h3 class="font-medium text-gray-900 mb-1 truncate">
              {{ product.name }}
            </h3>
            <p class="text-sm text-gray-500 mb-2">{{ product.category_name }}</p>
            <div class="flex justify-between items-center">
              <span class="text-lg font-bold text-gray-900">
                ₵{{ product.effective_price }}
              </span>
              <span
                class="text-xs px-2 py-1 rounded"
                :class="
                  product.stock > 10
                    ? 'bg-green-100 text-green-800'
                    : product.stock > 0
                    ? 'bg-yellow-100 text-yellow-800'
                    : 'bg-red-100 text-red-800'
                "
              >
                {{ product.stock }} in stock
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Pagination - same as products component -->
      <div v-if="products.length > 0" class="mt-6">
        <div class="bg-white px-4 py-3 flex items-center justify-between border-t border-gray-200 sm:px-6">
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
          <div class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
            <div>
              <p class="text-sm text-gray-700">
                Showing
                <span class="font-medium">{{ paginationStart }}</span>
                to
                <span class="font-medium">{{ paginationEnd }}</span>
                of
                <span class="font-medium">{{ totalProducts }}</span>
                products
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
                  v-for="page in totalPages"
                  :key="page"
                  @click="goToPage(page)"
                  :class="{
                    'relative inline-flex items-center px-4 py-2 border text-sm font-medium': true,
                    'bg-indigo-50 border-indigo-500 text-indigo-600': currentPage === page,
                    'bg-white border-gray-300 text-gray-500 hover:bg-gray-50': currentPage !== page,
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
    </div>

    <!-- Cart - Right Side -->
    <div class="w-96 bg-gray-50 border-l border-gray-200 flex flex-col">
      <!-- Cart Header -->
      <div class="p-6 border-b border-gray-200">
        <h2 class="text-xl font-bold text-gray-900">Current Order</h2>
        <p class="text-sm text-gray-500">{{ posStore.cartItemCount }} items</p>
      </div>

      <!-- Customer Name -->
      <div class="p-4 border-b border-gray-200">
        <input
          v-model="customerName"
          type="text"
          placeholder="Customer name (optional)"
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        />
      </div>

      <!-- Cart Items -->
      <div class="flex-1 overflow-y-auto p-4">
        <div
          v-if="posStore.cart.length === 0"
          class="text-center text-gray-500 mt-8"
        >
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
              d="M3 3h2l.4 2M7 13h10l4-8H5.4m0 0L7 13m0 0l-1.38 1.62M7 13l1.38 1.62M7 13V7a1 1 0 011-1h12M19 17h2m-2 0a2 2 0 01-2 2h-2m2-2a2 2 0 00-2-2h-2m0 0h2"
            />
          </svg>
          <p class="mt-2">Cart is empty</p>
          <p class="text-sm">Add products to start</p>
        </div>

        <div v-else class="space-y-3">
          <div
            v-for="item in posStore.cart"
            :key="item.product_id"
            class="bg-white p-3 rounded-lg border border-gray-200"
          >
            <div class="flex justify-between items-start mb-2">
              <h4 class="font-medium text-gray-900 text-sm">
                {{ item.product_name }}
              </h4>
              <button
                @click="removeFromCart(item.product_id)"
                class="text-red-500 hover:text-red-700"
              >
                <svg
                  class="h-4 w-4"
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

            <div class="flex justify-between items-center">
              <div class="flex items-center space-x-2">
                <button
                  @click="updateQuantity(item.product_id, item.quantity - 1)"
                  class="w-6 h-6 rounded-full bg-gray-200 flex items-center justify-center hover:bg-gray-300"
                >
                  -
                </button>
                <span class="w-8 text-center">{{ item.quantity }}</span>
                <button
                  @click="updateQuantity(item.product_id, item.quantity + 1)"
                  class="w-6 h-6 rounded-full bg-gray-200 flex items-center justify-center hover:bg-gray-300"
                >
                  +
                </button>
              </div>

              <div class="text-right">
                <p class="text-sm text-gray-500">₵{{ item.price }} each</p>
                <p class="font-medium">
                  ₵{{ (item.price * item.quantity).toFixed(2) }}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Cart Footer -->
      <div class="p-4 border-t border-gray-200 bg-white space-y-4">
        <!-- Payment Method -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Payment Method</label>
          <select
            v-model="paymentMethod"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="cash">Cash</option>
            <option value="card">Card</option>
            <option value="mobile_money">Mobile Money</option>
            <option value="bank_transfer">Bank Transfer</option>
            <option value="credit">Credit</option>
          </select>
        </div>

        <!-- Tax -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Tax Rate (%)</label>
          <input
            v-model.number="taxRate"
            type="number"
            min="0"
            max="100"
            step="0.1"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>

        <!-- Discount -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Discount</label>
          <div class="flex space-x-2">
            <input
              v-model.number="discountAmount"
              type="number"
              min="0"
              :step="discountType === 'percentage' ? '0.1' : '0.01'"
              class="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
            <select
              v-model="discountType"
              class="px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
            >
              <option value="amount">₵</option>
              <option value="percentage">%</option>
            </select>
          </div>
        </div>

        <!-- Order Summary -->
        <div class="space-y-2 pt-2 border-t border-gray-200">
          <div class="flex justify-between text-sm">
            <span>Subtotal:</span>
            <span>₵{{ subtotal.toFixed(2) }}</span>
          </div>
          <div v-if="taxAmount > 0" class="flex justify-between text-sm">
            <span>Tax ({{ taxRate }}%):</span>
            <span>₵{{ taxAmount.toFixed(2) }}</span>
          </div>
          <div v-if="discountValue > 0" class="flex justify-between text-sm">
            <span>Discount:</span>
            <span>-₵{{ discountValue.toFixed(2) }}</span>
          </div>
          <div class="flex justify-between items-center text-lg font-bold pt-2 border-t border-gray-200">
            <span>Total:</span>
            <span>{{ formattedTotal }}</span>
          </div>
        </div>

        <div class="space-y-2">
          <button
            @click="processOrder"
            :disabled="posStore.cart.length === 0 || loading"
            class="w-full bg-blue-600 text-white py-3 px-4 rounded-lg font-medium hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
          >
            <span v-if="loading">Processing...</span>
            <span v-else>Complete Order</span>
          </button>

          <button
            @click="clearCart"
            :disabled="posStore.cart.length === 0"
            class="w-full bg-gray-200 text-gray-800 py-2 px-4 rounded-lg font-medium hover:bg-gray-300 disabled:bg-gray-100 disabled:cursor-not-allowed"
          >
            Clear Cart
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
