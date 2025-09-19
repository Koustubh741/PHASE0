"""
Simple Backend Server for GRC Platform Demo
Serves BFSI agent data and API endpoints
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import json
from datetime import datetime
import random

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Sample data for the demo
SAMPLE_DATA = {
    "policies": [
        {"id": "POL-001", "title": "Information Security Policy", "status": "active", "compliance_score": 95},
        {"id": "POL-002", "title": "Data Protection Policy", "status": "draft", "compliance_score": 85},
        {"id": "POL-003", "title": "Risk Management Policy", "status": "active", "compliance_score": 92}
    ],
    "risks": [
        {"id": "RISK-001", "title": "Cybersecurity Risk", "level": "high", "score": 85},
        {"id": "RISK-002", "title": "Operational Risk", "level": "medium", "score": 65},
        {"id": "RISK-003", "title": "Compliance Risk", "level": "low", "score": 45}
    ],
    "compliance_frameworks": [
        {"name": "Basel III", "status": "compliant", "score": 95},
        {"name": "SOX", "status": "compliant", "score": 92},
        {"name": "PCI DSS", "status": "partially_compliant", "score": 85}
    ],
    "ai_agents": {
        "bfsi_agent": {"status": "active", "performance": 98},
        "compliance_agent": {"status": "active", "performance": 95},
        "risk_agent": {"status": "active", "performance": 97},
        "document_agent": {"status": "active", "performance": 94}
    }
}

@app.route('/')
def home():
    return jsonify({
        "message": "GRC Platform Backend API",
        "version": "1.0.0",
        "status": "running",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/health')
def health():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "frontend": "running",
            "backend": "running",
            "database": "connected",
            "ai_agents": "active"
        }
    })

@app.route('/api/policies')
def get_policies():
    return jsonify({
        "policies": SAMPLE_DATA["policies"],
        "total": len(SAMPLE_DATA["policies"]),
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/risks')
def get_risks():
    return jsonify({
        "risks": SAMPLE_DATA["risks"],
        "total": len(SAMPLE_DATA["risks"]),
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/compliance')
def get_compliance():
    return jsonify({
        "frameworks": SAMPLE_DATA["compliance_frameworks"],
        "overall_score": 95,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/ai-agents')
def get_ai_agents():
    return jsonify({
        "agents": SAMPLE_DATA["ai_agents"],
        "total_active": len([a for a in SAMPLE_DATA["ai_agents"].values() if a["status"] == "active"]),
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/dashboard')
def get_dashboard():
    return jsonify({
        "kpis": {
            "total_policies": len(SAMPLE_DATA["policies"]),
            "active_risks": len(SAMPLE_DATA["risks"]),
            "compliance_score": 95,
            "ai_agents_active": len([a for a in SAMPLE_DATA["ai_agents"].values() if a["status"] == "active"])
        },
        "recent_activity": [
            {"type": "policy_update", "message": "Information Security Policy updated", "timestamp": datetime.now().isoformat()},
            {"type": "risk_assessment", "message": "New risk assessment completed", "timestamp": datetime.now().isoformat()},
            {"type": "compliance_check", "message": "Basel III compliance check passed", "timestamp": datetime.now().isoformat()}
        ],
        "alerts": [
            {"type": "high_risk", "message": "Cybersecurity Risk requires attention", "severity": "high"},
            {"type": "compliance", "message": "PCI DSS compliance review due", "severity": "medium"}
        ],
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/bfsi-agent/assess', methods=['POST'])
def bfsi_risk_assessment():
    data = request.get_json()
    
    # Simulate BFSI agent processing
    business_unit = data.get('business_unit', 'retail_banking')
    risk_scope = data.get('risk_scope', 'comprehensive')
    
    # Generate realistic risk assessment
    risk_scores = {
        'credit_risk': random.randint(60, 80),
        'market_risk': random.randint(40, 60),
        'operational_risk': random.randint(70, 90),
        'liquidity_risk': random.randint(30, 50),
        'regulatory_risk': random.randint(50, 70)
    }
    
    overall_score = sum(risk_scores.values()) / len(risk_scores)
    
    return jsonify({
        "assessment_id": f"BFSI_ASSESS_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "business_unit": business_unit,
        "risk_scope": risk_scope,
        "overall_risk_score": round(overall_score, 1),
        "risk_breakdown": risk_scores,
        "recommendations": [
            "Enhance operational controls",
            "Monitor credit exposure",
            "Update risk models",
            "Implement additional safeguards"
        ],
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/bfsi-agent/compliance-check', methods=['POST'])
def bfsi_compliance_check():
    data = request.get_json()
    
    framework = data.get('framework', 'Basel III')
    business_unit = data.get('business_unit', 'capital_management')
    
    return jsonify({
        "framework": framework,
        "business_unit": business_unit,
        "compliance_score": 95,
        "compliance_status": "compliant",
        "regulations_checked": ["Basel III", "SOX", "PCI DSS"],
        "violations_found": 0,
        "recommendations": [
            "Maintain current compliance levels",
            "Schedule quarterly review"
        ],
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/bfsi-agent/analytics')
def bfsi_analytics():
    return jsonify({
        "performance_metrics": {
            "total_operations": 150,
            "successful_operations": 148,
            "failed_operations": 2,
            "compliance_score": 95.0,
            "risk_score": 75.0,
            "regulatory_status": "compliant"
        },
        "sub_agent_status": {
            "compliance_coordinator": {"name": "BFSI Compliance Coordinator", "status": "active"},
            "risk_analyzer": {"name": "BFSI Risk Analyzer", "status": "active"},
            "regulatory_monitor": {"name": "BFSI Regulatory Monitor", "status": "active"},
            "aml_analyzer": {"name": "BFSI AML Analyzer", "status": "active"},
            "capital_adequacy": {"name": "BFSI Capital Adequacy", "status": "active"},
            "operational_risk": {"name": "BFSI Operational Risk", "status": "active"},
            "cyber_security": {"name": "BFSI Cyber Security", "status": "active"},
            "fraud_detection": {"name": "BFSI Fraud Detection", "status": "active"}
        },
        "recent_alerts": [
            {"type": "compliance_degradation", "severity": "high", "message": "Compliance score dropped below threshold"},
            {"type": "risk_elevation", "severity": "medium", "message": "Risk score elevated above normal levels"}
        ],
        "timestamp": datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("🚀 Starting GRC Platform Backend Server...")
    print("📍 Backend API: http://localhost:8000")
    print("🌐 Frontend: http://localhost:3000")
    print("📊 API Documentation: http://localhost:8000/api/health")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=8000, debug=True)
