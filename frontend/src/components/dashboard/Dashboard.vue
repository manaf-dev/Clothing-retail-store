<script setup>
    import { ref } from "vue";

    const recentSales = ref([
        {
            product: "Men's Casual T-Shirt",
            customer: "John Doe",
            date: "May 10, 2025",
            amount: 29.99,
        },
        {
            product: "Women's Summer Dress",
            customer: "Jane Smith",
            date: "May 10, 2025",
            amount: 49.99,
        },
        {
            product: "Kids Denim Jacket",
            customer: "Mike Johnson",
            date: "May 9, 2025",
            amount: 34.99,
        },
        {
            product: "Women's Handbag",
            customer: "Sarah Williams",
            date: "May 9, 2025",
            amount: 89.99,
        },
        {
            product: "Men's Formal Shirt",
            customer: "Robert Brown",
            date: "May 8, 2025",
            amount: 59.99,
        },
    ]);

    const lowStockItems = ref([
        {
            product: "Men's Slim Fit Jeans",
            category: "Men",
            stock: 5,
        },
        {
            product: "Women's Leather Jacket",
            category: "Women",
            stock: 3,
        },
        {
            product: "Kids Winter Coat",
            category: "Kids",
            stock: 4,
        },
        {
            product: "Silver Necklace",
            category: "Accessories",
            stock: 2,
        },
        {
            product: "Men's Running Shoes",
            category: "Men",
            stock: 6,
        },
    ]);
</script>

<template>
    <div>
        <h1 class="text-2xl font-semibold text-gray-800 mb-6">Dashboard</h1>

        <!-- Stats Overview -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
            <!-- Total Sales -->
            <div class="bg-white rounded-lg shadow p-6">
                <div class="flex items-center">
                    <div class="p-3 rounded-full bg-indigo-100 text-indigo-500">
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
                                d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                            />
                        </svg>
                    </div>
                    <div class="ml-4">
                        <h2 class="text-sm font-medium text-gray-600">
                            Total Sales
                        </h2>
                        <div class="flex items-baseline">
                            <p class="text-2xl font-semibold text-gray-800">
                                $12,694
                            </p>
                            <p class="ml-2 text-sm text-green-600">+5.2%</p>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Total Products -->
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
                                d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4"
                            />
                        </svg>
                    </div>
                    <div class="ml-4">
                        <h2 class="text-sm font-medium text-gray-600">
                            Total Products
                        </h2>
                        <div class="flex items-baseline">
                            <p class="text-2xl font-semibold text-gray-800">
                                876
                            </p>
                            <p class="ml-2 text-sm text-gray-600">items</p>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Low Stock -->
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
                        <div class="flex items-baseline">
                            <p class="text-2xl font-semibold text-gray-800">
                                12
                            </p>
                            <p class="ml-2 text-sm text-red-600">products</p>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Customers -->
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
                                d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"
                            />
                        </svg>
                    </div>
                    <div class="ml-4">
                        <h2 class="text-sm font-medium text-gray-600">
                            Total Customers
                        </h2>
                        <div class="flex items-baseline">
                            <p class="text-2xl font-semibold text-gray-800">
                                258
                            </p>
                            <p class="ml-2 text-sm text-green-600">+18 new</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <!-- Recent Sales -->
            <div class="bg-white rounded-lg shadow overflow-hidden">
                <div class="px-6 py-4 border-b border-gray-200 bg-gray-50">
                    <h3 class="text-lg font-medium text-gray-800">
                        Recent Sales
                    </h3>
                </div>
                <div class="p-4">
                    <div class="overflow-x-auto">
                        <table class="min-w-full">
                            <thead>
                                <tr class="bg-gray-50">
                                    <th
                                        class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                                    >
                                        Product
                                    </th>
                                    <th
                                        class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                                    >
                                        Customer
                                    </th>
                                    <th
                                        class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                                    >
                                        Date
                                    </th>
                                    <th
                                        class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                                    >
                                        Amount
                                    </th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-gray-200">
                                <tr
                                    v-for="(sale, index) in recentSales"
                                    :key="index"
                                >
                                    <td class="px-4 py-3 whitespace-nowrap">
                                        <div
                                            class="text-sm font-medium text-gray-900"
                                        >
                                            {{ sale.product }}
                                        </div>
                                    </td>
                                    <td class="px-4 py-3 whitespace-nowrap">
                                        <div class="text-sm text-gray-500">
                                            {{ sale.customer }}
                                        </div>
                                    </td>
                                    <td class="px-4 py-3 whitespace-nowrap">
                                        <div class="text-sm text-gray-500">
                                            {{ sale.date }}
                                        </div>
                                    </td>
                                    <td class="px-4 py-3 whitespace-nowrap">
                                        <div class="text-sm text-gray-900">
                                            ${{ sale.amount }}
                                        </div>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                    <div class="mt-4 flex justify-center">
                        <button
                            class="text-sm text-indigo-600 hover:text-indigo-900"
                        >
                            View All Sales
                        </button>
                    </div>
                </div>
            </div>

            <!-- Low Stock Alert -->
            <div class="bg-white rounded-lg shadow overflow-hidden">
                <div class="px-6 py-4 border-b border-gray-200 bg-gray-50">
                    <h3 class="text-lg font-medium text-gray-800">
                        Low Stock Alert
                    </h3>
                </div>
                <div class="p-4">
                    <div class="overflow-x-auto">
                        <table class="min-w-full">
                            <thead>
                                <tr class="bg-gray-50">
                                    <th
                                        class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                                    >
                                        Product
                                    </th>
                                    <th
                                        class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                                    >
                                        Category
                                    </th>
                                    <th
                                        class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                                    >
                                        Current Stock
                                    </th>
                                    <th
                                        class="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                                    >
                                        Action
                                    </th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-gray-200">
                                <tr
                                    v-for="(item, index) in lowStockItems"
                                    :key="index"
                                >
                                    <td class="px-4 py-3 whitespace-nowrap">
                                        <div
                                            class="text-sm font-medium text-gray-900"
                                        >
                                            {{ item.product }}
                                        </div>
                                    </td>
                                    <td class="px-4 py-3 whitespace-nowrap">
                                        <div class="text-sm text-gray-500">
                                            {{ item.category }}
                                        </div>
                                    </td>
                                    <td class="px-4 py-3 whitespace-nowrap">
                                        <div class="text-sm">
                                            <span
                                                class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-red-100 text-red-800"
                                            >
                                                {{ item.stock }}
                                            </span>
                                        </div>
                                    </td>
                                    <td
                                        class="px-4 py-3 whitespace-nowrap text-sm text-gray-500"
                                    >
                                        <button
                                            class="text-indigo-600 hover:text-indigo-900"
                                        >
                                            Restock
                                        </button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                    <div class="mt-4 flex justify-center">
                        <button
                            class="text-sm text-indigo-600 hover:text-indigo-900"
                        >
                            View All Low Stock
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Product Category Distribution -->
        <div class="mt-8 bg-white rounded-lg shadow overflow-hidden">
            <div class="px-6 py-4 border-b border-gray-200 bg-gray-50">
                <h3 class="text-lg font-medium text-gray-800">
                    Product Category Distribution
                </h3>
            </div>
            <div class="p-6">
                <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                    <!-- Men's Clothing -->
                    <div class="bg-gray-50 rounded-lg p-4">
                        <h4 class="font-medium text-gray-800">
                            Men's Clothing
                        </h4>
                        <div class="mt-2 flex items-center justify-between">
                            <div class="w-full bg-gray-200 rounded-full h-2.5">
                                <div
                                    class="bg-blue-600 h-2.5 rounded-full"
                                    style="width: 40%"
                                ></div>
                            </div>
                            <span class="ml-4 text-sm font-medium text-gray-700"
                                >40%</span
                            >
                        </div>
                        <p class="mt-2 text-sm text-gray-600">352 products</p>
                    </div>

                    <!-- Women's Clothing -->
                    <div class="bg-gray-50 rounded-lg p-4">
                        <h4 class="font-medium text-gray-800">
                            Women's Clothing
                        </h4>
                        <div class="mt-2 flex items-center justify-between">
                            <div class="w-full bg-gray-200 rounded-full h-2.5">
                                <div
                                    class="bg-pink-500 h-2.5 rounded-full"
                                    style="width: 45%"
                                ></div>
                            </div>
                            <span class="ml-4 text-sm font-medium text-gray-700"
                                >45%</span
                            >
                        </div>
                        <p class="mt-2 text-sm text-gray-600">390 products</p>
                    </div>

                    <!-- Kids' Clothing -->
                    <div class="bg-gray-50 rounded-lg p-4">
                        <h4 class="font-medium text-gray-800">
                            Kids' Clothing
                        </h4>
                        <div class="mt-2 flex items-center justify-between">
                            <div class="w-full bg-gray-200 rounded-full h-2.5">
                                <div
                                    class="bg-green-500 h-2.5 rounded-full"
                                    style="width: 10%"
                                ></div>
                            </div>
                            <span class="ml-4 text-sm font-medium text-gray-700"
                                >10%</span
                            >
                        </div>
                        <p class="mt-2 text-sm text-gray-600">89 products</p>
                    </div>

                    <!-- Accessories -->
                    <div class="bg-gray-50 rounded-lg p-4">
                        <h4 class="font-medium text-gray-800">Accessories</h4>
                        <div class="mt-2 flex items-center justify-between">
                            <div class="w-full bg-gray-200 rounded-full h-2.5">
                                <div
                                    class="bg-purple-500 h-2.5 rounded-full"
                                    style="width: 5%"
                                ></div>
                            </div>
                            <span class="ml-4 text-sm font-medium text-gray-700"
                                >5%</span
                            >
                        </div>
                        <p class="mt-2 text-sm text-gray-600">45 products</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
