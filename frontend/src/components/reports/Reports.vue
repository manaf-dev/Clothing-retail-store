<script setup>
    import { ref } from "vue";

    const selectedReportType = ref("sales");
    const selectedPeriod = ref("month");
    const fromDate = ref("2025-05-01");
    const toDate = ref("2025-05-27");

    // Sales Report Data
    const salesSummary = ref({
        totalRevenue: 45678,
        totalOrders: 234,
        averageOrder: 195.23,
        itemsSold: 567,
    });

    const salesData = ref([
        {
            id: 1,
            date: "2025-05-27",
            invoice: "INV-001234",
            customer: "John Doe",
            items: 3,
            total: 159.97,
            status: "Completed",
        },
        {
            id: 2,
            date: "2025-05-27",
            invoice: "INV-001235",
            customer: "Jane Smith",
            items: 2,
            total: 89.98,
            status: "Completed",
        },
        {
            id: 3,
            date: "2025-05-26",
            invoice: "INV-001236",
            customer: "Mike Johnson",
            items: 1,
            total: 49.99,
            status: "Pending",
        },
        {
            id: 4,
            date: "2025-05-26",
            invoice: "INV-001237",
            customer: "Sarah Williams",
            items: 4,
            total: 299.96,
            status: "Completed",
        },
        {
            id: 5,
            date: "2025-05-25",
            invoice: "INV-001238",
            customer: "Robert Brown",
            items: 2,
            total: 119.98,
            status: "Refunded",
        },
    ]);

    // Inventory Report Data
    const inventorySummary = ref({
        inStock: 234,
        lowStock: 45,
        outOfStock: 12,
        totalValue: 125000,
        totalProducts: 291,
        categories: [
            { name: "Men's Clothing", count: 120 },
            { name: "Women's Clothing", count: 135 },
            { name: "Kids' Clothing", count: 25 },
            { name: "Accessories", count: 11 },
        ],
    });

    const inventoryData = ref([
        {
            id: 1,
            name: "Men's Casual T-Shirt",
            sku: "MCT-001",
            category: "Men's Clothing",
            stock: 45,
            unitPrice: 29.99,
        },
        {
            id: 2,
            name: "Women's Summer Dress",
            sku: "WSD-002",
            category: "Women's Clothing",
            stock: 23,
            unitPrice: 79.99,
        },
        {
            id: 3,
            name: "Kids Denim Jacket",
            sku: "KDJ-003",
            category: "Kids' Clothing",
            stock: 8,
            unitPrice: 49.99,
        },
        {
            id: 4,
            name: "Leather Handbag",
            sku: "LHB-004",
            category: "Accessories",
            stock: 3,
            unitPrice: 159.99,
        },
        {
            id: 5,
            name: "Men's Formal Shirt",
            sku: "MFS-005",
            category: "Men's Clothing",
            stock: 0,
            unitPrice: 69.99,
        },
    ]);

    // Product Performance Data
    const topProducts = ref([
        {
            id: 1,
            name: "Women's Summer Dress",
            category: "Women's Clothing",
            unitsSold: 89,
            revenue: 7119,
            profitMargin: 45,
        },
        {
            id: 2,
            name: "Men's Casual T-Shirt",
            category: "Men's Clothing",
            unitsSold: 156,
            revenue: 4678,
            profitMargin: 38,
        },
        {
            id: 3,
            name: "Leather Handbag",
            category: "Accessories",
            unitsSold: 34,
            revenue: 5439,
            profitMargin: 43,
        },
        {
            id: 4,
            name: "Kids Denim Jacket",
            category: "Kids' Clothing",
            unitsSold: 45,
            revenue: 2249,
            profitMargin: 40,
        },
        {
            id: 5,
            name: "Men's Formal Shirt",
            category: "Men's Clothing",
            unitsSold: 67,
            revenue: 4683,
            profitMargin: 35,
        },
    ]);

    const exportReport = () => {
        // Logic to export the report as PDF
        alert("Exporting report as PDF...");
    };

    const exportCSV = () => {
        // Logic to export the report as CSV
        alert("Exporting report as CSV...");
    };

    const generateReport = () => {
        // Logic to generate the report based on selected filters
        alert(
            `Generating ${selectedReportType.value} report for period: ${selectedPeriod.value}`
        );
    };

    const getStatusColor = (status) => {
        switch (status) {
            case "Completed":
                return "bg-green-100 text-green-800";
            case "Pending":
                return "bg-yellow-100 text-yellow-800";
            case "Refunded":
                return "bg-red-100 text-red-800";
            default:
                return "bg-gray-100 text-gray-800";
        }
    };

    const getStockStatus = (stock) => {
        if (stock > 20) return "In Stock";
        if (stock > 0 && stock <= 20) return "Low Stock";
        return "Out of Stock";
    };

    const getStockStatusColor = (stock) => {
        if (stock > 20) return "bg-green-100 text-green-800";
        if (stock > 0 && stock <= 20) return "bg-yellow-100 text-yellow-800";
        return "bg-red-100 text-red-800";
    };
</script>

<!-- src/views/ReportsView.vue -->
<template>
    <div>
        <div class="flex justify-between items-center mb-6">
            <h1 class="text-2xl font-semibold text-gray-800">
                Reports & Analytics
            </h1>
            <div class="flex space-x-3">
                <button
                    @click="exportReport"
                    class="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-md text-sm font-medium flex items-center"
                >
                    <svg
                        class="h-4 w-4 mr-2"
                        fill="none"
                        viewBox="0 0 24 24"
                        stroke="currentColor"
                    >
                        <path
                            stroke-linecap="round"
                            stroke-linejoin="round"
                            stroke-width="2"
                            d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                        />
                    </svg>
                    Export PDF
                </button>
                <button
                    @click="exportCSV"
                    class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md text-sm font-medium flex items-center"
                >
                    <svg
                        class="h-4 w-4 mr-2"
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
                    Export CSV
                </button>
            </div>
        </div>

        <!-- Report Filter Controls -->
        <div class="bg-white rounded-lg shadow mb-6 p-6">
            <h3 class="text-lg font-medium text-gray-800 mb-4">
                Report Filters
            </h3>
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2"
                        >Report Type</label
                    >
                    <select
                        v-model="selectedReportType"
                        @change="generateReport"
                        class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                    >
                        <option value="sales">Sales Report</option>
                        <option value="inventory">Inventory Report</option>
                        <option value="products">Product Performance</option>
                        <option value="customers">Customer Analysis</option>
                    </select>
                </div>

                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2"
                        >Time Period</label
                    >
                    <select
                        v-model="selectedPeriod"
                        @change="generateReport"
                        class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                    >
                        <option value="today">Today</option>
                        <option value="week">This Week</option>
                        <option value="month">This Month</option>
                        <option value="quarter">This Quarter</option>
                        <option value="year">This Year</option>
                        <option value="custom">Custom Range</option>
                    </select>
                </div>

                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2"
                        >From Date</label
                    >
                    <input
                        v-model="fromDate"
                        @change="generateReport"
                        type="date"
                        class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                    />
                </div>

                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2"
                        >To Date</label
                    >
                    <input
                        v-model="toDate"
                        @change="generateReport"
                        type="date"
                        class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                    />
                </div>
            </div>
        </div>

        <!-- Sales Report -->
        <div v-if="selectedReportType === 'sales'" class="space-y-6">
            <!-- Sales Summary Cards -->
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div class="bg-white rounded-lg shadow p-6">
                    <div class="flex items-center justify-between">
                        <div>
                            <p class="text-sm font-medium text-gray-600">
                                Total Revenue
                            </p>
                            <p class="text-2xl font-bold text-gray-900">
                                ${{
                                    salesSummary.totalRevenue.toLocaleString()
                                }}
                            </p>
                        </div>
                        <div class="p-3 bg-green-100 rounded-full">
                            <svg
                                class="h-6 w-6 text-green-600"
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
                    </div>
                    <p class="text-sm text-green-600 mt-2">
                        +12.5% from last period
                    </p>
                </div>

                <div class="bg-white rounded-lg shadow p-6">
                    <div class="flex items-center justify-between">
                        <div>
                            <p class="text-sm font-medium text-gray-600">
                                Total Orders
                            </p>
                            <p class="text-2xl font-bold text-gray-900">
                                {{ salesSummary.totalOrders }}
                            </p>
                        </div>
                        <div class="p-3 bg-blue-100 rounded-full">
                            <svg
                                class="h-6 w-6 text-blue-600"
                                fill="none"
                                viewBox="0 0 24 24"
                                stroke="currentColor"
                            >
                                <path
                                    stroke-linecap="round"
                                    stroke-linejoin="round"
                                    stroke-width="2"
                                    d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z"
                                />
                            </svg>
                        </div>
                    </div>
                    <p class="text-sm text-blue-600 mt-2">
                        +8.2% from last period
                    </p>
                </div>

                <div class="bg-white rounded-lg shadow p-6">
                    <div class="flex items-center justify-between">
                        <div>
                            <p class="text-sm font-medium text-gray-600">
                                Average Order
                            </p>
                            <p class="text-2xl font-bold text-gray-900">
                                ${{ salesSummary.averageOrder.toFixed(2) }}
                            </p>
                        </div>
                        <div class="p-3 bg-yellow-100 rounded-full">
                            <svg
                                class="h-6 w-6 text-yellow-600"
                                fill="none"
                                viewBox="0 0 24 24"
                                stroke="currentColor"
                            >
                                <path
                                    stroke-linecap="round"
                                    stroke-linejoin="round"
                                    stroke-width="2"
                                    d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
                                />
                            </svg>
                        </div>
                    </div>
                    <p class="text-sm text-yellow-600 mt-2">
                        +3.7% from last period
                    </p>
                </div>

                <div class="bg-white rounded-lg shadow p-6">
                    <div class="flex items-center justify-between">
                        <div>
                            <p class="text-sm font-medium text-gray-600">
                                Items Sold
                            </p>
                            <p class="text-2xl font-bold text-gray-900">
                                {{ salesSummary.itemsSold }}
                            </p>
                        </div>
                        <div class="p-3 bg-purple-100 rounded-full">
                            <svg
                                class="h-6 w-6 text-purple-600"
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
                    </div>
                    <p class="text-sm text-purple-600 mt-2">
                        +15.3% from last period
                    </p>
                </div>
            </div>

            <!-- Detailed Sales Table -->
            <div class="bg-white rounded-lg shadow overflow-hidden">
                <div class="px-6 py-4 border-b border-gray-200">
                    <h3 class="text-lg font-medium text-gray-800">
                        Detailed Sales Report
                    </h3>
                </div>
                <div class="overflow-x-auto">
                    <table class="min-w-full divide-y divide-gray-200">
                        <thead class="bg-gray-50">
                            <tr>
                                <th
                                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                                >
                                    Date
                                </th>
                                <th
                                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                                >
                                    Invoice #
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
                            </tr>
                        </thead>
                        <tbody class="bg-white divide-y divide-gray-200">
                            <tr v-for="sale in salesData" :key="sale.id">
                                <td
                                    class="px-6 py-4 whitespace-nowrap text-sm text-gray-900"
                                >
                                    {{ sale.date }}
                                </td>
                                <td
                                    class="px-6 py-4 whitespace-nowrap text-sm text-gray-900"
                                >
                                    {{ sale.invoice }}
                                </td>
                                <td
                                    class="px-6 py-4 whitespace-nowrap text-sm text-gray-900"
                                >
                                    {{ sale.customer }}
                                </td>
                                <td
                                    class="px-6 py-4 whitespace-nowrap text-sm text-gray-900"
                                >
                                    {{ sale.items }}
                                </td>
                                <td
                                    class="px-6 py-4 whitespace-nowrap text-sm text-gray-900"
                                >
                                    ${{ sale.total }}
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap">
                                    <span
                                        :class="getStatusColor(sale.status)"
                                        class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full"
                                    >
                                        {{ sale.status }}
                                    </span>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- Inventory Report -->
        <div v-if="selectedReportType === 'inventory'" class="space-y-6">
            <!-- Inventory Summary -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div class="bg-white rounded-lg shadow p-6">
                    <h3 class="text-lg font-medium text-gray-800 mb-4">
                        Stock Status
                    </h3>
                    <div class="space-y-3">
                        <div class="flex justify-between">
                            <span class="text-sm text-gray-600">In Stock</span>
                            <span class="text-sm font-medium text-green-600">{{
                                inventorySummary.inStock
                            }}</span>
                        </div>
                        <div class="flex justify-between">
                            <span class="text-sm text-gray-600">Low Stock</span>
                            <span class="text-sm font-medium text-yellow-600">{{
                                inventorySummary.lowStock
                            }}</span>
                        </div>
                        <div class="flex justify-between">
                            <span class="text-sm text-gray-600"
                                >Out of Stock</span
                            >
                            <span class="text-sm font-medium text-red-600">{{
                                inventorySummary.outOfStock
                            }}</span>
                        </div>
                    </div>
                </div>

                <div class="bg-white rounded-lg shadow p-6">
                    <h3 class="text-lg font-medium text-gray-800 mb-4">
                        Total Inventory Value
                    </h3>
                    <p class="text-3xl font-bold text-gray-900">
                        ${{ inventorySummary.totalValue.toLocaleString() }}
                    </p>
                    <p class="text-sm text-gray-600 mt-2">
                        Across {{ inventorySummary.totalProducts }} products
                    </p>
                </div>

                <div class="bg-white rounded-lg shadow p-6">
                    <h3 class="text-lg font-medium text-gray-800 mb-4">
                        Categories
                    </h3>
                    <div class="space-y-2">
                        <div
                            v-for="category in inventorySummary.categories"
                            :key="category.name"
                            class="flex justify-between"
                        >
                            <span class="text-sm text-gray-600">{{
                                category.name
                            }}</span>
                            <span class="text-sm font-medium text-gray-900">{{
                                category.count
                            }}</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Inventory Details Table -->
            <div class="bg-white rounded-lg shadow overflow-hidden">
                <div class="px-6 py-4 border-b border-gray-200">
                    <h3 class="text-lg font-medium text-gray-800">
                        Inventory Details
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
                                    Stock
                                </th>
                                <th
                                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                                >
                                    Unit Price
                                </th>
                                <th
                                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                                >
                                    Total Value
                                </th>
                                <th
                                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                                >
                                    Status
                                </th>
                            </tr>
                        </thead>
                        <tbody class="bg-white divide-y divide-gray-200">
                            <tr v-for="item in inventoryData" :key="item.id">
                                <td
                                    class="px-6 py-4 whitespace-nowrap text-sm text-gray-900"
                                >
                                    {{ item.name }}
                                </td>
                                <td
                                    class="px-6 py-4 whitespace-nowrap text-sm text-gray-500"
                                >
                                    {{ item.sku }}
                                </td>
                                <td
                                    class="px-6 py-4 whitespace-nowrap text-sm text-gray-500"
                                >
                                    {{ item.category }}
                                </td>
                                <td
                                    class="px-6 py-4 whitespace-nowrap text-sm text-gray-900"
                                >
                                    {{ item.stock }}
                                </td>
                                <td
                                    class="px-6 py-4 whitespace-nowrap text-sm text-gray-900"
                                >
                                    ${{ item.unitPrice }}
                                </td>
                                <td
                                    class="px-6 py-4 whitespace-nowrap text-sm text-gray-900"
                                >
                                    ${{
                                        (item.stock * item.unitPrice).toFixed(2)
                                    }}
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap">
                                    <span
                                        :class="getStockStatusColor(item.stock)"
                                        class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full"
                                    >
                                        {{ getStockStatus(item.stock) }}
                                    </span>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- Product Performance Report -->
        <div v-if="selectedReportType === 'products'" class="space-y-6">
            <!-- Top Performing Products -->
            <div class="bg-white rounded-lg shadow overflow-hidden">
                <div class="px-6 py-4 border-b border-gray-200">
                    <h3 class="text-lg font-medium text-gray-800">
                        Top Performing Products
                    </h3>
                </div>
                <div class="overflow-x-auto">
                    <table class="min-w-full divide-y divide-gray-200">
                        <thead class="bg-gray-50">
                            <tr>
                                <th
                                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                                >
                                    Rank
                                </th>
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
                                    Units Sold
                                </th>
                                <th
                                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                                >
                                    Revenue
                                </th>
                                <th
                                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                                >
                                    Profit Margin
                                </th>
                            </tr>
                        </thead>
                        <tbody class="bg-white divide-y divide-gray-200">
                            <tr
                                v-for="(product, index) in topProducts"
                                :key="product.id"
                            >
                                <td class="px-6 py-4 whitespace-nowrap">
                                    <span
                                        class="text-sm font-medium text-gray-900"
                                        >#{{ index + 1 }}</span
                                    >
                                </td>
                                <td
                                    class="px-6 py-4 whitespace-nowrap text-sm text-gray-900"
                                >
                                    {{ product.name }}
                                </td>
                                <td
                                    class="px-6 py-4 whitespace-nowrap text-sm text-gray-500"
                                >
                                    {{ product.category }}
                                </td>
                                <td
                                    class="px-6 py-4 whitespace-nowrap text-sm text-gray-900"
                                >
                                    {{ product.unitsSold }}
                                </td>
                                <td
                                    class="px-6 py-4 whitespace-nowrap text-sm text-gray-900"
                                >
                                    ${{ product.revenue.toLocaleString() }}
                                </td>
                                <td
                                    class="px-6 py-4 whitespace-nowrap text-sm text-gray-900"
                                >
                                    {{ product.profitMargin }}%
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- Customer Analysis Report -->
        <div v-if="selectedReportType === 'customers'" class="space-y-6">
            <!-- Customer Summary Cards -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div class="bg-white rounded-lg shadow p-6">
                    <h3 class="text-lg font-medium text-gray-800 mb-4">
                        Customer Metrics
                    </h3>
                    <div class="space-y-3">
                        <div class="flex justify-between">
                            <span class="text-sm text-gray-600"
                                >Total Customers</span
                            >
                            <span class="text-sm font-medium text-gray-900">{{
                                customerSummary.totalCustomers
                            }}</span>
                        </div>
                        <div class="flex justify-between">
                            <span class="text-sm text-gray-600"
                                >New This Month</span
                            >
                            <span class="text-sm font-medium text-green-600">{{
                                customerSummary.newCustomers
                            }}</span>
                        </div>
                        <div class="flex justify-between">
                            <span class="text-sm text-gray-600"
                                >Repeat Customers</span
                            >
                            <span class="text-sm font-medium text-blue-600">{{
                                customerSummary.repeatCustomers
                            }}</span>
                        </div>
                    </div>
                </div>

                <div class="bg-white rounded-lg shadow p-6">
                    <h3 class="text-lg font-medium text-gray-800 mb-4">
                        Average Spend
                    </h3>
                    <p class="text-3xl font-bold text-gray-900">
                        ${{ customerSummary.averageSpend.toFixed(2) }}
                    </p>
                    <p class="text-sm text-gray-600 mt-2">Per customer</p>
                </div>

                <div class="bg-white rounded-lg shadow p-6">
                    <h3 class="text-lg font-medium text-gray-800 mb-4">
                        Customer Lifetime Value
                    </h3>
                    <p class="text-3xl font-bold text-gray-900">
                        ${{ customerSummary.lifetimeValue.toFixed(2) }}
                    </p>
                    <p class="text-sm text-gray-600 mt-2">Average LTV</p>
                </div>
            </div>

            <!-- Top Customers Table -->
            <div class="bg-white rounded-lg shadow overflow-hidden">
                <div class="px-6 py-4 border-b border-gray-200">
                    <h3 class="text-lg font-medium text-gray-800">
                        Top Customers
                    </h3>
                </div>
                <div class="overflow-x-auto">
                    <table class="min-w-full divide-y divide-gray-200">
                        <thead class="bg-gray-50">
                            <tr>
                                <th
                                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                                >
                                    Customer
                                </th>
                                <th
                                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                                >
                                    Email
                                </th>
                                <th
                                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                                >
                                    Total Orders
                                </th>
                                <th
                                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                                >
                                    Total Spent
                                </th>
                                <th
                                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                                >
                                    Last Purchase
                                </th>
                                <th
                                    class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                                >
                                    Status
                                </th>
                            </tr>
                        </thead>
                        <tbody class="bg-white divide-y divide-gray-200">
                            <tr
                                v-for="customer in topCustomers"
                                :key="customer.id"
                            >
                                <td
                                    class="px-6 py-4 whitespace-nowrap text-sm text-gray-900"
                                >
                                    {{ customer.name }}
                                </td>
                                <td
                                    class="px-6 py-4 whitespace-nowrap text-sm text-gray-500"
                                >
                                    {{ customer.email }}
                                </td>
                                <td
                                    class="px-6 py-4 whitespace-nowrap text-sm text-gray-900"
                                >
                                    {{ customer.totalOrders }}
                                </td>
                                <td
                                    class="px-6 py-4 whitespace-nowrap text-sm text-gray-900"
                                >
                                    ${{ customer.totalSpent.toLocaleString() }}
                                </td>
                                <td
                                    class="px-6 py-4 whitespace-nowrap text-sm text-gray-500"
                                >
                                    {{ customer.lastPurchase }}
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap">
                                    <span
                                        :class="
                                            getCustomerStatusColor(
                                                customer.status
                                            )
                                        "
                                        class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full"
                                    >
                                        {{ customer.status }}
                                    </span>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</template>
