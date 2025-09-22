"""
BFSI AI Data Transfer Objects
DTOs for BFSI AI agent operations and responses
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum


class AnalysisType(str, Enum):
    """Analysis type enumeration"""
    RISK_ASSESSMENT = "risk_assessment"
    COMPLIANCE_CHECK = "compliance_check"
    POLICY_REVIEW = "policy_review"
    GAP_ANALYSIS = "gap_analysis"


class IndustryType(str, Enum):
    """Industry type enumeration"""
    BFSI = "bfsi"
    BANKING = "banking"
    FINANCIAL_SERVICES = "financial_services"
    INSURANCE = "insurance"
    FINTECH = "fintech"


class BusinessUnit(str, Enum):
    """Business unit enumeration"""
    RETAIL = "retail"
    COMMERCIAL = "commercial"
    INVESTMENT = "investment"
    TREASURY = "treasury"
    RISK_MANAGEMENT = "risk_management"
    COMPLIANCE = "compliance"


class BFSIAnalysisRequestDto(BaseModel):
    """BFSI analysis request DTO"""
    analysis_type: AnalysisType = Field(..., description="Type of analysis to perform")
    business_unit: BusinessUnit = Field(..., description="Business unit for analysis")
    industry_type: IndustryType = Field(..., description="Industry type for analysis")
    context: Dict[str, Any] = Field(default_factory=dict, description="Additional context for analysis")
    
    class Config:
        json_schema_extra = {
            "example": {
                "analysis_type": "risk_assessment",
                "business_unit": "retail",
                "industry_type": "bfsi",
                "context": {
                    "risk_factors": ["market_volatility", "regulatory_changes"],
                    "time_horizon": "12_months"
                }
            }
        }


class BFSIAnalysisResponseDto(BaseModel):
    """BFSI analysis response DTO"""
    analysis_id: str = Field(..., description="Unique analysis identifier")
    analysis_type: str = Field(..., description="Type of analysis performed")
    findings: List[str] = Field(..., description="Analysis findings")
    risk_score: float = Field(..., ge=0.0, le=1.0, description="Risk score (0-1)")
    compliance_score: float = Field(..., ge=0.0, le=1.0, description="Compliance score (0-1)")
    recommendations: List[str] = Field(..., description="AI-generated recommendations")
    ai_insights: str = Field(..., description="AI insights and analysis")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="AI confidence score")
    processing_time: float = Field(..., description="Processing time in seconds")
    timestamp: datetime = Field(..., description="Analysis timestamp")
    
    class Config:
        json_schema_extra = {
            "example": {
                "analysis_id": "123e4567-e89b-12d3-a456-426614174000",
                "analysis_type": "risk_assessment",
                "findings": [
                    "Operational risk identified in retail banking",
                    "Regulatory compliance gaps detected"
                ],
                "risk_score": 0.75,
                "compliance_score": 0.68,
                "recommendations": [
                    "Implement enhanced risk monitoring controls",
                    "Update risk management policies"
                ],
                "ai_insights": "AI analysis indicates elevated risk levels due to regulatory changes.",
                "confidence_score": 0.85,
                "processing_time": 2.5,
                "timestamp": "2024-01-15T10:30:00Z"
            }
        }


class BFSIGapAnalysisResponseDto(BaseModel):
    """BFSI gap analysis response DTO"""
    gap_id: str = Field(..., description="Unique gap identifier")
    policy_name: str = Field(..., description="Policy name")
    framework: str = Field(..., description="Compliance framework")
    severity: str = Field(..., description="Gap severity level")
    description: str = Field(..., description="Gap description")
    current_status: str = Field(..., description="Current implementation status")
    required_actions: List[str] = Field(..., description="Required actions to address gap")
    timeline: str = Field(..., description="Recommended timeline for resolution")
    priority: str = Field(..., description="Gap priority level")
    
    class Config:
        json_schema_extra = {
            "example": {
                "gap_id": "123e4567-e89b-12d3-a456-426614174000",
                "policy_name": "SOX Financial Controls",
                "framework": "SOX",
                "severity": "high",
                "description": "Missing financial control documentation",
                "current_status": "missing",
                "required_actions": [
                    "Develop revenue recognition controls",
                    "Document control procedures"
                ],
                "timeline": "30 days",
                "priority": "critical"
            }
        }


class BFSIAgentStatusResponseDto(BaseModel):
    """BFSI AI agent status response DTO"""
    agent_id: str = Field(..., description="Agent identifier")
    name: str = Field(..., description="Agent name")
    status: str = Field(..., description="Agent status")
    capabilities: List[str] = Field(..., description="Agent capabilities")
    last_updated: str = Field(..., description="Last update timestamp")
    version: str = Field(..., description="Agent version")
    
    class Config:
        json_schema_extra = {
            "example": {
                "agent_id": "bfsi-ai-service",
                "name": "BFSI AI Service",
                "status": "active",
                "capabilities": [
                    "risk_assessment",
                    "compliance_check",
                    "policy_review",
                    "gap_analysis"
                ],
                "last_updated": "2024-01-15T10:30:00Z",
                "version": "1.0.0"
            }
        }


class BFSIAnalysisHistoryDto(BaseModel):
    """BFSI analysis history DTO"""
    analysis_id: str = Field(..., description="Analysis identifier")
    analysis_type: str = Field(..., description="Analysis type")
    business_unit: str = Field(..., description="Business unit")
    industry_type: str = Field(..., description="Industry type")
    risk_score: float = Field(..., description="Risk score")
    compliance_score: float = Field(..., description="Compliance score")
    confidence_score: float = Field(..., description="AI confidence score")
    timestamp: datetime = Field(..., description="Analysis timestamp")
    user_id: str = Field(..., description="User who performed analysis")
    
    class Config:
        json_schema_extra = {
            "example": {
                "analysis_id": "123e4567-e89b-12d3-a456-426614174000",
                "analysis_type": "risk_assessment",
                "business_unit": "retail",
                "industry_type": "bfsi",
                "risk_score": 0.75,
                "compliance_score": 0.68,
                "confidence_score": 0.85,
                "timestamp": "2024-01-15T10:30:00Z",
                "user_id": "user-123"
            }
        }


class BFSIAnalysisSummaryDto(BaseModel):
    """BFSI analysis summary DTO"""
    total_analyses: int = Field(..., description="Total number of analyses")
    risk_assessments: int = Field(..., description="Number of risk assessments")
    compliance_checks: int = Field(..., description="Number of compliance checks")
    policy_reviews: int = Field(..., description="Number of policy reviews")
    gap_analyses: int = Field(..., description="Number of gap analyses")
    average_risk_score: float = Field(..., description="Average risk score")
    average_compliance_score: float = Field(..., description="Average compliance score")
    average_confidence_score: float = Field(..., description="Average AI confidence score")
    last_analysis: Optional[datetime] = Field(None, description="Last analysis timestamp")
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_analyses": 150,
                "risk_assessments": 45,
                "compliance_checks": 38,
                "policy_reviews": 32,
                "gap_analyses": 35,
                "average_risk_score": 0.72,
                "average_compliance_score": 0.68,
                "average_confidence_score": 0.82,
                "last_analysis": "2024-01-15T10:30:00Z"
            }
        }
