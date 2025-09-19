import { apiService, API_ENDPOINTS } from './api';

export const policyService = {
  // Get all policies
  getAllPolicies: async (params = {}) => {
    return await apiService.get(API_ENDPOINTS.POLICIES, params);
  },

  // Get policy by ID
  getPolicyById: async (id) => {
    return await apiService.get(API_ENDPOINTS.POLICY_BY_ID(id));
  },

  // Create new policy
  createPolicy: async (policyData) => {
    return await apiService.post(API_ENDPOINTS.POLICIES, policyData);
  },

  // Update policy
  updatePolicy: async (id, policyData) => {
    return await apiService.put(API_ENDPOINTS.POLICY_BY_ID(id), policyData);
  },

  // Delete policy
  deletePolicy: async (id) => {
    return await apiService.delete(API_ENDPOINTS.POLICY_BY_ID(id));
  },

  // Search policies
  searchPolicies: async (query, filters = {}) => {
    return await apiService.get(API_ENDPOINTS.POLICIES, {
      search: query,
      ...filters
    });
  },

  // Get policy statistics
  getPolicyStats: async () => {
    return await apiService.get(`${API_ENDPOINTS.POLICIES}/stats`);
  },

  // Approve policy
  approvePolicy: async (id, approvalData) => {
    return await apiService.patch(`${API_ENDPOINTS.POLICY_BY_ID(id)}/approve`, approvalData);
  },

  // Reject policy
  rejectPolicy: async (id, rejectionData) => {
    return await apiService.patch(`${API_ENDPOINTS.POLICY_BY_ID(id)}/reject`, rejectionData);
  },

  // Get policy versions
  getPolicyVersions: async (id) => {
    return await apiService.get(`${API_ENDPOINTS.POLICY_BY_ID(id)}/versions`);
  },

  // Upload policy document
  uploadPolicyDocument: async (id, file) => {
    const formData = new FormData();
    formData.append('file', file);
    
    return await apiService.post(`${API_ENDPOINTS.POLICY_BY_ID(id)}/upload`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
};
