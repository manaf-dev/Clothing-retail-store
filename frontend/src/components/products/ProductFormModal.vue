<script setup>
import { ProductService } from "@/services/productService.js";
import { onMounted, ref, watch } from "vue";

const props = defineProps({
    isOpen: {
        type: Boolean,
        required: true,
    },
    product: {
        type: Object,
        default: () => ({
            name: "",
            category: "",
            price: 0,
            sale_price: null,
            stock: 0,
            min_stock: 0,
            description: "",
        }),
    },
    isEditing: {
        type: Boolean,
        default: false,
    },
});

const emit = defineEmits(["close", "save"]);

const categories = ref([]);
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

onMounted(async () => {
    try {
        const response = await ProductService.getCategories();
        categories.value = response;
    } catch (error) {
        console.error("Failed to fetch categories:", error);
    }
});
</script>


<template>
    <div v-if="isOpen" class="fixed inset-0 z-50 flex items-center justify-center">
        <!-- Overlay -->
        <div class="fixed inset-0 bg-black/40 transition-opacity z-40"></div>

        <!-- Modal Content -->
        <div
            class="relative z-50 inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full"
        >
                <form @submit.prevent="handleSubmit">
                    <div class="bg-white px-6 pt-8 pb-6 sm:p-8 sm:pb-6">
                        <div class="mb-6">
                            <h3 class="text-xl leading-7 font-semibold text-gray-900">
                                {{ isEditing ? "Edit Product" : "Add New Product" }}
                            </h3>
                        </div>

                        <div class="grid grid-cols-1 gap-y-4 gap-x-6 sm:grid-cols-6">
                            <!-- Product Name -->
                            <div class="sm:col-span-6">
                                <label
                                    for="product-name"
                                    class="block text-base font-medium text-gray-700"
                                    >Product Name</label
                                >
                                <input
                                    type="text"
                                    id="product-name"
                                    v-model="productData.name"
                                    required
                                    class="mt-2 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm text-base border-gray-300 rounded-lg px-4 py-3"
                                />
                            </div>

                            <!-- Category -->
                            <div class="sm:col-span-3">
                                <label
                                    for="product-category"
                                    class="block text-base font-medium text-gray-700"
                                    >Category</label
                                >
                                <select
                                    id="product-category"
                                    v-model="productData.category"
                                    required
                                    class="mt-2 block w-full py-3 px-4 capitalize border border-gray-300 bg-white rounded-lg shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 text-base"
                                >
                                    <option v-if="isEditing" value="" :selected="isEditing">Select Category</option>
                                    <option v-for="category in categories" :key="category.id" :value="category.id">{{category.name}}</option>
                                    
                                </select>
                            </div>                            

                            <!-- Price -->
                            <div class="sm:col-span-3">
                                <label
                                    for="product-price"
                                    class="block text-base font-medium text-gray-700"
                                    >Price (₵)</label
                                >
                                <input
                                    type="number"
                                    id="product-price"
                                    v-model="productData.price"
                                    required
                                    min="0"
                                    step="0.01"
                                    class="mt-2 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm text-base border-gray-300 rounded-lg px-4 py-3"
                                />
                            </div>

                            <!-- Sale Price -->
                            <div class="sm:col-span-3">
                                <label
                                    for="product-sale-price"
                                    class="block text-base font-medium text-gray-700"
                                    >Sale Price (₵)</label
                                >
                                <input
                                    type="number"
                                    id="product-sale-price"
                                    v-model="productData.sale_price"
                                    min="0"
                                    step="0.01"
                                    class="mt-2 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm text-base border-gray-300 rounded-lg px-4 py-3"
                                />
                                <p class="mt-1 text-sm text-gray-500">
                                    Leave empty if not on sale
                                </p>
                            </div>

                            <!-- Stock -->
                            <div class="sm:col-span-3">
                                <label
                                    for="product-stock"
                                    class="block text-base font-medium text-gray-700"
                                    >Stock Quantity</label
                                >
                                <input
                                    type="number"
                                    id="product-stock"
                                    v-model="productData.stock"
                                    required
                                    min="0"
                                    class="mt-2 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm text-base border-gray-300 rounded-lg px-4 py-3"
                                />
                            </div>

                            <!-- Min Stock-->
                            <div class="sm:col-span-3">
                                <label
                                    for="product-min-stock"
                                    class="block text-base font-medium text-gray-700"
                                    >Minimum Stock Level</label
                                >
                                <input
                                    type="number"
                                    id="product-min-stock"
                                    v-model="productData.min_stock"
                                    required
                                    min="0"
                                    class="mt-2 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm text-base border-gray-300 rounded-lg px-4 py-3"
                                />
                                <p class="mt-1 text-sm text-gray-500">
                                    Set a minimum stock level for alerts
                                </p>
                            </div>

                            <!-- Description -->
                            <div class="sm:col-span-6">
                                <label
                                    for="product-description"
                                    class="block text-base font-medium text-gray-700"
                                    >Description</label
                                >
                                <textarea
                                    id="product-description"
                                    v-model="productData.description"
                                    rows="4"
                                    class="mt-2 focus:ring-indigo-500 focus:border-indigo-500 block w-full shadow-sm text-base border-gray-300 rounded-lg px-4 py-3"
                                ></textarea>
                            </div>
                        </div>
                    </div>

                    <div class="bg-gray-50 px-6 py-4 sm:px-8 sm:flex sm:flex-row-reverse">
                        <button
                            type="submit"
                            class="w-full inline-flex justify-center rounded-lg border border-transparent shadow-sm px-6 py-3 bg-indigo-600 text-lg font-medium text-white hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:ml-3 sm:w-auto sm:text-base"
                        >
                            {{ isEditing ? "Update Product" : "Add Product" }}
                        </button>
                        <button
                            type="button"
                            @click="onClose"
                            class="mt-3 w-full inline-flex justify-center rounded-lg border border-gray-300 shadow-sm px-6 py-3 bg-white text-lg font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:mt-0 sm:ml-3 sm:w-auto sm:text-base"
                        >
                            Cancel
                        </button>
                    </div>
                </form>
        </div>

    </div>
</template>


