<script setup>
import { ref, computed } from "vue";
import { useAuthStore } from "../../stores/auth";
import { useRouter } from "vue-router";

const isUserMenuOpen = ref(false);
const auth = useAuthStore();
const router = useRouter();

const userName = computed(() => {
  if (auth.user.value) {
    const fullName = `${auth.user.value.first_name || ''} ${auth.user.value.last_name || ''}`.trim();
    return fullName || auth.user.value.username;
  }
  return 'User';
});

const userRole = computed(() => {
  return auth.user.value?.staff_profile?.role || 'Staff';
});

const userProfileImage = computed(() => {
  const profileImage = auth.user.value?.staff_profile?.profile_image;
  if (profileImage) {
    // If it's a relative path, prepend the API base URL
    if (profileImage.startsWith('/')) {
      return `http://localhost:8000${profileImage}`;
    }
    // If it's already a full URL, use as is
    return profileImage;
  }
  return null;
});

const userInitials = computed(() => {
  const user = auth.user.value;
  if (user?.first_name && user?.last_name) {
    return `${user.first_name.charAt(0)}${user.last_name.charAt(0)}`.toUpperCase();
  }
  return user?.username?.charAt(0)?.toUpperCase() || 'U';
});

const handleLogout = async () => {
  try {
    await auth.logoutUser();
    router.push('/login');
  } catch (error) {
    console.error('Logout error:', error);
    router.push('/login');
  }
};
</script>


<template>
    <header class="bg-white shadow">
        <div class="flex items-center justify-between px-6 py-4">
            <div class="flex items-center">
                <input
                    class="bg-gray-100 rounded-lg px-4 py-2 w-64 text-sm focus:outline-none"
                    type="search"
                    placeholder="Search..."
                />
            </div>

            <div class="flex items-center space-x-4">
                <!-- Notifications -->
                <!-- <button
                    class="text-gray-500 hover:text-gray-700 focus:outline-none"
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
                            d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"
                        />
                    </svg>
                </button> -->

                <!-- User dropdown -->
                <div class="relative" ref="userMenuContainer">
                    <button
                        @click="isUserMenuOpen = !isUserMenuOpen"
                        class="flex items-center focus:outline-none"
                    >
                        <div class="relative">
                            <img
                                v-if="userProfileImage"
                                :src="userProfileImage"
                                class="h-8 w-8 rounded-full object-cover border"
                                alt="User avatar"
                                @error="$event.target.style.display = 'none'"
                            />
                            <div
                                v-if="!userProfileImage"
                                class="h-8 w-8 rounded-full bg-gray-400 flex items-center justify-center text-white text-sm font-semibold"
                            >
                                {{ userInitials }}
                            </div>
                        </div>

                        <span class="ml-2 text-sm font-medium text-gray-700">{{ userName }}</span>
                        <span class="ml-1 text-xs text-gray-500 capitalize">{{ userRole }}</span>
                        <svg
                            class="ml-1 h-5 w-5 text-gray-400"
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke="currentColor"
                        >
                            <path
                                stroke-linecap="round"
                                stroke-linejoin="round"
                                stroke-width="2"
                                d="M19 9l-7 7-7-7"
                            />
                        </svg>
                    </button>

                    <div
                        v-if="isUserMenuOpen"
                        class="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg py-1 z-10"
                    >
                        <router-link
                            to="/profile"
                            class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                            @click="isUserMenuOpen = false"
                        >
                            Your Profile
                        </router-link>

                        <button
                            @click="handleLogout"
                            class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                        >
                            Sign out
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </header>
</template>
