import { apiService, API_ENDPOINTS } from './api';

/**
 * AI Agents Service
 * Handles all AI agent operations and interactions
 */
export const aiAgentsService = {
  // Get AI agents status
  getAgentsStatus: async () => {
    try {
      return await apiService.get(`${API_ENDPOINTS.AI_AGENTS}/agents/status`);
    } catch (error) {
      console.error('Error getting AI agents status:', error);
      throw error;
    }
  },

  // Health check for AI agents
  healthCheck: async () => {
    try {
      return await apiService.get(`${API_ENDPOINTS.AI_AGENTS}/health`);
    } catch (error) {
      console.error('Error checking AI agents health:', error);
      throw error;
    }
  },

  // Risk Assessment
  assessRisk: async (riskData) => {
    try {
      const payload = {
        business_unit: riskData.businessUnit,
        risk_scope: riskData.riskScope,
        industry_type: riskData.industryType,
        context: riskData.context || {}
      };
      return await apiService.post(`${API_ENDPOINTS.AI_AGENTS}/risk/assess`, payload);
    } catch (error) {
      console.error('Error in risk assessment:', error);
      throw error;
    }
  },

  // Compliance Check
  checkCompliance: async (complianceData) => {
    try {
      const payload = {
        entity_id: complianceData.entityId,
        entity_type: complianceData.entityType,
        industry_type: complianceData.industryType,
        compliance_requirements: complianceData.complianceRequirements || []
      };
      return await apiService.post(`${API_ENDPOINTS.AI_AGENTS}/compliance/check`, payload);
    } catch (error) {
      console.error('Error in compliance check:', error);
      throw error;
    }
  },

  // Policy Review
  reviewPolicy: async (policyData) => {
    try {
      const payload = {
        policy_id: policyData.policyId,
        industry_type: policyData.industryType,
        review_scope: policyData.reviewScope,
        context: policyData.context || {}
      };
      return await apiService.post(`${API_ENDPOINTS.AI_AGENTS}/policy/review`, payload);
    } catch (error) {
      console.error('Error in policy review:', error);
      throw error;
    }
  },

  // Cross-domain Analysis
  performCrossDomainAnalysis: async (analysisData) => {
    try {
      const payload = {
        analysis_type: analysisData.analysisType,
        industry_type: analysisData.industryType,
        data: analysisData.data,
        context: analysisData.context || {}
      };
      return await apiService.post(`${API_ENDPOINTS.AI_AGENTS}/analysis/cross-domain`, payload);
    } catch (error) {
      console.error('Error in cross-domain analysis:', error);
      throw error;
    }
  },

  // Industry-specific Operations
  performIndustryOperation: async (industryType, operationData) => {
    try {
      const payload = {
        operation_type: operationData.operationType,
        context: operationData.context || {}
      };
      return await apiService.post(`${API_ENDPOINTS.AI_AGENTS}/industry/${industryType}/operations`, payload);
    } catch (error) {
      console.error('Error in industry operation:', error);
      throw error;
    }
  },

  // Get available industry types
  getAvailableIndustries: () => {
    return [
      { value: 'bfsi', label: 'Banking, Financial Services & Insurance' },
      { value: 'telecom', label: 'Telecommunications' },
      { value: 'manufacturing', label: 'Manufacturing' },
      { value: 'healthcare', label: 'Healthcare' }
    ];
  },

  // Get available operation types
  getAvailableOperations: () => {
    return [
      { value: 'risk_assessment', label: 'Risk Assessment' },
      { value: 'compliance_check', label: 'Compliance Check' },
      { value: 'policy_review', label: 'Policy Review' },
      { value: 'audit_planning', label: 'Audit Planning' },
      { value: 'incident_response', label: 'Incident Response' },
      { value: 'regulatory_reporting', label: 'Regulatory Reporting' }
    ];
  },

  // Get available analysis types
  getAvailableAnalysisTypes: () => {
    return [
      { value: 'comprehensive', label: 'Comprehensive Analysis' },
      { value: 'risk_focused', label: 'Risk-Focused Analysis' },
      { value: 'compliance_focused', label: 'Compliance-Focused Analysis' },
      { value: 'policy_focused', label: 'Policy-Focused Analysis' },
      { value: 'cross_industry', label: 'Cross-Industry Analysis' }
    ];
  }
};

export default aiAgentsService;


