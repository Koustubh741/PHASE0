#!/usr/bin/env python3
"""
Quick BFSI Policy Upload
Fast script to upload policies without interactive menus
"""

import sys
from bfsi_policy_uploader import upload_policy_text, get_policy_statistics

def upload_policy_quick(title, content, policy_type="compliance", framework="SOX"):
    """Quickly upload a policy"""
    try:
        policy_id = upload_policy_text(title, content, policy_type, framework)
        print(f"✅ Policy uploaded: {policy_id}")
        return policy_id
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def main():
    if len(sys.argv) < 2:
        print("Usage: python quick_policy_upload.py <title> [policy_type] [framework]")
        print("Example: python quick_policy_upload.py 'SOX Policy' compliance SOX")
        print("\nOr use the web interface for easier uploads!")
        return
    
    title = sys.argv[1]
    policy_type = sys.argv[2] if len(sys.argv) > 2 else "compliance"
    framework = sys.argv[3] if len(sys.argv) > 3 else "SOX"
    
    # Sample policy content
    sample_content = f"""
{title.upper()}

1. PURPOSE
This policy establishes the framework for {policy_type} requirements in accordance with {framework} regulations.

2. SCOPE
This policy applies to all relevant processes and personnel within the organization.

3. REQUIREMENTS
- Compliance with {framework} standards
- Regular monitoring and assessment
- Documentation and record keeping
- Training and awareness programs
- Incident reporting procedures

4. IMPLEMENTATION
- Automated monitoring systems
- Regular audits and reviews
- Staff training programs
- Policy updates and maintenance

5. RESPONSIBILITIES
- Management: Overall oversight and compliance
- Staff: Adherence to policy requirements
- IT: System controls and security
- Audit: Independent verification

This policy is effective immediately and must be reviewed annually.
    """
    
    print(f"🚀 Uploading {title}...")
    policy_id = upload_policy_quick(title, sample_content, policy_type, framework)
    
    if policy_id:
        print(f"\n📊 Current Statistics:")
        stats = get_policy_statistics()
        print(f"   Total Policies: {stats['total_policies']}")
        print(f"   By Type: {stats['policies_by_type']}")
        print(f"   By Framework: {stats['policies_by_framework']}")

if __name__ == "__main__":
    main()



