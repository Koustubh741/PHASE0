import { policyService } from '../policyService';
import { riskService } from '../riskService';
import { complianceService } from '../complianceService';
import { workflowService } from '../workflowService';
import { aiAgentsService } from '../aiAgentsService';
import { analyticsService } from '../analyticsService';
import { authService } from '../authService';
import { bfsiService } from '../bfsiService';
import API_CONFIG from '../../config/api';

// Mock axios for testing
jest.mock('axios');
import axios from 'axios';

describe('Frontend API Integration Tests', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    // Mock localStorage
    Object.defineProperty(window, 'localStorage', {
      value: {
        getItem: jest.fn(),
        setItem: jest.fn(),
        removeItem: jest.fn(),
      },
      writable: true,
    });
  });

  describe('API Configuration', () => {
    test('API_CONFIG should have correct structure', () => {
      expect(API_CONFIG).toHaveProperty('BASE_URL');
      expect(API_CONFIG).toHaveProperty('ENDPOINTS');
      expect(API_CONFIG).toHaveProperty('AUTH');
      expect(API_CONFIG).toHaveProperty('FEATURES');
    });

    test('API endpoints should be properly structured', () => {
      expect(API_CONFIG.ENDPOINTS).toHaveProperty('AUTH');
      expect(API_CONFIG.ENDPOINTS).toHaveProperty('POLICIES');
      expect(API_CONFIG.ENDPOINTS).toHaveProperty('RISKS');
      expect(API_CONFIG.ENDPOINTS).toHaveProperty('COMPLIANCE');
      expect(API_CONFIG.ENDPOINTS).toHaveProperty('WORKFLOWS');
      expect(API_CONFIG.ENDPOINTS).toHaveProperty('AI_AGENTS');
      expect(API_CONFIG.ENDPOINTS).toHaveProperty('ANALYTICS');
    });
  });

  describe('Policy Service', () => {
    test('should call correct API endpoints', async () => {
      const mockResponse = { data: { policies: [] } };
      axios.create.mockReturnValue({
        get: jest.fn().mockResolvedValue(mockResponse),
        post: jest.fn().mockResolvedValue(mockResponse),
        put: jest.fn().mockResolvedValue(mockResponse),
        delete: jest.fn().mockResolvedValue(mockResponse),
        patch: jest.fn().mockResolvedValue(mockResponse),
      });

      await policyService.getAllPolicies();
      expect(axios.create().get).toHaveBeenCalledWith('/api/v1/policies', {});
    });

    test('should handle policy creation', async () => {
      const mockResponse = { data: { id: '123', title: 'Test Policy' } };
      axios.create().post.mockResolvedValue(mockResponse);

      const policyData = { title: 'Test Policy', content: 'Test content' };
      const result = await policyService.createPolicy(policyData);
      
      expect(result).toEqual(mockResponse.data);
      expect(axios.create().post).toHaveBeenCalledWith('/api/v1/policies', policyData);
    });
  });

  describe('Risk Service', () => {
    test('should call correct risk API endpoints', async () => {
      const mockResponse = { data: { risks: [] } };
      axios.create().get.mockResolvedValue(mockResponse);

      await riskService.getAllRisks();
      expect(axios.create().get).toHaveBeenCalledWith('/api/v1/risks', {});
    });

    test('should handle risk assessment', async () => {
      const mockResponse = { data: { assessment: 'completed' } };
      axios.create().patch.mockResolvedValue(mockResponse);

      const assessmentData = { likelihood: 'high', impact: 'medium' };
      const result = await riskService.assessRisk('risk-123', assessmentData);
      
      expect(result).toEqual(mockResponse.data);
      expect(axios.create().patch).toHaveBeenCalledWith('/api/v1/risks/risk-123/assess', assessmentData);
    });
  });

  describe('Authentication Service', () => {
    test('should handle login correctly', async () => {
      const mockResponse = { data: { token: 'test-token', user: { id: '123' } } };
      axios.create().post.mockResolvedValue(mockResponse);

      const credentials = { username: 'test@example.com', password: 'password' };
      const result = await authService.login(credentials);
      
      expect(result).toEqual(mockResponse.data);
      expect(axios.create().post).toHaveBeenCalledWith('/api/v1/auth/login', credentials);
    });

    test('should handle logout correctly', async () => {
      const mockResponse = { data: { success: true } };
      axios.create().post.mockResolvedValue(mockResponse);

      const result = await authService.logout();
      
      expect(result).toEqual({ success: true });
      expect(axios.create().post).toHaveBeenCalledWith('/api/v1/auth/logout');
    });

    test('should check authentication status', () => {
      // Test with auth enabled
      window.localStorage.getItem.mockReturnValue('test-token');
      expect(authService.isAuthenticated()).toBe(true);

      // Test with no token
      window.localStorage.getItem.mockReturnValue(null);
      expect(authService.isAuthenticated()).toBe(false);
    });
  });

  describe('AI Agents Service', () => {
    test('should handle risk assessment', async () => {
      const mockResponse = { data: { assessment: 'completed' } };
      axios.create().post.mockResolvedValue(mockResponse);

      const riskData = {
        businessUnit: 'retail',
        riskScope: 'full',
        industryType: 'bfsi',
        context: {}
      };
      const result = await aiAgentsService.assessRisk(riskData);
      
      expect(result).toEqual(mockResponse.data);
      expect(axios.create().post).toHaveBeenCalledWith(
        '/api/v1/ai-agents/risk/assess',
        {
          business_unit: 'retail',
          risk_scope: 'full',
          industry_type: 'bfsi',
          context: {}
        }
      );
    });

    test('should handle compliance check', async () => {
      const mockResponse = { data: { compliance: 'checked' } };
      axios.create().post.mockResolvedValue(mockResponse);

      const complianceData = {
        entityId: 'entity-123',
        entityType: 'policy',
        industryType: 'bfsi',
        complianceRequirements: ['SOX', 'PCI-DSS']
      };
      const result = await aiAgentsService.checkCompliance(complianceData);
      
      expect(result).toEqual(mockResponse.data);
      expect(axios.create().post).toHaveBeenCalledWith(
        '/api/v1/ai-agents/compliance/check',
        {
          entity_id: 'entity-123',
          entity_type: 'policy',
          industry_type: 'bfsi',
          compliance_requirements: ['SOX', 'PCI-DSS']
        }
      );
    });
  });

  describe('Analytics Service', () => {
    test('should get dashboard data', async () => {
      const mockResponse = { data: { dashboard: 'data' } };
      axios.create().get.mockResolvedValue(mockResponse);

      const result = await analyticsService.getDashboardData();
      
      expect(result).toEqual(mockResponse.data);
      expect(axios.create().get).toHaveBeenCalledWith('/api/v1/analytics/dashboard');
    });

    test('should get KPI data', async () => {
      const mockResponse = { data: { kpis: [] } };
      axios.create().get.mockResolvedValue(mockResponse);

      const result = await analyticsService.getKPIData();
      
      expect(result).toEqual(mockResponse.data);
      expect(axios.create().get).toHaveBeenCalledWith('/api/v1/analytics/metrics/kpis');
    });
  });

  describe('BFSI Service', () => {
    test('should get BFSI status', async () => {
      const mockResponse = { data: { status: 'active' } };
      axios.create().get.mockResolvedValue(mockResponse);

      const result = await bfsiService.getBFSIStatus();
      
      expect(result).toEqual(mockResponse.data);
      expect(axios.create().get).toHaveBeenCalledWith('/api/v1/ai-agents/industry/bfsi/status');
    });

    test('should perform risk assessment', async () => {
      const mockResponse = { data: { assessment: 'completed' } };
      axios.create().post.mockResolvedValue(mockResponse);

      const riskData = {
        businessUnit: 'retail',
        riskScope: 'full',
        riskData: { type: 'operational' }
      };
      const result = await bfsiService.performRiskAssessment(riskData);
      
      expect(result).toEqual(mockResponse.data);
      expect(axios.create().post).toHaveBeenCalledWith(
        '/api/v1/ai-agents/industry/bfsi/risk-assessment',
        {
          business_unit: 'retail',
          risk_scope: 'full',
          risk_data: { type: 'operational' }
        }
      );
    });
  });

  describe('Error Handling', () => {
    test('should handle API errors gracefully', async () => {
      const error = new Error('API Error');
      axios.create().get.mockRejectedValue(error);

      await expect(policyService.getAllPolicies()).rejects.toThrow('API Error');
    });

    test('should handle 401 errors with auth logout', async () => {
      const error = {
        response: { status: 401 },
        message: 'Unauthorized'
      };
      axios.create().get.mockRejectedValue(error);

      // Mock the interceptor behavior
      const mockAxiosInstance = {
        get: jest.fn().mockRejectedValue(error),
        post: jest.fn(),
        put: jest.fn(),
        delete: jest.fn(),
        patch: jest.fn(),
        interceptors: {
          request: { use: jest.fn() },
          response: { use: jest.fn() }
        }
      };
      axios.create.mockReturnValue(mockAxiosInstance);

      await expect(policyService.getAllPolicies()).rejects.toThrow('Unauthorized');
    });
  });
});
