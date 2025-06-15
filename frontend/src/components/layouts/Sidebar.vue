<script setup>
  import { ref } from "vue";

  const isSidebarOpen = ref(false);
</script>

<template>
  <aside class="bg-gray-800 text-white w-64 flex-shrink-0 hidden md:block">
    <div class="p-4 border-b border-gray-700">
      <h2 class="text-xl font-bold">Clothing Store</h2>
    </div>

    <nav class="mt-6">
      <div class="px-4 py-2 text-xs uppercase tracking-wider text-gray-400">
        Main
      </div>

      <router-link
        to="/dashboard"
        class="flex items-center px-4 py-3 text-gray-300 hover:bg-gray-700 hover:text-white"
        active-class="bg-gray-700 text-white"
      >
        <svg
          class="h-5 w-5 mr-3"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"
          />
        </svg>
        Dashboard
      </router-link>

      <router-link
        to="/pos"
        class="flex items-center px-4 py-3 text-gray-300 hover:bg-gray-700 hover:text-white"
        active-class="bg-gray-700 text-white"
      >
        <svg
          class="h-5 w-5 mr-3"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"
          />
        </svg>
        Point of Sale
      </router-link>

      <router-link
        to="/products"
        class="flex items-center px-4 py-3 text-gray-300 hover:bg-gray-700 hover:text-white"
        active-class="bg-gray-700 text-white"
      >
        <svg
          class="h-5 w-5 mr-3"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4"
          />
        </svg>
        Products
      </router-link>

      <router-link
        to="/sales"
        class="flex items-center px-4 py-3 text-gray-300 hover:bg-gray-700 hover:text-white"
        active-class="bg-gray-700 text-white"
      >
        <svg
          class="h-5 w-5 mr-3"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
          />
        </svg>
        Sales
      </router-link>

      <router-link
        to="/inventory"
        class="flex items-center px-4 py-3 text-gray-300 hover:bg-gray-700 hover:text-white"
        active-class="bg-gray-700 text-white"
      >
        <svg
          class="h-5 w-5 mr-3"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"
          />
        </svg>
        Inventory
      </router-link>

      <router-link
        to="/reports"
        class="flex items-center px-4 py-3 text-gray-300 hover:bg-gray-700 hover:text-white"
        active-class="bg-gray-700 text-white"
      >
        <svg
          class="h-5 w-5 mr-3"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
          />
        </svg>
        Reports
      </router-link>
    </nav>
  </aside>

  <!-- Mobile sidebar toggle -->
  <div class="md:hidden">
    <button
      @click="isSidebarOpen = !isSidebarOpen"
      class="p-4 text-gray-800 focus:outline-none"
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
          d="M4 6h16M4 12h16M4 18h16"
        />
      </svg>
    </button>

    <!-- Mobile sidebar -->
    <div v-if="isSidebarOpen" class="fixed inset-0 z-40 flex">
      <div
        @click="isSidebarOpen = false"
        class="fixed inset-0 bg-black opacity-50"
      ></div>

      <div class="relative flex-1 flex flex-col max-w-xs w-full bg-gray-800">
        <div class="absolute top-0 right-0 -mr-12 pt-2">
          <button
            @click="isSidebarOpen = false"
            class="ml-1 flex items-center justify-center h-10 w-10 rounded-full focus:outline-none focus:ring-2 focus:ring-inset focus:ring-white"
          >
            <span class="sr-only">Close sidebar</span>
            <svg
              class="h-6 w-6 text-white"
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

        <div class="p-4 border-b border-gray-700">
          <h2 class="text-xl font-bold text-white">Clothing Store</h2>
        </div>

        <!-- Mobile navigation -->
        <nav class="mt-6">
          <router-link
            to="/dashboard"
            @click="isSidebarOpen = false"
            class="flex items-center px-4 py-3 text-gray-300 hover:bg-gray-700 hover:text-white"
            active-class="bg-gray-700 text-white"
          >
            <svg
              class="h-5 w-5 mr-3"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"
              />
            </svg>
            Dashboard
          </router-link>

          <router-link
            to="/pos"
            @click="isSidebarOpen = false"
            class="flex items-center px-4 py-3 text-gray-300 hover:bg-gray-700 hover:text-white"
            active-class="bg-gray-700 text-white"
          >
            <svg
              class="h-5 w-5 mr-3"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"
              />
            </svg>
            Point of Sale
          </router-link>
        </nav>
      </div>
    </div>
  </div>
</template>
