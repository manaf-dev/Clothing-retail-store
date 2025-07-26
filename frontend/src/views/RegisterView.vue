<template>
  <div class="flex items-center justify-center min-h-screen bg-gray-100">
    <form
      @submit.prevent="handleRegister"
      class="bg-white p-8 rounded shadow w-96"
    >
      <h2 class="text-2xl font-bold mb-6 text-center">Register</h2>
      <div class="mb-4">
        <label class="block mb-1">Username</label>
        <input
          v-model="username"
          type="text"
          class="w-full border rounded px-3 py-2"
          required
        />
      </div>
      <div class="mb-4">
        <label class="block mb-1">Email</label>
        <input
          v-model="email"
          type="email"
          class="w-full border rounded px-3 py-2"
          required
        />
      </div>
      <div class="mb-4">
        <label class="block mb-1">Password</label>
        <input
          v-model="password"
          type="password"
          class="w-full border rounded px-3 py-2"
          required
        />
      </div>
      <div class="mb-6">
        <label class="block mb-1">Confirm Password</label>
        <input
          v-model="password2"
          type="password"
          class="w-full border rounded px-3 py-2"
          required
        />
      </div>
      <button
        type="submit"
        class="w-full bg-green-600 text-white py-2 rounded hover:bg-green-700"
      >
        Register
      </button>
      <div v-if="error" class="mt-4 text-red-600 text-center">{{ error }}</div>
      <div v-if="success" class="mt-4 text-green-600 text-center">
        {{ success }}
      </div>
    </form>
  </div>
</template>

<script setup>
  import { ref } from "vue";
  import { useRouter } from "vue-router";
  import { useAuthStore } from "../stores/auth";

  const username = ref("");
  const email = ref("");
  const password = ref("");
  const password2 = ref("");
  const error = ref("");
  const success = ref("");
  const router = useRouter();
  const auth = useAuthStore();

  const handleRegister = async () => {
    error.value = "";
    success.value = "";
    try {
      await auth.registerUser({
        username: username.value,
        email: email.value,
        password: password.value,
        password2: password2.value,
      });
      success.value = "Registration successful! You can now log in.";
      setTimeout(() => router.push("/login"), 1500);
    } catch (e) {
      error.value =
        e.response?.data?.password ||
        e.response?.data?.detail ||
        "Registration failed.";
    }
  };
</script>
