<script setup>
    import { ref, watch } from "vue";

    const props = defineProps({
        showViewModal: {
            type: Boolean,
            required: true,
        },
        selectedCustomer: {
            type: Object,
            default: null,
        },
    });
    const emit = defineEmits(["close"]);

    const showViewModal = ref(props.showViewModal);
    const selectedCustomer = ref(props.selectedCustomer);
    console.log("Selected Customer:", selectedCustomer.value);

    const getStatusClass = (status) => {
        switch (status) {
            case "active":
                return "bg-green-100 text-green-800";
            case "inactive":
                return "bg-yellow-100 text-yellow-800";
            case "banned":
                return "bg-red-100 text-red-800";
            default:
                return "bg-gray-100 text-gray-800";
        }
    };

    watch(
        () => props.showViewModal,
        (newVal) => {
            showViewModal.value = newVal;
        }
    );

    watch(
        () => props.selectedCustomer,
        (newVal) => {
            selectedCustomer.value = newVal;
        }
    );
</script>

<template>
    <div
        v-if="showViewModal"
        class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50"
    >
        <div
            class="relative top-20 mx-auto p-5 border w-11/12 md:w-3/4 lg:w-2/3 shadow-lg rounded-md bg-white"
        >
            <div class="mt-3">
                <div class="flex items-center justify-between mb-4">
                    <h3 class="text-lg font-medium text-gray-900">
                        Customer Details
                    </h3>
                    <button
                        @click="showViewModal = false"
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

                <div
                    v-if="selectedCustomer"
                    class="grid grid-cols-1 lg:grid-cols-2 gap-6"
                >
                    <!-- Customer Info -->
                    <div class="bg-gray-50 rounded-lg p-4">
                        <h4 class="font-medium text-gray-900 mb-3">
                            Personal Information
                        </h4>
                        <div class="space-y-2">
                            <p>
                                <span class="font-medium">Name:</span>
                                {{ selectedCustomer.name }}
                            </p>
                            <p>
                                <span class="font-medium">Email:</span>
                                {{ selectedCustomer.email }}
                            </p>
                            <p>
                                <span class="font-medium">Phone:</span>
                                {{ selectedCustomer.phone }}
                            </p>
                            <p>
                                <span class="font-medium">Address:</span>
                                {{ selectedCustomer.address || "Not provided" }}
                            </p>
                            <p>
                                <span class="font-medium">Status:</span>
                                <span
                                    :class="
                                        getStatusClass(selectedCustomer.status)
                                    "
                                    class="px-2 py-1 text-xs rounded-full"
                                >
                                    {{ selectedCustomer.status.toUpperCase() }}
                                </span>
                            </p>
                        </div>
                    </div>

                    <!-- Purchase History -->
                    <div class="bg-gray-50 rounded-lg p-4">
                        <h4 class="font-medium text-gray-900 mb-3">
                            Purchase Summary
                        </h4>
                        <div class="space-y-2">
                            <p>
                                <span class="font-medium">Total Orders:</span>
                                {{ selectedCustomer.totalOrders }}
                            </p>
                            <p>
                                <span class="font-medium">Total Spent:</span>
                                ${{
                                    selectedCustomer.totalSpent.toLocaleString()
                                }}
                            </p>
                            <p>
                                <span class="font-medium">Average Order:</span>
                                ${{
                                    (
                                        selectedCustomer.totalSpent /
                                        selectedCustomer.totalOrders
                                    ).toFixed(2)
                                }}
                            </p>
                            <p>
                                <span class="font-medium">Last Order:</span>
                                {{ selectedCustomer.lastOrder }}
                            </p>
                            <p>
                                <span class="font-medium">Customer Since:</span>
                                {{ selectedCustomer.joinDate }}
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
