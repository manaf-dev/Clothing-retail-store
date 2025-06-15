<script setup>
  import { ref, onMounted, computed } from "vue";
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

  // Computed properties
  const filteredProducts = computed(() => {
    let filtered = products.value;

    if (searchQuery.value) {
      filtered = filtered.filter((product) =>
        product.name.toLowerCase().includes(searchQuery.value.toLowerCase())
      );
    }

    if (selectedCategory.value !== "all") {
      filtered = filtered.filter(
        (product) => product.category.id === selectedCategory.value
      );
    }

    return filtered;
  });

  const formattedTotal = computed(() => {
    return new Intl.NumberFormat("en-US", {
      style: "currency",
      currency: "USD",
    }).format(posStore.cartTotal);
  });

  // Methods
  const loadProducts = async () => {
    try {
      loading.value = true;
      const response = await productService.getAllProducts();
      products.value = response.results || response;
    } catch (error) {
      toast.error("Failed to load products");
      console.error("Error loading products:", error);
    } finally {
      loading.value = false;
    }
  };

  const loadCategories = async () => {
    try {
      loading.value = true;
      const response = await productService.getCategories();
      console.log("Categories loaded:", response);
      categories.value = response;
    } catch (error) {
      console.error("Error loading categories:", error);
    } finally {
      loading.value = false;
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
      await posStore.processOrder(customerName.value);
      customerName.value = "";
      toast.success("Order processed successfully!");

      // Reload products to update stock
      await loadProducts();
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
    toast.info("Cart cleared");
  };

  // Lifecycle
  onMounted(async () => {
    await loadProducts();
    await loadCategories();
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

      <div v-else class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        <div
          v-for="product in filteredProducts"
          :key="product.id"
          class="bg-white border border-gray-200 rounded-lg shadow-sm hover:shadow-md transition-shadow cursor-pointer"
          @click="addToCart(product)"
        >
          <div class="p-4">
            <div class="aspect-w-1 aspect-h-1 mb-3">
              <!-- <img
                :src="product.image || '/api/placeholder/150/150'"
                :alt="product.name"
                class="w-full h-32 object-cover rounded"
              /> -->
            </div>
            <h3 class="font-medium text-gray-900 mb-1 truncate">
              {{ product.name }}
            </h3>
            <p class="text-sm text-gray-500 mb-2">{{ product.sku }}</p>
            <div class="flex justify-between items-center">
              <span class="text-lg font-bold text-gray-900">
                ${{ product.price }}
              </span>
              <span
                class="text-xs px-2 py-1 rounded"
                :class="
                  product.stock_quantity > 10
                    ? 'bg-green-100 text-green-800'
                    : product.stock_quantity > 0
                    ? 'bg-yellow-100 text-yellow-800'
                    : 'bg-red-100 text-red-800'
                "
              >
                {{ product.stock_quantity }} in stock
              </span>
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
                <p class="text-sm text-gray-500">${{ item.price }} each</p>
                <p class="font-medium">
                  ${{ (item.price * item.quantity).toFixed(2) }}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Cart Footer -->
      <div class="p-4 border-t border-gray-200 bg-white">
        <div class="mb-4">
          <div class="flex justify-between items-center text-lg font-bold">
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
