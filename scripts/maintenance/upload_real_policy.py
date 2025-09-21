#!/usr/bin/env python3
"""
Upload Real BFSI Policy
Simple script to upload your actual policy files
"""

import os
import sys
from pathlib import Path
from bfsi_policy_uploader import upload_policy_file

# Security validation functions
def validate_file_path(file_path):
    """
    Validate file path for security:
    - Prevent path traversal attacks
    - Check file extension is allowed
    - Ensure path is within allowed directories
    """
    # Allowed file extensions for policy documents
    ALLOWED_EXTENSIONS = {'.txt', '.pdf', '.doc', '.docx'}
    
    # Convert to Path object for easier manipulation
    path = Path(file_path)
    
    # Check if file exists
    if not path.exists():
        return False, f"File not found: {file_path}"
    
    # Check if it's a file (not directory)
    if not path.is_file():
        return False, f"Path is not a file: {file_path}"
    
    # Check file extension
    file_extension = path.suffix.lower()
    if file_extension not in ALLOWED_EXTENSIONS:
        allowed_exts = ', '.join(ALLOWED_EXTENSIONS)
        return False, f"Invalid file type '{file_extension}'. Allowed types: {allowed_exts}"
    
    # Prevent path traversal attacks
    try:
        # Resolve the path to get absolute path
        resolved_path = path.resolve()
        
        # Ensure the resolved path doesn't escape current directory
        current_dir = Path.cwd().resolve()
        resolved_path.relative_to(current_dir)
        
        # Optional: Restrict to specific allowed directories
        # You can uncomment and modify this section to restrict uploads to specific directories
        # ALLOWED_DIRS = [Path.cwd() / "uploads", Path.cwd() / "policies"]
        # if not any(resolved_path.is_relative_to(allowed_dir) for allowed_dir in ALLOWED_DIRS):
        #     return False, f"File must be in allowed directories"
        
    except (OSError, ValueError) as e:
        return False, f"Invalid path: {file_path} - {str(e)}"
    
    return True, "Valid file path"


def validate_directory_path(directory_path):
    """
    Validate directory path for security:
    - Ensure path is absolute and normalized
    - Prevent path traversal attacks
    - Check that directory resides within approved base directory
    - Reject any input paths outside allowed scope
    """
    
    # Define approved base directories for security
    APPROVED_BASE_DIRS = [
        Path.cwd().resolve(),  # Current working directory
        Path.cwd().resolve() / "policies",  # Policies subdirectory
        Path.cwd().resolve() / "uploads",  # Uploads subdirectory
        Path.cwd().resolve() / "bfsi_policies",  # BFSI policies directory
    ]
    
    try:
        # Convert to Path object
        dir_path = Path(directory_path)
        
        # Check if directory exists
        if not dir_path.exists():
            return False, f"Directory not found: {directory_path}"
        
        # Check if it's actually a directory
        if not dir_path.is_dir():
            return False, f"Path is not a directory: {directory_path}"
        
        # Resolve to absolute path and normalize
        resolved_dir = dir_path.resolve()
        normalized_dir = os.path.normpath(str(resolved_dir))
        
        # Security check 1: Ensure path is absolute
        if not resolved_dir.is_absolute():
            return False, f"Directory path must be absolute: {directory_path}"
        
        # Security check 2: Prevent path traversal patterns in input
        input_path_str = str(directory_path)
        dangerous_patterns = ['..', '~', '//', '\\\\', '../', '..\\']
        for pattern in dangerous_patterns:
            if pattern in input_path_str:
                return False, f"Path traversal pattern detected in input: {pattern}"
        
        # Security check 3: Check that resolved directory is within approved base directories
        is_within_approved = False
        for approved_dir in APPROVED_BASE_DIRS:
            try:
                # Check if the resolved directory is within the approved directory
                resolved_dir.relative_to(approved_dir)
                is_within_approved = True
                break
            except ValueError:
                # Directory is not within this approved directory, continue checking others
                continue
        
        if not is_within_approved:
            approved_dirs_str = ', '.join([str(d) for d in APPROVED_BASE_DIRS])
            return False, f"Directory must be within approved base directories: {approved_dirs_str}"
        
        # Security check 4: Additional validation for Windows paths
        if os.name == 'nt':  # Windows
            # Check for UNC paths and other Windows-specific security issues
            path_str = str(resolved_dir).lower()
            # Check if it's a valid UNC path or drive letter path
            if not (path_str.startswith('\\\\') or (len(path_str) >= 2 and path_str[1] == ':')):
                return False, f"Invalid Windows path format: {directory_path}"
        
        # Security check 5: Ensure directory is readable
        if not os.access(resolved_dir, os.R_OK):
            return False, f"Directory is not readable: {directory_path}"
        
        return True, f"Valid directory path: {normalized_dir}"
        
    except (OSError, ValueError, PermissionError) as e:
        return False, f"Invalid directory path: {directory_path} - {str(e)}"

def upload_real_policy():
    """Upload your real BFSI policy"""
    
    print("🚀 BFSI Policy Upload - Real Data")
    print("=" * 50)
    
    # Get file path with security validation
    file_path = input("Enter the path to your policy file: ").strip().replace('"', '')
    
    # Validate file path for security
    is_valid, message = validate_file_path(file_path)
    if not is_valid:
        print(f"❌ {message}")
        return
    
    print(f"📁 Found file: {file_path}")
    
    # Get policy metadata
    print("\n📋 Policy Information:")
    
    title = input("Policy title (or press Enter for filename): ").strip()
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
    
    # Upload the policy
    try:
        print(f"\n📤 Uploading policy...")
        policy_id = upload_policy_file(file_path, policy_type, framework, version)
        print(f"✅ SUCCESS! Policy uploaded with ID: {policy_id}")
        print(f"   Title: {title}")
        print(f"   Type: {policy_type}")
        print(f"   Framework: {framework}")
        print(f"   Version: {version}")
        
        print(f"\n🎯 Next steps:")
        print(f"   1. Upload more policies if needed")
        print(f"   2. Create training dataset")
        print(f"   3. Train your LLM models")
        
    except Exception as e:
        print(f"❌ Error uploading policy: {e}")

def upload_multiple_policies():
    """Upload multiple policies from a directory"""
    
    print("🚀 Upload Multiple BFSI Policies")
    print("=" * 50)
    
    directory = input("Enter directory path containing policy files: ").strip().replace('"', '')
    
    # Validate directory path for security using enhanced validation
    is_valid, message = validate_directory_path(directory)
    if not is_valid:
        print(f"❌ {message}")
        return
    
    print(f"✅ {message}")
    
    # Find policy files
    policy_files = []
    for ext in ['.txt', '.pdf', '.doc', '.docx']:
        policy_files.extend(Path(directory).glob(f'*{ext}'))
    
    if not policy_files:
        print(f"❌ No policy files found in: {directory}")
        return
    
    print(f"📁 Found {len(policy_files)} policy files:")
    for i, file in enumerate(policy_files, 1):
        print(f"   {i}. {file.name}")
    
    print(f"\n📋 Default settings for all policies:")
    policy_type = input("Policy type (compliance/risk/fraud/operational/security/audit): ").strip() or "compliance"
    framework = input("Framework (SOX/PCI DSS/Basel III/GDPR/etc): ").strip() or "SOX"
    version = input("Version (default 1.0): ").strip() or "1.0"
    
    # Upload all files with security validation
    success_count = 0
    for i, file_path in enumerate(policy_files, 1):
        try:
            print(f"\n📤 Uploading {i}/{len(policy_files)}: {file_path.name}")
            
            # Validate each file before upload
            is_valid, message = validate_file_path(str(file_path))
            if not is_valid:
                print(f"❌ Skipping {file_path.name}: {message}")
                continue
            
            policy_id = upload_policy_file(str(file_path), policy_type, framework, version)
            print(f"✅ Success: {policy_id}")
            success_count += 1
        except Exception as e:
            print(f"❌ Failed: {e}")
    
    print(f"\n🎯 Upload complete: {success_count}/{len(policy_files)} policies uploaded successfully")

def main():
    print("Choose upload method:")
    print("1. Upload single policy file")
    print("2. Upload multiple policies from directory")
    print("3. Enter policy content manually")
    
    choice = input("Enter choice (1-3): ").strip()
    
    if choice == "1":
        upload_real_policy()
    elif choice == "2":
        upload_multiple_policies()
    elif choice == "3":
        upload_manual_policy()
    else:
        print("Invalid choice")

def upload_manual_policy():
    """Upload policy by manually entering content"""
    
    print("🚀 Manual Policy Entry")
    print("=" * 50)
    
    title = input("Policy title: ").strip()
    if not title:
        print("❌ Title is required")
        return
    
    print("\nEnter your policy content (press Enter twice when done):")
    content_lines = []
    while True:
        line = input()
        if line == "" and len(content_lines) > 0 and content_lines[-1] == "":
            break
        content_lines.append(line)
    
    content = "\n".join(content_lines).strip()
    if not content:
        print("❌ Content is required")
        return
    
    # Get metadata
    print("\nPolicy type (compliance/risk/fraud/operational/security/audit):")
    policy_type = input("Enter type: ").strip() or "compliance"
    
    framework = input("Framework (SOX/PCI DSS/Basel III/GDPR/etc): ").strip() or "SOX"
    version = input("Version (default 1.0): ").strip() or "1.0"
    
    # Upload
    try:
        from bfsi_policy_uploader import upload_policy_text
        print(f"\n📤 Uploading policy...")
        policy_id = upload_policy_text(title, content, policy_type, framework, version)
        print(f"✅ SUCCESS! Policy uploaded with ID: {policy_id}")
    except Exception as e:
        print(f"❌ Error uploading policy: {e}")

if __name__ == "__main__":
    main()



