import { apiService, API_ENDPOINTS } from './api';

export const policyService = {
  // Get all policies
  getAllPolicies: async (params = {}) => {
    return await apiService.get(API_ENDPOINTS.POLICIES.BASE, params);
  },

  // Get policy by ID
  getPolicyById: async (id) => {
    return await apiService.get(API_ENDPOINTS.POLICIES.BY_ID(id));
  },

  // Create new policy
  createPolicy: async (policyData) => {
    return await apiService.post(API_ENDPOINTS.POLICIES.BASE, policyData);
  },

  // Update policy
  updatePolicy: async (id, policyData) => {
    return await apiService.put(API_ENDPOINTS.POLICIES.BY_ID(id), policyData);
  },

  // Delete policy
  deletePolicy: async (id) => {
    return await apiService.delete(API_ENDPOINTS.POLICIES.BY_ID(id));
  },

  // Search policies
  searchPolicies: async (query, filters = {}) => {
    return await apiService.get(API_ENDPOINTS.POLICIES.SEARCH, {
      search: query,
      ...filters
    });
  },

  // Get policy statistics
  getPolicyStats: async () => {
    return await apiService.get(API_ENDPOINTS.POLICIES.STATS);
  },

  // Approve policy
  approvePolicy: async (id, approvalData) => {
    return await apiService.patch(API_ENDPOINTS.POLICIES.APPROVE(id), approvalData);
  },

  // Reject policy
  rejectPolicy: async (id, rejectionData) => {
    return await apiService.patch(API_ENDPOINTS.POLICIES.REJECT(id), rejectionData);
  },

  // Get policy versions
  getPolicyVersions: async (id) => {
    return await apiService.get(API_ENDPOINTS.POLICIES.VERSIONS(id));
  },

  // Upload policy document
  uploadPolicyDocument: async (id, file) => {
    const formData = new FormData();
    formData.append('file', file);
    
    return await apiService.post(API_ENDPOINTS.POLICIES.UPLOAD(id), formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
};
