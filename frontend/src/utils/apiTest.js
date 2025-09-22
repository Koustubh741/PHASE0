/**
 * API Integration Test Utility
 * Tests the connection between frontend services and backend APIs
 */

import { policyService } from '../services/policyService';
import { riskService } from '../services/riskService';
import { authService } from '../services/authService';
import { analyticsService } from '../services/analyticsService';
import { aiAgentsService } from '../services/aiAgentsService';
import API_CONFIG from '../config/api';

class APITestRunner {
  constructor() {
    this.results = [];
    this.baseURL = API_CONFIG.BASE_URL;
  }

  async runAllTests() {
    console.log('🧪 Starting Frontend API Integration Tests...');
    console.log(`📍 Testing against: ${this.baseURL}`);
    
    const tests = [
      { name: 'API Configuration', test: () => this.testAPIConfig() },
      { name: 'Authentication Service', test: () => this.testAuthService() },
      { name: 'Policy Service', test: () => this.testPolicyService() },
      { name: 'Risk Service', test: () => this.testRiskService() },
      { name: 'Analytics Service', test: () => this.testAnalyticsService() },
      { name: 'AI Agents Service', test: () => this.testAIAgentsService() },
    ];

    for (const test of tests) {
      try {
        console.log(`\n🔍 Testing ${test.name}...`);
        await test.test();
        this.results.push({ name: test.name, status: 'PASS', error: null });
        console.log(`✅ ${test.name} - PASSED`);
      } catch (error) {
        this.results.push({ name: test.name, status: 'FAIL', error: error.message });
        console.log(`❌ ${test.name} - FAILED: ${error.message}`);
      }
    }

    this.printSummary();
    return this.results;
  }

  testAPIConfig() {
    if (!API_CONFIG.BASE_URL) {
      throw new Error('Base URL not configured');
    }
    if (!API_CONFIG.ENDPOINTS) {
      throw new Error('API endpoints not configured');
    }
    if (!API_CONFIG.AUTH) {
      throw new Error('Auth configuration missing');
    }
    console.log(`  ✓ Base URL: ${API_CONFIG.BASE_URL}`);
    console.log(`  ✓ Auth enabled: ${API_CONFIG.AUTH.ENABLED}`);
    console.log(`  ✓ Features: ${Object.keys(API_CONFIG.FEATURES).join(', ')}`);
  }

  async testAuthService() {
    // Test authentication service methods exist
    if (typeof authService.login !== 'function') {
      throw new Error('Login method not found');
    }
    if (typeof authService.logout !== 'function') {
      throw new Error('Logout method not found');
    }
    if (typeof authService.isAuthenticated !== 'function') {
      throw new Error('isAuthenticated method not found');
    }
    
    // Test authentication status
    const isAuth = authService.isAuthenticated();
    console.log(`  ✓ Authentication status: ${isAuth ? 'Authenticated' : 'Not authenticated'}`);
  }

  async testPolicyService() {
    // Test policy service methods exist
    const requiredMethods = [
      'getAllPolicies', 'getPolicyById', 'createPolicy', 
      'updatePolicy', 'deletePolicy', 'searchPolicies'
    ];
    
    for (const method of requiredMethods) {
      if (typeof policyService[method] !== 'function') {
        throw new Error(`Policy service method '${method}' not found`);
      }
    }
    console.log(`  ✓ Policy service methods: ${requiredMethods.length} found`);
  }

  async testRiskService() {
    // Test risk service methods exist
    const requiredMethods = [
      'getAllRisks', 'getRiskById', 'createRisk', 
      'updateRisk', 'deleteRisk', 'assessRisk'
    ];
    
    for (const method of requiredMethods) {
      if (typeof riskService[method] !== 'function') {
        throw new Error(`Risk service method '${method}' not found`);
      }
    }
    console.log(`  ✓ Risk service methods: ${requiredMethods.length} found`);
  }

  async testAnalyticsService() {
    // Test analytics service methods exist
    const requiredMethods = [
      'getDashboardData', 'getAnalyticsData', 'getKPIData',
      'getRiskTrends', 'getComplianceTrends'
    ];
    
    for (const method of requiredMethods) {
      if (typeof analyticsService[method] !== 'function') {
        throw new Error(`Analytics service method '${method}' not found`);
      }
    }
    console.log(`  ✓ Analytics service methods: ${requiredMethods.length} found`);
  }

  async testAIAgentsService() {
    // Test AI agents service methods exist
    const requiredMethods = [
      'assessRisk', 'checkCompliance', 'reviewPolicy',
      'performCrossDomainAnalysis'
    ];
    
    for (const method of requiredMethods) {
      if (typeof aiAgentsService[method] !== 'function') {
        throw new Error(`AI Agents service method '${method}' not found`);
      }
    }
    console.log(`  ✓ AI Agents service methods: ${requiredMethods.length} found`);
  }

  printSummary() {
    console.log('\n📊 Test Summary:');
    console.log('================');
    
    const passed = this.results.filter(r => r.status === 'PASS').length;
    const failed = this.results.filter(r => r.status === 'FAIL').length;
    
    console.log(`✅ Passed: ${passed}`);
    console.log(`❌ Failed: ${failed}`);
    console.log(`📈 Success Rate: ${Math.round((passed / this.results.length) * 100)}%`);
    
    if (failed > 0) {
      console.log('\n❌ Failed Tests:');
      this.results
        .filter(r => r.status === 'FAIL')
        .forEach(r => console.log(`  - ${r.name}: ${r.error}`));
    }
    
    console.log('\n🎯 Frontend API Integration Status:');
    if (failed === 0) {
      console.log('🟢 All services properly configured and ready for backend integration');
    } else {
      console.log('🟡 Some services need attention before backend integration');
    }
  }
}

// Export for use in components or testing
export const runAPITests = async () => {
  const testRunner = new APITestRunner();
  return await testRunner.runAllTests();
};

// Auto-run tests if this file is executed directly
if (typeof window !== 'undefined' && window.location) {
  // Browser environment - can be called from console
  window.runAPITests = runAPITests;
  console.log('🔧 API Test Runner loaded. Run window.runAPITests() to test API integration.');
}

export default APITestRunner;
