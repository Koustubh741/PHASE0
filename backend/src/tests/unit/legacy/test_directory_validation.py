#!/usr/bin/env python3
"""
Test script for directory path validation security
"""

import sys

# Add the current directory to path to import the validation function
sys.path.append('.')

from upload_real_policy import validate_directory_path

def test_directory_validation():
    """Test the enhanced directory path validation"""
    
    print("🧪 Testing Directory Path Validation Security")
    print("=" * 50)
    
    # Test cases for security validation
    test_cases = [
        # Valid cases
        (".", "Current directory (should be valid)"),
        ("./policies", "Policies subdirectory (should be valid if exists)"),
        ("./uploads", "Uploads subdirectory (should be valid if exists)"),
        
        # Invalid cases - path traversal attacks
        ("../", "Parent directory traversal"),
        ("../../", "Double parent directory traversal"),
        ("../..", "Parent directory traversal (no slash)"),
        ("..\\", "Windows parent directory traversal"),
        ("..\\..", "Windows double parent directory traversal"),
        ("/etc/passwd", "System file access attempt"),
        ("C:\\Windows\\System32", "Windows system directory access"),
        ("~/.ssh", "Home directory access"),
        ("//server/share", "UNC path access"),
        
        # Invalid cases - relative paths that might escape
        ("./../../../etc", "Relative path escaping"),
        ("./..\\..\\..", "Mixed path traversal"),
    ]
    
    print("Testing security validation...")
    print()
    
    for test_path, description in test_cases:
        print(f"Testing: {test_path}")
        print(f"Description: {description}")
        
        is_valid, message = validate_directory_path(test_path)
        
        if is_valid:
            print(f"✅ Result: {message}")
        else:
            print(f"❌ Result: {message}")
        
        print("-" * 30)
    
    print("\n🔒 Security validation test completed!")
    print("All path traversal attempts should be blocked.")

if __name__ == "__main__":
    test_directory_validation()
