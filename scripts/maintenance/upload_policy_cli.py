#!/usr/bin/env python3
"""
BFSI Policy Upload CLI
Simple command-line interface for uploading BFSI policies
"""

import os
import webbrowser
from pathlib import Path
from bfsi_policy_uploader import upload_policy_file, upload_policy_text, get_policy_statistics, policy_manager

def print_header(title):
    print(f"\n{'='*60}")
    print(f"🚀 {title}")
    print(f"{'='*60}")

def print_success(message):
    print(f"✅ {message}")

def print_error(message):
    print(f"❌ {message}")

def print_info(message):
    print(f"ℹ️ {message}")

def upload_file_policy():
    """Upload policy from file"""
    print_header("Upload Policy from File")
    
    file_path = input("Enter file path: ").strip()
    
    if not os.path.exists(file_path):
        print_error(f"File not found: {file_path}")
        return
    
    # Get policy metadata
    title = input("Policy title (or press Enter to use filename): ").strip()
    if not title:
        title = Path(file_path).stem
    
    print("\nPolicy types:")
    print("1. compliance")
    print("2. risk")
    print("3. fraud")
    print("4. operational")
    print("5. security")
    print("6. audit")
    
    type_choice = input("Select policy type (1-6): ").strip()
    type_map = {
        "1": "compliance",
        "2": "risk", 
        "3": "fraud",
        "4": "operational",
        "5": "security",
        "6": "audit"
    }
    
    policy_type = type_map.get(type_choice, "compliance")
    
    print("\nRegulatory frameworks:")
    print("1. SOX")
    print("2. PCI DSS")
    print("3. Basel III")
    print("4. GDPR")
    print("5. CCPA")
    print("6. FATCA")
    print("7. AML")
    print("8. KYC")
    print("9. Other")
    
    framework_choice = input("Select framework (1-9): ").strip()
    framework_map = {
        "1": "SOX",
        "2": "PCI DSS",
        "3": "Basel III",
        "4": "GDPR",
        "5": "CCPA",
        "6": "FATCA",
        "7": "AML",
        "8": "KYC",
        "9": "Other"
    }
    
    framework = framework_map.get(framework_choice, "SOX")
    
    version = input("Policy version (default 1.0): ").strip() or "1.0"
    
    try:
        policy_id = upload_policy_file(file_path, policy_type, framework, version, {"title": title})
        print_success(f"Policy uploaded successfully: {policy_id}")
    except Exception as e:
        print_error(f"Error uploading policy: {e}")

def upload_text_policy():
    """Upload policy from text input"""
    print_header("Upload Policy from Text")
    
    title = input("Policy title: ").strip()
    if not title:
        print_error("Policy title is required")
        return
    
    print("\nEnter policy content (press Enter twice when done):")
    content_lines = []
    while True:
        line = input()
        if line == "" and len(content_lines) > 0 and content_lines[-1] == "":
            break
        content_lines.append(line)
    
    content = "\n".join(content_lines).strip()
    if not content:
        print_error("Policy content is required")
        return
    
    # Get policy metadata
    print("\nPolicy types:")
    print("1. compliance")
    print("2. risk")
    print("3. fraud")
    print("4. operational")
    print("5. security")
    print("6. audit")
    
    type_choice = input("Select policy type (1-6): ").strip()
    type_map = {
        "1": "compliance",
        "2": "risk",
        "3": "fraud",
        "4": "operational",
        "5": "security",
        "6": "audit"
    }
    
    policy_type = type_map.get(type_choice, "compliance")
    
    print("\nRegulatory frameworks:")
    print("1. SOX")
    print("2. PCI DSS")
    print("3. Basel III")
    print("4. GDPR")
    print("5. CCPA")
    print("6. FATCA")
    print("7. AML")
    print("8. KYC")
    print("9. Other")
    
    framework_choice = input("Select framework (1-9): ").strip()
    framework_map = {
        "1": "SOX",
        "2": "PCI DSS",
        "3": "Basel III",
        "4": "GDPR",
        "5": "CCPA",
        "6": "FATCA",
        "7": "AML",
        "8": "KYC",
        "9": "Other"
    }
    
    framework = framework_map.get(framework_choice, "SOX")
    
    version = input("Policy version (default 1.0): ").strip() or "1.0"
    
    try:
        policy_id = upload_policy_text(title, content, policy_type, framework, version)
        print_success(f"Policy uploaded successfully: {policy_id}")
    except Exception as e:
        print_error(f"Error uploading policy: {e}")

def view_statistics():
    """View policy statistics"""
    print_header("Policy Statistics")
    
    try:
        stats = get_policy_statistics()
        
        print(f"Total Policies: {stats['total_policies']}")
        print(f"Total Datasets: {stats['total_datasets']}")
        print(f"Total Chunks: {stats['total_chunks']}")
        
        print(f"\nPolicies by Type:")
        for policy_type, count in stats['policies_by_type'].items():
            print(f"  {policy_type}: {count}")
        
        print(f"\nPolicies by Framework:")
        for framework, count in stats['policies_by_framework'].items():
            print(f"  {framework}: {count}")
            
    except Exception as e:
        print_error(f"Error getting statistics: {e}")

def view_policies():
    """View all policies"""
    print_header("Uploaded Policies")
    
    try:
        policies = policy_manager.get_all_policies()
        
        if not policies:
            print_info("No policies uploaded yet")
            return
        
        for i, policy in enumerate(policies, 1):
            print(f"\n{i}. {policy.title}")
            print(f"   ID: {policy.policy_id}")
            print(f"   Type: {policy.policy_type}")
            print(f"   Framework: {policy.framework}")
            print(f"   Version: {policy.version}")
            print(f"   Uploaded: {policy.upload_date.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"   Content: {policy.content[:100]}...")
            
    except Exception as e:
        print_error(f"Error getting policies: {e}")

def create_sample_policies():
    """Create sample BFSI policies"""
    print_header("Create Sample BFSI Policies")
    
    sample_policies = [
        {
            "title": "SOX Compliance Policy",
            "content": """
SARBANES-OXLEY ACT COMPLIANCE POLICY

1. PURPOSE
This policy establishes the framework for compliance with the Sarbanes-Oxley Act (SOX) requirements for financial reporting and internal controls.

2. SCOPE
This policy applies to all financial reporting, internal controls, and audit processes within the organization.

3. REQUIREMENTS
- All financial statements must be accurate and complete
- Internal controls must be documented and tested regularly
- Audit trails must be maintained for all financial transactions
- Management must certify financial reports
- Independent audit committee oversight required

4. IMPLEMENTATION
- Quarterly control testing
- Annual risk assessments
- Continuous monitoring systems
- Regular training programs
- Incident reporting procedures

5. RESPONSIBILITIES
- CFO: Overall financial reporting responsibility
- Internal Audit: Control testing and validation
- Management: Certification and oversight
- IT: System controls and security

This policy is effective immediately and must be reviewed annually.
            """,
            "policy_type": "compliance",
            "framework": "SOX",
            "version": "2.1"
        },
        {
            "title": "PCI DSS Security Standards",
            "content": """
PAYMENT CARD INDUSTRY DATA SECURITY STANDARDS (PCI DSS)

1. OVERVIEW
This policy outlines the requirements for protecting payment card data according to PCI DSS standards.

2. CARDHOLDER DATA PROTECTION
- Primary Account Number (PAN) must be encrypted
- Cardholder names, expiration dates, and service codes must be protected
- Sensitive authentication data must never be stored
- Data retention policies must be enforced

3. NETWORK SECURITY
- Firewall configuration and maintenance
- Default passwords must be changed
- Network segmentation for card data
- Regular security updates and patches

4. ACCESS CONTROL
- Unique user IDs for each person with computer access
- Strong password requirements
- Regular access reviews and deactivation
- Physical access restrictions

5. MONITORING AND TESTING
- Regular network scans and penetration testing
- Security monitoring and incident response
- Vulnerability management program
- Regular security awareness training

6. COMPLIANCE
- Annual compliance assessments required
- Quarterly security scans mandated
- Incident reporting within 24 hours
- Regular policy reviews and updates

This policy ensures compliance with PCI DSS requirements and protects customer payment data.
            """,
            "policy_type": "security",
            "framework": "PCI DSS",
            "version": "3.2.1"
        },
        {
            "title": "Basel III Risk Management Framework",
            "content": """
BASEL III RISK MANAGEMENT FRAMEWORK

1. INTRODUCTION
This policy establishes the risk management framework in accordance with Basel III regulatory requirements.

2. CAPITAL ADEQUACY
- Minimum Common Equity Tier 1 (CET1) ratio of 4.5%
- Tier 1 capital ratio of 6.0%
- Total capital ratio of 8.0%
- Capital conservation buffer of 2.5%
- Countercyclical buffer as required

3. RISK MEASUREMENT
- Credit risk assessment using standardized and internal ratings-based approaches
- Market risk measurement using Value-at-Risk (VaR) models
- Operational risk assessment using standardized and advanced approaches
- Liquidity risk monitoring using Liquidity Coverage Ratio (LCR)

4. RISK GOVERNANCE
- Board-level risk oversight
- Chief Risk Officer (CRO) appointment
- Independent risk management function
- Regular risk reporting to regulators

5. STRESS TESTING
- Annual stress testing programs
- Scenario analysis and sensitivity testing
- Reverse stress testing requirements
- Recovery and resolution planning

6. DISCLOSURE REQUIREMENTS
- Quarterly public disclosure of risk metrics
- Annual Pillar 3 disclosure requirements
- Regulatory reporting compliance
- Transparency and market discipline

This framework ensures robust risk management and regulatory compliance.
            """,
            "policy_type": "risk",
            "framework": "Basel III",
            "version": "1.0"
        }
    ]
    
    try:
        for policy_data in sample_policies:
            policy_id = upload_policy_text(
                title=policy_data["title"],
                content=policy_data["content"],
                policy_type=policy_data["policy_type"],
                framework=policy_data["framework"],
                version=policy_data["version"]
            )
            print_success(f"Created: {policy_data['title']} ({policy_id})")
        
        print_success("All sample policies created successfully!")
        
    except Exception as e:
        print_error(f"Error creating sample policies: {e}")

def show_menu():
    """Show main menu"""
    print_header("BFSI Policy Upload CLI")
    print("Available options:")
    print("1. Upload policy from file")
    print("2. Upload policy from text input")
    print("3. View policy statistics")
    print("4. View all policies")
    print("5. Create sample BFSI policies")
    print("6. Open web interface")
    print("0. Exit")

def main():
    """Main function"""
    while True:
        show_menu()
        
        try:
            choice = input("\nEnter your choice (0-6): ").strip()
            
            if choice == "0":
                print_success("Goodbye!")
                break
            elif choice == "1":
                upload_file_policy()
            elif choice == "2":
                upload_text_policy()
            elif choice == "3":
                view_statistics()
            elif choice == "4":
                view_policies()
            elif choice == "5":
                create_sample_policies()
            elif choice == "6":
                print_info("Opening web interface...")
                webbrowser.open("bfsi_policy_upload_interface.html")
            else:
                print_error("Invalid choice")
            
            input("\nPress Enter to continue...")
            
        except KeyboardInterrupt:
            print_success("\nGoodbye!")
            break
        except Exception as e:
            print_error(f"Error: {e}")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()



