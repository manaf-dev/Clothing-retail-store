<!-- Deprecated: OrdersView merged into SalesView. Route now redirects to /sales. -->
<script setup>
  import DashboardLayout from "@/components/layouts/DashboardLayout.vue";
  // Keeping component for backward compatibility during transition.
  import Sales from "@/components/sales/Sales.vue";
</script>

<template>
  <DashboardLayout>
    <Sales />
  </DashboardLayout>
</template>
