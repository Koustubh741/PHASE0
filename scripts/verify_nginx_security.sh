#!/bin/bash
# Script to verify Nginx and Alpine security versions
# This script should be run inside the nginx container

echo "=== Nginx Security Verification ==="
echo "Date: $(date)"
echo

# Check Alpine version
echo "1. Alpine Linux Version:"
if [ -f /etc/alpine-release ]; then
    echo "   Alpine Release: $(cat /etc/alpine-release)"
else
    echo "   Alpine release file not found"
fi

# Check nginx version
echo
echo "2. Nginx Version Information:"
nginx -v 2>&1

# Check nginx package info
echo
echo "3. Nginx Package Information:"
if command -v apk >/dev/null 2>&1; then
    apk info nginx
else
    echo "   apk command not available (not Alpine-based)"
fi

# Check if vulnerable modules are compiled in
echo
echo "4. Checking for vulnerable modules:"
nginx -V 2>&1 | grep -E "(http_mp4_module|http_v3_module)"

if [ $? -eq 0 ]; then
    echo "   WARNING: Potentially vulnerable modules detected!"
else
    echo "   ✓ No vulnerable modules detected"
fi

# Check SSL configuration
echo
echo "5. SSL Configuration Check:"
echo "   Checking if ssl_session_cache is disabled..."
if grep -q "ssl_session_cache off" /etc/nginx/conf.d/bfsi-api.conf 2>/dev/null; then
    echo "   ✓ ssl_session_cache is disabled"
else
    echo "   ✗ ssl_session_cache may not be properly disabled"
fi

echo "   Checking if ssl_session_tickets is disabled..."
if grep -q "ssl_session_tickets off" /etc/nginx/conf.d/bfsi-api.conf 2>/dev/null; then
    echo "   ✓ ssl_session_tickets is disabled"
else
    echo "   ✗ ssl_session_tickets may not be properly disabled"
fi

# Check for HTTP/3/QUIC
echo
echo "6. HTTP/3/QUIC Configuration Check:"
if grep -q "quic" /etc/nginx/conf.d/bfsi-api.conf 2>/dev/null; then
    echo "   ✗ HTTP/3/QUIC is enabled - this should be disabled for security"
else
    echo "   ✓ HTTP/3/QUIC is not enabled"
fi

echo
echo "=== Security Verification Complete ==="
