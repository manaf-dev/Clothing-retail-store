<script setup>
    import { ref, computed } from "vue";
    import CustomerDetailModal from "./CustomerDetailModal.vue";
    import CustomerFormModal from "./CustomerFormModal.vue";

    const searchQuery = ref("");
    const selectedStatus = ref("");
    const sortBy = ref("name");
    const showAddModal = ref(false);
    const showEditModal = ref(false);
    const showViewModal = ref(false);
    const selectedCustomer = ref(null);
    const customerForm = ref({
        name: "",
        email: "",
        phone: "",
        address: "",
        dateOfBirth: "",
        status: "active",
        gender: "",
    });
    const customers = ref([
        {
            id: 1,
            name: "John Doe",
            email: "john.doe@email.com",
            phone: "+1 (555) 123-4567",
            address: "123 Main St, City, State 12345",
            status: "active",
            totalOrders: 15,
            totalSpent: 1250.0,
            lastOrder: "2025-05-20",
            joinDate: "2024-01-15",
            gender: "male",
        },
        {
            id: 2,
            name: "Jane Smith",
            email: "jane.smith@email.com",
            phone: "+1 (555) 234-5678",
            address: "456 Oak Ave, City, State 12345",
            status: "vip",
            totalOrders: 28,
            totalSpent: 3420.0,
            lastOrder: "2025-05-25",
            joinDate: "2023-08-20",
            gender: "female",
        },
        {
            id: 3,
            name: "Mike Johnson",
            email: "mike.johnson@email.com",
            phone: "+1 (555) 345-6789",
            address: "789 Pine Rd, City, State 12345",
            status: "active",
            totalOrders: 8,
            totalSpent: 650.0,
            lastOrder: "2025-05-18",
            joinDate: "2024-03-10",
            gender: "male",
        },
        {
            id: 4,
            name: "Sarah Williams",
            email: "sarah.williams@email.com",
            phone: "+1 (555) 456-7890",
            address: "321 Elm St, City, State 12345",
            status: "inactive",
            totalOrders: 3,
            totalSpent: 180.0,
            lastOrder: "2025-03-15",
            joinDate: "2024-02-05",
            gender: "female",
        },
        {
            id: 5,
            name: "Robert Brown",
            email: "robert.brown@email.com",
            phone: "+1 (555) 567-8901",
            address: "654 Maple Dr, City, State 12345",
            status: "vip",
            totalOrders: 22,
            totalSpent: 2890.0,
            lastOrder: "2025-05-22",
            joinDate: "2023-11-12",
            gender: "male",
        },
    ]);

    const totalCustomers = computed(() => customers.value.length);
    const activeCustomers = computed(
        () =>
            customers.value.filter(
                (c) => c.status === "active" || c.status === "vip"
            ).length
    );
    const totalSpent = computed(() =>
        customers.value.reduce((sum, customer) => sum + customer.totalSpent, 0)
    );
    const vipCustomers = computed(
        () => customers.value.filter((c) => c.status === "vip").length
    );

    const filteredCustomers = computed(() => {
        let filtered = [...customers.value];

        // Filter by search query
        if (searchQuery.value) {
            const query = searchQuery.value.toLowerCase();
            filtered = filtered.filter(
                (customer) =>
                    customer.name.toLowerCase().includes(query) ||
                    customer.email.toLowerCase().includes(query) ||
                    customer.phone.includes(query)
            );
        }

        // Filter by status
        if (selectedStatus.value) {
            filtered = filtered.filter(
                (customer) => customer.status === selectedStatus.value
            );
        }

        // Sort
        if (sortBy.value === "name") {
            filtered.sort((a, b) => a.name.localeCompare(b.name));
        } else if (sortBy.value === "date") {
            filtered.sort(
                (a, b) => new Date(b.lastOrder) - new Date(a.lastOrder)
            );
        } else if (sortBy.value === "spent") {
            filtered.sort((a, b) => b.totalSpent - a.totalSpent);
        } else if (sortBy.value === "orders") {
            filtered.sort((a, b) => b.totalOrders - a.totalOrders);
        }

        return filtered;
    });

    function getStatusClass(status) {
        const classes = {
            active: "bg-green-100 text-green-800",
            inactive: "bg-red-100 text-red-800",
            vip: "bg-purple-100 text-purple-800",
        };
        return classes[status] || "bg-gray-100 text-gray-800";
    }

    function viewCustomer(customer) {
        selectedCustomer.value = customer;
        showViewModal.value = true;
    }

    function editCustomer(customer) {
        customerForm.value = { ...customer };
        showEditModal.value = true;
    }

    function deleteCustomer(customer) {
        // Implement delete logic here
    }
</script>

<!-- src/views/CustomersView.vue -->
<template>
    <div>
        <!-- Page Header -->
        <div class="flex justify-between items-center mb-6">
            <h1 class="text-2xl font-semibold text-gray-800">
                Customer Management
            </h1>
            <button
                @click="showAddModal = true"
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
                        d="M12 6v6m0 0v6m0-6h6m-6 0H6"
                    />
                </svg>
                Add Customer
            </button>
        </div>

        <!-- Stats Cards -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
            <div class="bg-white rounded-lg shadow p-4">
                <div class="flex items-center">
                    <div class="p-2 rounded-full bg-blue-100 text-blue-600">
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
                                d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"
                            />
                        </svg>
                    </div>
                    <div class="ml-3">
                        <p class="text-sm font-medium text-gray-600">
                            Total Customers
                        </p>
                        <p class="text-xl font-semibold text-gray-800">
                            {{ totalCustomers }}
                        </p>
                    </div>
                </div>
            </div>

            <div class="bg-white rounded-lg shadow p-4">
                <div class="flex items-center">
                    <div class="p-2 rounded-full bg-green-100 text-green-600">
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
                                d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"
                            />
                        </svg>
                    </div>
                    <div class="ml-3">
                        <p class="text-sm font-medium text-gray-600">
                            Active Customers
                        </p>
                        <p class="text-xl font-semibold text-gray-800">
                            {{ activeCustomers }}
                        </p>
                    </div>
                </div>
            </div>

            <div class="bg-white rounded-lg shadow p-4">
                <div class="flex items-center">
                    <div class="p-2 rounded-full bg-purple-100 text-purple-600">
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
                                d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                            />
                        </svg>
                    </div>
                    <div class="ml-3">
                        <p class="text-sm font-medium text-gray-600">
                            Total Spent
                        </p>
                        <p class="text-xl font-semibold text-gray-800">
                            ${{ totalSpent.toLocaleString() }}
                        </p>
                    </div>
                </div>
            </div>

            <div class="bg-white rounded-lg shadow p-4">
                <div class="flex items-center">
                    <div class="p-2 rounded-full bg-yellow-100 text-yellow-600">
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
                                d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z"
                            />
                        </svg>
                    </div>
                    <div class="ml-3">
                        <p class="text-sm font-medium text-gray-600">
                            VIP Customers
                        </p>
                        <p class="text-xl font-semibold text-gray-800">
                            {{ vipCustomers }}
                        </p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Search and Filter -->
        <div class="bg-white rounded-lg shadow mb-6">
            <div class="p-4 border-b border-gray-200">
                <div
                    class="flex flex-col md:flex-row md:items-center md:justify-between gap-4"
                >
                    <div class="flex-1 min-w-0">
                        <div class="relative">
                            <div
                                class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none"
                            >
                                <svg
                                    class="h-5 w-5 text-gray-400"
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
                            <input
                                v-model="searchQuery"
                                type="text"
                                class="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500"
                                placeholder="Search customers by name, email, or phone..."
                            />
                        </div>
                    </div>

                    <div class="flex gap-3">
                        <select
                            v-model="selectedStatus"
                            class="block w-full pl-3 pr-10 py-2 text-base border border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 rounded-md"
                        >
                            <option value="">All Status</option>
                            <option value="active">Active</option>
                            <option value="inactive">Inactive</option>
                            <option value="vip">VIP</option>
                        </select>

                        <select
                            v-model="sortBy"
                            class="block w-full pl-3 pr-10 py-2 text-base border border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 rounded-md"
                        >
                            <option value="name">Sort by Name</option>
                            <option value="date">Sort by Date</option>
                            <option value="spent">Sort by Total Spent</option>
                            <option value="orders">Sort by Orders</option>
                        </select>
                    </div>
                </div>
            </div>
        </div>

        <!-- Customers Table -->
        <div class="bg-white rounded-lg shadow overflow-hidden">
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
                                Contact
                            </th>
                            <th
                                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                            >
                                Status
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
                                Last Order
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
                            v-for="customer in filteredCustomers"
                            :key="customer.id"
                            class="hover:bg-gray-50"
                        >
                            <td class="px-6 py-4 whitespace-nowrap">
                                <div class="flex items-center">
                                    <div class="flex-shrink-0 h-10 w-10">
                                        <div
                                            class="h-10 w-10 rounded-full bg-gray-300 flex items-center justify-center"
                                        >
                                            <span
                                                class="text-sm font-medium text-gray-700"
                                            >
                                                {{
                                                    customer.name
                                                        .split(" ")
                                                        .map((n) => n[0])
                                                        .join("")
                                                        .toUpperCase()
                                                }}
                                            </span>
                                        </div>
                                    </div>
                                    <div class="ml-4">
                                        <div
                                            class="text-sm font-medium text-gray-900"
                                        >
                                            {{ customer.name }}
                                        </div>
                                        <div class="text-sm text-gray-500">
                                            ID: #{{ customer.id }}
                                        </div>
                                    </div>
                                </div>
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap">
                                <div class="text-sm text-gray-900">
                                    {{ customer.email }}
                                </div>
                                <div class="text-sm text-gray-500">
                                    {{ customer.phone }}
                                </div>
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap">
                                <span
                                    :class="getStatusClass(customer.status)"
                                    class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full"
                                >
                                    {{ customer.status.toUpperCase() }}
                                </span>
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
                                {{ customer.lastOrder }}
                            </td>
                            <td
                                class="px-6 py-4 whitespace-nowrap text-sm font-medium"
                            >
                                <div class="flex space-x-2">
                                    <button
                                        @click="viewCustomer(customer)"
                                        class="text-indigo-600 hover:text-indigo-900"
                                    >
                                        View
                                    </button>
                                    <button
                                        @click="editCustomer(customer)"
                                        class="text-green-600 hover:text-green-900"
                                    >
                                        Edit
                                    </button>
                                    <button
                                        @click="deleteCustomer(customer)"
                                        class="text-red-600 hover:text-red-900"
                                    >
                                        Delete
                                    </button>
                                </div>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <!-- Pagination -->
            <div
                class="bg-white px-4 py-3 flex items-center justify-between border-t border-gray-200"
            >
                <div class="flex-1 flex justify-between sm:hidden">
                    <button
                        class="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
                    >
                        Previous
                    </button>
                    <button
                        class="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
                    >
                        Next
                    </button>
                </div>
                <div
                    class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between"
                >
                    <div>
                        <p class="text-sm text-gray-700">
                            Showing <span class="font-medium">1</span> to
                            <span class="font-medium">10</span> of
                            <span class="font-medium">{{
                                customers.length
                            }}</span>
                            results
                        </p>
                    </div>
                    <div>
                        <nav
                            class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px"
                        >
                            <button
                                class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50"
                            >
                                <span class="sr-only">Previous</span>
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
                                        d="M15 19l-7-7 7-7"
                                    />
                                </svg>
                            </button>
                            <button
                                class="relative inline-flex items-center px-4 py-2 border border-gray-300 bg-white text-sm font-medium text-gray-700 hover:bg-gray-50"
                            >
                                1
                            </button>
                            <button
                                class="relative inline-flex items-center px-4 py-2 border border-gray-300 bg-white text-sm font-medium text-gray-700 hover:bg-gray-50"
                            >
                                2
                            </button>
                            <button
                                class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50"
                            >
                                <span class="sr-only">Next</span>
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
                                        d="M9 5l7 7-7 7"
                                    />
                                </svg>
                            </button>
                        </nav>
                    </div>
                </div>
            </div>
        </div>

        <!-- Add/Edit Customer Modal -->
        <CustomerFormModal
            v-if="showAddModal || showEditModal"
            :showAddModal="showAddModal"
            :showEditModal="showEditModal"
            :customer="customerForm"
            @close="
                showAddModal = false;
                showEditModal = false;
            "
            @save="
                showAddModal = false;
                showEditModal = false;
            "
        />

        <!-- Customer Details Modal -->
        <CustomerDetailModal
            v-if="showViewModal"
            :showViewModal="showViewModal"
            :selectedCustomer="selectedCustomer"
            @close="showViewModal = false"
        />
    </div>
</template>
