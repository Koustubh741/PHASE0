#!/usr/bin/env python3
"""
Real-Time BFSI Command Line Interface
Simple CLI for interacting with the real-time BFSI system
"""

import requests
import json
import time
from datetime import datetime
from pathlib import Path

class BFSICLI:
    def __init__(self, api_base_url="http://localhost:8009"):
        self.api_base_url = api_base_url
        self.session = requests.Session()
        self.timeout = 30  # Default timeout in seconds
    
    def print_header(self, title):
        print(f"\n{'='*60}")
        print(f"🚀 {title}")
        print(f"{'='*60}")
    
    def print_status(self, message, status="info"):
        icons = {"success": "✅", "error": "❌", "warning": "⚠️", "info": "ℹ️"}
        print(f"{icons.get(status, 'ℹ️')} {message}")
    
    def get_health(self):
        """Get system health"""
        try:
            response = self.session.get(f"{self.api_base_url}/health", timeout=self.timeout)
            if response.status_code == 200:
                data = response.json()
                self.print_header("System Health")
                print(f"Service: {data['service']}")
                print(f"Status: {data['status']}")
                print(f"Processing: {'Active' if data['processing_active'] else 'Inactive'}")
                print(f"Database: {data['database']}")
                return True
            else:
                self.print_status(f"Health check failed: {response.status_code}", "error")
                return False
        except Exception as e:
            self.print_status(f"Health check error: {e}", "error")
            return False
    
    def get_status(self):
        """Get processing status"""
        try:
            response = self.session.get(f"{self.api_base_url}/status", timeout=self.timeout)
            if response.status_code == 200:
                data = response.json()
                self.print_header("Processing Status")
                print(f"Processing Active: {'✅ Yes' if data['processing_status']['active'] else '❌ No'}")
                print(f"Queue Size: {data['processing_status']['queue_size']}")
                print(f"Data Sources: {data['processing_status']['data_sources']}")
                print(f"Enabled Sources: {data['processing_status']['enabled_sources']}")
                return True
            else:
                self.print_status(f"Status check failed: {response.status_code}", "error")
                return False
        except Exception as e:
            self.print_status(f"Status check error: {e}", "error")
            return False
    
    def get_metrics(self):
        """Get processing metrics"""
        try:
            response = self.session.get(f"{self.api_base_url}/metrics", timeout=self.timeout)
            if response.status_code == 200:
                data = response.json()
                self.print_header("Processing Metrics")
                
                if 'total_processed' in data:
                    print("📊 Total Processed:")
                    print(f"   Transactions: {data['total_processed']['transactions']}")
                    print(f"   Compliance Checks: {data['total_processed']['compliance_checks']}")
                    print(f"   Risk Assessments: {data['total_processed']['risk_assessments']}")
                    print(f"   Documents: {data['total_processed']['documents']}")
                
                if 'recent_activity_1h' in data:
                    print("\n⚡ Recent Activity (1 hour):")
                    print(f"   Transactions: {data['recent_activity_1h']['transactions']}")
                    print(f"   Compliance: {data['recent_activity_1h']['compliance_checks']}")
                    print(f"   Risk: {data['recent_activity_1h']['risk_assessments']}")
                    print(f"   Documents: {data['recent_activity_1h']['documents']}")
                
                return True
            else:
                self.print_status(f"Metrics check failed: {response.status_code}", "error")
                return False
        except Exception as e:
            self.print_status(f"Metrics check error: {e}", "error")
            return False
    
    def get_events(self, limit=10):
        """Get recent events"""
        try:
            response = self.session.get(f"{self.api_base_url}/events?limit={limit}&hours=24", timeout=self.timeout)
            if response.status_code == 200:
                data = response.json()
                self.print_header(f"Recent Events ({data['total_count']} total)")
                
                for i, event in enumerate(data['events'][:limit], 1):
                    print(f"\n{i}. {event['event_type'].replace('_', ' ').title()}")
                    print(f"   Time: {event['timestamp']}")
                    
                    if 'risk_score' in event:
                        print(f"   Risk Score: {event['risk_score']}")
                    if 'compliance_score' in event:
                        print(f"   Compliance Score: {event['compliance_score']}")
                    
                    # Show specific details based on event type
                    if event['event_type'] == 'fraud_detection':
                        if 'transaction_id' in event:
                            print(f"   Transaction: {event['transaction_id']}")
                        if 'amount' in event:
                            print(f"   Amount: ${event['amount']:,.2f}")
                    elif event['event_type'] == 'compliance_check':
                        if 'regulation' in event:
                            print(f"   Regulation: {event['regulation']}")
                    elif event['event_type'] == 'risk_assessment':
                        if 'risk_type' in event:
                            print(f"   Risk Type: {event['risk_type']}")
                    elif event['event_type'] == 'document_analysis':
                        if 'document_type' in event:
                            print(f"   Document: {event['document_type']}")
                
                return True
            else:
                self.print_status(f"Events check failed: {response.status_code}", "error")
                return False
        except Exception as e:
            self.print_status(f"Events check error: {e}", "error")
            return False
    
    def start_processing(self):
        """Start real-time processing"""
        try:
            response = self.session.post(f"{self.api_base_url}/start", timeout=self.timeout)
            if response.status_code == 200:
                data = response.json()
                self.print_status(f"Processing started: {data['message']}", "success")
                return True
            else:
                self.print_status(f"Failed to start processing: {response.status_code}", "error")
                return False
        except Exception as e:
            self.print_status(f"Start processing error: {e}", "error")
            return False
    
    def stop_processing(self):
        """Stop real-time processing"""
        try:
            response = self.session.post(f"{self.api_base_url}/stop", timeout=self.timeout)
            if response.status_code == 200:
                data = response.json()
                self.print_status(f"Processing stopped: {data['message']}", "warning")
                return True
            else:
                self.print_status(f"Failed to stop processing: {response.status_code}", "error")
                return False
        except Exception as e:
            self.print_status(f"Stop processing error: {e}", "error")
            return False
    
    def process_manual_event(self, event_type="fraud_detection"):
        """Process a manual event"""
        # Sample data for different event types
        sample_data = {
            "fraud_detection": {
                "transaction_id": f"MANUAL-TXN-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
                "amount": 125000,
                "customer_id": "MANUAL-CUST-001",
                "transaction_type": "Wire Transfer",
                "location": "International",
                "timestamp": datetime.now().isoformat()
            },
            "compliance_check": {
                "regulation": "SOX",
                "process": "Financial Reporting",
                "controls": ["Access Control", "Data Integrity", "Audit Trail"],
                "documents": [f"SOX_Manual_{datetime.now().strftime('%Y%m%d')}.pdf"],
                "priority": "high"
            },
            "risk_assessment": {
                "risk_type": "Credit Risk",
                "portfolio": "Corporate Loans",
                "exposure": 15000000,
                "probability": "high",
                "impact": "high",
                "controls": ["Credit Scoring", "Collateral Management"]
            },
            "document_analysis": {
                "document_type": "Loan Agreement",
                "content": f"Manual Loan Agreement - Generated {datetime.now().isoformat()}\n\nThis is a manually submitted document for AI analysis.",
                "classification": "Credit Documentation",
                "compliance_framework": "Basel III"
            }
        }
        
        event_data = sample_data.get(event_type, sample_data["fraud_detection"])
        
        try:
            response = self.session.post(
                f"{self.api_base_url}/events/process",
                json={
                    "event_type": event_type,
                    "data": event_data,
                    "priority": "high",
                    "source_system": "CLI Manual Input"
                },
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                self.print_status(f"Manual {event_type} event queued", "success")
                print(f"   Event ID: {data['event_id']}")
                print(f"   Queue Position: {data['queue_position']}")
                return True
            else:
                self.print_status(f"Failed to process manual event: {response.status_code}", "error")
                return False
        except Exception as e:
            self.print_status(f"Manual event processing error: {e}", "error")
            return False
    
    def monitor_live(self, duration_minutes=5):
        """Monitor live processing"""
        self.print_header(f"Live Monitoring ({duration_minutes} minutes)")
        
        if not self.start_processing():
            return
        
        start_time = time.time()
        end_time = start_time + (duration_minutes * 60)
        
        print("Monitoring real-time processing...")
        print("Press Ctrl+C to stop early")
        
        try:
            while time.time() < end_time:
                response = self.session.get(f"{self.api_base_url}/status", timeout=self.timeout)
                if response.status_code == 200:
                    data = response.json()
                    queue_size = data['processing_status']['queue_size']
                    active = data['processing_status']['active']
                    
                    elapsed = int(time.time() - start_time)
                    remaining = int(end_time - time.time())
                    
                    status_icon = "✅" if active else "❌"
                    print(f"[{elapsed:03d}s] Queue: {queue_size:2d} | Active: {status_icon} | Remaining: {remaining:03d}s")
                
                time.sleep(10)
            
            self.print_status(f"Live monitoring completed ({duration_minutes} minutes)", "success")
            
        except KeyboardInterrupt:
            self.print_status("Live monitoring stopped by user", "warning")
        
        finally:
            self.stop_processing()
    
    def show_menu(self):
        """Show main menu"""
        self.print_header("Real-Time BFSI System Interface")
        print("Available commands:")
        print("1. Health Check")
        print("2. Status")
        print("3. Metrics")
        print("4. Recent Events")
        print("5. Start Processing")
        print("6. Stop Processing")
        print("7. Process Manual Event")
        print("8. Live Monitor")
        print("9. Open Web Dashboard")
        print("0. Exit")
    
    def run(self):
        """Run interactive CLI"""
        while True:
            self.show_menu()
            
            try:
                choice = input("\nEnter your choice (0-9): ").strip()
                
                if choice == "0":
                    self.print_status("Goodbye!", "info")
                    break
                elif choice == "1":
                    self.get_health()
                elif choice == "2":
                    self.get_status()
                elif choice == "3":
                    self.get_metrics()
                elif choice == "4":
                    limit = input("Enter number of events to show (default 10): ").strip()
                    limit = int(limit) if limit.isdigit() else 10
                    self.get_events(limit)
                elif choice == "5":
                    self.start_processing()
                elif choice == "6":
                    self.stop_processing()
                elif choice == "7":
                    print("\nEvent types:")
                    print("1. fraud_detection")
                    print("2. compliance_check")
                    print("3. risk_assessment")
                    print("4. document_analysis")
                    event_choice = input("Enter event type (1-4): ").strip()
                    event_types = ["fraud_detection", "compliance_check", "risk_assessment", "document_analysis"]
                    if event_choice.isdigit() and 1 <= int(event_choice) <= 4:
                        self.process_manual_event(event_types[int(event_choice)-1])
                    else:
                        self.print_status("Invalid choice", "error")
                elif choice == "8":
                    duration = input("Enter monitoring duration in minutes (default 5): ").strip()
                    duration = int(duration) if duration.isdigit() else 5
                    self.monitor_live(duration)
                elif choice == "9":
                    self.print_status("Opening web dashboard...", "info")
                    # Construct file URI using pathlib for proper cross-platform path handling
                    dashboard_path = Path(__file__).parent / "realtime_bfsi_dashboard.html"
                    dashboard_uri = dashboard_path.as_uri()
                    print(f"🌐 Dashboard URL: {dashboard_uri}")
                    print("Or open: realtime_bfsi_dashboard.html in your browser")
                else:
                    self.print_status("Invalid choice", "error")
                
                input("\nPress Enter to continue...")
                
            except KeyboardInterrupt:
                self.print_status("\nGoodbye!", "info")
                break
            except Exception as e:
                self.print_status(f"Error: {e}", "error")
                input("Press Enter to continue...")

if __name__ == "__main__":
    cli = BFSICLI()
    cli.run()



