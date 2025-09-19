#!/usr/bin/env python3
"""
BFSI Frontend Server
Simple HTTP server to serve the BFSI frontend integration test page
"""

import http.server
import socketserver
import webbrowser
import os
from pathlib import Path

def start_bfsi_frontend():
    """Start the BFSI frontend server"""
    print("🏦 BFSI Frontend Server")
    print("=" * 40)
    
    # Change to the frontend public directory
    frontend_dir = Path(__file__).parent / "frontend" / "public"
    os.chdir(frontend_dir)
    
    PORT = 3000
    
    class CustomHandler(http.server.SimpleHTTPRequestHandler):
        def end_headers(self):
            # Add CORS headers
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            super().end_headers()
    
    try:
        with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
            print(f"✅ BFSI Frontend server started on http://localhost:{PORT}")
            print(f"📁 Serving from: {frontend_dir}")
            print(f"🌐 BFSI Test Page: http://localhost:{PORT}/bfsi-test.html")
            print("\n🎯 Features Available:")
            print("   • Industry Standard Policy Toggle")
            print("   • BFSI Dashboard with real-time metrics")
            print("   • Policy management interface")
            print("   • Real-time compliance monitoring")
            print("   • No mock data - ready for production")
            print("\n⌨️  Press Ctrl+C to stop the server")
            
            # Open browser automatically
            try:
                webbrowser.open(f"http://localhost:{PORT}/bfsi-test.html")
                print("🌐 Browser opened automatically")
            except:
                print("🌐 Please open http://localhost:3000/bfsi-test.html in your browser")
            
            print("\n🚀 Server is running...")
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

if __name__ == "__main__":
    start_bfsi_frontend()
