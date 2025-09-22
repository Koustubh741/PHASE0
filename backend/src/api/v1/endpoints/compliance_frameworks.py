"""
Compliance Frameworks API Endpoints
RESTful API endpoints for compliance framework management
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

from ...core.application.services.compliance_framework_service import (
    ComplianceFrameworkService,
    ComplianceFramework,
    ComplianceStatus,
    RequirementType,
    AssessmentStatus
)
from ...core.application.dto.compliance_dto import (
    FrameworkResponse,
    RequirementResponse,
    AssessmentRequest,
    AssessmentResponse,
    ComplianceDashboardResponse,
    GapResponse,
    PerformanceMetricsResponse
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/compliance-frameworks", tags=["Compliance Frameworks"])

# Global service instance
compliance_service = ComplianceFrameworkService()

@router.get("/frameworks", response_model=List[FrameworkResponse])
async def get_compliance_frameworks():
    """Get all available compliance frameworks"""
    try:
        frameworks = compliance_service.get_frameworks()
        return frameworks
    except Exception as e:
        logger.error(f"Error getting compliance frameworks: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/frameworks/{framework_name}", response_model=FrameworkResponse)
async def get_framework(framework_name: str):
    """Get specific compliance framework"""
    try:
        frameworks = compliance_service.get_frameworks()
        framework = next((f for f in frameworks if f["framework"] == framework_name), None)
        
        if not framework:
            raise HTTPException(status_code=404, detail="Framework not found")
        
        return framework
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting framework: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/frameworks/{framework_name}/requirements", response_model=List[RequirementResponse])
async def get_framework_requirements(framework_name: str):
    """Get requirements for a specific framework"""
    try:
        framework_enum = ComplianceFramework(framework_name)
        requirements = compliance_service.get_requirements(framework_enum)
        return requirements
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid framework name")
    except Exception as e:
        logger.error(f"Error getting framework requirements: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/requirements", response_model=List[RequirementResponse])
async def get_all_requirements(framework: Optional[str] = None):
    """Get all compliance requirements"""
    try:
        framework_enum = ComplianceFramework(framework) if framework else None
        requirements = compliance_service.get_requirements(framework_enum)
        return requirements
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid framework name")
    except Exception as e:
        logger.error(f"Error getting requirements: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/requirements/{requirement_id}", response_model=RequirementResponse)
async def get_requirement(requirement_id: str):
    """Get specific requirement"""
    try:
        requirements = compliance_service.get_requirements()
        requirement = next((r for r in requirements if r["requirement_id"] == requirement_id), None)
        
        if not requirement:
            raise HTTPException(status_code=404, detail="Requirement not found")
        
        return requirement
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting requirement: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/assessments", response_model=AssessmentResponse)
async def create_assessment(request: AssessmentRequest):
    """Create a new compliance assessment"""
    try:
        framework_enum = ComplianceFramework(request.framework)
        assessment_id = compliance_service.create_assessment(
            framework=framework_enum,
            organization_id=request.organization_id,
            assessor_id=request.assessor_id,
            scope=request.scope,
            methodology=request.methodology
        )
        
        return AssessmentResponse(
            assessment_id=assessment_id,
            framework=request.framework,
            organization_id=request.organization_id,
            assessor_id=request.assessor_id,
            status=AssessmentStatus.NOT_STARTED.value,
            start_date=datetime.utcnow(),
            scope=request.scope,
            methodology=request.methodology
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error creating assessment: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/assessments/{assessment_id}/conduct")
async def conduct_assessment(assessment_id: str):
    """Conduct a compliance assessment"""
    try:
        results = compliance_service.conduct_assessment(assessment_id)
        return results
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error conducting assessment: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/assessments/{assessment_id}", response_model=AssessmentResponse)
async def get_assessment(assessment_id: str):
    """Get assessment results"""
    try:
        results = compliance_service.get_assessment_results(assessment_id)
        return results
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error getting assessment: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/assessments/{assessment_id}/gaps", response_model=List[GapResponse])
async def get_assessment_gaps(assessment_id: str):
    """Get compliance gaps from assessment"""
    try:
        gaps = compliance_service.identify_gaps(assessment_id)
        return gaps
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error getting assessment gaps: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/dashboard", response_model=ComplianceDashboardResponse)
async def get_compliance_dashboard():
    """Get compliance dashboard data"""
    try:
        dashboard_data = compliance_service.get_compliance_dashboard()
        return dashboard_data
    except Exception as e:
        logger.error(f"Error getting compliance dashboard: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/metrics", response_model=PerformanceMetricsResponse)
async def get_performance_metrics():
    """Get compliance performance metrics"""
    try:
        metrics = compliance_service.get_performance_metrics()
        return metrics
    except Exception as e:
        logger.error(f"Error getting performance metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/frameworks/{framework_name}/compliance-status")
async def get_framework_compliance_status(framework_name: str):
    """Get compliance status for a specific framework"""
    try:
        framework_enum = ComplianceFramework(framework_name)
        dashboard_data = compliance_service.get_compliance_dashboard()
        framework_data = dashboard_data["framework_scores"].get(framework_name)
        
        if not framework_data:
            raise HTTPException(status_code=404, detail="Framework data not found")
        
        return {
            "framework": framework_name,
            "compliance_percentage": framework_data["compliance_percentage"],
            "risk_level": framework_data["risk_level"],
            "last_assessment": framework_data["last_assessment"],
            "status": "compliant" if framework_data["compliance_percentage"] >= 90 else "non_compliant"
        }
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid framework name")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting framework compliance status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        metrics = compliance_service.get_performance_metrics()
        return {
            "status": "healthy",
            "service": "compliance-frameworks",
            "version": "2.0.0",
            "frameworks_loaded": metrics["total_frameworks"],
            "requirements_loaded": metrics["total_requirements"],
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "service": "compliance-frameworks",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
        )
