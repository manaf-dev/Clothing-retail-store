<script setup></script>

<template>
    <div
        class="not-found flex flex-col items-center justify-center min-h-[80vh] text-center"
    >
        <span class="text-[5rem] mb-4 text-red-500">&#9888;</span>
        <h1 class="text-[4rem] mb-4 text-red-500">404</h1>
        <h2 class="text-2xl mb-2">Page Not Found</h2>
        <p class="mb-8 text-gray-500">
            The page you are looking for does not exist or has been moved.
        </p>
        <router-link
            to="/dashboard"
            class="px-8 py-3 bg-blue-500 text-white rounded font-bold transition-colors duration-200 hover:bg-blue-600"
        >
            Go back to Home
        </router-link>
    </div>
</template>
