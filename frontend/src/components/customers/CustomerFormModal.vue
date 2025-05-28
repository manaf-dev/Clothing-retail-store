<script setup>
    import { ref, watch } from "vue";

    const props = defineProps({
        showAddModal: {
            type: Boolean,
            required: true,
        },
        showEditModal: {
            type: Boolean,
            required: true,
        },
        customer: {
            type: Object,
            default: () => ({}),
        },
    });

    const emit = defineEmits(["close", "save"]);

    const showAddModal = ref(props.showAddModal);
    const showEditModal = ref(props.showEditModal);
    const customerForm = ref({ ...props.customer });

    watch(
        () => props.showAddModal,
        (newVal) => {
            showAddModal.value = newVal;
        }
    );

    watch(
        () => props.showEditModal,
        (newVal) => {
            showEditModal.value = newVal;
        }
    );

    watch(
        () => props.customer,
        (newVal) => {
            customerForm.value = { ...newVal };
        }
    );
</script>

<template>
    <div
        v-if="showAddModal || showEditModal"
        class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50"
    >
        <div
            class="relative top-20 mx-auto p-5 border w-11/12 md:w-3/4 lg:w-1/2 shadow-lg rounded-md bg-white"
        >
            <div class="mt-3">
                <div class="flex items-center justify-between mb-4">
                    <h3 class="text-lg font-medium text-gray-900">
                        {{
                            showAddModal ? "Add New Customer" : "Edit Customer"
                        }}
                    </h3>
                    <button
                        @click="$emit('close')"
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

                <form @submit.prevent="saveCustomer">
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                            <label
                                class="block text-sm font-medium text-gray-700 mb-1"
                                >Full Name</label
                            >
                            <input
                                v-model="customerForm.name"
                                type="text"
                                required
                                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                            />
                        </div>

                        <div>
                            <label
                                class="block text-sm font-medium text-gray-700 mb-1"
                                >Email</label
                            >
                            <input
                                v-model="customerForm.email"
                                type="email"
                                required
                                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                            />
                        </div>

                        <div>
                            <label
                                class="block text-sm font-medium text-gray-700 mb-1"
                                >Phone</label
                            >
                            <input
                                v-model="customerForm.phone"
                                type="tel"
                                required
                                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                            />
                        </div>

                        <div>
                            <label
                                class="block text-sm font-medium text-gray-700 mb-1"
                                >Date of Birth</label
                            >
                            <input
                                v-model="customerForm.dateOfBirth"
                                type="date"
                                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                            />
                        </div>

                        <div class="md:col-span-2">
                            <label
                                class="block text-sm font-medium text-gray-700 mb-1"
                                >Address</label
                            >
                            <textarea
                                v-model="customerForm.address"
                                rows="3"
                                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                            >
                            </textarea>
                        </div>

                        <div>
                            <label
                                class="block text-sm font-medium text-gray-700 mb-1"
                                >Status</label
                            >
                            <select
                                v-model="customerForm.status"
                                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                            >
                                <option value="active">Active</option>
                                <option value="inactive">Inactive</option>
                                <option value="vip">VIP</option>
                            </select>
                        </div>

                        <div>
                            <label
                                class="block text-sm font-medium text-gray-700 mb-1"
                                >Gender</label
                            >
                            <select
                                v-model="customerForm.gender"
                                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                            >
                                <option value="">Select Gender</option>
                                <option value="male">Male</option>
                                <option value="female">Female</option>
                                <option value="other">Other</option>
                            </select>
                        </div>
                    </div>

                    <div class="flex justify-end space-x-3 mt-6">
                        <button
                            type="button"
                            @click="$emit('close')"
                            class="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-md"
                        >
                            Cancel
                        </button>
                        <button
                            type="submit"
                            class="px-4 py-2 text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 rounded-md"
                        >
                            {{
                                showAddModal
                                    ? "Add Customer"
                                    : "Update Customer"
                            }}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>
