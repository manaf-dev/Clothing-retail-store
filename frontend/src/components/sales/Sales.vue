<script setup>
    import { ref, computed } from "vue";
    import NewSaleModal from "./NewSaleModal.vue";
    import SaleDetailModal from "./SaleDetailModal.vue";
    import Formatters from "@/utils/formatters.js";

    const totalSales = ref(245);
    const selectedSale = ref(null);
    const openNewSaleModal = ref(false);
    const openSaleDetailModal = ref(false);
    const salesDetail = ref(null);
    const filters = ref({
        startDate: "",
        endDate: "",
        customer: "",
        product: "",
    });

    const salesSummary = ref({
        daily: 1250.75,
        dailyPercentage: 12.5,
        weekly: 8760.4,
        weeklyPercentage: 8.2,
        monthly: 32450.8,
        monthlyPercentage: -3.4,
    });

    const sales = ref([
        {
            id: 1,
            invoiceNumber: "INV-2025-001",
            date: new Date("2025-05-14T13:24:00"),
            customer: {
                name: "John Doe",
                email: "john.doe@example.com",
                phone: "(555) 123-4567",
                address: "123 Main St, Anytown, USA",
            },
            items: [
                {
                    product: {
                        id: 1,
                        name: "T-Shirt Classic",
                        sku: "TS-CL-001",
                    },
                    quantity: 2,
                    price: 29.99,
                    total: 59.98,
                },
                {
                    product: { id: 3, name: "Denim Jeans", sku: "DJ-BL-002" },
                    quantity: 1,
                    price: 79.99,
                    total: 79.99,
                },
            ],
            subtotal: 139.97,
            taxRate: 8.5,
            tax: 11.9,
            total: 151.87,
            status: "Completed",
            paymentMethod: "card",
            notes: "Customer requested gift wrapping.",
        },
        {
            id: 2,
            invoiceNumber: "INV-2025-002",
            date: new Date("2025-05-14T15:45:00"),
            customer: {
                name: "Jane Smith",
                email: "jane.smith@example.com",
                phone: "(555) 987-6543",
                address: "456 Oak Ave, Sometown, USA",
            },
            items: [
                {
                    product: { id: 5, name: "Summer Dress", sku: "SD-FL-003" },
                    quantity: 1,
                    price: 89.99,
                    total: 89.99,
                },
            ],
            subtotal: 89.99,
            taxRate: 8.5,
            tax: 7.65,
            total: 97.64,
            status: "Completed",
            paymentMethod: "cash",
            notes: "",
        },
        {
            id: 3,
            invoiceNumber: "INV-2025-003",
            date: new Date("2025-05-15T09:15:00"),
            customer: {
                name: "Robert Johnson",
                email: "robert.j@example.com",
                phone: "(555) 765-4321",
                address: "789 Pine St, Othertown, USA",
            },
            items: [
                {
                    product: { id: 2, name: "Polo Shirt", sku: "PS-ST-001" },
                    quantity: 3,
                    price: 49.99,
                    total: 149.97,
                },
                {
                    product: { id: 7, name: "Leather Belt", sku: "LB-BR-001" },
                    quantity: 1,
                    price: 34.99,
                    total: 34.99,
                },
            ],
            subtotal: 184.96,
            taxRate: 8.5,
            tax: 15.72,
            total: 200.68,
            status: "Pending",
            paymentMethod: "bank_transfer",
            notes: "Customer will pick up tomorrow.",
        },
    ]);

    const applySalesFilter = () => {
        // Implementation would filter sales based on criteria
        // For demo purposes, we'll show a console message
        console.log("Applying filters:", filters.value);
        // In a real app, this would call an API or filter local data
    };

    const viewSaleDetails = (sale) => {
        selectedSale.value = { ...sale };
    };

    const printInvoice = (sale) => {
        // In a real app, this would generate a printable invoice
        // For this demo, we'll just show an alert
        alert(`Printing invoice #${sale.invoiceNumber}...`);

        // In a real implementation, you might use a library like pdfmake
        // or open a new window with a printable version of the invoice

        // Example of what might happen in a real app:
        // const invoiceWindow = window.open('', '_blank');
        // invoiceWindow.document.write(`<html><head>
    };
</script>

<template>
    <div>
        <div class="flex justify-between items-center mb-6">
            <h1 class="text-2xl font-semibold text-gray-800">
                Sales Management
            </h1>
            <button
                @click="openNewSaleModal = true"
                class="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg flex items-center"
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
                        d="M12 4v16m8-8H4"
                    />
                </svg>
                New Sale
            </button>
        </div>

        <!-- Sales Filters -->
        <div class="bg-white rounded-lg shadow mb-6 p-4">
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1"
                        >Date Range</label
                    >
                    <div class="flex space-x-2">
                        <input
                            type="date"
                            v-model="filters.startDate"
                            class="border border-gray-300 rounded-md px-3 py-2 text-sm w-full"
                        />
                        <input
                            type="date"
                            v-model="filters.endDate"
                            class="border border-gray-300 rounded-md px-3 py-2 text-sm w-full"
                        />
                    </div>
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1"
                        >Customer</label
                    >
                    <input
                        type="text"
                        v-model="filters.customer"
                        placeholder="Search customer"
                        class="border border-gray-300 rounded-md px-3 py-2 text-sm w-full"
                    />
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1"
                        >Product</label
                    >
                    <input
                        type="text"
                        v-model="filters.product"
                        placeholder="Search product"
                        class="border border-gray-300 rounded-md px-3 py-2 text-sm w-full"
                    />
                </div>
                <div class="flex items-end">
                    <button
                        @click="applySalesFilter"
                        class="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg w-full"
                    >
                        Apply Filter
                    </button>
                </div>
            </div>
        </div>

        <!-- Sales Summary -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            <div class="bg-white rounded-lg shadow p-4">
                <h3 class="text-lg font-medium text-gray-800 mb-2">
                    Daily Sales
                </h3>
                <div class="flex items-center justify-between">
                    <span class="text-2xl font-bold text-gray-900"
                        >${{
                            Formatters.formatNumber(salesSummary.daily)
                        }}</span
                    >
                    <span
                        :class="
                            salesSummary.dailyPercentage >= 0
                                ? 'text-green-600'
                                : 'text-red-600'
                        "
                        class="text-sm font-medium"
                    >
                        {{ salesSummary.dailyPercentage >= 0 ? "+" : ""
                        }}{{ salesSummary.dailyPercentage }}% from yesterday
                    </span>
                </div>
            </div>

            <div class="bg-white rounded-lg shadow p-4">
                <h3 class="text-lg font-medium text-gray-800 mb-2">
                    Weekly Sales
                </h3>
                <div class="flex items-center justify-between">
                    <span class="text-2xl font-bold text-gray-900"
                        >${{
                            Formatters.formatNumber(salesSummary.weekly)
                        }}</span
                    >
                    <span
                        :class="
                            salesSummary.weeklyPercentage >= 0
                                ? 'text-green-600'
                                : 'text-red-600'
                        "
                        class="text-sm font-medium"
                    >
                        {{ salesSummary.weeklyPercentage >= 0 ? "+" : ""
                        }}{{ salesSummary.weeklyPercentage }}% from last week
                    </span>
                </div>
            </div>

            <div class="bg-white rounded-lg shadow p-4">
                <h3 class="text-lg font-medium text-gray-800 mb-2">
                    Monthly Sales
                </h3>
                <div class="flex items-center justify-between">
                    <span class="text-2xl font-bold text-gray-900"
                        >${{
                            Formatters.formatNumber(salesSummary.monthly)
                        }}</span
                    >
                    <span
                        :class="
                            salesSummary.monthlyPercentage >= 0
                                ? 'text-green-600'
                                : 'text-red-600'
                        "
                        class="text-sm font-medium"
                    >
                        {{ salesSummary.monthlyPercentage >= 0 ? "+" : ""
                        }}{{ salesSummary.monthlyPercentage }}% from last month
                    </span>
                </div>
            </div>
        </div>

        <!-- Sales Table -->
        <div class="bg-white rounded-lg shadow overflow-hidden">
            <div
                class="px-6 py-4 border-b border-gray-200 bg-gray-50 flex justify-between items-center"
            >
                <h3 class="text-lg font-medium text-gray-800">Sales History</h3>
                <div class="flex items-center space-x-2">
                    <button class="text-gray-600 hover:text-gray-900">
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
                                d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"
                            />
                        </svg>
                    </button>
                    <span class="text-gray-600">Export</span>
                </div>
            </div>
            <div class="overflow-x-auto">
                <table class="min-w-full divide-y divide-gray-200">
                    <thead class="bg-gray-50">
                        <tr>
                            <th
                                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                            >
                                Invoice #
                            </th>
                            <th
                                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                            >
                                Date & Time
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
                                class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider"
                            >
                                Actions
                            </th>
                        </tr>
                    </thead>
                    <tbody class="bg-white divide-y divide-gray-200">
                        <tr v-for="sale in sales" :key="sale.id">
                            <td class="px-6 py-4 whitespace-nowrap">
                                <div class="font-medium text-gray-900">
                                    #{{ sale.invoiceNumber }}
                                </div>
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap">
                                <div class="text-sm text-gray-900">
                                    {{ Formatters.formatDate(sale.date) }}
                                </div>
                                <div class="text-sm text-gray-500">
                                    {{ Formatters.formatTime(sale.date) }}
                                </div>
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap">
                                <div class="text-sm text-gray-900">
                                    {{ sale.customer.name }}
                                </div>
                                <div class="text-sm text-gray-500">
                                    {{ sale.customer.email }}
                                </div>
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap">
                                <div class="text-sm text-gray-900">
                                    {{ sale.items.length }} items
                                </div>
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap">
                                <div class="text-sm font-medium text-gray-900">
                                    ${{ Formatters.formatNumber(sale.total) }}
                                </div>
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap">
                                <span
                                    :class="{
                                        'bg-green-100 text-green-800':
                                            sale.status === 'Completed',
                                        'bg-yellow-100 text-yellow-800':
                                            sale.status === 'Pending',
                                        'bg-red-100 text-red-800':
                                            sale.status === 'Cancelled',
                                    }"
                                    class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full"
                                >
                                    {{ sale.status }}
                                </span>
                            </td>
                            <td
                                class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium"
                            >
                                <button
                                    @click="viewSaleDetails(sale)"
                                    class="text-indigo-600 hover:text-indigo-900 mr-3"
                                >
                                    View
                                </button>
                                <button
                                    @click="printInvoice(sale)"
                                    class="text-gray-600 hover:text-gray-900"
                                >
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
                                            d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z"
                                        />
                                    </svg>
                                </button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <div class="px-6 py-4 border-t border-gray-200 bg-gray-50">
                <div class="flex items-center justify-between">
                    <div class="text-sm text-gray-700">
                        Showing <span class="font-medium">1</span> to
                        <span class="font-medium">10</span> of
                        <span class="font-medium">{{ totalSales }}</span> sales
                    </div>
                    <div class="flex-1 flex justify-end">
                        <div class="flex rounded-md shadow-sm">
                            <button
                                class="px-3 py-1 border border-gray-300 bg-white text-sm font-medium text-gray-700 hover:bg-gray-50 rounded-l-md"
                            >
                                Previous
                            </button>
                            <button
                                class="px-3 py-1 border-t border-b border-r border-gray-300 bg-white text-sm font-medium text-gray-700 hover:bg-gray-50"
                            >
                                1
                            </button>
                            <button
                                class="px-3 py-1 border-t border-b border-gray-300 bg-indigo-50 text-sm font-medium text-indigo-600"
                            >
                                2
                            </button>
                            <button
                                class="px-3 py-1 border-t border-b border-gray-300 bg-white text-sm font-medium text-gray-700 hover:bg-gray-50"
                            >
                                3
                            </button>
                            <button
                                class="px-3 py-1 border border-gray-300 bg-white text-sm font-medium text-gray-700 hover:bg-gray-50 rounded-r-md"
                            >
                                Next
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- New Sale Modal -->
        <NewSaleModal
            :isNewSaleModalOpen="openNewSaleModal"
            @closeNewSaleModal="openNewSaleModal = false"
        />

        <!-- Sale Details Modal -->
        <SaleDetailModal
            :selectedSale="selectedSale"
            @closeDetailModal="selectedSale = null"
        />
    </div>
</template>
