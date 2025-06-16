import { apiClient } from "./api.js";

export class BaseRequests {
  static async get(url, params = {}) {
    try {
      const response = await apiClient.get(url, { params });
      return response.data;
    } catch (error) {
      console.error("API GET Error:", error);
      throw error;
    }
  }

  static async post(url, data = {}) {
    try {
      const response = await apiClient.post(url, data);
      return response.data;
    } catch (error) {
      console.error("API POST Error:", error);
      throw error;
    }
  }

  static async postFormData(url, formData) {
    try {
      const response = await apiClient.post(url, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      return response.data;
    } catch (error) {
      console.error("API POST FormData Error:", error);
      throw error;
    }
  }

  static async put(url, data = {}) {
    try {
      const response = await apiClient.put(url, data);
      return response.data;
    } catch (error) {
      console.error("API PUT Error:", error);
      throw error;
    }
  }

  static async putFormData(url, formData) {
    try {
      const response = await apiClient.put(url, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      return response.data;
    } catch (error) {
      console.error("API PUT FormData Error:", error);
      throw error;
    }
  }

  static async del(url) {
    try {
      const response = await apiClient.delete(url);
      return response.data;
    } catch (error) {
      console.error("API DELETE Error:", error);
      throw error;
    }
  }

  static async patch(url, data = {}) {
    try {
      const response = await apiClient.patch(url, data);
      return response.data;
    } catch (error) {
      console.error("API PATCH Error:", error);
      throw error;
    }
  }
}

