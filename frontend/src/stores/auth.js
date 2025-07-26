import { ref } from "vue";
import { login, register, logout, refreshToken, getCurrentUser } from "../services/authService";

const accessToken = ref(localStorage.getItem("accessToken") || "");
const refreshTokenValue = ref(localStorage.getItem("refreshToken") || "");
const user = ref(null);
const isAuthenticated = ref(!!accessToken.value);

export const useAuthStore = () => {
  const setTokens = (access, refresh) => {
    accessToken.value = access;
    refreshTokenValue.value = refresh;
    localStorage.setItem("accessToken", access);
    localStorage.setItem("refreshToken", refresh);
    isAuthenticated.value = true;
  };

  const clearTokens = () => {
    accessToken.value = "";
    refreshTokenValue.value = "";
    localStorage.removeItem("accessToken");
    localStorage.removeItem("refreshToken");
    isAuthenticated.value = false;
    user.value = null;
  };

  const loadUser = async () => {
    if (accessToken.value && !user.value) {
      try {
        const res = await getCurrentUser();
        user.value = res.data;
        localStorage.setItem("user", JSON.stringify(res.data));
      } catch (error) {
        console.error("Failed to load user:", error);
        clearTokens();
      }
    }
  };

  const loginUser = async (credentials) => {
    const res = await login(credentials);
    setTokens(res.data.access, res.data.refresh);
    await loadUser();
    return res;
  };

  const registerUser = async (data) => {
    return await register(data);
  };

  const logoutUser = async () => {
    try {
      await logout({ refresh: refreshTokenValue.value });
    } catch (error) {
      console.error("Logout error:", error);
    } finally {
      clearTokens();
    }
  };

  const refreshUserToken = async () => {
    const res = await refreshToken({ refresh: refreshTokenValue.value });
    setTokens(res.data.access, refreshTokenValue.value);
    return res;
  };

  // Initialize user on store creation
  if (accessToken.value && !user.value) {
    loadUser();
  }

  return {
    accessToken,
    refreshToken: refreshTokenValue,
    user,
    isAuthenticated,
    loginUser,
    registerUser,
    logoutUser,
    refreshUserToken,
    loadUser,
    setTokens,
    clearTokens,
  };
};
