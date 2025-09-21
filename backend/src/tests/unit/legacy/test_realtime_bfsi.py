#!/usr/bin/env python3
"""
Real-Time BFSI System Test
Comprehensive testing of real-time BFSI data processing
"""

import json
import requests
import time
from datetime import datetime
from typing import Dict, Any

class RealTimeBFSITester:
    """Real-Time BFSI System Tester"""
    
    def __init__(self, api_base_url: str = "http://localhost:8009"):
        self.api_base_url = api_base_url
        self.session = requests.Session()
        
    def test_api_health(self) -> bool:
        """Test API health"""
        try:
            response = self.session.get(f"{self.api_base_url}/health")
            if response.status_code == 200:
                health_data = response.json()
                print("✅ Real-Time API Health Check:")
                print(f"   Service: {health_data['service']}")
                print(f"   Status: {health_data['status']}")
                print(f"   Processing: {health_data['processing_active']}")
                print(f"   Database: {health_data['database']}")
                return True
            else:
                print(f"❌ Health check failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Health check error: {e}")
            return False
    
    def test_start_processing(self) -> bool:
        """Test starting real-time processing"""
        try:
            response = self.session.post(f"{self.api_base_url}/start")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Processing Start: {data['message']}")
                return True
            else:
                print(f"❌ Failed to start processing: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Start processing error: {e}")
            return False
    
    def test_stop_processing(self) -> bool:
        """Test stopping real-time processing"""
        try:
            response = self.session.post(f"{self.api_base_url}/stop")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Processing Stop: {data['message']}")
                return True
            else:
                print(f"❌ Failed to stop processing: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Stop processing error: {e}")
            return False
    
    def test_manual_event_processing(self) -> bool:
        """Test manual event processing"""
        print("\n🔄 Testing Manual Event Processing...")
        
        # Test fraud detection event
        fraud_event = {
            "event_type": "fraud_detection",
            "data": {
                "transaction_id": f"TEST-TXN-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
                "amount": 75000,
                "customer_id": "TEST-CUST-001",
                "transaction_type": "Wire Transfer",
                "location": "International",
                "timestamp": datetime.now().isoformat()
            },
            "priority": "high",
            "source_system": "Test System"
        }
        
        try:
            response = self.session.post(
                f"{self.api_base_url}/events/process",
                json=fraud_event
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Fraud Detection Event: {data['message']}")
                print(f"   Event ID: {data['event_id']}")
                print(f"   Queue Position: {data['queue_position']}")
                return True
            else:
                print(f"❌ Failed to process fraud event: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Manual event processing error: {e}")
            return False
    
    def test_status_endpoint(self) -> bool:
        """Test status endpoint"""
        try:
            response = self.session.get(f"{self.api_base_url}/status")
            if response.status_code == 200:
                data = response.json()
                print("\n📊 Real-Time Status:")
                print(f"   Processing Active: {data['processing_status']['active']}")
                print(f"   Queue Size: {data['processing_status']['queue_size']}")
                print(f"   Data Sources: {data['processing_status']['data_sources']}")
                print(f"   Enabled Sources: {data['processing_status']['enabled_sources']}")
                return True
            else:
                print(f"❌ Status check failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Status check error: {e}")
            return False
    
    def test_metrics_endpoint(self) -> bool:
        """Test metrics endpoint"""
        try:
            response = self.session.get(f"{self.api_base_url}/metrics")
            if response.status_code == 200:
                data = response.json()
                print("\n📈 Real-Time Metrics:")
                
                if 'total_processed' in data:
                    print(f"   Total Transactions: {data['total_processed']['transactions']}")
                    print(f"   Total Compliance: {data['total_processed']['compliance_checks']}")
                    print(f"   Total Risk: {data['total_processed']['risk_assessments']}")
                    print(f"   Total Documents: {data['total_processed']['documents']}")
                
                if 'recent_activity_1h' in data:
                    print(f"   Recent Transactions (1h): {data['recent_activity_1h']['transactions']}")
                    print(f"   Recent Compliance (1h): {data['recent_activity_1h']['compliance_checks']}")
                    print(f"   Recent Risk (1h): {data['recent_activity_1h']['risk_assessments']}")
                    print(f"   Recent Documents (1h): {data['recent_activity_1h']['documents']}")
                
                return True
            else:
                print(f"❌ Metrics check failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Metrics check error: {e}")
            return False
    
    def test_events_endpoint(self) -> bool:
        """Test events endpoint"""
        try:
            response = self.session.get(f"{self.api_base_url}/events?limit=10&hours=24")
            if response.status_code == 200:
                data = response.json()
                print(f"\n📋 Recent Events ({data['total_count']} total):")
                
                for i, event in enumerate(data['events'][:5], 1):
                    print(f"   {i}. {event['event_type']} - {event['timestamp']}")
                    if 'risk_score' in event:
                        print(f"      Risk Score: {event['risk_score']}")
                    if 'compliance_score' in event:
                        print(f"      Compliance Score: {event['compliance_score']}")
                
                return True
            else:
                print(f"❌ Events check failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Events check error: {e}")
            return False
    
    def test_data_sources_endpoint(self) -> bool:
        """Test data sources endpoint"""
        try:
            response = self.session.get(f"{self.api_base_url}/data-sources")
            if response.status_code == 200:
                data = response.json()
                print(f"\n🔗 Data Sources ({len(data['data_sources'])} configured):")
                
                for source in data['data_sources']:
                    print(f"   - {source['name']} ({source['type']}) - {'Enabled' if source['enabled'] else 'Disabled'}")
                
                return True
            else:
                print(f"❌ Data sources check failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Data sources check error: {e}")
            return False
    
    def test_dashboard_endpoint(self) -> bool:
        """Test dashboard endpoint"""
        try:
            response = self.session.get(f"{self.api_base_url}/dashboard")
            if response.status_code == 200:
                data = response.json()
                print("\n🎯 Dashboard Data:")
                print(f"   Processing Active: {data['dashboard']['system_status']['processing_active']}")
                print(f"   Queue Size: {data['dashboard']['system_status']['queue_size']}")
                print(f"   Recent Events: {len(data['dashboard']['recent_activity']['events'])}")
                return True
            else:
                print(f"❌ Dashboard check failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Dashboard check error: {e}")
            return False
    
    def run_comprehensive_test(self):
        """Run comprehensive real-time system test"""
        print("🚀 Real-Time BFSI System Test")
        print("=" * 60)
        
        # Test API health
        if not self.test_api_health():
            print("❌ API is not healthy. Please check if the Real-Time BFSI API service is running.")
            return
        
        # Test all endpoints
        tests = [
            ("Status Endpoint", self.test_status_endpoint),
            ("Metrics Endpoint", self.test_metrics_endpoint),
            ("Events Endpoint", self.test_events_endpoint),
            ("Data Sources Endpoint", self.test_data_sources_endpoint),
            ("Dashboard Endpoint", self.test_dashboard_endpoint),
            ("Manual Event Processing", self.test_manual_event_processing),
            ("Start Processing", self.test_start_processing),
            ("Stop Processing", self.test_stop_processing)
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            print(f"\n🧪 Testing {test_name}...")
            if test_func():
                passed += 1
                print(f"✅ {test_name} - PASSED")
            else:
                print(f"❌ {test_name} - FAILED")
        
        # Summary
        print("\n" + "=" * 60)
        print(f"🎯 Test Summary: {passed}/{total} tests passed")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        if passed == total:
            print("🎉 All tests passed! Real-Time BFSI system is working correctly.")
        else:
            print("⚠️ Some tests failed. Please check the system configuration.")
    
    def run_live_monitoring_test(self, duration_minutes: int = 5):
        """Run live monitoring test"""
        print(f"\n🔍 Live Monitoring Test ({duration_minutes} minutes)")
        print("=" * 60)
        
        # Start processing
        print("Starting real-time processing...")
        if not self.test_start_processing():
            print("❌ Failed to start processing")
            return
        
        start_time = time.time()
        end_time = start_time + (duration_minutes * 60)
        
        print(f"Monitoring for {duration_minutes} minutes...")
        print("Press Ctrl+C to stop early")
        
        try:
            while time.time() < end_time:
                # Get current status
                response = self.session.get(f"{self.api_base_url}/status")
                if response.status_code == 200:
                    data = response.json()
                    queue_size = data['processing_status']['queue_size']
                    active = data['processing_status']['active']
                    
                    elapsed = int(time.time() - start_time)
                    remaining = int(end_time - time.time())
                    
                    print(f"[{elapsed:03d}s] Queue: {queue_size:2d} | Active: {'✅' if active else '❌'} | Remaining: {remaining:03d}s")
                
                time.sleep(10)  # Check every 10 seconds
            
            print(f"\n✅ Live monitoring completed ({duration_minutes} minutes)")
            
        except KeyboardInterrupt:
            print(f"\n⏹️ Live monitoring stopped by user")
        
        finally:
            # Stop processing
            print("Stopping real-time processing...")
            self.test_stop_processing()

def main():
    """Main test function"""
    tester = RealTimeBFSITester()
    
    print("Choose test mode:")
    print("1. Comprehensive Test")
    print("2. Live Monitoring Test")
    print("3. Both")
    
    choice = input("Enter choice (1-3): ").strip()
    
    if choice == "1":
        tester.run_comprehensive_test()
    elif choice == "2":
        duration = int(input("Enter monitoring duration in minutes (default 5): ") or "5")
        tester.run_live_monitoring_test(duration)
    elif choice == "3":
        tester.run_comprehensive_test()
        input("\nPress Enter to start live monitoring test...")
        duration = int(input("Enter monitoring duration in minutes (default 5): ") or "5")
        tester.run_live_monitoring_test(duration)
    else:
        print("Invalid choice. Running comprehensive test...")
        tester.run_comprehensive_test()

if __name__ == "__main__":
    main()



