import { apiService, API_ENDPOINTS } from './api';

export const workflowService = {
  // Get all workflows
  getAllWorkflows: async (params = {}) => {
    return await apiService.get(API_ENDPOINTS.WORKFLOWS, params);
  },

  // Get workflow by ID
  getWorkflowById: async (id) => {
    return await apiService.get(API_ENDPOINTS.WORKFLOW_BY_ID(id));
  },

  // Create new workflow
  createWorkflow: async (workflowData) => {
    return await apiService.post(API_ENDPOINTS.WORKFLOWS, workflowData);
  },

  // Update workflow
  updateWorkflow: async (id, workflowData) => {
    return await apiService.put(API_ENDPOINTS.WORKFLOW_BY_ID(id), workflowData);
  },

  // Delete workflow
  deleteWorkflow: async (id) => {
    return await apiService.delete(API_ENDPOINTS.WORKFLOW_BY_ID(id));
  },

  // Search workflows
  searchWorkflows: async (query, filters = {}) => {
    return await apiService.get(API_ENDPOINTS.WORKFLOWS, {
      search: query,
      ...filters
    });
  },

  // Get workflow statistics
  getWorkflowStats: async () => {
    return await apiService.get(`${API_ENDPOINTS.WORKFLOWS}/stats`);
  },

  // Start workflow
  startWorkflow: async (id, startData = {}) => {
    return await apiService.post(`${API_ENDPOINTS.WORKFLOW_BY_ID(id)}/start`, startData);
  },

  // Pause workflow
  pauseWorkflow: async (id) => {
    return await apiService.patch(`${API_ENDPOINTS.WORKFLOW_BY_ID(id)}/pause`);
  },

  // Resume workflow
  resumeWorkflow: async (id) => {
    return await apiService.patch(`${API_ENDPOINTS.WORKFLOW_BY_ID(id)}/resume`);
  },

  // Complete workflow
  completeWorkflow: async (id, completionData = {}) => {
    return await apiService.patch(`${API_ENDPOINTS.WORKFLOW_BY_ID(id)}/complete`, completionData);
  },

  // Get workflow steps
  getWorkflowSteps: async (id) => {
    return await apiService.get(`${API_ENDPOINTS.WORKFLOW_BY_ID(id)}/steps`);
  },

  // Update workflow step
  updateWorkflowStep: async (id, stepId, stepData) => {
    return await apiService.patch(`${API_ENDPOINTS.WORKFLOW_BY_ID(id)}/steps/${stepId}`, stepData);
  },

  // Get workflow history
  getWorkflowHistory: async (id) => {
    return await apiService.get(`${API_ENDPOINTS.WORKFLOW_BY_ID(id)}/history`);
  },

  // Get workflow templates
  getWorkflowTemplates: async () => {
    return await apiService.get(`${API_ENDPOINTS.WORKFLOWS}/templates`);
  },

  // Create workflow from template
  createWorkflowFromTemplate: async (templateId, workflowData) => {
    return await apiService.post(`${API_ENDPOINTS.WORKFLOWS}/templates/${templateId}`, workflowData);
  },

  // Get workflow performance metrics
  getWorkflowMetrics: async (id) => {
    return await apiService.get(`${API_ENDPOINTS.WORKFLOW_BY_ID(id)}/metrics`);
  },
};
