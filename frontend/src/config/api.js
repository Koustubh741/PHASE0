// API Configuration for GRC Platform Frontend
const API_CONFIG = {
  // Base API URL - Points to API Gateway
  BASE_URL: process.env.REACT_APP_API_URL || 'http://localhost:8000',
  
  // Service URLs (for direct access if needed)
  SERVICES: {
    GATEWAY: process.env.REACT_APP_GATEWAY_URL || 'http://localhost:8000',
    POLICY: process.env.REACT_APP_POLICY_SERVICE_URL || 'http://localhost:8001',
    RISK: process.env.REACT_APP_RISK_SERVICE_URL || 'http://localhost:8002',
    COMPLIANCE: process.env.REACT_APP_COMPLIANCE_SERVICE_URL || 'http://localhost:8003',
    WORKFLOW: process.env.REACT_APP_WORKFLOW_SERVICE_URL || 'http://localhost:8004',
    AI_AGENTS: process.env.REACT_APP_AI_AGENTS_SERVICE_URL || 'http://localhost:8005',
  },
  
  // API Endpoints
  ENDPOINTS: {
    // Authentication
    AUTH: {
      LOGIN: '/api/v1/auth/login',
      LOGOUT: '/api/v1/auth/logout',
      REFRESH: '/api/v1/auth/refresh',
      REGISTER: '/api/v1/auth/register',
      PROFILE: '/api/v1/auth/profile',
      CHANGE_PASSWORD: '/api/v1/auth/change-password',
    },
    
    // Policies
    POLICIES: {
      BASE: '/api/v1/policies',
      BY_ID: (id) => `/api/v1/policies/${id}`,
      SEARCH: '/api/v1/policies/search',
      STATS: '/api/v1/policies/stats',
      APPROVE: (id) => `/api/v1/policies/${id}/approve`,
      REJECT: (id) => `/api/v1/policies/${id}/reject`,
      VERSIONS: (id) => `/api/v1/policies/${id}/versions`,
      UPLOAD: (id) => `/api/v1/policies/${id}/upload`,
    },
    
    // Risks
    RISKS: {
      BASE: '/api/v1/risks',
      BY_ID: (id) => `/api/v1/risks/${id}`,
      SEARCH: '/api/v1/risks/search',
      STATS: '/api/v1/risks/stats',
      HEATMAP: '/api/v1/risks/heatmap',
      ASSESS: (id) => `/api/v1/risks/${id}/assess`,
      MITIGATE: (id) => `/api/v1/risks/${id}/mitigate`,
      TRENDS: '/api/v1/risks/trends',
      CATEGORIES: '/api/v1/risks/categories',
      BULK_UPDATE: '/api/v1/risks/bulk',
    },
    
    // Compliance
    COMPLIANCE: {
      BASE: '/api/v1/compliance',
      BY_ID: (id) => `/api/v1/compliance/${id}`,
      ASSESSMENTS: '/api/v1/compliance/assessments',
      REQUIREMENTS: '/api/v1/compliance/requirements',
      FRAMEWORKS: '/api/v1/compliance/frameworks',
      REPORTS: '/api/v1/compliance/reports',
    },
    
    // Workflows
    WORKFLOWS: {
      BASE: '/api/v1/workflows',
      BY_ID: (id) => `/api/v1/workflows/${id}`,
      EXECUTE: (id) => `/api/v1/workflows/${id}/execute`,
      STATUS: (id) => `/api/v1/workflows/${id}/status`,
      HISTORY: (id) => `/api/v1/workflows/${id}/history`,
    },
    
    // AI Agents
    AI_AGENTS: {
      BASE: '/api/v1/ai-agents',
      BY_ID: (id) => `/api/v1/ai-agents/${id}`,
      CHAT: (id) => `/api/v1/ai-agents/${id}/chat`,
      TRAIN: (id) => `/api/v1/ai-agents/${id}/train`,
      STATUS: (id) => `/api/v1/ai-agents/${id}/status`,
    },
    
    // Analytics
    ANALYTICS: {
      DASHBOARD: '/api/v1/analytics/dashboard',
      METRICS: '/api/v1/analytics/metrics',
      REPORTS: '/api/v1/analytics/reports',
      TRENDS: '/api/v1/analytics/trends',
    },
    
    // Users
    USERS: {
      BASE: '/api/v1/users',
      BY_ID: (id) => `/api/v1/users/${id}`,
      PROFILE: '/api/v1/users/profile',
      ROLES: '/api/v1/users/roles',
      PERMISSIONS: '/api/v1/users/permissions',
    },
  },
  
  // Request Configuration
  TIMEOUT: 30000, // 30 seconds
  RETRY_ATTEMPTS: 3,
  RETRY_DELAY: 1000, // 1 second
  
  // Authentication
  AUTH: {
    ENABLED: process.env.REACT_APP_AUTH_ENABLED === 'true',
    TOKEN_KEY: process.env.REACT_APP_TOKEN_STORAGE_KEY || 'authToken',
    REFRESH_THRESHOLD: 300, // 5 minutes before expiry
  },
  
  // Feature Flags
  FEATURES: {
    AI_AGENTS: process.env.REACT_APP_AI_AGENTS_ENABLED === 'true',
    ANALYTICS: process.env.REACT_APP_ANALYTICS_ENABLED === 'true',
    BFSI_MODE: process.env.REACT_APP_BFSI_MODE === 'true',
  },
};

export default API_CONFIG;
