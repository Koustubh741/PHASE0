import { apiService, API_ENDPOINTS } from './api';

export const analyticsService = {
  // Get dashboard data
  getDashboardData: async () => {
    return await apiService.get(API_ENDPOINTS.ANALYTICS.DASHBOARD);
  },

  // Get analytics data
  getAnalyticsData: async (params = {}) => {
    return await apiService.get(API_ENDPOINTS.ANALYTICS.METRICS, params);
  },

  // Get compliance trends
  getComplianceTrends: async (timeRange = '30d') => {
    return await apiService.get(`${API_ENDPOINTS.ANALYTICS.TRENDS}/compliance`, { timeRange });
  },

  // Get risk trends
  getRiskTrends: async (timeRange = '30d') => {
    return await apiService.get(`${API_ENDPOINTS.ANALYTICS.TRENDS}/risk`, { timeRange });
  },

  // Get policy trends
  getPolicyTrends: async (timeRange = '30d') => {
    return await apiService.get(`${API_ENDPOINTS.ANALYTICS.TRENDS}/policy`, { timeRange });
  },

  // Get workflow trends
  getWorkflowTrends: async (timeRange = '30d') => {
    return await apiService.get(`${API_ENDPOINTS.ANALYTICS.TRENDS}/workflow`, { timeRange });
  },

  // Get KPI data
  getKPIData: async () => {
    return await apiService.get(`${API_ENDPOINTS.ANALYTICS.METRICS}/kpis`);
  },

  // Get risk distribution
  getRiskDistribution: async () => {
    return await apiService.get(`${API_ENDPOINTS.ANALYTICS.METRICS}/risk/distribution`);
  },

  // Get compliance distribution
  getComplianceDistribution: async () => {
    return await apiService.get(`${API_ENDPOINTS.ANALYTICS.METRICS}/compliance/distribution`);
  },

  // Get policy status distribution
  getPolicyStatusDistribution: async () => {
    return await apiService.get(`${API_ENDPOINTS.ANALYTICS.METRICS}/policy/distribution`);
  },

  // Get workflow progress
  getWorkflowProgress: async () => {
    return await apiService.get(`${API_ENDPOINTS.ANALYTICS.METRICS}/workflow/progress`);
  },

  // Get executive summary
  getExecutiveSummary: async () => {
    return await apiService.get(`${API_ENDPOINTS.ANALYTICS.REPORTS}/executive-summary`);
  },

  // Generate custom report
  generateCustomReport: async (reportConfig) => {
    return await apiService.post(`${API_ENDPOINTS.ANALYTICS.REPORTS}/custom`, reportConfig);
  },

  // Get report templates
  getReportTemplates: async () => {
    return await apiService.get(`${API_ENDPOINTS.ANALYTICS.REPORTS}/templates`);
  },

  // Export analytics data
  exportAnalyticsData: async (format = 'csv', filters = {}) => {
    return await apiService.post(`${API_ENDPOINTS.ANALYTICS.REPORTS}/export`, {
      format,
      filters
    });
  },

  // Get real-time metrics
  getRealTimeMetrics: async () => {
    return await apiService.get(`${API_ENDPOINTS.ANALYTICS.METRICS}/realtime`);
  },

  // Get performance metrics
  getPerformanceMetrics: async (timeRange = '24h') => {
    return await apiService.get(`${API_ENDPOINTS.ANALYTICS.METRICS}/performance`, { timeRange });
  },
};
