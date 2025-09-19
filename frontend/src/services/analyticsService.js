import { apiService, API_ENDPOINTS } from './api';

export const analyticsService = {
  // Get dashboard data
  getDashboardData: async () => {
    return await apiService.get(API_ENDPOINTS.DASHBOARD);
  },

  // Get analytics data
  getAnalyticsData: async (params = {}) => {
    return await apiService.get(API_ENDPOINTS.ANALYTICS, params);
  },

  // Get compliance trends
  getComplianceTrends: async (timeRange = '30d') => {
    return await apiService.get(`${API_ENDPOINTS.ANALYTICS}/compliance/trends`, { timeRange });
  },

  // Get risk trends
  getRiskTrends: async (timeRange = '30d') => {
    return await apiService.get(`${API_ENDPOINTS.ANALYTICS}/risk/trends`, { timeRange });
  },

  // Get policy trends
  getPolicyTrends: async (timeRange = '30d') => {
    return await apiService.get(`${API_ENDPOINTS.ANALYTICS}/policy/trends`, { timeRange });
  },

  // Get workflow trends
  getWorkflowTrends: async (timeRange = '30d') => {
    return await apiService.get(`${API_ENDPOINTS.ANALYTICS}/workflow/trends`, { timeRange });
  },

  // Get KPI data
  getKPIData: async () => {
    return await apiService.get(`${API_ENDPOINTS.ANALYTICS}/kpis`);
  },

  // Get risk distribution
  getRiskDistribution: async () => {
    return await apiService.get(`${API_ENDPOINTS.ANALYTICS}/risk/distribution`);
  },

  // Get compliance distribution
  getComplianceDistribution: async () => {
    return await apiService.get(`${API_ENDPOINTS.ANALYTICS}/compliance/distribution`);
  },

  // Get policy status distribution
  getPolicyStatusDistribution: async () => {
    return await apiService.get(`${API_ENDPOINTS.ANALYTICS}/policy/distribution`);
  },

  // Get workflow progress
  getWorkflowProgress: async () => {
    return await apiService.get(`${API_ENDPOINTS.ANALYTICS}/workflow/progress`);
  },

  // Get executive summary
  getExecutiveSummary: async () => {
    return await apiService.get(`${API_ENDPOINTS.ANALYTICS}/executive-summary`);
  },

  // Generate custom report
  generateCustomReport: async (reportConfig) => {
    return await apiService.post(`${API_ENDPOINTS.ANALYTICS}/reports/custom`, reportConfig);
  },

  // Get report templates
  getReportTemplates: async () => {
    return await apiService.get(`${API_ENDPOINTS.ANALYTICS}/reports/templates`);
  },

  // Export analytics data
  exportAnalyticsData: async (format = 'csv', filters = {}) => {
    return await apiService.post(`${API_ENDPOINTS.ANALYTICS}/export`, {
      format,
      filters
    });
  },

  // Get real-time metrics
  getRealTimeMetrics: async () => {
    return await apiService.get(`${API_ENDPOINTS.ANALYTICS}/realtime`);
  },

  // Get performance metrics
  getPerformanceMetrics: async (timeRange = '24h') => {
    return await apiService.get(`${API_ENDPOINTS.ANALYTICS}/performance`, { timeRange });
  },
};
