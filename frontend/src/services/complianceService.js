import { apiService, API_ENDPOINTS } from './api';

export const complianceService = {
  // Get all compliance items
  getAllComplianceItems: async (params = {}) => {
    return await apiService.get(API_ENDPOINTS.COMPLIANCE, params);
  },

  // Get compliance item by ID
  getComplianceItemById: async (id) => {
    return await apiService.get(API_ENDPOINTS.COMPLIANCE_BY_ID(id));
  },

  // Create new compliance item
  createComplianceItem: async (complianceData) => {
    return await apiService.post(API_ENDPOINTS.COMPLIANCE, complianceData);
  },

  // Update compliance item
  updateComplianceItem: async (id, complianceData) => {
    return await apiService.put(API_ENDPOINTS.COMPLIANCE_BY_ID(id), complianceData);
  },

  // Delete compliance item
  deleteComplianceItem: async (id) => {
    return await apiService.delete(API_ENDPOINTS.COMPLIANCE_BY_ID(id));
  },

  // Search compliance items
  searchComplianceItems: async (query, filters = {}) => {
    return await apiService.get(API_ENDPOINTS.COMPLIANCE, {
      search: query,
      ...filters
    });
  },

  // Get compliance statistics
  getComplianceStats: async () => {
    return await apiService.get(`${API_ENDPOINTS.COMPLIANCE}/stats`);
  },

  // Get compliance score
  getComplianceScore: async () => {
    return await apiService.get(`${API_ENDPOINTS.COMPLIANCE}/score`);
  },

  // Get compliance frameworks
  getComplianceFrameworks: async () => {
    return await apiService.get(`${API_ENDPOINTS.COMPLIANCE}/frameworks`);
  },

  // Update compliance status
  updateComplianceStatus: async (id, status, evidence = '') => {
    return await apiService.patch(`${API_ENDPOINTS.COMPLIANCE_BY_ID(id)}/status`, {
      status,
      evidence
    });
  },

  // Get compliance gaps
  getComplianceGaps: async () => {
    return await apiService.get(`${API_ENDPOINTS.COMPLIANCE}/gaps`);
  },

  // Get compliance trends
  getComplianceTrends: async (timeRange = '30d') => {
    return await apiService.get(`${API_ENDPOINTS.COMPLIANCE}/trends`, { timeRange });
  },

  // Upload compliance evidence
  uploadComplianceEvidence: async (id, file) => {
    const formData = new FormData();
    formData.append('file', file);
    
    return await apiService.post(`${API_ENDPOINTS.COMPLIANCE_BY_ID(id)}/evidence`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },

  // Generate compliance report
  generateComplianceReport: async (framework, format = 'pdf') => {
    return await apiService.post(`${API_ENDPOINTS.COMPLIANCE}/report`, {
      framework,
      format
    });
  },
};
