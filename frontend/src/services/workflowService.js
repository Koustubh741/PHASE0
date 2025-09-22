import { apiService, API_ENDPOINTS } from './api';

export const workflowService = {
  // Get all workflows
  getAllWorkflows: async (params = {}) => {
    return await apiService.get(API_ENDPOINTS.WORKFLOWS.BASE, params);
  },

  // Get workflow by ID
  getWorkflowById: async (id) => {
    return await apiService.get(API_ENDPOINTS.WORKFLOWS.BY_ID(id));
  },

  // Create new workflow
  createWorkflow: async (workflowData) => {
    return await apiService.post(API_ENDPOINTS.WORKFLOWS.BASE, workflowData);
  },

  // Update workflow
  updateWorkflow: async (id, workflowData) => {
    return await apiService.put(API_ENDPOINTS.WORKFLOWS.BY_ID(id), workflowData);
  },

  // Delete workflow
  deleteWorkflow: async (id) => {
    return await apiService.delete(API_ENDPOINTS.WORKFLOWS.BY_ID(id));
  },

  // Search workflows
  searchWorkflows: async (query, filters = {}) => {
    return await apiService.get(API_ENDPOINTS.WORKFLOWS.BASE, {
      search: query,
      ...filters
    });
  },

  // Get workflow statistics
  getWorkflowStats: async () => {
    return await apiService.get(`${API_ENDPOINTS.WORKFLOWS.BASE}/stats`);
  },

  // Execute workflow
  executeWorkflow: async (id, executionData = {}) => {
    return await apiService.post(API_ENDPOINTS.WORKFLOWS.EXECUTE(id), executionData);
  },

  // Get workflow status
  getWorkflowStatus: async (id) => {
    return await apiService.get(API_ENDPOINTS.WORKFLOWS.STATUS(id));
  },

  // Get workflow history
  getWorkflowHistory: async (id) => {
    return await apiService.get(API_ENDPOINTS.WORKFLOWS.HISTORY(id));
  },

  // Get workflow templates
  getWorkflowTemplates: async () => {
    return await apiService.get(`${API_ENDPOINTS.WORKFLOWS.BASE}/templates`);
  },

  // Create workflow from template
  createWorkflowFromTemplate: async (templateId, workflowData) => {
    return await apiService.post(`${API_ENDPOINTS.WORKFLOWS.BASE}/templates/${templateId}`, workflowData);
  },

  // Get workflow performance metrics
  getWorkflowMetrics: async (id) => {
    return await apiService.get(`${API_ENDPOINTS.WORKFLOWS.BY_ID(id)}/metrics`);
  },
};
