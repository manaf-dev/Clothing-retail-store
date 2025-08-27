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
            image: null,
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
const selectedFile = ref(null);
const imagePreview = ref(null);
const isDragOver = ref(false);
const fileInputRef = ref(null);

watch(
    () => props.product,
    (newProduct) => {
        productData.value = { ...newProduct };
        // Set image preview for existing product
        if (newProduct.image) {
            imagePreview.value = newProduct.image;
        } else {
            imagePreview.value = null;
        }
        selectedFile.value = null;
    },
    { deep: true }
);

const validateAndProcessFile = (file) => {
    // Validate file type
    if (!file.type.startsWith('image/')) {
        alert('Please select an image file (JPG, PNG, GIF, etc.)');
        return false;
    }
    
    // Validate file size (5MB limit)
    if (file.size > 5 * 1024 * 1024) {
        alert('Image size must be less than 5MB');
        return false;
    }
    
    selectedFile.value = file;
    
    // Create preview
    const reader = new FileReader();
    reader.onload = (e) => {
        imagePreview.value = e.target.result;
    };
    reader.readAsDataURL(file);
    return true;
};

const handleFileSelect = (event) => {
    const file = event.target.files[0];
    if (file) {
        validateAndProcessFile(file);
    }
};

// Drag and drop handlers
const handleDragOver = (event) => {
    event.preventDefault();
    event.stopPropagation();
    isDragOver.value = true;
};

const handleDragLeave = (event) => {
    event.preventDefault();
    event.stopPropagation();
    isDragOver.value = false;
};

const handleDrop = (event) => {
    event.preventDefault();
    event.stopPropagation();
    isDragOver.value = false;
    
    const files = event.dataTransfer.files;
    if (files.length > 0) {
        validateAndProcessFile(files[0]);
    }
};

// const triggerFileInput = () => {
//     if (fileInputRef.value) {
//         fileInputRef.value.click();
//     }
// };

const removeImage = () => {
    selectedFile.value = null;
    imagePreview.value = null;
    productData.value.image = null;
    // Clear the file input
    if (fileInputRef.value) {
        fileInputRef.value.value = '';
    }
};

const handleSubmit = () => {
    // Include the selected file in the data
    const submitData = {
        ...productData.value,
        imageFile: selectedFile.value
    };
    emit("save", submitData);
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
    <div v-if="isOpen" class="fixed inset-0 z-50 overflow-y-auto">
        <!-- Backdrop with blur -->
        <div class="fixed inset-0 bg-white/20 backdrop-blur-sm transition-all duration-300"></div>
        
        <!-- Modal Container -->
        <div class="flex min-h-full items-center justify-center p-4 sm:p-6">
            <div class="relative bg-white rounded-xl shadow-2xl w-full max-w-4xl max-h-[95vh] overflow-hidden">
                <!-- Header -->
                <div class="flex items-center justify-between p-4 sm:p-6 border-b border-gray-200 bg-gradient-to-r from-indigo-500 to-indigo-600">
                    <h2 class="text-lg sm:text-xl font-bold text-white">
                        {{ isEditing ? "Edit Product" : "Add New Product" }}
                    </h2>
                    <button
                        @click="onClose"
                        class="text-white hover:text-gray-200 transition-colors p-1"
                    >
                        <svg class="w-5 h-5 sm:w-6 sm:h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                        </svg>
                    </button>
                </div>

                <!-- Form Content -->
                <form @submit.prevent="handleSubmit" class="flex flex-col max-h-[calc(95vh-80px)]">
                    <div class="flex-1 overflow-y-auto p-4 sm:p-6">
                        <div class="grid grid-cols-1 lg:grid-cols-3 gap-4 sm:gap-6">
                            <!-- Left Column - Basic Information -->
                            <div class="lg:col-span-2 space-y-3 sm:space-y-4">
                            <!-- Product Name -->
                            <div>
                                <label for="product-name" class="block text-sm font-medium text-gray-700 mb-1">
                                    Product Name *
                                </label>
                                <input
                                    type="text"
                                    id="product-name"
                                    v-model="productData.name"
                                    required
                                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-colors"
                                    placeholder="Enter product name"
                                />
                            </div>

                            <!-- Category and Price Row -->
                            <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 sm:gap-4">
                                <div>
                                    <label for="product-category" class="block text-sm font-medium text-gray-700 mb-1">
                                        Category *
                                    </label>
                                    <select
                                        id="product-category"
                                        v-model="productData.category"
                                        required
                                        class="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-colors"
                                    >
                                        <option value="">Select Category</option>
                                        <option v-for="category in categories" :key="category.id" :value="category.id">
                                            {{ category.name }}
                                        </option>
                                    </select>
                                </div>
                                <div>
                                    <label for="product-price" class="block text-sm font-medium text-gray-700 mb-1">
                                        Price (₵) *
                                    </label>
                                    <input
                                        type="number"
                                        id="product-price"
                                        v-model="productData.price"
                                        required
                                        min="0"
                                        step="0.01"
                                        class="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-colors"
                                        placeholder="0.00"
                                    />
                                </div>
                            </div>

                            <!-- Sale Price and Stock Row -->
                            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                                <div>
                                    <label for="product-sale-price" class="block text-sm font-medium text-gray-700 mb-1">
                                        Sale Price (₵)
                                    </label>
                                    <input
                                        type="number"
                                        id="product-sale-price"
                                        v-model="productData.sale_price"
                                        min="0"
                                        step="0.01"
                                        class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-colors"
                                        placeholder="Optional"
                                    />
                                </div>
                                <div>
                                    <label for="product-stock" class="block text-sm font-medium text-gray-700 mb-1">
                                        Stock Quantity *
                                    </label>
                                    <input
                                        type="number"
                                        id="product-stock"
                                        v-model="productData.stock"
                                        required
                                        min="0"
                                        class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-colors"
                                        placeholder="0"
                                    />
                                </div>
                                <div>
                                    <label for="product-min-stock" class="block text-sm font-medium text-gray-700 mb-1">
                                        Min Stock Level *
                                    </label>
                                    <input
                                        type="number"
                                        id="product-min-stock"
                                        v-model="productData.min_stock"
                                        required
                                        min="0"
                                        class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-colors"
                                        placeholder="0"
                                    />
                                </div>
                            </div>

                            <!-- Description -->
                            <div>
                                <label for="product-description" class="block text-sm font-medium text-gray-700 mb-1">
                                    Description
                                </label>
                                <textarea
                                    id="product-description"
                                    v-model="productData.description"
                                    rows="3"
                                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-colors resize-none"
                                    placeholder="Enter product description..."
                                ></textarea>
                            </div>
                        </div>

                        <!-- Right Column - Image Upload -->
                        <div class="lg:col-span-1">
                            <label class="block text-sm font-medium text-gray-700 mb-1">
                                Product Image
                            </label>
                            
                            <!-- Image Upload Area -->
                            <div class="relative">
                                <!-- Image Preview -->
                                <div 
                                    v-if="imagePreview"
                                    class="relative mb-4 group"
                                >
                                    <img 
                                        :src="imagePreview" 
                                        alt="Product preview" 
                                        class="w-full h-48 object-cover rounded-lg border-2 border-gray-200"
                                    />
                                    <!-- Delete button - positioned in top-right corner -->
                                    <button
                                        type="button"
                                        @click="removeImage"
                                        class="absolute top-2 right-2 opacity-0 group-hover:opacity-100 bg-red-500 text-white rounded-full p-2 hover:bg-red-600 transition-all duration-200 shadow-lg"
                                    >
                                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                                        </svg>
                                    </button>
                                </div>

                                <!-- Upload Area -->
                                <div 
                                    @dragover="handleDragOver"
                                    @dragleave="handleDragLeave"
                                    @drop="handleDrop"
                                    :class="[
                                        'relative border-2 border-dashed rounded-lg p-6 cursor-pointer transition-all duration-200',
                                        isDragOver 
                                            ? 'border-indigo-500 bg-indigo-50' 
                                            : 'border-gray-300 hover:border-gray-400 hover:bg-gray-50'
                                    ]"
                                >
                                    <div class="text-center">
                                        <div class="mx-auto w-12 h-12 text-gray-400 mb-3">
                                            <svg fill="none" stroke="currentColor" viewBox="0 0 48 48">
                                                <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" />
                                            </svg>
                                        </div>
                                        <p class="text-sm text-gray-600 mb-1">
                                            <span class="font-medium text-indigo-600">Click to upload</span> or drag and drop
                                        </p>
                                        <p class="text-xs text-gray-500">
                                            PNG, JPG, JPEG up to 5MB
                                        </p>
                                    </div>
                                    
                                    <!-- Hidden file input -->
                                    <input 
                                        ref="fileInputRef"
                                        type="file" 
                                        accept="image/*"
                                        @change="handleFileSelect"
                                        class="absolute inset-0 w-full h-full opacity-0 cursor-pointer" 
                                    />
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Footer -->
                <div class="flex items-center justify-end space-x-3 p-6 border-t border-gray-200 bg-gray-50">
                    <button
                        type="button"
                        @click="onClose"
                        class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-colors"
                    >
                        Cancel
                    </button>
                    <button
                        type="submit"
                        class="px-6 py-2 text-sm font-medium text-white bg-gradient-to-r from-indigo-500 to-indigo-600 rounded-lg hover:from-indigo-600 hover:to-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-all duration-200 transform hover:scale-105"
                    >
                        {{ isEditing ? "Update Product" : "Create Product" }}
                    </button>
                </div>
            </form>
        </div>
        </div>
    </div>
</template>


