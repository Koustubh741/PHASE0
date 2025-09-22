#!/usr/bin/env python3
"""
BFSI Gap Analysis API
FastAPI service for comprehensive policy gap analysis and mitigation
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

from bfsi_gap_analysis_service import BFSIGapAnalysisService, GapAnalysisReport, PolicyGap

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="BFSI Gap Analysis API",
    description="Comprehensive policy gap analysis and mitigation system for BFSI organizations",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize gap analysis service
gap_service = BFSIGapAnalysisService()

# Pydantic models for API
class GapAnalysisRequest(BaseModel):
    organization_name: str
    organization_policies: Optional[List[Dict[str, Any]]] = None

class GapAnalysisResponse(BaseModel):
    report_id: str
    organization_name: str
    analysis_date: str
    compliance_score: float
    total_gaps: int
    critical_gaps: int
    high_priority_gaps: int
    executive_summary: str

class PolicyGapResponse(BaseModel):
    gap_id: str
    policy_name: str
    framework: str
    severity: str
    description: str
    current_status: str
    required_actions: List[str]
    mitigation_strategies: List[str]
    estimated_effort: str
    business_impact: str
    regulatory_impact: str
    priority_score: int
    due_date: Optional[str]

class MitigationWorkflowRequest(BaseModel):
    gap_id: str
    assigned_owner: str
    target_completion_date: str
    mitigation_approach: str

# API Endpoints

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "BFSI Gap Analysis API",
        "version": "1.0.0",
        "endpoints": {
            "gap_analysis": "/api/gap-analysis",
            "reports": "/api/reports",
            "mitigation": "/api/mitigation",
            "dashboard": "/dashboard"
        }
    }

@app.post("/api/gap-analysis", response_model=GapAnalysisResponse)
async def perform_gap_analysis(request: GapAnalysisRequest):
    """Perform comprehensive gap analysis for an organization"""
    try:
        logger.info(f"Starting gap analysis for {request.organization_name}")
        
        # Perform gap analysis
        report = await gap_service.perform_comprehensive_gap_analysis(
            organization_name=request.organization_name,
            organization_policies=request.organization_policies
        )
        
        # Return response
        return GapAnalysisResponse(
            report_id=report.report_id,
            organization_name=report.organization_name,
            analysis_date=report.analysis_date.isoformat(),
            compliance_score=report.compliance_score,
            total_gaps=len(report.gaps),
            critical_gaps=report.critical_gaps,
            high_priority_gaps=report.high_priority_gaps,
            executive_summary=report.executive_summary
        )
        
    except Exception as e:
        logger.error(f"Error performing gap analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/gap-analysis/{report_id}")
async def get_gap_analysis_report(report_id: str):
    """Get detailed gap analysis report by ID"""
    try:
        report = gap_service.get_gap_analysis_report(report_id)
        
        if not report:
            raise HTTPException(status_code=404, detail="Report not found")
        
        # Convert gaps to response format
        gaps_response = []
        for gap in report.gaps:
            gaps_response.append(PolicyGapResponse(
                gap_id=gap.gap_id,
                policy_name=gap.policy_name,
                framework=gap.framework.value,
                severity=gap.severity.value,
                description=gap.description,
                current_status=gap.current_status.value,
                required_actions=gap.required_actions,
                mitigation_strategies=gap.mitigation_strategies,
                estimated_effort=gap.estimated_effort,
                business_impact=gap.business_impact,
                regulatory_impact=gap.regulatory_impact,
                priority_score=gap.priority_score,
                due_date=gap.due_date.isoformat() if gap.due_date else None
            ))
        
        return {
            "report_id": report.report_id,
            "organization_name": report.organization_name,
            "analysis_date": report.analysis_date.isoformat(),
            "compliance_score": report.compliance_score,
            "total_policies": report.total_policies,
            "implemented_policies": report.implemented_policies,
            "partial_policies": report.partial_policies,
            "missing_policies": report.missing_policies,
            "outdated_policies": report.outdated_policies,
            "critical_gaps": report.critical_gaps,
            "high_priority_gaps": report.high_priority_gaps,
            "medium_priority_gaps": report.medium_priority_gaps,
            "low_priority_gaps": report.low_priority_gaps,
            "gaps": gaps_response,
            "recommendations": report.recommendations,
            "next_review_date": report.next_review_date.isoformat(),
            "executive_summary": report.executive_summary
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving gap analysis report: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/reports")
async def get_all_reports():
    """Get all gap analysis reports"""
    try:
        reports = gap_service.get_all_gap_analysis_reports()
        return {"reports": reports}
        
    except Exception as e:
        logger.error(f"Error retrieving reports: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/mitigation/workflow")
async def create_mitigation_workflow(request: MitigationWorkflowRequest):
    """Create mitigation workflow for a specific gap"""
    try:
        # This would integrate with the GRC workflow system
        workflow_data = {
            "gap_id": request.gap_id,
            "assigned_owner": request.assigned_owner,
            "target_completion_date": request.target_completion_date,
            "mitigation_approach": request.mitigation_approach,
            "status": "created",
            "created_date": datetime.now().isoformat()
        }
        
        # In a real implementation, this would create a workflow in the GRC system
        logger.info(f"Created mitigation workflow for gap {request.gap_id}")
        
        return {
            "message": "Mitigation workflow created successfully",
            "workflow_id": f"workflow_{request.gap_id}",
            "gap_id": request.gap_id,
            "assigned_owner": request.assigned_owner,
            "target_completion_date": request.target_completion_date,
            "status": "created"
        }
        
    except Exception as e:
        logger.error(f"Error creating mitigation workflow: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/mitigation/workflows")
async def get_mitigation_workflows():
    """Get all mitigation workflows"""
    try:
        # This would retrieve workflows from the GRC system
        # For now, return mock data
        workflows = [
            {
                "workflow_id": "workflow_001",
                "gap_id": "gap_001",
                "assigned_owner": "John Doe",
                "target_completion_date": "2024-01-15",
                "status": "in_progress",
                "progress": 45
            },
            {
                "workflow_id": "workflow_002",
                "gap_id": "gap_002",
                "assigned_owner": "Jane Smith",
                "target_completion_date": "2024-02-01",
                "status": "pending",
                "progress": 0
            }
        ]
        
        return {"workflows": workflows}
        
    except Exception as e:
        logger.error(f"Error retrieving mitigation workflows: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/compliance/frameworks")
async def get_compliance_frameworks():
    """Get available compliance frameworks"""
    try:
        frameworks = [
            {
                "framework": "sox",
                "name": "Sarbanes-Oxley Act",
                "priority": "critical",
                "requirements_count": 8
            },
            {
                "framework": "basel_iii",
                "name": "Basel III Capital Requirements",
                "priority": "critical",
                "requirements_count": 8
            },
            {
                "framework": "pci_dss",
                "name": "Payment Card Industry Data Security Standard",
                "priority": "high",
                "requirements_count": 6
            },
            {
                "framework": "gdpr",
                "name": "General Data Protection Regulation",
                "priority": "high",
                "requirements_count": 8
            }
        ]
        
        return {"frameworks": frameworks}
        
    except Exception as e:
        logger.error(f"Error retrieving compliance frameworks: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/dashboard")
async def serve_dashboard():
    """Serve the gap analysis dashboard"""
    try:
        dashboard_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BFSI Gap Analysis Dashboard</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            padding: 30px;
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 2px solid #e0e0e0;
        }
        .header h1 {
            color: #2c3e50;
            margin: 0;
        }
        .header p {
            color: #7f8c8d;
            margin: 10px 0 0 0;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .stat-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
        }
        .stat-card h3 {
            margin: 0 0 10px 0;
            font-size: 2em;
        }
        .stat-card p {
            margin: 0;
            opacity: 0.9;
        }
        .critical { background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%); }
        .high { background: linear-gradient(135deg, #ffa726 0%, #ff9800 100%); }
        .medium { background: linear-gradient(135deg, #42a5f5 0%, #1e88e5 100%); }
        .low { background: linear-gradient(135deg, #66bb6a 0%, #4caf50 100%); }
        .actions {
            display: flex;
            gap: 15px;
            margin-bottom: 30px;
            flex-wrap: wrap;
        }
        .btn {
            padding: 12px 24px;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 600;
            text-decoration: none;
            display: inline-block;
            transition: all 0.3s ease;
        }
        .btn-primary {
            background: #3498db;
            color: white;
        }
        .btn-primary:hover {
            background: #2980b9;
            transform: translateY(-2px);
        }
        .btn-success {
            background: #27ae60;
            color: white;
        }
        .btn-success:hover {
            background: #229954;
            transform: translateY(-2px);
        }
        .btn-warning {
            background: #f39c12;
            color: white;
        }
        .btn-warning:hover {
            background: #e67e22;
            transform: translateY(-2px);
        }
        .section {
            margin-bottom: 30px;
        }
        .section h2 {
            color: #2c3e50;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 1px solid #e0e0e0;
        }
        .gap-list {
            background: #f8f9fa;
            border-radius: 6px;
            padding: 20px;
        }
        .gap-item {
            background: white;
            border-left: 4px solid #e74c3c;
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 4px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        .gap-item.medium { border-left-color: #f39c12; }
        .gap-item.low { border-left-color: #27ae60; }
        .gap-item h4 {
            margin: 0 0 8px 0;
            color: #2c3e50;
        }
        .gap-item p {
            margin: 0 0 8px 0;
            color: #7f8c8d;
        }
        .gap-item .severity {
            display: inline-block;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
        }
        .severity.critical { background: #ffebee; color: #c62828; }
        .severity.high { background: #fff3e0; color: #ef6c00; }
        .severity.medium { background: #e3f2fd; color: #1976d2; }
        .severity.low { background: #e8f5e8; color: #388e3c; }
        .loading {
            text-align: center;
            padding: 40px;
            color: #7f8c8d;
        }
        .error {
            background: #ffebee;
            color: #c62828;
            padding: 15px;
            border-radius: 6px;
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏦 BFSI Gap Analysis Dashboard</h1>
            <p>Comprehensive policy gap analysis and mitigation system</p>
        </div>
        
        <div class="actions">
            <button class="btn btn-primary" onclick="performGapAnalysis()">🔍 Perform Gap Analysis</button>
            <button class="btn btn-success" onclick="viewReports()">📊 View Reports</button>
            <button class="btn btn-warning" onclick="viewMitigationWorkflows()">🔄 Mitigation Workflows</button>
        </div>
        
        <div id="content">
            <div class="loading">
                <h3>Welcome to BFSI Gap Analysis Dashboard</h3>
                <p>Click "Perform Gap Analysis" to start analyzing your organization's compliance gaps.</p>
            </div>
        </div>
    </div>

    <script>
        async function performGapAnalysis() {
            const content = document.getElementById('content');
            content.innerHTML = '<div class="loading">🔄 Performing gap analysis...</div>';
            
            try {
                const response = await fetch('/api/gap-analysis', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        organization_name: 'Sample Financial Institution'
                    })
                });
                
                if (!response.ok) {
                    throw new Error('Gap analysis failed');
                }
                
                const result = await response.json();
                displayGapAnalysisResults(result);
                
            } catch (error) {
                content.innerHTML = `<div class="error">❌ Error performing gap analysis: ${error.message}</div>`;
            }
        }
        
        function displayGapAnalysisResults(result) {
            const content = document.getElementById('content');
            content.innerHTML = `
                <div class="section">
                    <h2>📊 Gap Analysis Results</h2>
                    <div class="stats-grid">
                        <div class="stat-card">
                            <h3>${result.compliance_score.toFixed(1)}%</h3>
                            <p>Compliance Score</p>
                        </div>
                        <div class="stat-card critical">
                            <h3>${result.critical_gaps}</h3>
                            <p>Critical Gaps</p>
                        </div>
                        <div class="stat-card high">
                            <h3>${result.high_priority_gaps}</h3>
                            <p>High Priority Gaps</p>
                        </div>
                        <div class="stat-card medium">
                            <h3>${result.total_gaps}</h3>
                            <p>Total Gaps</p>
                        </div>
                    </div>
                </div>
                
                <div class="section">
                    <h2>📋 Executive Summary</h2>
                    <div style="background: #f8f9fa; padding: 20px; border-radius: 6px; white-space: pre-line;">${result.executive_summary}</div>
                </div>
                
                <div class="section">
                    <h2>🎯 Recommended Actions</h2>
                    <div class="actions">
                        <button class="btn btn-primary" onclick="viewDetailedReport('${result.report_id}')">View Detailed Report</button>
                        <button class="btn btn-success" onclick="createMitigationWorkflows()">Create Mitigation Workflows</button>
                    </div>
                </div>
            `;
        }
        
        async function viewDetailedReport(reportId) {
            try {
                const response = await fetch(`/api/gap-analysis/${reportId}`);
                const report = await response.json();
                displayDetailedReport(report);
            } catch (error) {
                document.getElementById('content').innerHTML = `<div class="error">❌ Error loading detailed report: ${error.message}</div>`;
            }
        }
        
        function displayDetailedReport(report) {
            const content = document.getElementById('content');
            const gapsHtml = report.gaps.map(gap => `
                <div class="gap-item ${gap.severity}">
                    <h4>${gap.policy_name}</h4>
                    <p>${gap.description}</p>
                    <span class="severity ${gap.severity}">${gap.severity}</span>
                    <p><strong>Business Impact:</strong> ${gap.business_impact}</p>
                    <p><strong>Estimated Effort:</strong> ${gap.estimated_effort}</p>
                </div>
            `).join('');
            
            content.innerHTML = `
                <div class="section">
                    <h2>📊 Detailed Gap Analysis Report</h2>
                    <div class="stats-grid">
                        <div class="stat-card">
                            <h3>${report.compliance_score.toFixed(1)}%</h3>
                            <p>Compliance Score</p>
                        </div>
                        <div class="stat-card critical">
                            <h3>${report.critical_gaps}</h3>
                            <p>Critical Gaps</p>
                        </div>
                        <div class="stat-card high">
                            <h3>${report.high_priority_gaps}</h3>
                            <p>High Priority Gaps</p>
                        </div>
                        <div class="stat-card medium">
                            <h3>${report.medium_priority_gaps}</h3>
                            <p>Medium Priority Gaps</p>
                        </div>
                    </div>
                </div>
                
                <div class="section">
                    <h2>🔍 Policy Gaps</h2>
                    <div class="gap-list">
                        ${gapsHtml}
                    </div>
                </div>
            `;
        }
        
        async function viewReports() {
            try {
                const response = await fetch('/api/reports');
                const data = await response.json();
                displayReports(data.reports);
            } catch (error) {
                document.getElementById('content').innerHTML = `<div class="error">❌ Error loading reports: ${error.message}</div>`;
            }
        }
        
        function displayReports(reports) {
            const content = document.getElementById('content');
            const reportsHtml = reports.map(report => `
                <div class="gap-item">
                    <h4>${report.organization_name}</h4>
                    <p>Analysis Date: ${new Date(report.analysis_date).toLocaleDateString()}</p>
                    <p>Compliance Score: ${report.compliance_score.toFixed(1)}%</p>
                    <p>Critical Gaps: ${report.critical_gaps} | High Priority: ${report.high_priority_gaps}</p>
                    <button class="btn btn-primary" onclick="viewDetailedReport('${report.report_id}')">View Details</button>
                </div>
            `).join('');
            
            content.innerHTML = `
                <div class="section">
                    <h2>📊 Gap Analysis Reports</h2>
                    <div class="gap-list">
                        ${reportsHtml}
                    </div>
                </div>
            `;
        }
        
        async function viewMitigationWorkflows() {
            try {
                const response = await fetch('/api/mitigation/workflows');
                const data = await response.json();
                displayMitigationWorkflows(data.workflows);
            } catch (error) {
                document.getElementById('content').innerHTML = `<div class="error">❌ Error loading mitigation workflows: ${error.message}</div>`;
            }
        }
        
        function displayMitigationWorkflows(workflows) {
            const content = document.getElementById('content');
            const workflowsHtml = workflows.map(workflow => `
                <div class="gap-item">
                    <h4>Workflow ${workflow.workflow_id}</h4>
                    <p>Gap ID: ${workflow.gap_id}</p>
                    <p>Assigned Owner: ${workflow.assigned_owner}</p>
                    <p>Target Completion: ${workflow.target_completion_date}</p>
                    <p>Status: ${workflow.status} (${workflow.progress}% complete)</p>
                </div>
            `).join('');
            
            content.innerHTML = `
                <div class="section">
                    <h2>🔄 Mitigation Workflows</h2>
                    <div class="gap-list">
                        ${workflowsHtml}
                    </div>
                </div>
            `;
        }
        
        function createMitigationWorkflows() {
            document.getElementById('content').innerHTML = `
                <div class="section">
                    <h2>🔄 Create Mitigation Workflows</h2>
                    <p>Mitigation workflow creation functionality would be implemented here.</p>
                    <button class="btn btn-primary" onclick="viewMitigationWorkflows()">View Existing Workflows</button>
                </div>
            `;
        }
    </script>
</body>
</html>
        """
        
        return HTMLResponse(content=dashboard_html)
        
    except Exception as e:
        logger.error(f"Error serving dashboard: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "BFSI Gap Analysis API",
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8011))
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    )
