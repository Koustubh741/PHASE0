"""
BFSI AI API Endpoints
Handles BFSI AI agent operations and integrations
"""

from fastapi import APIRouter, HTTPException, Depends, status, Request
from typing import List, Dict, Any, Optional
from uuid import UUID
from datetime import datetime

from ....core.application.services.bfsi_ai_service import (
    BFSIAIService, BFSIAnalysisRequest, BFSIAnalysisResult, BFSIGapAnalysis
)
from ....core.application.services.audit_service import AuditService
from ....core.infrastructure.dependency_injection import get_audit_service
from ....core.domain.entities.user import User
from ....core.domain.entities.audit_log import AuditAction, AuditResource
from ....core.application.dto.bfsi_ai_dto import (
    BFSIAnalysisRequestDto, BFSIAnalysisResponseDto, BFSIGapAnalysisResponseDto,
    BFSIAgentStatusResponseDto
)
from ...middleware.auth_middleware import require_auth, require_permission

router = APIRouter(prefix="/bfsi-ai", tags=["BFSI AI Agents"])


class BFSIAIController:
    """BFSI AI controller"""
    
    def __init__(
        self,
        bfsi_ai_service: BFSIAIService,
        audit_service: AuditService
    ):
        self.bfsi_ai_service = bfsi_ai_service
        self.audit_service = audit_service
    
    async def perform_risk_assessment(
        self,
        request: BFSIAnalysisRequestDto,
        current_user: User = Depends(require_permission("can_assess_risks"))
    ) -> BFSIAnalysisResponseDto:
        """Perform BFSI risk assessment using AI agents"""
        try:
            # Convert DTO to service request
            analysis_request = BFSIAnalysisRequest(
                analysis_type=request.analysis_type,
                business_unit=request.business_unit,
                industry_type=request.industry_type,
                context=request.context,
                user_id=str(current_user.id),
                organization_id=str(current_user.organization_id)
            )
            
            # Perform risk assessment
            result = await self.bfsi_ai_service.perform_risk_assessment(
                analysis_request, current_user
            )
            
            # Convert result to response DTO
            response = BFSIAnalysisResponseDto(
                analysis_id=result.analysis_id,
                analysis_type=result.analysis_type,
                findings=result.findings,
                risk_score=result.risk_score,
                compliance_score=result.compliance_score,
                recommendations=result.recommendations,
                ai_insights=result.ai_insights,
                confidence_score=result.confidence_score,
                processing_time=result.processing_time,
                timestamp=result.timestamp
            )
            
            return response
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Risk assessment failed: {str(e)}"
            )
    
    async def perform_compliance_check(
        self,
        request: BFSIAnalysisRequestDto,
        current_user: User = Depends(require_permission("can_check_compliance"))
    ) -> BFSIAnalysisResponseDto:
        """Perform BFSI compliance check using AI agents"""
        try:
            # Convert DTO to service request
            analysis_request = BFSIAnalysisRequest(
                analysis_type=request.analysis_type,
                business_unit=request.business_unit,
                industry_type=request.industry_type,
                context=request.context,
                user_id=str(current_user.id),
                organization_id=str(current_user.organization_id)
            )
            
            # Perform compliance check
            result = await self.bfsi_ai_service.perform_compliance_check(
                analysis_request, current_user
            )
            
            # Convert result to response DTO
            response = BFSIAnalysisResponseDto(
                analysis_id=result.analysis_id,
                analysis_type=result.analysis_type,
                findings=result.findings,
                risk_score=result.risk_score,
                compliance_score=result.compliance_score,
                recommendations=result.recommendations,
                ai_insights=result.ai_insights,
                confidence_score=result.confidence_score,
                processing_time=result.processing_time,
                timestamp=result.timestamp
            )
            
            return response
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Compliance check failed: {str(e)}"
            )
    
    async def perform_policy_review(
        self,
        policy_id: str,
        request: BFSIAnalysisRequestDto,
        current_user: User = Depends(require_permission("can_review_policies"))
    ) -> BFSIAnalysisResponseDto:
        """Perform BFSI policy review using AI agents"""
        try:
            # Convert DTO to service request
            analysis_request = BFSIAnalysisRequest(
                analysis_type=request.analysis_type,
                business_unit=request.business_unit,
                industry_type=request.industry_type,
                context=request.context,
                user_id=str(current_user.id),
                organization_id=str(current_user.organization_id)
            )
            
            # Perform policy review
            result = await self.bfsi_ai_service.perform_policy_review(
                policy_id, analysis_request, current_user
            )
            
            # Convert result to response DTO
            response = BFSIAnalysisResponseDto(
                analysis_id=result.analysis_id,
                analysis_type=result.analysis_type,
                findings=result.findings,
                risk_score=result.risk_score,
                compliance_score=result.compliance_score,
                recommendations=result.recommendations,
                ai_insights=result.ai_insights,
                confidence_score=result.confidence_score,
                processing_time=result.processing_time,
                timestamp=result.timestamp
            )
            
            return response
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Policy review failed: {str(e)}"
            )
    
    async def perform_gap_analysis(
        self,
        request: BFSIAnalysisRequestDto,
        current_user: User = Depends(require_permission("can_analyze_gaps"))
    ) -> List[BFSIGapAnalysisResponseDto]:
        """Perform BFSI gap analysis using AI agents"""
        try:
            # Convert DTO to service request
            analysis_request = BFSIAnalysisRequest(
                analysis_type=request.analysis_type,
                business_unit=request.business_unit,
                industry_type=request.industry_type,
                context=request.context,
                user_id=str(current_user.id),
                organization_id=str(current_user.organization_id)
            )
            
            # Perform gap analysis
            gaps = await self.bfsi_ai_service.perform_gap_analysis(
                analysis_request, current_user
            )
            
            # Convert results to response DTOs
            response = [
                BFSIGapAnalysisResponseDto(
                    gap_id=gap.gap_id,
                    policy_name=gap.policy_name,
                    framework=gap.framework,
                    severity=gap.severity,
                    description=gap.description,
                    current_status=gap.current_status,
                    required_actions=gap.required_actions,
                    timeline=gap.timeline,
                    priority=gap.priority
                )
                for gap in gaps
            ]
            
            return response
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Gap analysis failed: {str(e)}"
            )
    
    async def get_agent_status(
        self,
        current_user: User = Depends(require_auth)
    ) -> BFSIAgentStatusResponseDto:
        """Get BFSI AI agent status"""
        try:
            status_info = await self.bfsi_ai_service.get_agent_status()
            
            response = BFSIAgentStatusResponseDto(
                agent_id=status_info["agent_id"],
                name=status_info["name"],
                status=status_info["status"],
                capabilities=status_info["capabilities"],
                last_updated=status_info["last_updated"],
                version=status_info["version"]
            )
            
            return response
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to get agent status: {str(e)}"
            )


# Create controller instance
def get_bfsi_ai_controller(
    bfsi_ai_service: BFSIAIService = Depends(),
    audit_service: AuditService = Depends(get_audit_service)
) -> BFSIAIController:
    """Get BFSI AI controller with dependencies"""
    return BFSIAIController(bfsi_ai_service, audit_service)


# API Routes
@router.post("/risk/assess", response_model=BFSIAnalysisResponseDto)
async def assess_risk(
    request: BFSIAnalysisRequestDto,
    controller: BFSIAIController = Depends(get_bfsi_ai_controller)
):
    """Perform BFSI risk assessment using AI agents"""
    return await controller.perform_risk_assessment(request)


@router.post("/compliance/check", response_model=BFSIAnalysisResponseDto)
async def check_compliance(
    request: BFSIAnalysisRequestDto,
    controller: BFSIAIController = Depends(get_bfsi_ai_controller)
):
    """Perform BFSI compliance check using AI agents"""
    return await controller.perform_compliance_check(request)


@router.post("/policy/{policy_id}/review", response_model=BFSIAnalysisResponseDto)
async def review_policy(
    policy_id: str,
    request: BFSIAnalysisRequestDto,
    controller: BFSIAIController = Depends(get_bfsi_ai_controller)
):
    """Perform BFSI policy review using AI agents"""
    return await controller.perform_policy_review(policy_id, request)


@router.post("/gap/analyze", response_model=List[BFSIGapAnalysisResponseDto])
async def analyze_gaps(
    request: BFSIAnalysisRequestDto,
    controller: BFSIAIController = Depends(get_bfsi_ai_controller)
):
    """Perform BFSI gap analysis using AI agents"""
    return await controller.perform_gap_analysis(request)


@router.get("/status", response_model=BFSIAgentStatusResponseDto)
async def get_status(
    controller: BFSIAIController = Depends(get_bfsi_ai_controller)
):
    """Get BFSI AI agent status"""
    return await controller.get_agent_status()
