<script setup>
    import { ref } from "vue";
    import Formatters from "@/utils/formatters.js";

    const props = defineProps({
        selectedSale: {
            type: Object,
            required: false,
        },
    });

    const cancelSale = (saleId) => {
        // Find the sale
        const saleIndex = sales.value.findIndex((s) => s.id === saleId);

        if (saleIndex !== -1) {
            // Get the sale
            const sale = sales.value[saleIndex];

            // Confirm cancellation
            if (
                confirm(
                    `Are you sure you want to cancel sale #${sale.invoiceNumber}?`
                )
            ) {
                // Update sale status
                sales.value[saleIndex].status = "Cancelled";

                // If we're viewing the selected sale, update that too
                if (selectedSale.value && selectedSale.value.id === saleId) {
                    selectedSale.value.status = "Cancelled";
                }

                // In a real app, you would also:
                // 1. Update the server
                // 2. Return items to inventory
                // 3. Process refund if necessary

                alert(`Sale #${sale.invoiceNumber} has been cancelled.`);
            }
        }
    };
</script>

<template>
    <div v-if="props.selectedSale" class="fixed inset-0 z-50 overflow-y-auto">
        <div class="flex items-center justify-center min-h-screen p-4">
            <div
                class="fixed inset-0 bg-black opacity-30"
                @click="props.selectedSale = null"
            ></div>
            <div
                class="relative bg-white rounded-lg shadow-xl max-w-3xl w-full mx-auto"
            >
                <div
                    class="px-6 py-4 border-b border-gray-200 flex justify-between items-center"
                >
                    <h3 class="text-lg font-medium text-gray-900">
                        Sale Details - Invoice #{{
                            props.selectedSale.invoiceNumber
                        }}
                    </h3>
                    <button
                        @click="$emit('closeDetailModal')"
                        class="text-gray-400 hover:text-gray-500"
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
                <div class="p-6">
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                        <div>
                            <h4 class="text-sm font-medium text-gray-500 mb-1">
                                Customer Information
                            </h4>
                            <p class="text-sm text-gray-900">
                                {{ props.selectedSale.customer.name }}
                            </p>
                            <p class="text-sm text-gray-500">
                                {{ props.selectedSale.customer.email }}
                            </p>
                            <p class="text-sm text-gray-500">
                                {{ props.selectedSale.customer.phone }}
                            </p>
                        </div>
                        <div>
                            <h4 class="text-sm font-medium text-gray-500 mb-1">
                                Sale Information
                            </h4>
                            <p class="text-sm text-gray-900">
                                Date:
                                {{
                                    Formatters.formatDate(
                                        props.selectedSale.date
                                    )
                                }}
                                at
                                {{
                                    Formatters.formatTime(
                                        props.selectedSale.date
                                    )
                                }}
                            </p>
                            <p class="text-sm text-gray-900">
                                Status:
                                <span
                                    :class="{
                                        'text-green-600':
                                            props.selectedSale.status ===
                                            'Completed',
                                        'text-yellow-600':
                                            props.selectedSale.status ===
                                            'Pending',
                                        'text-red-600':
                                            props.selectedSale.status ===
                                            'Cancelled',
                                    }"
                                >
                                    {{ props.selectedSale.status }}
                                </span>
                            </p>
                            <p class="text-sm text-gray-900">
                                Payment Method:
                                {{
                                    Formatters.formatPaymentMethod(
                                        props.selectedSale.paymentMethod
                                    )
                                }}
                            </p>
                        </div>
                    </div>

                    <h4 class="text-sm font-medium text-gray-700 mb-2">
                        Items
                    </h4>
                    <div class="bg-gray-50 rounded-lg p-4 mb-6">
                        <table class="min-w-full">
                            <thead>
                                <tr>
                                    <th
                                        class="text-left text-xs font-medium text-gray-500 uppercase tracking-wider pb-2"
                                    >
                                        Product
                                    </th>
                                    <th
                                        class="text-right text-xs font-medium text-gray-500 uppercase tracking-wider pb-2"
                                    >
                                        Price
                                    </th>
                                    <th
                                        class="text-right text-xs font-medium text-gray-500 uppercase tracking-wider pb-2"
                                    >
                                        Quantity
                                    </th>
                                    <th
                                        class="text-right text-xs font-medium text-gray-500 uppercase tracking-wider pb-2"
                                    >
                                        Total
                                    </th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr
                                    v-for="(item, index) in props.selectedSale
                                        .items"
                                    :key="index"
                                    class="border-t border-gray-200"
                                >
                                    <td class="py-2 text-sm text-gray-900">
                                        {{ item.product.name }}
                                    </td>
                                    <td
                                        class="py-2 text-sm text-gray-900 text-right"
                                    >
                                        ${{
                                            Formatters.formatNumber(item.price)
                                        }}
                                    </td>
                                    <td
                                        class="py-2 text-sm text-gray-900 text-right"
                                    >
                                        {{ item.quantity }}
                                    </td>
                                    <td
                                        class="py-2 text-sm text-gray-900 text-right"
                                    >
                                        ${{
                                            Formatters.formatNumber(item.total)
                                        }}
                                    </td>
                                </tr>
                            </tbody>
                            <tfoot>
                                <tr class="border-t border-gray-200">
                                    <td
                                        colspan="3"
                                        class="py-2 text-sm font-medium text-gray-900 text-right"
                                    >
                                        Subtotal:
                                    </td>
                                    <td
                                        class="py-2 text-sm font-medium text-gray-900 text-right"
                                    >
                                        ${{
                                            Formatters.formatNumber(
                                                props.selectedSale.subtotal
                                            )
                                        }}
                                    </td>
                                </tr>
                                <tr>
                                    <td
                                        colspan="3"
                                        class="py-2 text-sm font-medium text-gray-900 text-right"
                                    >
                                        Tax ({{ props.selectedSale.taxRate }}%):
                                    </td>
                                    <td
                                        class="py-2 text-sm font-medium text-gray-900 text-right"
                                    >
                                        ${{
                                            Formatters.formatNumber(
                                                props.selectedSale.tax
                                            )
                                        }}
                                    </td>
                                </tr>
                                <tr>
                                    <td
                                        colspan="3"
                                        class="py-2 text-sm font-bold text-gray-900 text-right"
                                    >
                                        Total:
                                    </td>
                                    <td
                                        class="py-2 text-sm font-bold text-gray-900 text-right"
                                    >
                                        ${{
                                            Formatters.formatNumber(
                                                props.selectedSale.total
                                            )
                                        }}
                                    </td>
                                </tr>
                            </tfoot>
                        </table>
                    </div>

                    <div v-if="props.selectedSale.notes" class="mb-6">
                        <h4 class="text-sm font-medium text-gray-700 mb-1">
                            Notes
                        </h4>
                        <p
                            class="text-sm text-gray-600 bg-gray-50 p-3 rounded-lg"
                        >
                            {{ props.selectedSale.notes }}
                        </p>
                    </div>
                </div>
                <div
                    class="px-6 py-4 border-t border-gray-200 flex justify-between"
                >
                    <div>
                        <button
                            v-if="props.selectedSale.status !== 'Cancelled'"
                            @click="cancelSale(props.selectedSale.id)"
                            class="text-red-600 hover:text-red-800 mr-4"
                        >
                            Cancel Sale
                        </button>
                    </div>
                    <div>
                        <button
                            @click="printInvoice(props.selectedSale)"
                            class="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-md"
                        >
                            Print Invoice
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
