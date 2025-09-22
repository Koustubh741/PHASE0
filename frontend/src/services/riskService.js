import { apiService, API_ENDPOINTS } from './api';

export const riskService = {
  // Get all risks
  getAllRisks: async (params = {}) => {
    return await apiService.get(API_ENDPOINTS.RISKS.BASE, params);
  },

  // Get risk by ID
  getRiskById: async (id) => {
    return await apiService.get(API_ENDPOINTS.RISKS.BY_ID(id));
  },

  // Create new risk
  createRisk: async (riskData) => {
    return await apiService.post(API_ENDPOINTS.RISKS.BASE, riskData);
  },

  // Update risk
  updateRisk: async (id, riskData) => {
    return await apiService.put(API_ENDPOINTS.RISKS.BY_ID(id), riskData);
  },

  // Delete risk
  deleteRisk: async (id) => {
    return await apiService.delete(API_ENDPOINTS.RISKS.BY_ID(id));
  },

  // Search risks
  searchRisks: async (query, filters = {}) => {
    return await apiService.get(API_ENDPOINTS.RISKS.SEARCH, {
      search: query,
      ...filters
    });
  },

  // Get risk statistics
  getRiskStats: async () => {
    return await apiService.get(API_ENDPOINTS.RISKS.STATS);
  },

  // Get risk heat map data
  getRiskHeatMap: async () => {
    return await apiService.get(API_ENDPOINTS.RISKS.HEATMAP);
  },

  // Assess risk
  assessRisk: async (id, assessmentData) => {
    return await apiService.patch(API_ENDPOINTS.RISKS.ASSESS(id), assessmentData);
  },

  // Mitigate risk
  mitigateRisk: async (id, mitigationData) => {
    return await apiService.patch(API_ENDPOINTS.RISKS.MITIGATE(id), mitigationData);
  },

  // Get risk trends
  getRiskTrends: async (timeRange = '30d') => {
    return await apiService.get(API_ENDPOINTS.RISKS.TRENDS, { timeRange });
  },

  // Get risk categories
  getRiskCategories: async () => {
    return await apiService.get(API_ENDPOINTS.RISKS.CATEGORIES);
  },

  // Bulk update risks
  bulkUpdateRisks: async (riskIds, updateData) => {
    return await apiService.patch(API_ENDPOINTS.RISKS.BULK_UPDATE, {
      riskIds,
      updateData
    });
  },
};
