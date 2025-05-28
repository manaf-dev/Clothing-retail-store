<!-- src/views/ProductsView.vue -->
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
                        <label
                            class="block text-sm font-medium text-gray-700 mb-1"
                            >Category</label
                        >
                        <select
                            v-model="filters.category"
                            class="border border-gray-300 rounded-md shadow-sm px-4 py-2 focus:ring-indigo-500 focus:border-indigo-500"
                        >
                            <option value="">All Categories</option>
                            <option value="Men">Men's Clothing</option>
                            <option value="Women">Women's Clothing</option>
                            <option value="Kids">Kids' Clothing</option>
                            <option value="Accessories">Accessories</option>
                        </select>
                    </div>

                    <!-- Stock Filter -->
                    <div>
                        <label
                            class="block text-sm font-medium text-gray-700 mb-1"
                            >Stock Status</label
                        >
                        <select
                            v-model="filters.stockStatus"
                            class="border border-gray-300 rounded-md shadow-sm px-4 py-2 focus:ring-indigo-500 focus:border-indigo-500"
                        >
                            <option value="">All</option>
                            <option value="inStock">In Stock</option>
                            <option value="lowStock">Low Stock</option>
                            <option value="outOfStock">Out of Stock</option>
                        </select>
                    </div>

                    <!-- Price Range Filter -->
                    <div>
                        <label
                            class="block text-sm font-medium text-gray-700 mb-1"
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
            </div>
        </div>

        <!-- Products Table -->
        <div class="bg-white rounded-lg shadow overflow-hidden">
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
                        <tr
                            v-for="product in paginatedProducts"
                            :key="product.id"
                        >
                            <td class="px-6 py-4 whitespace-nowrap">
                                <div class="flex items-center">
                                    <div class="h-10 w-10 flex-shrink-0">
                                        <img
                                            class="h-10 w-10 rounded-md object-cover"
                                            :src="product.image"
                                            alt="Product image"
                                        />
                                    </div>
                                    <div class="ml-4">
                                        <div
                                            class="text-sm font-medium text-gray-900"
                                        >
                                            {{ product.name }}
                                        </div>
                                        <div class="text-sm text-gray-500">
                                            SKU: {{ product.sku }}
                                        </div>
                                    </div>
                                </div>
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap">
                                <div class="text-sm text-gray-900">
                                    {{ product.category }}
                                </div>
                                <div class="text-sm text-gray-500">
                                    {{ product.subCategory }}
                                </div>
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap">
                                <div class="text-sm text-gray-900">
                                    ${{ product.price.toFixed(2) }}
                                </div>
                                <div
                                    v-if="product.salePrice"
                                    class="text-sm text-red-600"
                                >
                                    Sale: ${{ product.salePrice.toFixed(2) }}
                                </div>
                            </td>
                            <td
                                class="px-6 py-4 whitespace-nowrap text-sm text-gray-500"
                            >
                                {{ product.stock }}
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap">
                                <span
                                    :class="{
                                        'px-2 inline-flex text-xs leading-5 font-semibold rounded-full': true,
                                        'bg-green-100 text-green-800':
                                            product.stock > 10,
                                        'bg-yellow-100 text-yellow-800':
                                            product.stock > 0 &&
                                            product.stock <= 10,
                                        'bg-red-100 text-red-800':
                                            product.stock === 0,
                                    }"
                                >
                                    {{
                                        product.stock > 10
                                            ? "In Stock"
                                            : product.stock > 0
                                            ? "Low Stock"
                                            : "Out of Stock"
                                    }}
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
                            <span class="font-medium">{{
                                paginationStart
                            }}</span>
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
                                @click="
                                    currentPage = Math.max(1, currentPage - 1)
                                "
                                :disabled="currentPage === 1"
                                class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50"
                                :class="{
                                    'opacity-50 cursor-not-allowed':
                                        currentPage === 1,
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
                                @click="currentPage = page"
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
                                @click="
                                    currentPage = Math.min(
                                        totalPages,
                                        currentPage + 1
                                    )
                                "
                                :disabled="currentPage === totalPages"
                                class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50"
                                :class="{
                                    'opacity-50 cursor-not-allowed':
                                        currentPage === totalPages,
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

<script setup>
    import { ref, computed } from "vue";
    import ProductFormModal from "./ProductFormModal.vue";
    import DeleteConfirmModal from "./DeleteConfirmModal.vue";

    const showProductModal = ref(false);
    const showDeleteModal = ref(false);
    const editingProduct = ref(false);
    const currentProduct = ref({
        name: "",
        sku: "",
        category: "",
        subCategory: "",
        price: 0,
        salePrice: null,
        stock: 0,
        description: "",
        image: "",
    });
    const productToDelete = ref(null);

    const openAddProduct = () => {
        currentProduct.value = {
            id: null,
            name: "",
            sku: "",
            category: "",
            subCategory: "",
            price: 0,
            salePrice: null,
            stock: 0,
            description: "",
            image: "/api/placeholder/100/100",
        };
        editingProduct.value = false;
        showProductModal.value = true;
    };

    const closeProductModal = () => {
        showProductModal.value = false;
        currentProduct.value = {
            name: "",
            sku: "",
            category: "",
            subCategory: "",
            price: 0,
            salePrice: null,
            stock: 0,
            description: "",
            image: "",
        };
        editingProduct.value = false;
    };

    const openEditProduct = (product) => {
        currentProduct.value = { ...product };
        editingProduct.value = true;
        showProductModal.value = true;
    };

    const saveProduct = () => {
        // TODO: Implement save logic
        if (editingProduct.value) {
            // Update existing product
            const index = products.value.findIndex((p) => p.id === product.id);
            if (index !== -1) {
                products.value[index] = { ...product };
            }
        } else {
            // Add new product
            const newId = Math.max(...products.value.map((p) => p.id)) + 1;
            products.value.push({ ...product, id: newId });
        }
        closeProductModal();
    };

    const confirmDeleteProduct = (product) => {
        productToDelete.value = product;
        showDeleteModal.value = true;
    };

    const closeDeleteModal = () => {
        showDeleteModal.value = false;
        productToDelete.value = null;
    };

    const deleteProduct = () => {
        // TODO: Implement delete logic
        const index = products.value.findIndex(
            (p) => p.id === productToDelete.value.id
        );
        if (index !== -1) {
            products.value.splice(index, 1);
        }
        closeDeleteModal();
    };

    // State
    const searchQuery = ref("");
    const filters = ref({
        category: "",
        stockStatus: "",
        minPrice: "",
        maxPrice: "",
    });

    const currentPage = ref(1);
    const perPage = 10;

    // Sample product data (will be replaced by API calls)
    const products = ref([
        {
            id: 1,
            name: "Men's Slim Fit Jeans",
            sku: "MJ-101",
            category: "Men",
            subCategory: "Jeans",
            price: 59.99,
            salePrice: null,
            stock: 5,
            description:
                "Classic blue slim fit jeans for men. Comfortable and stylish for everyday wear.",
            image: "/api/placeholder/100/100",
        },
        {
            id: 2,
            name: "Women's Summer Dress",
            sku: "WD-202",
            category: "Women",
            subCategory: "Dresses",
            price: 79.99,
            salePrice: 49.99,
            stock: 15,
            description: "Light and flowy summer dress with floral pattern.",
            image: "/api/placeholder/100/100",
        },
        {
            id: 3,
            name: "Kids Winter Coat",
            sku: "KC-303",
            category: "Kids",
            subCategory: "Outerwear",
            price: 89.99,
            salePrice: null,
            stock: 4,
            description:
                "Warm winter coat for kids with hood and water-resistant outer shell.",
            image: "/api/placeholder/100/100",
        },
        {
            id: 4,
            name: "Silver Necklace",
            sku: "AN-404",
            category: "Accessories",
            subCategory: "Jewelry",
            price: 129.99,
            salePrice: null,
            stock: 2,
            description:
                "Sterling silver necklace with pendant. Perfect for special occasions.",
            image: "/api/placeholder/100/100",
        },
        {
            id: 5,
            name: "Men's Formal Shirt",
            sku: "MS-505",
            category: "Men",
            subCategory: "Shirts",
            price: 69.99,
            salePrice: null,
            stock: 20,
            description:
                "Classic white formal shirt for men. Perfect for business and formal occasions.",
            image: "/api/placeholder/100/100",
        },
        {
            id: 6,
            name: "Women's Leather Jacket",
            sku: "WJ-606",
            category: "Women",
            subCategory: "Jackets",
            price: 199.99,
            salePrice: 159.99,
            stock: 3,
            description:
                "Stylish faux leather jacket for women with quilted lining.",
            image: "/api/placeholder/100/100",
        },
        {
            id: 7,
            name: "Kids Denim Jeans",
            sku: "KJ-707",
            category: "Kids",
            subCategory: "Jeans",
            price: 39.99,
            salePrice: null,
            stock: 12,
            description: "Comfortable and durable denim jeans for active kids.",
            image: "/api/placeholder/100/100",
        },
        {
            id: 8,
            name: "Leather Belt",
            sku: "AB-808",
            category: "Accessories",
            subCategory: "Belts",
            price: 45.99,
            salePrice: null,
            stock: 8,
            description: "Premium leather belt with metal buckle.",
            image: "/api/placeholder/100/100",
        },
        {
            id: 9,
            name: "Men's Running Shoes",
            sku: "MF-909",
            category: "Men",
            subCategory: "Footwear",
            price: 129.99,
            salePrice: 99.99,
            stock: 6,
            description: "Lightweight and comfortable running shoes for men.",
            image: "/api/placeholder/100/100",
        },
        {
            id: 10,
            name: "Women's Handbag",
            sku: "WB-010",
            category: "Women",
            subCategory: "Bags",
            price: 89.99,
            salePrice: null,
            stock: 7,
            description: "Stylish and spacious handbag for everyday use.",
            image: "/api/placeholder/100/100",
        },
        {
            id: 11,
            name: "Kids T-Shirt",
            sku: "KT-011",
            category: "Kids",
            subCategory: "T-Shirts",
            price: 24.99,
            salePrice: 19.99,
            stock: 25,
            description: "Soft cotton t-shirt with fun graphic print for kids.",
            image: "/api/placeholder/100/100",
        },
        {
            id: 12,
            name: "Sunglasses",
            sku: "AS-012",
            category: "Accessories",
            subCategory: "Eyewear",
            price: 79.99,
            salePrice: null,
            stock: 10,
            description: "Stylish sunglasses with UV protection.",
            image: "/api/placeholder/100/100",
        },
    ]);

    // Computed Properties
    const filteredProducts = computed(() => {
        let filtered = [...products.value];

        // Apply category filter
        if (filters.value.category) {
            filtered = filtered.filter(
                (product) => product.category === filters.value.category
            );
        }

        // Apply stock status filter
        if (filters.value.stockStatus) {
            switch (filters.value.stockStatus) {
                case "inStock":
                    filtered = filtered.filter((product) => product.stock > 10);
                    break;
                case "lowStock":
                    filtered = filtered.filter(
                        (product) => product.stock > 0 && product.stock <= 10
                    );
                    break;
                case "outOfStock":
                    filtered = filtered.filter(
                        (product) => product.stock === 0
                    );
                    break;
            }
        }

        // Apply price range filter
        if (filters.value.minPrice) {
            filtered = filtered.filter(
                (product) => product.price >= parseFloat(filters.value.minPrice)
            );
        }
        if (filters.value.maxPrice) {
            filtered = filtered.filter(
                (product) => product.price <= parseFloat(filters.value.maxPrice)
            );
        }

        // Apply search query
        if (searchQuery.value) {
            const query = searchQuery.value.toLowerCase();
            filtered = filtered.filter(
                (product) =>
                    product.name.toLowerCase().includes(query) ||
                    product.sku.toLowerCase().includes(query) ||
                    product.description.toLowerCase().includes(query)
            );
        }

        return filtered;
    });

    const paginatedProducts = computed(() => {
        const start = (currentPage.value - 1) * perPage;
        const end = start + perPage;
        return filteredProducts.value.slice(start, end);
    });

    const totalProducts = computed(() => filteredProducts.value.length);
    const totalPages = computed(() => Math.ceil(totalProducts.value / perPage));
    const paginationStart = computed(
        () => (currentPage.value - 1) * perPage + 1
    );
    const paginationEnd = computed(() =>
        Math.min(currentPage.value * perPage, totalProducts.value)
    );

    // Methods
    const getStockStatus = (stock) => {
        if (stock > 10) return "In Stock";
        if (stock > 0) return "Low Stock";
        return "Out of Stock";
    };
</script>
