<script setup>
    import Sidebar from "./Sidebar.vue";
    import Topbar from "./Topbar.vue";
</script>

<template>
    <div class="flex h-screen bg-gray-100">
        <Sidebar />

        <div class="flex-1 flex flex-col overflow-hidden">
            <Topbar />

            <main class="flex-1 overflow-y-auto bg-gray-100 p-6">
                <slot></slot>
            </main>
        </div>
    </div>
</template>
