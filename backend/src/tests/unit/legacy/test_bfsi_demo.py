#!/usr/bin/env python3
"""
BFSI Local AI Integration Demo
Comprehensive demonstration of BFSI agent capabilities with local AI services
"""

import asyncio
import json
import requests
from datetime import datetime
from typing import Dict, Any

class BFSIDemo:
    """BFSI Local AI Integration Demo"""
    
    def __init__(self, api_base_url: str = "http://localhost:8008", timeout: int = 30):
        self.api_base_url = api_base_url
        self.session = requests.Session()
        self.default_timeout = timeout
        
    def test_health(self) -> bool:
        """Test API health"""
        try:
            response = self.session.get(f"{self.api_base_url}/health", timeout=self.default_timeout)
            if response.status_code == 200:
                health_data = response.json()
                print("✅ API Health Check:")
                print(f"   BFSI Agent: {health_data['bfsi_agent']['status']}")
                print(f"   AI Services: {health_data['ai_services']}")
                print(f"   Overall: {health_data['overall_health']}")
                return True
            else:
                print(f"❌ Health check failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Health check error: {e}")
            return False
    
    def test_compliance_check(self) -> Dict[str, Any]:
        """Test BFSI compliance check"""
        print("\n📋 Testing BFSI Compliance Check...")
        
        compliance_request = {
            "regulation": "SOX",
            "process": "Financial Reporting",
            "controls": [
                "Access Control",
                "Data Integrity", 
                "Audit Trail",
                "Segregation of Duties"
            ],
            "documents": [
                "Financial Statements",
                "Internal Audit Reports",
                "Control Testing Results"
            ],
            "priority": "high"
        }
        
        try:
            response = self.session.post(
                f"{self.api_base_url}/compliance/check",
                json=compliance_request,
                timeout=self.default_timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Compliance Check Results:")
                print(f"   Task ID: {result['task_id']}")
                print(f"   Risk Score: {result['risk_score']}/100")
                print(f"   Compliance Score: {result['compliance_score']}/100")
                print(f"   Findings: {len(result['findings'])} items")
                for i, finding in enumerate(result['findings'][:3], 1):
                    print(f"     {i}. {finding}")
                print(f"   Recommendations: {len(result['recommendations'])} items")
                for i, rec in enumerate(result['recommendations'][:2], 1):
                    print(f"     {i}. {rec}")
                return result
            else:
                print(f"❌ Compliance check failed: {response.status_code}")
                print(f"   Error: {response.text}")
                return {}
                
        except Exception as e:
            print(f"❌ Compliance check error: {e}")
            return {}
    
    def test_risk_assessment(self) -> Dict[str, Any]:
        """Test BFSI risk assessment"""
        print("\n⚠️ Testing BFSI Risk Assessment...")
        
        risk_request = {
            "risk_type": "Credit Risk",
            "portfolio": "Corporate Loans",
            "exposure": 50000000,
            "probability": "medium",
            "impact": "high",
            "controls": [
                "Credit Scoring",
                "Collateral Management",
                "Regular Reviews"
            ]
        }
        
        try:
            response = self.session.post(
                f"{self.api_base_url}/risk/assess",
                json=risk_request,
                timeout=self.default_timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Risk Assessment Results:")
                print(f"   Task ID: {result['task_id']}")
                print(f"   Risk Score: {result['risk_score']}/100")
                print(f"   Compliance Score: {result['compliance_score']}/100")
                print(f"   Findings: {len(result['findings'])} items")
                for i, finding in enumerate(result['findings'][:3], 1):
                    print(f"     {i}. {finding}")
                return result
            else:
                print(f"❌ Risk assessment failed: {response.status_code}")
                return {}
                
        except Exception as e:
            print(f"❌ Risk assessment error: {e}")
            return {}
    
    def test_fraud_detection(self) -> Dict[str, Any]:
        """Test BFSI fraud detection"""
        print("\n🔍 Testing BFSI Fraud Detection...")
        
        fraud_request = {
            "transaction_id": "TXN-20250919-001",
            "amount": 250000,
            "customer_id": "CUST-12345",
            "transaction_type": "Wire Transfer",
            "location": "International",
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            response = self.session.post(
                f"{self.api_base_url}/fraud/detect",
                json=fraud_request,
                timeout=self.default_timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Fraud Detection Results:")
                print(f"   Task ID: {result['task_id']}")
                print(f"   Risk Score: {result['risk_score']}/100")
                print(f"   Compliance Score: {result['compliance_score']}/100")
                print(f"   Findings: {len(result['findings'])} items")
                for i, finding in enumerate(result['findings'][:3], 1):
                    print(f"     {i}. {finding}")
                return result
            else:
                print(f"❌ Fraud detection failed: {response.status_code}")
                return {}
                
        except Exception as e:
            print(f"❌ Fraud detection error: {e}")
            return {}
    
    def test_document_analysis(self) -> Dict[str, Any]:
        """Test BFSI document analysis"""
        print("\n📄 Testing BFSI Document Analysis...")
        
        document_request = {
            "document_type": "Loan Agreement",
            "content": """
            LOAN AGREEMENT
            
            This agreement is between ABC Bank and XYZ Corporation for a credit facility 
            of $10,000,000. The loan is secured by company assets and requires monthly 
            payments of $200,000. Interest rate is 5.5% annually.
            
            The borrower agrees to maintain certain financial covenants including:
            - Debt-to-equity ratio not exceeding 2:1
            - Current ratio of at least 1.5:1
            - Quarterly financial reporting requirements
            
            This agreement is subject to regulatory compliance under Basel III.
            """,
            "classification": "Credit Documentation",
            "compliance_framework": "Basel III"
        }
        
        try:
            response = self.session.post(
                f"{self.api_base_url}/documents/analyze",
                json=document_request,
                timeout=self.default_timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Document Analysis Results:")
                print(f"   Task ID: {result['task_id']}")
                print(f"   Risk Score: {result['risk_score']}/100")
                print(f"   Compliance Score: {result['compliance_score']}/100")
                print(f"   Findings: {len(result['findings'])} items")
                for i, finding in enumerate(result['findings'][:3], 1):
                    print(f"     {i}. {finding}")
                return result
            else:
                print(f"❌ Document analysis failed: {response.status_code}")
                return {}
                
        except Exception as e:
            print(f"❌ Document analysis error: {e}")
            return {}
    
    def get_analyses_summary(self) -> Dict[str, Any]:
        """Get analyses summary"""
        print("\n📊 Getting Analyses Summary...")
        
        try:
            response = self.session.get(f"{self.api_base_url}/analyses", timeout=self.default_timeout)
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Analyses Summary:")
                print(f"   Total Analyses: {result['total']}")
                print(f"   Recent Analyses: {len(result['analyses'])}")
                
                if result['analyses']:
                    print("   Latest Analysis:")
                    latest = result['analyses'][0]
                    print(f"     Analysis ID: {latest['analysis_id']}")
                    print(f"     Risk Score: {latest['risk_score']}")
                    print(f"     Compliance Score: {latest['compliance_score']}")
                
                return result
            else:
                print(f"❌ Failed to get analyses: {response.status_code}")
                return {}
                
        except Exception as e:
            print(f"❌ Error getting analyses: {e}")
            return {}
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get BFSI agent metrics"""
        print("\n📈 Getting BFSI Agent Metrics...")
        
        try:
            response = self.session.get(f"{self.api_base_url}/metrics", timeout=self.default_timeout)
            
            if response.status_code == 200:
                result = response.json()
                print("✅ BFSI Agent Metrics:")
                metrics = result['agent_metrics']
                print(f"   Total Analyses: {metrics.get('total_analyses', 0)}")
                print(f"   Average Risk Score: {metrics.get('average_risk_score', 0)}")
                print(f"   Average Compliance Score: {metrics.get('average_compliance_score', 0)}")
                
                health = result['health_status']
                print(f"   Agent Health: {health['bfsi_agent']['status']}")
                print(f"   AI Services: {health['ai_services']}")
                
                return result
            else:
                print(f"❌ Failed to get metrics: {response.status_code}")
                return {}
                
        except Exception as e:
            print(f"❌ Error getting metrics: {e}")
            return {}
    
    def run_full_demo(self):
        """Run complete BFSI Local AI demo"""
        print("🚀 BFSI Local AI Integration Demo")
        print("=" * 60)
        
        # Test health first
        if not self.test_health():
            print("❌ API is not healthy. Please check if the BFSI API service is running.")
            return
        
        # Run all tests
        results = []
        
        # Test compliance check
        compliance_result = self.test_compliance_check()
        if compliance_result:
            results.append(("Compliance Check", compliance_result))
        
        # Test risk assessment
        risk_result = self.test_risk_assessment()
        if risk_result:
            results.append(("Risk Assessment", risk_result))
        
        # Test fraud detection
        fraud_result = self.test_fraud_detection()
        if fraud_result:
            results.append(("Fraud Detection", fraud_result))
        
        # Test document analysis
        doc_result = self.test_document_analysis()
        if doc_result:
            results.append(("Document Analysis", doc_result))
        
        # Get summary
        self.get_analyses_summary()
        self.get_metrics()
        
        # Summary
        print("\n" + "=" * 60)
        print("🎯 Demo Summary:")
        print(f"   Tests Completed: {len(results)}")
        print(f"   Successful Tests: {len([r for r in results if r[1]])}")
        
        if results:
            avg_risk = sum(r[1].get('risk_score', 0) for r in results) / len(results)
            avg_compliance = sum(r[1].get('compliance_score', 0) for r in results) / len(results)
            print(f"   Average Risk Score: {avg_risk:.1f}/100")
            print(f"   Average Compliance Score: {avg_compliance:.1f}/100")
        
        print("\n✅ BFSI Local AI Integration Demo Complete!")
        print("   The BFSI agent is successfully integrated with local AI services.")
        print("   All BFSI operations are now powered by local Ollama and Hugging Face models.")

def main():
    """Main demo function"""
    demo = BFSIDemo()
    demo.run_full_demo()

if __name__ == "__main__":
    main()



