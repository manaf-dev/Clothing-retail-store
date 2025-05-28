<template>
    <div v-if="isOpen" class="fixed z-10 inset-0 overflow-y-auto">
        <div
            class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0"
        >
            <div class="fixed inset-0 transition-opacity" aria-hidden="true">
                <div class="absolute inset-0 bg-gray-500 opacity-75"></div>
            </div>

            <span
                class="hidden sm:inline-block sm:align-middle sm:h-screen"
                aria-hidden="true"
                >&#8203;</span
            >

            <div
                class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full"
            >
                <form @submit.prevent="handleSubmit">
                    <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
                        <div class="mb-4">
                            <h3
                                class="text-lg leading-6 font-medium text-gray-900"
                            >
                                {{
                                    isEditing
                                        ? "Edit Product"
                                        : "Add New Product"
                                }}
                            </h3>
                        </div>

                        <div
                            class="grid grid-cols-1 gap-y-6 gap-x-4 sm:grid-cols-6"
                        >
                            <!-- Product Name -->
                            <div class="sm:col-span-6">
                                <label
                                    for="product-name"
                                    class="block text-sm font-medium text-gray-700"
                                    >Product Name</label
                                >
                                <input
                                    type="text"
                                    id="product-name"
                                    v-model="productData.name"
                                    required
                                    class="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                                />
                            </div>

                            <!-- SKU -->
                            <div class="sm:col-span-3">
                                <label
                                    for="product-sku"
                                    class="block text-sm font-medium text-gray-700"
                                    >SKU</label
                                >
                                <input
                                    type="text"
                                    id="product-sku"
                                    v-model="productData.sku"
                                    required
                                    class="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                                />
                            </div>

                            <!-- Category -->
                            <div class="sm:col-span-3">
                                <label
                                    for="product-category"
                                    class="block text-sm font-medium text-gray-700"
                                    >Category</label
                                >
                                <select
                                    id="product-category"
                                    v-model="productData.category"
                                    required
                                    class="mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                                >
                                    <option value="Men">Men's Clothing</option>
                                    <option value="Women">
                                        Women's Clothing
                                    </option>
                                    <option value="Kids">Kids' Clothing</option>
                                    <option value="Accessories">
                                        Accessories
                                    </option>
                                </select>
                            </div>

                            <!-- Sub-Category -->
                            <div class="sm:col-span-3">
                                <label
                                    for="product-subcategory"
                                    class="block text-sm font-medium text-gray-700"
                                    >Sub-Category</label
                                >
                                <input
                                    type="text"
                                    id="product-subcategory"
                                    v-model="productData.subCategory"
                                    class="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                                />
                            </div>

                            <!-- Price -->
                            <div class="sm:col-span-3">
                                <label
                                    for="product-price"
                                    class="block text-sm font-medium text-gray-700"
                                    >Price ($)</label
                                >
                                <input
                                    type="number"
                                    id="product-price"
                                    v-model="productData.price"
                                    required
                                    min="0"
                                    step="0.01"
                                    class="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                                />
                            </div>

                            <!-- Sale Price -->
                            <div class="sm:col-span-3">
                                <label
                                    for="product-sale-price"
                                    class="block text-sm font-medium text-gray-700"
                                    >Sale Price ($)</label
                                >
                                <input
                                    type="number"
                                    id="product-sale-price"
                                    v-model="productData.salePrice"
                                    min="0"
                                    step="0.01"
                                    class="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                                />
                                <p class="mt-1 text-sm text-gray-500">
                                    Leave empty if not on sale
                                </p>
                            </div>

                            <!-- Stock -->
                            <div class="sm:col-span-3">
                                <label
                                    for="product-stock"
                                    class="block text-sm font-medium text-gray-700"
                                    >Stock Quantity</label
                                >
                                <input
                                    type="number"
                                    id="product-stock"
                                    v-model="productData.stock"
                                    required
                                    min="0"
                                    class="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                                />
                            </div>

                            <!-- Description -->
                            <div class="sm:col-span-6">
                                <label
                                    for="product-description"
                                    class="block text-sm font-medium text-gray-700"
                                    >Description</label
                                >
                                <textarea
                                    id="product-description"
                                    v-model="productData.description"
                                    rows="3"
                                    class="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                                ></textarea>
                            </div>

                            <!-- Image URL -->
                            <div class="sm:col-span-6">
                                <label
                                    for="product-image"
                                    class="block text-sm font-medium text-gray-700"
                                    >Image URL</label
                                >
                                <input
                                    type="text"
                                    id="product-image"
                                    v-model="productData.image"
                                    class="mt-1 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                                />
                            </div>
                        </div>
                    </div>

                    <div
                        class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse"
                    >
                        <button
                            type="submit"
                            class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-indigo-600 text-base font-medium text-white hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:ml-3 sm:w-auto sm:text-sm"
                        >
                            {{ isEditing ? "Update Product" : "Add Product" }}
                        </button>
                        <button
                            type="button"
                            @click="onClose"
                            class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm"
                        >
                            Cancel
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script setup>
    import { ref, watch } from "vue";

    const props = defineProps({
        isOpen: {
            type: Boolean,
            required: true,
        },
        product: {
            type: Object,
            default: () => ({
                id: null,
                name: "",
                sku: "",
                category: "",
                subCategory: "",
                price: 0,
                salePrice: null,
                stock: 0,
                description: "",
                image: "/api/placeholder/100/100",
            }),
        },
        isEditing: {
            type: Boolean,
            default: false,
        },
    });

    const emit = defineEmits(["close", "save"]);

    const productData = ref({ ...props.product });

    watch(
        () => props.product,
        (newProduct) => {
            productData.value = { ...newProduct };
        },
        { deep: true }
    );

    const handleSubmit = () => {
        emit("save", productData.value);
    };

    const onClose = () => {
        emit("close");
    };
</script>
