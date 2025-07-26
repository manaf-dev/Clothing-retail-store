<template>
  <DashboardLayout>
    <div class="p-6">
      <h1 class="text-2xl font-bold mb-6">My Profile</h1>
      <UserProfile />
    </div>
  </DashboardLayout>
</template>

<script setup>
  import DashboardLayout from "@/components/layouts/DashboardLayout.vue";
  import UserProfile from "@/components/UserProfile.vue";
</script>
