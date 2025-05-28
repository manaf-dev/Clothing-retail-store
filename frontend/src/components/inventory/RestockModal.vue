<script setup>
    import { ref, watch } from "vue";

    const props = defineProps({
        showRestockModal: {
            type: Boolean,
            required: true,
        },
        inventory: {
            type: Array,
            required: true,
        },
        selectedItem: {
            type: Object,
            default: null,
        },
    });

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
</script>

<template>
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
                        {{ selectedItem ? "Restock Product" : "Bulk Restock" }}
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
                                    {{ item.name }} ({{ item.currentStock }})
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
</template>
