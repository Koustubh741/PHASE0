import axios from 'axios';

// Create axios instance with base configuration
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized access
      localStorage.removeItem('authToken');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// API endpoints
export const API_ENDPOINTS = {
  // Authentication
  LOGIN: '/auth/login',
  LOGOUT: '/auth/logout',
  REFRESH: '/auth/refresh',
  
  // Policies
  POLICIES: '/policies',
  POLICY_BY_ID: (id) => `/policies/${id}`,
  
  // Risks
  RISKS: '/risks',
  RISK_BY_ID: (id) => `/risks/${id}`,
  
  // Compliance
  COMPLIANCE: '/compliance',
  COMPLIANCE_BY_ID: (id) => `/compliance/${id}`,
  
  // Workflows
  WORKFLOWS: '/workflows',
  WORKFLOW_BY_ID: (id) => `/workflows/${id}`,
  
  // Analytics
  ANALYTICS: '/analytics',
  DASHBOARD: '/dashboard',
  
  // AI Agents
  AI_AGENTS: '/ai-agents',
  AI_AGENT_BY_ID: (id) => `/ai-agents/${id}`,
  
  // Vector Store
  VECTOR_SEARCH: '/vector/search',
  VECTOR_ADD: '/vector/add',
};

// Generic API methods
export const apiService = {
  // GET request
  get: async (endpoint, params = {}) => {
    try {
      const response = await api.get(endpoint, { params });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || error.message);
    }
  },

  // POST request
  post: async (endpoint, data = {}) => {
    try {
      const response = await api.post(endpoint, data);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || error.message);
    }
  },

  // PUT request
  put: async (endpoint, data = {}) => {
    try {
      const response = await api.put(endpoint, data);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || error.message);
    }
  },

  // DELETE request
  delete: async (endpoint) => {
    try {
      const response = await api.delete(endpoint);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || error.message);
    }
  },

  // PATCH request
  patch: async (endpoint, data = {}) => {
    try {
      const response = await api.patch(endpoint, data);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || error.message);
    }
  },
};

export default api;
