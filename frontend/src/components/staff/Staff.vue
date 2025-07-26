<script setup>
  import { ref, onMounted, computed } from "vue";
  import { useAuthStore } from "@/stores/auth";
  import { staffService } from "@/services/staffService";

  const auth = useAuthStore();
  const staffList = ref([]);
  const roles = ref([]);
  const showCreateModal = ref(false);
  const editingStaff = ref(null);

  const canManageStaff = computed(() => {
    return (
      auth.user.value?.is_staff &&
      (auth.user.value?.staff_profile?.role === "admin" ||
        auth.user.value?.staff_profile?.role === "manager")
    );
  });

  const staffForm = ref({
    first_name: "",
    last_name: "",
    username: "",
    email: "",
    password: "",
    password2: "",
    is_staff: true,
    staff_profile: {
      role: "",
      employee_id: "",
      hire_date: "",
      phone: "",
      address: "",
      salary: null,
      is_active: true,
    },
  });

  const loadStaff = async () => {
    try {
      const response = await staffService.getStaff();
      staffList.value = response.data.results || response.data;
    } catch (error) {
      console.error("Error loading staff:", error);
    }
  };

  const loadRoles = async () => {
    try {
      const response = await staffService.getRoles();
      roles.value = response.data;
    } catch (error) {
      console.error("Error loading roles:", error);
    }
  };

  const getInitials = (name) => {
    return name
      .split(" ")
      .map((n) => n[0])
      .join("")
      .toUpperCase();
  };

  const formatDate = (dateString) => {
    if (!dateString) return "N/A";
    return new Date(dateString).toLocaleDateString();
  };

  const editStaff = (staff) => {
    editingStaff.value = staff;
    staffForm.value = {
      first_name: staff.first_name || "",
      last_name: staff.last_name || "",
      username: staff.username,
      email: staff.email,
      is_staff: staff.is_staff,
      staff_profile: {
        role: staff.staff_profile?.role || "",
        employee_id: staff.staff_profile?.employee_id || "",
        hire_date: staff.staff_profile?.hire_date || "",
        phone: staff.staff_profile?.phone || "",
        address: staff.staff_profile?.address || "",
        salary: staff.staff_profile?.salary || null,
        is_active: staff.staff_profile?.is_active ?? true,
      },
    };
  };

  const saveStaff = async () => {
    try {
      if (editingStaff.value) {
        await staffService.updateStaff(editingStaff.value.id, staffForm.value);
      } else {
        await staffService.createStaff(staffForm.value);
      }
      await loadStaff();
      closeModal();
    } catch (error) {
      console.error("Error saving staff:", error);
      alert("Error saving staff member. Please check the form and try again.");
    }
  };

  const deactivateStaff = async (id) => {
    if (confirm("Are you sure you want to deactivate this staff member?")) {
      try {
        await staffService.deactivateStaff(id);
        await loadStaff();
      } catch (error) {
        console.error("Error deactivating staff:", error);
      }
    }
  };

  const activateStaff = async (id) => {
    try {
      await staffService.activateStaff(id);
      await loadStaff();
    } catch (error) {
      console.error("Error activating staff:", error);
    }
  };

  const closeModal = () => {
    showCreateModal.value = false;
    editingStaff.value = null;
    staffForm.value = {
      first_name: "",
      last_name: "",
      username: "",
      email: "",
      password: "",
      password2: "",
      is_staff: true,
      staff_profile: {
        role: "",
        employee_id: "",
        hire_date: "",
        phone: "",
        address: "",
        salary: null,
        is_active: true,
      },
    };
  };

  onMounted(() => {
    loadStaff();
    loadRoles();
  });
</script>

<template>
  <div class="p-6">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold text-gray-900">Staff Management</h1>
      <button
        @click="showCreateModal = true"
        class="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700"
        v-if="canManageStaff"
      >
        Add Staff Member
      </button>
    </div>

    <!-- Staff List -->
    <div class="bg-white shadow rounded-lg">
      <div class="px-6 py-4 border-b border-gray-200">
        <h2 class="text-lg font-medium text-gray-900">Staff Directory</h2>
      </div>

      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                Employee
              </th>
              <th
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                Role
              </th>
              <th
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                Employee ID
              </th>
              <th
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                Hire Date
              </th>
              <th
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                Status
              </th>
              <th
                class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                v-if="canManageStaff"
              >
                Actions
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="staff in staffList" :key="staff.id">
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center">
                  <div class="h-10 w-10 flex-shrink-0">
                    <div
                      class="h-10 w-10 rounded-full bg-gray-300 flex items-center justify-center"
                    >
                      <span class="text-sm font-medium text-gray-700">
                        {{ getInitials(staff.full_name) }}
                      </span>
                    </div>
                  </div>
                  <div class="ml-4">
                    <div class="text-sm font-medium text-gray-900">
                      {{ staff.full_name }}
                    </div>
                    <div class="text-sm text-gray-500">{{ staff.email }}</div>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span
                  class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-blue-100 text-blue-800 capitalize"
                >
                  {{ staff.staff_profile?.role || "Staff" }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                {{ staff.staff_profile?.employee_id || "N/A" }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ formatDate(staff.staff_profile?.hire_date) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span
                  :class="
                    staff.is_active
                      ? 'bg-green-100 text-green-800'
                      : 'bg-red-100 text-red-800'
                  "
                  class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full"
                >
                  {{ staff.is_active ? "Active" : "Inactive" }}
                </span>
              </td>
              <td
                class="px-6 py-4 whitespace-nowrap text-sm font-medium"
                v-if="canManageStaff"
              >
                <button
                  @click="editStaff(staff)"
                  class="text-indigo-600 hover:text-indigo-900 mr-3"
                >
                  Edit
                </button>
                <button
                  @click="
                    staff.is_active
                      ? deactivateStaff(staff.id)
                      : activateStaff(staff.id)
                  "
                  :class="
                    staff.is_active
                      ? 'text-red-600 hover:text-red-900'
                      : 'text-green-600 hover:text-green-900'
                  "
                >
                  {{ staff.is_active ? "Deactivate" : "Activate" }}
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Create/Edit Modal -->
    <div
      v-if="showCreateModal || editingStaff"
      class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50"
    >
      <div
        class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white"
      >
        <div class="mt-3">
          <h3 class="text-lg font-medium text-gray-900 mb-4">
            {{ editingStaff ? "Edit Staff Member" : "Add New Staff Member" }}
          </h3>

          <form @submit.prevent="saveStaff" class="space-y-4">
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700"
                  >First Name</label
                >
                <input
                  v-model="staffForm.first_name"
                  type="text"
                  class="mt-1 block w-full border rounded-md px-3 py-2"
                  required
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700"
                  >Last Name</label
                >
                <input
                  v-model="staffForm.last_name"
                  type="text"
                  class="mt-1 block w-full border rounded-md px-3 py-2"
                  required
                />
              </div>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700"
                >Username</label
              >
              <input
                v-model="staffForm.username"
                type="text"
                class="mt-1 block w-full border rounded-md px-3 py-2"
                required
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700"
                >Email</label
              >
              <input
                v-model="staffForm.email"
                type="email"
                class="mt-1 block w-full border rounded-md px-3 py-2"
                required
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700"
                >Role</label
              >
              <select
                v-model="staffForm.staff_profile.role"
                class="mt-1 block w-full border rounded-md px-3 py-2"
                required
              >
                <option value="">Select Role</option>
                <option
                  v-for="role in roles"
                  :key="role.value"
                  :value="role.value"
                >
                  {{ role.label }}
                </option>
              </select>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700"
                >Employee ID</label
              >
              <input
                v-model="staffForm.staff_profile.employee_id"
                type="text"
                class="mt-1 block w-full border rounded-md px-3 py-2"
                required
              />
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700"
                >Hire Date</label
              >
              <input
                v-model="staffForm.staff_profile.hire_date"
                type="date"
                class="mt-1 block w-full border rounded-md px-3 py-2"
                required
              />
            </div>

            <div v-if="!editingStaff" class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700"
                  >Password</label
                >
                <input
                  v-model="staffForm.password"
                  type="password"
                  class="mt-1 block w-full border rounded-md px-3 py-2"
                  required
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700"
                  >Confirm Password</label
                >
                <input
                  v-model="staffForm.password2"
                  type="password"
                  class="mt-1 block w-full border rounded-md px-3 py-2"
                  required
                />
              </div>
            </div>

            <div class="flex justify-end space-x-3 pt-4">
              <button
                type="button"
                @click="closeModal"
                class="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-md hover:bg-gray-200"
              >
                Cancel
              </button>
              <button
                type="submit"
                class="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700"
              >
                {{ editingStaff ? "Update" : "Create" }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>
