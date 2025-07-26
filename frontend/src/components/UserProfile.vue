<template>
  <div class="bg-white rounded-lg shadow p-6">
    <h2 class="text-lg font-medium text-gray-900 mb-4">Profile Information</h2>
    <form @submit.prevent="updateProfile">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
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
        <div>
          <label class="block text-sm font-medium text-gray-700"
            >Username</label
          >
          <input
            v-model="user.username"
            type="text"
            disabled
            class="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 bg-gray-100 text-gray-500"
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
  import { ref, computed, onMounted } from "vue";
  import { useAuthStore } from "@/stores/auth";
  import { apiClient } from "@/services/api";

  const auth = useAuthStore();
  const loading = ref(false);
  const message = ref("");
  const messageType = ref("");

  const user = computed(() => auth.user.value || {});

  const form = ref({
    first_name: "",
    last_name: "",
    email: "",
  });

  const updateProfile = async () => {
    try {
      loading.value = true;
      message.value = "";

      await apiClient.put("/auth/profile/update/", form.value);

      // Reload user data
      await auth.loadUser();

      message.value = "Profile updated successfully!";
      messageType.value = "success";
    } catch (error) {
      message.value = "Failed to update profile. Please try again.";
      messageType.value = "error";
      console.error("Profile update error:", error);
    } finally {
      loading.value = false;
    }
  };

  onMounted(() => {
    if (user.value) {
      form.value = {
        first_name: user.value.first_name || "",
        last_name: user.value.last_name || "",
        email: user.value.email || "",
      };
    }
  });
</script>
