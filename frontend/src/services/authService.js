import { apiClient } from "./api";

export const register = (data) =>
  apiClient.post("/auth/register/", data);

export const login = (data) =>
  apiClient.post("/auth/login/", data);

export const refreshToken = (data) =>
  apiClient.post("/auth/token/refresh/", data);

export const logout = (data) =>
  apiClient.post("/auth/logout/", data);

export const getCurrentUser = () =>
  apiClient.get("/auth/profile/");
