import { apiService } from './api';

// BFSI-specific API endpoints
export const BFSI_API_ENDPOINTS = {
  // BFSI Industry Status
  STATUS: '/grc/industry/bfsi/status',
  INDUSTRIES: '/grc/industries',
  
  // BFSI Risk Assessment
  RISK_ASSESSMENT: '/grc/industry/bfsi/risk-assessment',
  
  // BFSI Compliance Check
  COMPLIANCE_CHECK: '/grc/industry/bfsi/compliance-check',
  
  // BFSI Assessment
  ASSESSMENT: '/grc/industry/bfsi/assessment',
  
  // BFSI Reports
  REPORT: '/grc/industry/bfsi/report',
  
  // BFSI Policy Management
  POLICIES: '/grc/industry/bfsi/policies',
  POLICY_STANDARDS: '/grc/industry/bfsi/policy-standards',
  
  // BFSI Agent Status
  AGENT_STATUS: '/grc/status',
};

// BFSI Service class
class BFSIService {
  
  // Get BFSI industry status
  async getBFSIStatus() {
    try {
      return await apiService.get(BFSI_API_ENDPOINTS.STATUS);
    } catch (error) {
      console.error('Failed to get BFSI status:', error);
      throw error;
    }
  }

  // Get supported industries (should only return BFSI)
  async getSupportedIndustries() {
    try {
      return await apiService.get(BFSI_API_ENDPOINTS.INDUSTRIES);
    } catch (error) {
      console.error('Failed to get supported industries:', error);
      throw error;
    }
  }

  // Perform BFSI risk assessment
  async performRiskAssessment(riskData) {
    try {
      return await apiService.post(BFSI_API_ENDPOINTS.RISK_ASSESSMENT, {
        business_unit: riskData.businessUnit || 'all',
        risk_scope: riskData.riskScope || 'full',
        risk_data: riskData
      });
    } catch (error) {
      console.error('Failed to perform risk assessment:', error);
      throw error;
    }
  }

  // Perform BFSI compliance check
  async performComplianceCheck(complianceData) {
    try {
      return await apiService.post(BFSI_API_ENDPOINTS.COMPLIANCE_CHECK, {
        framework: complianceData.framework || 'all',
        business_unit: complianceData.businessUnit || 'all',
        compliance_data: complianceData
      });
    } catch (error) {
      console.error('Failed to perform compliance check:', error);
      throw error;
    }
  }

  // Perform BFSI comprehensive assessment
  async performAssessment(assessmentData) {
    try {
      return await apiService.post(BFSI_API_ENDPOINTS.ASSESSMENT, {
        assessment_type: assessmentData.assessmentType || 'comprehensive',
        context: assessmentData.context || {},
        assessment_data: assessmentData
      });
    } catch (error) {
      console.error('Failed to perform assessment:', error);
      throw error;
    }
  }

  // Generate BFSI report
  async generateReport(reportData) {
    try {
      return await apiService.post(BFSI_API_ENDPOINTS.REPORT, {
        report_type: reportData.reportType || 'executive_summary',
        format: reportData.format || 'pdf',
        data: reportData.data || {}
      });
    } catch (error) {
      console.error('Failed to generate report:', error);
      throw error;
    }
  }

  // Get BFSI policy standards
  async getPolicyStandards() {
    try {
      return await apiService.get(BFSI_API_ENDPOINTS.POLICY_STANDARDS);
    } catch (error) {
      console.error('Failed to get policy standards:', error);
      throw error;
    }
  }

  // Add industry standard policy
  async addIndustryStandardPolicy(policyData) {
    try {
      return await apiService.post(BFSI_API_ENDPOINTS.POLICIES, {
        policy_type: 'industry_standard',
        policy_data: policyData
      });
    } catch (error) {
      console.error('Failed to add industry standard policy:', error);
      throw error;
    }
  }

  // Get BFSI agent status
  async getAgentStatus() {
    try {
      return await apiService.get(BFSI_API_ENDPOINTS.AGENT_STATUS);
    } catch (error) {
      console.error('Failed to get agent status:', error);
      throw error;
    }
  }

  // Execute BFSI operation
  async executeBFSOperation(operationData) {
    try {
      return await apiService.post('/grc/industry/bfsi/operation', {
        operation_type: operationData.operationType,
        context: operationData.context,
        operation_data: operationData
      });
    } catch (error) {
      console.error('Failed to execute BFSI operation:', error);
      throw error;
    }
  }
}

// Export singleton instance
export const bfsiService = new BFSIService();
export default bfsiService;
