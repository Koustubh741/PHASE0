import { apiService, API_ENDPOINTS } from './api';

export const riskService = {
  // Get all risks
  getAllRisks: async (params = {}) => {
    return await apiService.get(API_ENDPOINTS.RISKS, params);
  },

  // Get risk by ID
  getRiskById: async (id) => {
    return await apiService.get(API_ENDPOINTS.RISK_BY_ID(id));
  },

  // Create new risk
  createRisk: async (riskData) => {
    return await apiService.post(API_ENDPOINTS.RISKS, riskData);
  },

  // Update risk
  updateRisk: async (id, riskData) => {
    return await apiService.put(API_ENDPOINTS.RISK_BY_ID(id), riskData);
  },

  // Delete risk
  deleteRisk: async (id) => {
    return await apiService.delete(API_ENDPOINTS.RISK_BY_ID(id));
  },

  // Search risks
  searchRisks: async (query, filters = {}) => {
    return await apiService.get(API_ENDPOINTS.RISKS, {
      search: query,
      ...filters
    });
  },

  // Get risk statistics
  getRiskStats: async () => {
    return await apiService.get(`${API_ENDPOINTS.RISKS}/stats`);
  },

  // Get risk heat map data
  getRiskHeatMap: async () => {
    return await apiService.get(`${API_ENDPOINTS.RISKS}/heatmap`);
  },

  // Assess risk
  assessRisk: async (id, assessmentData) => {
    return await apiService.patch(`${API_ENDPOINTS.RISK_BY_ID(id)}/assess`, assessmentData);
  },

  // Mitigate risk
  mitigateRisk: async (id, mitigationData) => {
    return await apiService.patch(`${API_ENDPOINTS.RISK_BY_ID(id)}/mitigate`, mitigationData);
  },

  // Get risk trends
  getRiskTrends: async (timeRange = '30d') => {
    return await apiService.get(`${API_ENDPOINTS.RISKS}/trends`, { timeRange });
  },

  // Get risk categories
  getRiskCategories: async () => {
    return await apiService.get(`${API_ENDPOINTS.RISKS}/categories`);
  },

  // Bulk update risks
  bulkUpdateRisks: async (riskIds, updateData) => {
    return await apiService.patch(`${API_ENDPOINTS.RISKS}/bulk`, {
      riskIds,
      updateData
    });
  },
};
