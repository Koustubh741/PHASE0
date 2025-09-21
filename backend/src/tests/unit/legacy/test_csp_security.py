#!/usr/bin/env python3
"""
Test script to verify CSP security implementation
"""

import requests
import re
from typing import Dict, List, Tuple


def test_csp_headers(url: str) -> Dict[str, any]:
    """
    Test CSP headers on a given URL
    
    Args:
        url: URL to test
        
    Returns:
        Dictionary with test results
    """
    try:
        response = requests.get(url, timeout=10)
        
        # Check for CSP header
        csp_header = response.headers.get('Content-Security-Policy', '')
        
        # Check for unsafe-inline (should not be present)
        has_unsafe_inline = "'unsafe-inline'" in csp_header
        
        # Check for nonce support
        has_nonce = "'nonce-" in csp_header or "nonce-" in csp_header
        
        # Check for proper directives
        has_script_src = "script-src" in csp_header
        has_style_src = "style-src" in csp_header
        has_frame_ancestors = "frame-ancestors" in csp_header
        
        return {
            'url': url,
            'status_code': response.status_code,
            'csp_header': csp_header,
            'has_unsafe_inline': has_unsafe_inline,
            'has_nonce': has_nonce,
            'has_script_src': has_script_src,
            'has_style_src': has_style_src,
            'has_frame_ancestors': has_frame_ancestors,
            'security_score': calculate_security_score({
                'has_unsafe_inline': has_unsafe_inline,
                'has_nonce': has_nonce,
                'has_script_src': has_script_src,
                'has_style_src': has_style_src,
                'has_frame_ancestors': has_frame_ancestors
            })
        }
        
    except Exception as e:
        return {
            'url': url,
            'error': str(e),
            'security_score': 0
        }


def calculate_security_score(results: Dict[str, bool]) -> int:
    """
    Calculate security score based on CSP implementation
    
    Args:
        results: Dictionary with test results
        
    Returns:
        Security score (0-100)
    """
    score = 0
    
    # Positive indicators
    if results.get('has_nonce'):
        score += 30
    if results.get('has_script_src'):
        score += 20
    if results.get('has_style_src'):
        score += 20
    if results.get('has_frame_ancestors'):
        score += 15
    
    # Negative indicators
    if results.get('has_unsafe_inline'):
        score -= 50  # Major security risk
    
    return max(0, min(100, score))


def test_html_content_security(html_content: str) -> Dict[str, any]:
    """
    Test HTML content for security issues
    
    Args:
        html_content: HTML content to analyze
        
    Returns:
        Dictionary with security analysis
    """
    issues = []
    
    # Check for inline scripts without nonce
    inline_scripts = re.findall(r'<script[^>]*(?!nonce)[^>]*>', html_content)
    if inline_scripts:
        issues.append(f"Found {len(inline_scripts)} inline scripts without nonce")
    
    # Check for inline styles without nonce
    inline_styles = re.findall(r'<style[^>]*(?!nonce)[^>]*>', html_content)
    if inline_styles:
        issues.append(f"Found {len(inline_styles)} inline styles without nonce")
    
    # Check for external script references
    external_scripts = re.findall(r'<script[^>]*src=["\'][^"\']*["\']', html_content)
    external_script_count = len(external_scripts)
    
    # Check for external style references
    external_styles = re.findall(r'<link[^>]*rel=["\']stylesheet["\'][^>]*href=["\'][^"\']*["\']', html_content)
    external_style_count = len(external_styles)
    
    return {
        'inline_scripts_without_nonce': len(inline_scripts),
        'inline_styles_without_nonce': len(inline_styles),
        'external_scripts': external_script_count,
        'external_styles': external_style_count,
        'issues': issues,
        'security_score': calculate_html_security_score({
            'inline_scripts_without_nonce': len(inline_scripts),
            'inline_styles_without_nonce': len(inline_styles),
            'external_scripts': external_script_count,
            'external_styles': external_style_count
        })
    }


def calculate_html_security_score(results: Dict[str, int]) -> int:
    """
    Calculate security score for HTML content
    
    Args:
        results: Dictionary with HTML analysis results
        
    Returns:
        Security score (0-100)
    """
    score = 100
    
    # Deduct points for security issues
    score -= results.get('inline_scripts_without_nonce', 0) * 20
    score -= results.get('inline_styles_without_nonce', 0) * 15
    
    # Bonus points for external files
    if results.get('external_scripts', 0) > 0:
        score += 10
    if results.get('external_styles', 0) > 0:
        score += 10
    
    return max(0, min(100, score))


def test_static_files(base_url: str) -> Dict[str, any]:
    """
    Test if static files are accessible
    
    Args:
        base_url: Base URL of the application
        
    Returns:
        Dictionary with static file test results
    """
    static_files = [
        'static/css/archer-dashboard.css',
        'static/css/functional-dashboard.css',
        'static/js/archer-dashboard.js',
        'static/js/functional-dashboard.js'
    ]
    
    results = {}
    
    for file_path in static_files:
        try:
            url = f"{base_url}/{file_path}"
            response = requests.get(url, timeout=5)
            results[file_path] = {
                'accessible': response.status_code == 200,
                'status_code': response.status_code,
                'content_length': len(response.content)
            }
        except Exception as e:
            results[file_path] = {
                'accessible': False,
                'error': str(e)
            }
    
    return results


def main():
    """Main test function"""
    print("🔒 CSP Security Implementation Test")
    print("=" * 50)
    
    # Test URLs (update these for your environment)
    test_urls = [
        "http://localhost:8000/api/health",
        "http://localhost:8000/bfsi-archer-dashboard.html",
        "http://localhost:8000/bfsi-functional-dashboard.html"
    ]
    
    print("\n1. Testing CSP Headers...")
    for url in test_urls:
        print(f"\nTesting: {url}")
        result = test_csp_headers(url)
        
        if 'error' in result:
            print(f"❌ Error: {result['error']}")
        else:
            print(f"✅ Status: {result['status_code']}")
            print(f"🔒 CSP Header: {result['csp_header']}")
            print(f"⚠️  Has unsafe-inline: {result['has_unsafe_inline']}")
            print(f"🔑 Has nonce support: {result['has_nonce']}")
            print(f"📊 Security Score: {result['security_score']}/100")
    
    print("\n2. Testing Static Files...")
    static_results = test_static_files("http://localhost:8000")
    
    for file_path, result in static_results.items():
        if result.get('accessible'):
            print(f"✅ {file_path} - {result['content_length']} bytes")
        else:
            print(f"❌ {file_path} - {result.get('error', 'Not accessible')}")
    
    print("\n3. Security Recommendations...")
    print("✅ Remove 'unsafe-inline' from CSP")
    print("✅ Use nonces for inline content")
    print("✅ Externalize CSS and JavaScript")
    print("✅ Implement proper CSP headers")
    print("✅ Test thoroughly before production")
    
    print("\n🔒 CSP Security Test Complete!")


if __name__ == "__main__":
    main()
