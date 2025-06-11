<script setup>
    import { ref, computed } from "vue";
    import { Formatters } from "@/utils/formatters.js";

    const props = defineProps({
        isNewSaleModalOpen: {
            type: Boolean,
            required: true,
            default: false,
        },
    });
    const emit = defineEmits(["closeNewSaleModal"]);

    const showNewCustomerForm = ref(false);
    const selectedSale = ref(null);
    const newCustomer = ref({
        name: "",
        email: "",
        phone: "",
        address: "",
    });

    const newSale = ref({
        customerId: "",
        items: [],
        taxRate: 8.5,
        paymentMethod: "cash",
        notes: "",
    });

    const updateProductDetails = (index) => {
        const item = newSale.value.items[index];
        const product = availableProducts.value.find(
            (p) => p.id === item.productId
        );

        if (product) {
            item.price = product.price;
            item.total = item.price * item.quantity;
            calculateItemTotal(index);
        }
    };

    const customers = ref([
        {
            id: 1,
            name: "John Doe",
            email: "john.doe@example.com",
            phone: "(555) 123-4567",
            address: "123 Main St, Anytown, USA",
        },
        {
            id: 2,
            name: "Jane Smith",
            email: "jane.smith@example.com",
            phone: "(555) 987-6543",
            address: "456 Oak Ave, Sometown, USA",
        },
        {
            id: 3,
            name: "Robert Johnson",
            email: "robert.j@example.com",
            phone: "(555) 765-4321",
            address: "789 Pine St, Othertown, USA",
        },
    ]);

    const availableProducts = ref([
        {
            id: 1,
            name: "T-Shirt Classic",
            sku: "TS-CL-001",
            price: 29.99,
            stock: 45,
        },
        {
            id: 2,
            name: "Polo Shirt",
            sku: "PS-ST-001",
            price: 49.99,
            stock: 32,
        },
        {
            id: 3,
            name: "Denim Jeans",
            sku: "DJ-BL-002",
            price: 79.99,
            stock: 28,
        },
        {
            id: 4,
            name: "Casual Jacket",
            sku: "CJ-BK-001",
            price: 129.99,
            stock: 15,
        },
        {
            id: 5,
            name: "Summer Dress",
            sku: "SD-FL-003",
            price: 89.99,
            stock: 20,
        },
        {
            id: 6,
            name: "Athletic Socks (3 Pack)",
            sku: "AS-WH-003",
            price: 19.99,
            stock: 50,
        },
        {
            id: 7,
            name: "Leather Belt",
            sku: "LB-BR-001",
            price: 34.99,
            stock: 22,
        },
    ]);

    const canSaveSale = computed(() => {
        return (
            newSale.value.customerId &&
            newSale.value.items.length > 0 &&
            newSale.value.paymentMethod &&
            !newSale.value.items.some(
                (item) => !item.productId || item.quantity <= 0
            )
        );
    });

    const openNewCustomerForm = () => {
        showNewCustomerForm.value = true;
        newCustomer.value = {
            name: "",
            email: "",
            phone: "",
            address: "",
        };
    };

    const calculateItemTotal = (index) => {
        const item = newSale.value.items[index];
        const product = availableProducts.value.find(
            (p) => p.id === item.productId
        );

        if (product) {
            // Check if quantity exceeds available stock
            item.stockWarning = item.quantity > product.stock;
            item.availableStock = product.stock;
        }

        item.total = item.price * item.quantity;
    };

    const calculateSubtotal = () => {
        return newSale.value.items.reduce(
            (sum, item) => sum + (item.total || 0),
            0
        );
    };

    const calculateTax = () => {
        const subtotal = calculateSubtotal();
        return subtotal * (newSale.value.taxRate / 100);
    };

    const calculateTotal = () => {
        const subtotal = calculateSubtotal();
        const tax = calculateTax();
        return subtotal + tax;
    };

    const cancelNewCustomer = () => {
        showNewCustomerForm.value = false;
    };

    const saveNewCustomer = () => {
        // Simple validation
        if (!newCustomer.value.name || !newCustomer.value.email) {
            alert("Please provide at least a name and email for the customer.");
            return;
        }
    };

    const addProductLine = () => {
        newSale.value.items.push({
            productId: "",
            quantity: 1,
            price: 0,
            total: 0,
            stockWarning: false,
            availableStock: 0,
        });
    };

    const removeProductLine = (index) => {
        newSale.value.items.splice(index, 1);
    };

    const saveSale = () => {
        if (!canSaveSale.value) {
            return;
        }

        // Get customer details
        const customer = customers.value.find(
            (c) => c.id === newSale.value.customerId
        );

        if (!customer) {
            alert("Please select a valid customer.");
            return;
        }

        // Check stock levels
        for (const item of newSale.value.items) {
            const product = availableProducts.value.find(
                (p) => p.id === item.productId
            );
            if (item.quantity > product.stock) {
                alert(
                    `Insufficient stock for ${product.name}. Available: ${product.stock}, Requested: ${item.quantity}`
                );
                return;
            }
        }

        // Create sale object
        const subtotal = calculateSubtotal();
        const tax = calculateTax();
        const total = calculateTotal();

        const saleData = {
            id: sales.value.length + 1,
            invoiceNumber: `INV-2025-${String(sales.value.length + 1).padStart(
                3,
                "0"
            )}`,
            date: new Date(),
            customer: customer,
            items: newSale.value.items.map((item) => {
                const product = availableProducts.value.find(
                    (p) => p.id === item.productId
                );
                return {
                    product: product,
                    quantity: item.quantity,
                    price: item.price,
                    total: item.total,
                };
            }),
            subtotal: subtotal,
            taxRate: newSale.value.taxRate,
            tax: tax,
            total: total,
            status: "Completed",
            paymentMethod: newSale.value.paymentMethod,
            notes: newSale.value.notes,
        };

        // Add to sales array
        sales.value.unshift(saleData);
        totalSales.value++;

        // Update product stock (in a real app, this would be done on the server)
        for (const item of newSale.value.items) {
            const product = availableProducts.value.find(
                (p) => p.id === item.productId
            );
            if (product) {
                product.stock -= item.quantity;
            }
        }

        // Update sales summary (in a real app, this would be calculated from actual data)
        // salesSummary.value.daily += total;
        // salesSummary.value.dailyPercentage = 15.8; // Example value
        // salesSummary.value.weekly += total;
        // salesSummary.value.weeklyPercentage = 10.2; // Example value

        // Close the modal
        closeNewSaleModal();

        // Show success notification (in a real app)
        alert(
            `Sale completed successfully. Invoice #${saleData.invoiceNumber}`
        );
    };

    const closeNewSaleModal = () => {
        isNewSaleModalOpen.value = false;
        showNewCustomerForm.value = false;
    };
</script>

<template>
    <div
        v-if="props.isNewSaleModalOpen"
        class="fixed inset-0 z-50 overflow-y-auto"
    >
        <div class="flex items-center justify-center min-h-screen p-4">
            <div class="fixed inset-0 bg-black opacity-30"></div>
            <div
                class="relative bg-white rounded-lg shadow-xl max-w-4xl w-full mx-auto"
            >
                <div class="px-6 py-4 border-b border-gray-200">
                    <h3 class="text-lg font-medium text-gray-900">
                        Create New Sale
                    </h3>
                </div>
                <div class="p-6">
                    <div class="mb-6">
                        <label
                            class="block text-sm font-medium text-gray-700 mb-1"
                            >Customer</label
                        >
                        <div class="flex space-x-2">
                            <select
                                v-model="newSale.customerId"
                                class="border border-gray-300 rounded-md px-3 py-2 w-full"
                            >
                                <option value="" disabled>
                                    Select a customer
                                </option>
                                <option
                                    v-for="customer in customers"
                                    :key="customer.id"
                                    :value="customer.id"
                                >
                                    {{ customer.name }}
                                </option>
                            </select>
                            <button
                                class="bg-gray-100 hover:bg-gray-200 text-gray-700 px-3 py-2 rounded-md"
                                @click="
                                    showNewCustomerForm = !showNewCustomerForm
                                "
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
                                        d="M12 4v16m8-8H4"
                                    />
                                </svg>
                            </button>
                        </div>
                    </div>

                    <!-- New Customer Form (conditionally shown) -->
                    <div
                        v-if="showNewCustomerForm"
                        class="mb-6 p-4 bg-gray-50 rounded-lg"
                    >
                        <h4 class="text-sm font-medium text-gray-700 mb-3">
                            New Customer Details
                        </h4>
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div>
                                <label
                                    class="block text-sm font-medium text-gray-700 mb-1"
                                    >Name</label
                                >
                                <input
                                    type="text"
                                    v-model="newCustomer.name"
                                    class="border border-gray-300 rounded-md px-3 py-2 w-full"
                                />
                            </div>
                            <div>
                                <label
                                    class="block text-sm font-medium text-gray-700 mb-1"
                                    >Email</label
                                >
                                <input
                                    type="email"
                                    v-model="newCustomer.email"
                                    class="border border-gray-300 rounded-md px-3 py-2 w-full"
                                />
                            </div>
                            <div>
                                <label
                                    class="block text-sm font-medium text-gray-700 mb-1"
                                    >Phone</label
                                >
                                <input
                                    type="tel"
                                    v-model="newCustomer.phone"
                                    class="border border-gray-300 rounded-md px-3 py-2 w-full"
                                />
                            </div>
                            <div>
                                <label
                                    class="block text-sm font-medium text-gray-700 mb-1"
                                    >Address</label
                                >
                                <input
                                    type="text"
                                    v-model="newCustomer.address"
                                    class="border border-gray-300 rounded-md px-3 py-2 w-full"
                                />
                            </div>
                        </div>
                        <div class="flex justify-end mt-4">
                            <button
                                @click="showNewCustomerForm = false"
                                class="bg-white border border-gray-300 text-gray-700 px-4 py-2 rounded-md mr-2"
                            >
                                Cancel
                            </button>
                            <button
                                @click="saveNewCustomer"
                                class="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-md"
                            >
                                Save Customer
                            </button>
                        </div>
                    </div>

                    <!-- Product Selection -->
                    <div class="mb-6">
                        <div class="flex justify-between items-center mb-2">
                            <label
                                class="block text-sm font-medium text-gray-700"
                                >Products</label
                            >
                            <button
                                @click="addProductLine"
                                class="text-indigo-600 hover:text-indigo-900 text-sm flex items-center"
                            >
                                <svg
                                    class="h-4 w-4 mr-1"
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
                                Add Product
                            </button>
                        </div>

                        <div class="bg-gray-50 rounded-lg p-4">
                            <div
                                v-for="(item, index) in newSale.items"
                                :key="index"
                                class="mb-4"
                            >
                                <div
                                    class="grid grid-cols-12 gap-2 items-center"
                                >
                                    <div class="col-span-5">
                                        <select
                                            v-model="item.productId"
                                            @change="
                                                updateProductDetails(index)
                                            "
                                            class="border border-gray-300 rounded-md px-3 py-2 w-full"
                                        >
                                            <option value="" disabled>
                                                Select a product
                                            </option>
                                            <option
                                                v-for="product in availableProducts"
                                                :key="product.id"
                                                :value="product.id"
                                            >
                                                {{ product.name }} -
                                                {{
                                                    Formatters.formatCurrency(
                                                        product.price
                                                    )
                                                }}
                                            </option>
                                        </select>
                                    </div>
                                    <div class="col-span-2">
                                        <input
                                            type="number"
                                            v-model="item.quantity"
                                            min="1"
                                            @change="calculateItemTotal(index)"
                                            class="border border-gray-300 rounded-md px-3 py-2 w-full"
                                        />
                                    </div>
                                    <div class="col-span-2">
                                        <input
                                            type="number"
                                            v-model="item.price"
                                            readonly
                                            class="border border-gray-300 rounded-md px-3 py-2 w-full bg-gray-100"
                                        />
                                    </div>
                                    <div class="col-span-2">
                                        <input
                                            type="number"
                                            v-model="item.total"
                                            readonly
                                            class="border border-gray-300 rounded-md px-3 py-2 w-full bg-gray-100"
                                        />
                                    </div>
                                    <div class="col-span-1 flex justify-center">
                                        <button
                                            @click="removeProductLine(index)"
                                            class="text-red-500 hover:text-red-700"
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
                                                    d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                                                />
                                            </svg>
                                        </button>
                                    </div>
                                </div>
                                <div
                                    v-if="item.stockWarning"
                                    class="mt-1 text-xs text-red-500"
                                >
                                    Warning: Only
                                    {{ item.availableStock }} items in stock
                                </div>
                            </div>

                            <div
                                v-if="newSale.items.length === 0"
                                class="text-center py-4 text-gray-500"
                            >
                                No products added yet. Click "Add Product" to
                                start creating your sale.
                            </div>

                            <div
                                v-if="newSale.items.length > 0"
                                class="mt-4 border-t border-gray-200 pt-4"
                            >
                                <div class="flex justify-end">
                                    <div class="w-64">
                                        <div class="flex justify-between mb-2">
                                            <span class="text-sm text-gray-600"
                                                >Subtotal:</span
                                            >
                                            <span class="text-sm font-medium">{{
                                                Formatters.formatCurrency(
                                                    calculateSubtotal()
                                                )
                                            }}</span>
                                        </div>
                                        <div class="flex justify-between mb-2">
                                            <span class="text-sm text-gray-600"
                                                >Tax ({{
                                                    newSale.taxRate
                                                }}%):</span
                                            >
                                            <span class="text-sm font-medium">{{
                                                Formatters.formatCurrency(
                                                    calculateTax()
                                                )
                                            }}</span>
                                        </div>
                                        <div
                                            class="flex justify-between font-medium"
                                        >
                                            <span>Total:</span>
                                            <span>{{
                                                Formatters.formatCurrency(
                                                    calculateTotal()
                                                )
                                            }}</span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Payment Method -->
                    <div class="mb-6">
                        <label
                            class="block text-sm font-medium text-gray-700 mb-1"
                            >Payment Method</label
                        >
                        <div class="flex space-x-4">
                            <label class="inline-flex items-center">
                                <input
                                    type="radio"
                                    v-model="newSale.paymentMethod"
                                    value="cash"
                                    class="text-indigo-600"
                                />
                                <span class="ml-2">Cash</span>
                            </label>
                            <label class="inline-flex items-center">
                                <input
                                    type="radio"
                                    v-model="newSale.paymentMethod"
                                    value="card"
                                    class="text-indigo-600"
                                />
                                <span class="ml-2">Card</span>
                            </label>
                            <label class="inline-flex items-center">
                                <input
                                    type="radio"
                                    v-model="newSale.paymentMethod"
                                    value="bank_transfer"
                                    class="text-indigo-600"
                                />
                                <span class="ml-2">Bank Transfer</span>
                            </label>
                        </div>
                    </div>

                    <!-- Notes -->
                    <div class="mb-6">
                        <label
                            class="block text-sm font-medium text-gray-700 mb-1"
                            >Notes</label
                        >
                        <textarea
                            v-model="newSale.notes"
                            rows="3"
                            class="border border-gray-300 rounded-md px-3 py-2 w-full"
                            placeholder="Add any notes about this sale..."
                        ></textarea>
                    </div>
                </div>
                <div
                    class="px-6 py-4 border-t border-gray-200 flex justify-end"
                >
                    <button
                        @click="$emit('closeNewSaleModal')"
                        class="bg-white border border-gray-300 text-gray-700 px-4 py-2 rounded-md mr-2"
                    >
                        Cancel
                    </button>
                    <button
                        @click="saveSale"
                        class="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-md"
                        :disabled="!canSaveSale"
                    >
                        Complete Sale
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>
