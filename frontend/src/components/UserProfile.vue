<template>
  <div class="bg-white rounded-lg shadow p-6">
    <h2 class="text-lg font-medium text-gray-900 mb-4">Profile Information</h2>
    <form @submit.prevent="updateProfile" enctype="multipart/form-data">
      <div class="flex items-center mb-6 space-x-6">
        <div class="relative">
          <img
            v-if="previewImage || profileImageUrl"
            :src="previewImage || profileImageUrl"
            class="h-24 w-24 rounded-full object-cover border"
            alt="Profile"
            @error="handleImageError"
          />
          <div v-else class="h-24 w-24 rounded-full bg-gray-100 flex items-center justify-center text-gray-400 text-xl font-semibold border">
            {{ user?.username?.charAt(0)?.toUpperCase() || 'U' }}
          </div>
          <label class="absolute bottom-0 right-0 bg-blue-600 hover:bg-blue-700 text-white rounded-full p-2 cursor-pointer shadow">
            <input type="file" class="hidden" accept="image/*" @change="onFileChange" />
            <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536M9 13l6.768-6.768a2.5 2.5 0 113.536 3.536L12.536 16.536a2.5 2.5 0 01-1.768.732H8v-2.768a2.5 2.5 0 01.732-1.768z" />
            </svg>
          </label>
        </div>
        <div>
          <p class="text-sm text-gray-500">Upload a profile picture (optional)</p>
          <p v-if="imageError" class="text-xs text-red-600 mt-1">{{ imageError }}</p>
        </div>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700">Username</label>
          <input
            v-model="form.username"
            type="text"
            class="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700"
            >First Name</label
          >
          <input
            v-model="form.first_name"
            type="text"
            class="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700"
            >Last Name</label
          >
          <input
            v-model="form.last_name"
            type="text"
            class="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700">Email</label>
          <input
            v-model="form.email"
            type="email"
            class="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
          />
        </div>
      </div>
      <div class="mt-6">
        <button
          type="submit"
          :disabled="loading"
          class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:opacity-50"
        >
          {{ loading ? "Updating..." : "Update Profile" }}
        </button>
      </div>
    </form>
    <div
      v-if="message"
      class="mt-4 p-3 rounded"
      :class="
        messageType === 'success'
          ? 'bg-green-100 text-green-700'
          : 'bg-red-100 text-red-700'
      "
    >
      {{ message }}
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from "vue";
import { useAuthStore } from "@/stores/auth";
import { apiClient } from "@/services/api";

const auth = useAuthStore();
const loading = ref(false);
const message = ref("");
const messageType = ref("");
const imageFile = ref(null);
const previewImage = ref(null);
const imageError = ref("");

const user = computed(() => auth.user.value || {});

// Get the full URL for profile image
const profileImageUrl = computed(() => {
  const imagePath = user.value?.staff_profile?.profile_image;
  if (!imagePath) return null;
  
  // If it's already a full URL, return as is
  if (imagePath.startsWith('http')) return imagePath;
  
  // Otherwise, construct the full URL
  const baseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
  return `${baseUrl}${imagePath}`;
});

const form = ref({
  username: "",
  first_name: "",
  last_name: "",
  email: "",
});

const onFileChange = (e) => {
  const file = e.target.files[0];
  if (!file) return;
  if (!file.type.startsWith("image/")) {
    imageError.value = "Please select a valid image file.";
    return;
  }
  if (file.size > 2 * 1024 * 1024) {
    imageError.value = "Image must be less than 2MB.";
    return;
  }
  imageError.value = "";
  imageFile.value = file;
  previewImage.value = URL.createObjectURL(file);
};

const handleImageError = (event) => {
  console.warn('Profile image failed to load:', event.target.src);
  event.target.style.display = 'none';
};

const updateProfile = async () => {
  try {
    loading.value = true;
    message.value = "";
    const data = new FormData();
    Object.keys(form.value).forEach((k) => data.append(k, form.value[k] || ""));
    if (imageFile.value) {
      data.append("profile_image", imageFile.value);
    }
    
    const response = await apiClient.put("/auth/profile/update/", data, {
      headers: { "Content-Type": "multipart/form-data" },
    });
    
    // Force refresh user data from server
    await auth.loadUser(true);
    
    // Clear the preview image so the new image from server is shown
    if (imageFile.value) {
      imageFile.value = null;
      previewImage.value = null;
      // Reset file input
      const fileInput = document.querySelector('input[type="file"]');
      if (fileInput) fileInput.value = '';
    }
    
    // Update form with fresh data
    const updatedUser = auth.user.value;
    if (updatedUser) {
      form.value = {
        username: updatedUser.username || "",
        first_name: updatedUser.first_name || "",
        last_name: updatedUser.last_name || "",
        email: updatedUser.email || "",
      };
    }
    
    message.value = "Profile updated successfully!";
    messageType.value = "success";
  } catch (error) {
    message.value =
      error.response?.data?.detail || "Failed to update profile. Please try again.";
    messageType.value = "error";
    console.error("Profile update error:", error);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  if (user.value) {
    form.value = {
      username: user.value.username || "",
      first_name: user.value.first_name || "",
      last_name: user.value.last_name || "",
      email: user.value.email || "",
    };
  }
});
</script>
