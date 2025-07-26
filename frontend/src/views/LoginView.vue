<template>
  <div class="flex items-center justify-center min-h-screen bg-gray-100">
    <form
      @submit.prevent="handleLogin"
      class="bg-white p-8 rounded shadow w-96"
    >
      <h2 class="text-2xl font-bold mb-6 text-center">Login</h2>
      <div class="mb-4">
        <label class="block mb-1">Username</label>
        <input
          v-model="username"
          type="text"
          class="w-full border rounded px-3 py-2"
          required
        />
      </div>
      <div class="mb-6">
        <label class="block mb-1">Password</label>
        <input
          v-model="password"
          type="password"
          class="w-full border rounded px-3 py-2"
          required
        />
      </div>
      <button
        type="submit"
        class="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700"
      >
        Login
      </button>
      <div v-if="error" class="mt-4 text-red-600 text-center">{{ error }}</div>
    </form>
  </div>
</template>

<script setup>
  import { ref } from "vue";
  import { useRouter } from "vue-router";
  import { useAuthStore } from "../stores/auth";

  const username = ref("");
  const password = ref("");
  const error = ref("");
  const router = useRouter();
  const auth = useAuthStore();

  const handleLogin = async () => {
    error.value = "";
    try {
      await auth.loginUser({
        username: username.value,
        password: password.value,
      });
      router.push("/");
    } catch (e) {
      error.value =
        e.response?.data?.detail ||
        "Login failed. Please check your credentials.";
    }
  };
</script>
