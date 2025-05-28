<script setup>
    import { ref, computed } from "vue";

    const searchTerm = ref("");
    const selectedCategory = ref("");
    const selectedStockStatus = ref("");
    const currentPage = ref(1);
    const itemsPerPage = ref(10);
    const showRestockModal = ref(false);
    const selectedItem = ref(null);
    const selectedBulkItems = ref([]);
    const restockQuantity = ref(1);
    const supplier = ref("");
    const restockNotes = ref("");

    const inventory = ref([
        {
            id: 1,
            name: "Men's Casual T-Shirt",
            sku: "MCT001",
            category: "Men",
            price: 29.99,
            currentStock: 15,
            minStockLevel: 10,
            lastRestocked: "2025-05-20",
            image: "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=100&h=100&fit=crop",
        },
        {
            id: 2,
            name: "Women's Summer Dress",
            sku: "WSD002",
            category: "Women",
            price: 59.99,
            currentStock: 8,
            minStockLevel: 10,
            lastRestocked: "2025-05-18",
            image: "https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=100&h=100&fit=crop",
        },
        {
            id: 3,
            name: "Kids Denim Jacket",
            sku: "KDJ003",
            category: "Kids",
            price: 39.99,
            currentStock: 0,
            minStockLevel: 5,
            lastRestocked: "2025-05-10",
            image: "https://images.unsplash.com/photo-1503919005314-30d93d07d823?w=100&h=100&fit=crop",
        },
        {
            id: 4,
            name: "Women's Leather Handbag",
            sku: "WLH004",
            category: "Accessories",
            price: 89.99,
            currentStock: 12,
            minStockLevel: 8,
            lastRestocked: "2025-05-22",
            image: "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=100&h=100&fit=crop",
        },
        {
            id: 5,
            name: "Men's Formal Shirt",
            sku: "MFS005",
            category: "Men",
            price: 49.99,
            currentStock: 3,
            minStockLevel: 8,
            lastRestocked: "2025-05-15",
            image: "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=100&h=100&fit=crop",
        },
        {
            id: 6,
            name: "Women's Athletic Wear",
            sku: "WAW006",
            category: "Women",
            price: 34.99,
            currentStock: 18,
            minStockLevel: 12,
            lastRestocked: "2025-05-25",
            image: "https://images.unsplash.com/photo-1506629905607-4b11abb7e54b?w=100&h=100&fit=crop",
        },
        {
            id: 7,
            name: "Kids School Uniform",
            sku: "KSU007",
            category: "Kids",
            price: 25.99,
            currentStock: 22,
            minStockLevel: 15,
            lastRestocked: "2025-05-23",
            image: "https://images.unsplash.com/photo-1503919005314-30d93d07d823?w=100&h=100&fit=crop",
        },
        {
            id: 8,
            name: "Silver Watch",
            sku: "SW008",
            category: "Accessories",
            price: 149.99,
            currentStock: 6,
            minStockLevel: 10,
            lastRestocked: "2025-05-19",
            image: "https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=100&h=100&fit=crop",
        },
    ]);

    const totalItems = computed(() => inventory.value.length);

    const inStockItems = computed(
        () =>
            inventory.value.filter(
                (item) => item.currentStock > item.minStockLevel
            ).length
    );

    const lowStockItems = computed(
        () =>
            inventory.value.filter(
                (item) =>
                    item.currentStock <= item.minStockLevel &&
                    item.currentStock > 0
            ).length
    );

    const outOfStockItems = computed(
        () => inventory.value.filter((item) => item.currentStock === 0).length
    );

    const filteredInventory = computed(() => {
        let filtered = inventory.value;

        if (searchTerm.value) {
            filtered = filtered.filter(
                (item) =>
                    item.name
                        .toLowerCase()
                        .includes(searchTerm.value.toLowerCase()) ||
                    item.sku
                        .toLowerCase()
                        .includes(searchTerm.value.toLowerCase())
            );
        }

        if (selectedCategory.value) {
            filtered = filtered.filter(
                (item) => item.category === selectedCategory.value
            );
        }

        if (selectedStockStatus.value) {
            filtered = filtered.filter((item) => {
                if (selectedStockStatus.value === "in-stock") {
                    return item.currentStock > item.minStockLevel;
                } else if (selectedStockStatus.value === "low-stock") {
                    return (
                        item.currentStock <= item.minStockLevel &&
                        item.currentStock > 0
                    );
                } else if (selectedStockStatus.value === "out-of-stock") {
                    return item.currentStock === 0;
                }
                return true;
            });
        }

        return filtered;
    });

    const paginatedInventory = computed(() => {
        const start = (currentPage.value - 1) * itemsPerPage.value;
        const end = start + itemsPerPage.value;
        return filteredInventory.value.slice(start, end);
    });

    const totalPages = computed(() =>
        Math.ceil(filteredInventory.value.length / itemsPerPage.value)
    );

    const visiblePages = computed(() => {
        const pages = [];
        const start = Math.max(1, currentPage.value - 2);
        const end = Math.min(totalPages.value, currentPage.value + 2);
        for (let i = start; i <= end; i++) {
            pages.push(i);
        }
        return pages;
    });

    function clearFilters() {
        searchTerm.value = "";
        selectedCategory.value = "";
        selectedStockStatus.value = "";
        currentPage.value = 1;
    }

    function previousPage() {
        if (currentPage.value > 1) {
            currentPage.value--;
        }
    }

    function nextPage() {
        if (currentPage.value < totalPages.value) {
            currentPage.value++;
        }
    }

    function goToPage(page) {
        currentPage.value = page;
    }

    function openRestockModal(item = null) {
        selectedItem.value = item;
        showRestockModal.value = true;
        restockQuantity.value = 1;
        supplier.value = "";
        restockNotes.value = "";
        selectedBulkItems.value = [];
    }

    function closeRestockModal() {
        showRestockModal.value = false;
        selectedItem.value = null;
        selectedBulkItems.value = [];
    }

    function submitRestock() {
        if (selectedItem.value) {
            // Single item restock
            const item = inventory.value.find(
                (i) => i.id === selectedItem.value.id
            );
            if (item) {
                item.currentStock += restockQuantity.value;
                item.lastRestocked = new Date().toISOString().split("T")[0];
            }
            console.log(
                `Restocked ${selectedItem.value.name} with ${restockQuantity.value} units`
            );
        } else {
            // Bulk restock
            selectedBulkItems.value.forEach((itemId) => {
                const item = inventory.value.find((i) => i.id === itemId);
                if (item) {
                    item.currentStock += restockQuantity.value;
                    item.lastRestocked = new Date().toISOString().split("T")[0];
                }
            });
            console.log(
                `Bulk restocked ${selectedBulkItems.value.length} items with ${restockQuantity.value} units each`
            );
        }

        // API call would be made here
        // POST /api/inventory/restock

        closeRestockModal();
    }

    function generateInventoryReport() {
        console.log("Generating inventory report...");
        // API call would be made here
        // GET /api/inventory/report
    }
</script>

<!-- src/views/InventoryView.vue -->
<template>
    <div>
        <div class="flex justify-between items-center mb-6">
            <h1 class="text-2xl font-semibold text-gray-800">
                Inventory Management
            </h1>
            <div class="flex space-x-3">
                <button
                    @click="showRestockModal = true"
                    class="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg text-sm font-medium"
                >
                    <svg
                        class="h-4 w-4 mr-2 inline"
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
                    Restock Products
                </button>
                <button
                    @click="generateInventoryReport"
                    class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm font-medium"
                >
                    <svg
                        class="h-4 w-4 mr-2 inline"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                    >
                        <path
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            stroke-width="2"
                            d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                        />
                    </svg>
                    Generate Report
                </button>
            </div>
        </div>

        <!-- Inventory Stats -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
            <div class="bg-white rounded-lg shadow p-6">
                <div class="flex items-center">
                    <div class="p-3 rounded-full bg-blue-100 text-blue-500">
                        <svg
                            class="h-8 w-8"
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke="currentColor"
                        >
                            <path
                                stroke-linecap="round"
                                stroke-linejoin="round"
                                stroke-width="2"
                                d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"
                            />
                        </svg>
                    </div>
                    <div class="ml-4">
                        <h2 class="text-sm font-medium text-gray-600">
                            Total Items
                        </h2>
                        <p class="text-2xl font-semibold text-gray-800">
                            {{ totalItems }}
                        </p>
                    </div>
                </div>
            </div>

            <div class="bg-white rounded-lg shadow p-6">
                <div class="flex items-center">
                    <div class="p-3 rounded-full bg-green-100 text-green-500">
                        <svg
                            class="h-8 w-8"
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke="currentColor"
                        >
                            <path
                                stroke-linecap="round"
                                stroke-linejoin="round"
                                stroke-width="2"
                                d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                            />
                        </svg>
                    </div>
                    <div class="ml-4">
                        <h2 class="text-sm font-medium text-gray-600">
                            In Stock
                        </h2>
                        <p class="text-2xl font-semibold text-gray-800">
                            {{ inStockItems }}
                        </p>
                    </div>
                </div>
            </div>

            <div class="bg-white rounded-lg shadow p-6">
                <div class="flex items-center">
                    <div class="p-3 rounded-full bg-yellow-100 text-yellow-500">
                        <svg
                            class="h-8 w-8"
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke="currentColor"
                        >
                            <path
                                stroke-linecap="round"
                                stroke-linejoin="round"
                                stroke-width="2"
                                d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
                            />
                        </svg>
                    </div>
                    <div class="ml-4">
                        <h2 class="text-sm font-medium text-gray-600">
                            Low Stock
                        </h2>
                        <p class="text-2xl font-semibold text-gray-800">
                            {{ lowStockItems }}
                        </p>
                    </div>
                </div>
            </div>

            <div class="bg-white rounded-lg shadow p-6">
                <div class="flex items-center">
                    <div class="p-3 rounded-full bg-red-100 text-red-500">
                        <svg
                            class="h-8 w-8"
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
                    </div>
                    <div class="ml-4">
                        <h2 class="text-sm font-medium text-gray-600">
                            Out of Stock
                        </h2>
                        <p class="text-2xl font-semibold text-gray-800">
                            {{ outOfStockItems }}
                        </p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Filters and Search -->
        <div class="bg-white rounded-lg shadow p-4 mb-6">
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1"
                        >Search Products</label
                    >
                    <input
                        v-model="searchTerm"
                        type="text"
                        placeholder="Search by name or SKU..."
                        class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                </div>

                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1"
                        >Category</label
                    >
                    <select
                        v-model="selectedCategory"
                        class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                        <option value="">All Categories</option>
                        <option value="Men">Men's Clothing</option>
                        <option value="Women">Women's Clothing</option>
                        <option value="Kids">Kids' Clothing</option>
                        <option value="Accessories">Accessories</option>
                    </select>
                </div>

                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1"
                        >Stock Status</label
                    >
                    <select
                        v-model="selectedStockStatus"
                        class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                        <option value="">All Items</option>
                        <option value="in-stock">In Stock</option>
                        <option value="low-stock">Low Stock</option>
                        <option value="out-of-stock">Out of Stock</option>
                    </select>
                </div>

                <div class="flex items-end">
                    <button
                        @click="clearFilters"
                        class="w-full bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded-lg text-sm font-medium"
                    >
                        Clear Filters
                    </button>
                </div>
            </div>
        </div>

        <!-- Inventory Table -->
        <div class="bg-white rounded-lg shadow overflow-hidden">
            <div class="px-6 py-4 border-b border-gray-200">
                <h3 class="text-lg font-medium text-gray-800">
                    Inventory Items ({{ filteredInventory.length }})
                </h3>
            </div>

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
                                SKU
                            </th>
                            <th
                                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                            >
                                Category
                            </th>
                            <th
                                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                            >
                                Current Stock
                            </th>
                            <th
                                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                            >
                                Min Stock Level
                            </th>
                            <th
                                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                            >
                                Last Restocked
                            </th>
                            <th
                                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                            >
                                Actions
                            </th>
                        </tr>
                    </thead>
                    <tbody class="bg-white divide-y divide-gray-200">
                        <tr v-for="item in paginatedInventory" :key="item.id">
                            <td class="px-6 py-4 whitespace-nowrap">
                                <div class="flex items-center">
                                    <img
                                        :src="item.image"
                                        :alt="item.name"
                                        class="h-12 w-12 rounded-lg object-cover"
                                    />
                                    <div class="ml-4">
                                        <div
                                            class="text-sm font-medium text-gray-900"
                                        >
                                            {{ item.name }}
                                        </div>
                                        <div class="text-sm text-gray-500">
                                            ${{ item.price }}
                                        </div>
                                    </div>
                                </div>
                            </td>
                            <td
                                class="px-6 py-4 whitespace-nowrap text-sm text-gray-900"
                            >
                                {{ item.sku }}
                            </td>
                            <td
                                class="px-6 py-4 whitespace-nowrap text-sm text-gray-500"
                            >
                                {{ item.category }}
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap">
                                <span
                                    :class="{
                                        'bg-green-100 text-green-800':
                                            item.currentStock >
                                            item.minStockLevel,
                                        'bg-yellow-100 text-yellow-800':
                                            item.currentStock <=
                                                item.minStockLevel &&
                                            item.currentStock > 0,
                                        'bg-red-100 text-red-800':
                                            item.currentStock === 0,
                                    }"
                                    class="px-2 py-1 text-xs font-semibold rounded-full"
                                >
                                    {{ item.currentStock }}
                                </span>
                            </td>
                            <td
                                class="px-6 py-4 whitespace-nowrap text-sm text-gray-500"
                            >
                                {{ item.minStockLevel }}
                            </td>
                            <td
                                class="px-6 py-4 whitespace-nowrap text-sm text-gray-500"
                            >
                                {{ item.lastRestocked }}
                            </td>
                            <td
                                class="px-6 py-4 whitespace-nowrap text-sm font-medium"
                            >
                                <div class="flex space-x-2">
                                    <button
                                        @click="openRestockModal(item)"
                                        class="text-blue-600 hover:text-blue-900"
                                    >
                                        Restock
                                    </button>
                                    <button
                                        class="text-green-600 hover:text-green-900"
                                    >
                                        History
                                    </button>
                                    <button
                                        class="text-gray-600 hover:text-gray-900"
                                    >
                                        Edit
                                    </button>
                                </div>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <!-- Pagination -->
            <div
                class="bg-white px-4 py-3 flex items-center justify-between border-t border-gray-200 sm:px-6"
            >
                <div class="flex-1 flex justify-between sm:hidden">
                    <button
                        @click="previousPage"
                        :disabled="currentPage === 1"
                        class="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50"
                    >
                        Previous
                    </button>
                    <button
                        @click="nextPage"
                        :disabled="currentPage === totalPages"
                        class="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50"
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
                            {{ (currentPage - 1) * itemsPerPage + 1 }} to
                            {{
                                Math.min(
                                    currentPage * itemsPerPage,
                                    filteredInventory.length
                                )
                            }}
                            of {{ filteredInventory.length }} results
                        </p>
                    </div>
                    <div>
                        <nav
                            class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px"
                        >
                            <button
                                @click="previousPage"
                                :disabled="currentPage === 1"
                                class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50"
                            >
                                Previous
                            </button>

                            <span
                                v-for="page in visiblePages"
                                :key="page"
                                @click="goToPage(page)"
                                :class="{
                                    'bg-blue-50 border-blue-500 text-blue-600':
                                        page === currentPage,
                                    'bg-white border-gray-300 text-gray-500 hover:bg-gray-50':
                                        page !== currentPage,
                                }"
                                class="relative inline-flex items-center px-4 py-2 border text-sm font-medium cursor-pointer"
                            >
                                {{ page }}
                            </span>

                            <button
                                @click="nextPage"
                                :disabled="currentPage === totalPages"
                                class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 disabled:opacity-50"
                            >
                                Next
                            </button>
                        </nav>
                    </div>
                </div>
            </div>
        </div>

        <!-- Restock Modal -->
        <div
            v-if="showRestockModal"
            class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50"
        >
            <div
                class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white"
            >
                <div class="mt-3">
                    <div class="flex items-center justify-between mb-4">
                        <h3 class="text-lg font-medium text-gray-900">
                            {{
                                selectedItem
                                    ? "Restock Product"
                                    : "Bulk Restock"
                            }}
                        </h3>
                        <button
                            @click="closeRestockModal"
                            class="text-gray-400 hover:text-gray-600"
                        >
                            <svg
                                class="h-6 w-6"
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

                    <form @submit.prevent="submitRestock">
                        <div v-if="selectedItem" class="mb-4">
                            <div class="flex items-center mb-3">
                                <img
                                    :src="selectedItem.image"
                                    :alt="selectedItem.name"
                                    class="h-16 w-16 rounded-lg object-cover"
                                />
                                <div class="ml-3">
                                    <h4 class="font-medium text-gray-900">
                                        {{ selectedItem.name }}
                                    </h4>
                                    <p class="text-sm text-gray-500">
                                        Current Stock:
                                        {{ selectedItem.currentStock }}
                                    </p>
                                    <p class="text-sm text-gray-500">
                                        SKU: {{ selectedItem.sku }}
                                    </p>
                                </div>
                            </div>
                        </div>

                        <div v-if="!selectedItem" class="mb-4">
                            <label
                                class="block text-sm font-medium text-gray-700 mb-2"
                                >Select Products</label
                            >
                            <div
                                class="max-h-32 overflow-y-auto border border-gray-300 rounded-lg p-2"
                            >
                                <div
                                    v-for="item in inventory.filter(
                                        (i) => i.currentStock <= i.minStockLevel
                                    )"
                                    :key="item.id"
                                    class="flex items-center mb-2"
                                >
                                    <input
                                        type="checkbox"
                                        :id="`bulk-${item.id}`"
                                        v-model="selectedBulkItems"
                                        :value="item.id"
                                        class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                                    />
                                    <label
                                        :for="`bulk-${item.id}`"
                                        class="ml-2 text-sm text-gray-900"
                                    >
                                        {{ item.name }} ({{
                                            item.currentStock
                                        }})
                                    </label>
                                </div>
                            </div>
                        </div>

                        <div class="mb-4">
                            <label
                                class="block text-sm font-medium text-gray-700 mb-2"
                            >
                                {{
                                    selectedItem
                                        ? "Quantity to Add"
                                        : "Quantity per Product"
                                }}
                            </label>
                            <input
                                v-model.number="restockQuantity"
                                type="number"
                                min="1"
                                required
                                class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                            />
                        </div>

                        <div class="mb-4">
                            <label
                                class="block text-sm font-medium text-gray-700 mb-2"
                                >Supplier (Optional)</label
                            >
                            <input
                                v-model="supplier"
                                type="text"
                                placeholder="Enter supplier name"
                                class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                            />
                        </div>

                        <div class="mb-4">
                            <label
                                class="block text-sm font-medium text-gray-700 mb-2"
                                >Notes (Optional)</label
                            >
                            <textarea
                                v-model="restockNotes"
                                rows="3"
                                placeholder="Enter any notes about this restock"
                                class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                            ></textarea>
                        </div>

                        <div class="flex justify-end space-x-3">
                            <button
                                type="button"
                                @click="closeRestockModal"
                                class="px-4 py-2 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 hover:bg-gray-50"
                            >
                                Cancel
                            </button>
                            <button
                                type="submit"
                                class="px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg text-sm font-medium"
                            >
                                Confirm Restock
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>
