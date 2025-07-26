import { apiClient } from "./api";

export const staffService = {
  // Get all staff
  getStaff(params = {}) {
    return apiClient.get("/staff/", { params });
  },

  // Get staff member by ID
  getStaffMember(id) {
    return apiClient.get(`/staff/${id}/`);
  },

  // Create new staff member
  createStaff(staffData) {
    return apiClient.post("/staff/", staffData);
  },

  // Update staff member
  updateStaff(id, staffData) {
    return apiClient.put(`/staff/${id}/`, staffData);
  },

  // Delete staff member
  deleteStaff(id) {
    return apiClient.delete(`/staff/${id}/`);
  },

  // Deactivate staff member
  deactivateStaff(id) {
    return apiClient.post(`/staff/${id}/deactivate/`);
  },

  // Activate staff member
  activateStaff(id) {
    return apiClient.post(`/staff/${id}/activate/`);
  },

  // Get available roles
  getRoles() {
    return apiClient.get("/staff/roles/");
  },
};
