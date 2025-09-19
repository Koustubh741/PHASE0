"""
GRC Workflow Engine
Orchestrates industry-specific GRC operations across different sectors
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from enum import Enum

from core.industry_agent import IndustryType, GRCOperationType
from base.mcp_broker import MCPBroker

class WorkflowStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class WorkflowPriority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class GRCWorkflowEngine:
    """
    GRC Workflow Engine for orchestrating industry-specific GRC operations
    Similar to Archer GRC workflow capabilities
    """
    
    def __init__(self):
        self.mcp_broker = MCPBroker()
        self.workflows = {}
        self.industry_agents = {}
        self.workflow_templates = {}
        self.reporting_engine = None
        
        # Initialize workflow templates
        self._initialize_workflow_templates()
        
        logging.info("GRC Workflow Engine initialized")

    def _initialize_workflow_templates(self):
        """Initialize standard GRC workflow templates"""
        self.workflow_templates = {
            "comprehensive_grc_assessment": {
                "name": "Comprehensive GRC Assessment",
                "description": "Full GRC assessment across all risk categories",
                "industries": ["bfsi", "telecom", "manufacturing", "healthcare"],
                "operations": [
                    "risk_assessment",
                    "compliance_check",
                    "policy_review",
                    "audit_planning"
                ],
                "estimated_duration": "2-4 weeks",
                "priority": "high"
            },
            "quarterly_compliance_review": {
                "name": "Quarterly Compliance Review",
                "description": "Quarterly compliance assessment and reporting",
                "industries": ["bfsi", "telecom", "manufacturing", "healthcare"],
                "operations": [
                    "compliance_check",
                    "regulatory_reporting",
                    "policy_review"
                ],
                "estimated_duration": "1-2 weeks",
                "priority": "high"
            },
            "risk_assessment_workflow": {
                "name": "Risk Assessment Workflow",
                "description": "Comprehensive risk assessment and mitigation planning",
                "industries": ["bfsi", "telecom", "manufacturing", "healthcare"],
                "operations": [
                    "risk_assessment",
                    "third_party_assessment",
                    "business_continuity"
                ],
                "estimated_duration": "1-3 weeks",
                "priority": "medium"
            },
            "incident_response_workflow": {
                "name": "Incident Response Workflow",
                "description": "Automated incident response and recovery",
                "industries": ["bfsi", "telecom", "manufacturing", "healthcare"],
                "operations": [
                    "incident_response",
                    "compliance_check",
                    "regulatory_reporting"
                ],
                "estimated_duration": "1-7 days",
                "priority": "critical"
            },
            "audit_planning_workflow": {
                "name": "Audit Planning Workflow",
                "description": "Comprehensive audit planning and execution",
                "industries": ["bfsi", "telecom", "manufacturing", "healthcare"],
                "operations": [
                    "audit_planning",
                    "compliance_check",
                    "policy_review"
                ],
                "estimated_duration": "2-6 weeks",
                "priority": "medium"
            }
        }

    async def register_industry_agent(self, industry: IndustryType, agent):
        """Register an industry-specific GRC agent"""
        self.industry_agents[industry] = agent
        logging.info(f"Registered {industry.value} GRC agent")

    async def create_workflow(self, workflow_template: str, industry: IndustryType, 
                            context: Dict[str, Any]) -> str:
        """Create a new GRC workflow"""
        if workflow_template not in self.workflow_templates:
            raise ValueError(f"Unknown workflow template: {workflow_template}")
        
        template = self.workflow_templates[workflow_template]
        
        if industry.value not in template["industries"]:
            raise ValueError(f"Industry {industry.value} not supported for workflow {workflow_template}")
        
        workflow_id = f"workflow_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{industry.value}"
        
        workflow = {
            "id": workflow_id,
            "template": workflow_template,
            "name": template["name"],
            "description": template["description"],
            "industry": industry.value,
            "status": WorkflowStatus.PENDING.value,
            "priority": template["priority"],
            "created_at": datetime.now().isoformat(),
            "estimated_duration": template["estimated_duration"],
            "operations": template["operations"],
            "context": context,
            "results": {},
            "current_step": 0,
            "total_steps": len(template["operations"]),
            "progress": 0.0,
            "started_at": None,
            "completed_at": None,
            "error": None
        }
        
        self.workflows[workflow_id] = workflow
        
        logging.info(f"Created workflow {workflow_id} for {industry.value}")
        return workflow_id

    async def execute_workflow(self, workflow_id: str) -> Dict[str, Any]:
        """Execute a GRC workflow"""
        if workflow_id not in self.workflows:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        workflow = self.workflows[workflow_id]
        
        if workflow["status"] != WorkflowStatus.PENDING.value:
            raise ValueError(f"Workflow {workflow_id} is not in pending status")
        
        try:
            # Update workflow status
            workflow["status"] = WorkflowStatus.RUNNING.value
            workflow["started_at"] = datetime.now().isoformat()
            
            # Get industry agent
            industry = IndustryType(workflow["industry"])
            if industry not in self.industry_agents:
                raise ValueError(f"No agent registered for industry {industry.value}")
            
            agent = self.industry_agents[industry]
            
            # Execute workflow operations
            results = {}
            total_operations = len(workflow["operations"])
            
            for i, operation_name in enumerate(workflow["operations"]):
                try:
                    logging.info(f"Executing operation {operation_name} for workflow {workflow_id}")
                    
                    # Update progress
                    workflow["current_step"] = i + 1
                    workflow["progress"] = (i / total_operations) * 100
                    
                    # Execute operation
                    operation_type = GRCOperationType(operation_name)
                    operation_result = await agent.perform_grc_operation(operation_type, workflow["context"])
                    
                    results[operation_name] = operation_result
                    
                    # Check if operation failed
                    if not operation_result.get("success", False):
                        logging.warning(f"Operation {operation_name} failed in workflow {workflow_id}")
                        # Continue with other operations unless it's critical
                        if workflow["priority"] == WorkflowPriority.CRITICAL.value:
                            raise Exception(f"Critical operation {operation_name} failed")
                    
                except Exception as e:
                    logging.error(f"Error in operation {operation_name}: {str(e)}")
                    results[operation_name] = {
                        "success": False,
                        "error": str(e),
                        "operation": operation_name,
                        "timestamp": datetime.now().isoformat()
                    }
            
            # Complete workflow
            workflow["results"] = results
            workflow["status"] = WorkflowStatus.COMPLETED.value
            workflow["completed_at"] = datetime.now().isoformat()
            workflow["progress"] = 100.0
            
            # Generate workflow report
            workflow_report = await self._generate_workflow_report(workflow)
            workflow["report"] = workflow_report
            
            logging.info(f"Workflow {workflow_id} completed successfully")
            
            return {
                "success": True,
                "workflow_id": workflow_id,
                "status": workflow["status"],
                "results": results,
                "report": workflow_report,
                "duration": self._calculate_workflow_duration(workflow)
            }
            
        except Exception as e:
            logging.error(f"Workflow {workflow_id} failed: {str(e)}")
            
            # Update workflow status
            workflow["status"] = WorkflowStatus.FAILED.value
            workflow["error"] = str(e)
            workflow["completed_at"] = datetime.now().isoformat()
            
            return {
                "success": False,
                "workflow_id": workflow_id,
                "status": workflow["status"],
                "error": str(e),
                "duration": self._calculate_workflow_duration(workflow)
            }

    async def get_workflow_status(self, workflow_id: str) -> Dict[str, Any]:
        """Get workflow status and progress"""
        if workflow_id not in self.workflows:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        workflow = self.workflows[workflow_id]
        
        return {
            "workflow_id": workflow_id,
            "status": workflow["status"],
            "progress": workflow["progress"],
            "current_step": workflow["current_step"],
            "total_steps": workflow["total_steps"],
            "created_at": workflow["created_at"],
            "started_at": workflow["started_at"],
            "completed_at": workflow["completed_at"],
            "estimated_duration": workflow["estimated_duration"],
            "priority": workflow["priority"],
            "industry": workflow["industry"],
            "error": workflow.get("error")
        }

    async def list_workflows(self, status: Optional[str] = None, 
                           industry: Optional[str] = None) -> List[Dict[str, Any]]:
        """List workflows with optional filtering"""
        workflows = []
        
        for workflow_id, workflow in self.workflows.items():
            # Apply filters
            if status and workflow["status"] != status:
                continue
            if industry and workflow["industry"] != industry:
                continue
            
            workflows.append({
                "workflow_id": workflow_id,
                "name": workflow["name"],
                "description": workflow["description"],
                "industry": workflow["industry"],
                "status": workflow["status"],
                "priority": workflow["priority"],
                "progress": workflow["progress"],
                "created_at": workflow["created_at"],
                "estimated_duration": workflow["estimated_duration"]
            })
        
        return workflows

    async def cancel_workflow(self, workflow_id: str) -> Dict[str, Any]:
        """Cancel a running workflow"""
        if workflow_id not in self.workflows:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        workflow = self.workflows[workflow_id]
        
        if workflow["status"] not in [WorkflowStatus.PENDING.value, WorkflowStatus.RUNNING.value]:
            raise ValueError(f"Cannot cancel workflow in status {workflow['status']}")
        
        workflow["status"] = WorkflowStatus.CANCELLED.value
        workflow["completed_at"] = datetime.now().isoformat()
        
        logging.info(f"Workflow {workflow_id} cancelled")
        
        return {
            "success": True,
            "workflow_id": workflow_id,
            "status": workflow["status"],
            "message": "Workflow cancelled successfully"
        }

    async def _generate_workflow_report(self, workflow: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive workflow report"""
        industry = IndustryType(workflow["industry"])
        agent = self.industry_agents.get(industry)
        
        # Aggregate results from all operations
        total_operations = len(workflow["operations"])
        successful_operations = sum(1 for result in workflow["results"].values() 
                                  if result.get("success", False))
        
        # Calculate overall success rate
        success_rate = (successful_operations / total_operations) * 100 if total_operations > 0 else 0
        
        # Generate industry-specific insights
        insights = await self._generate_industry_insights(workflow, agent)
        
        # Generate recommendations
        recommendations = await self._generate_workflow_recommendations(workflow)
        
        report = {
            "workflow_id": workflow["id"],
            "workflow_name": workflow["name"],
            "industry": workflow["industry"],
            "execution_summary": {
                "total_operations": total_operations,
                "successful_operations": successful_operations,
                "failed_operations": total_operations - successful_operations,
                "success_rate": round(success_rate, 2),
                "duration": self._calculate_workflow_duration(workflow),
                "started_at": workflow["started_at"],
                "completed_at": workflow["completed_at"]
            },
            "operation_results": workflow["results"],
            "industry_insights": insights,
            "recommendations": recommendations,
            "next_steps": await self._generate_next_steps(workflow),
            "generated_at": datetime.now().isoformat()
        }
        
        return report

    async def _generate_industry_insights(self, workflow: Dict[str, Any], agent) -> Dict[str, Any]:
        """Generate industry-specific insights from workflow results"""
        insights = {
            "industry": workflow["industry"],
            "key_findings": [],
            "risk_summary": {},
            "compliance_summary": {},
            "performance_metrics": {}
        }
        
        # Analyze results based on industry
        for operation_name, result in workflow["results"].items():
            if not result.get("success", False):
                continue
            
            if operation_name == "risk_assessment":
                insights["risk_summary"] = {
                    "risks_identified": result.get("risks_identified", 0),
                    "risk_scores": result.get("risk_scores", {}),
                    "recommendations": result.get("recommendations", [])
                }
            
            elif operation_name == "compliance_check":
                insights["compliance_summary"] = {
                    "compliance_score": result.get("compliance_score", 0),
                    "requirements_checked": result.get("requirements_checked", 0),
                    "compliance_results": result.get("compliance_results", {})
                }
            
            elif operation_name == "policy_review":
                insights["key_findings"].append({
                    "area": "Policy Review",
                    "finding": f"Policy alignment score: {result.get('policy_analysis', {}).get('alignment_score', 'N/A')}",
                    "priority": "medium"
                })
        
        return insights

    async def _generate_workflow_recommendations(self, workflow: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate workflow-specific recommendations"""
        recommendations = []
        
        # Analyze workflow results for recommendations
        for operation_name, result in workflow["results"].items():
            if not result.get("success", False):
                recommendations.append({
                    "priority": "high",
                    "category": "Workflow Execution",
                    "recommendation": f"Address failure in {operation_name} operation",
                    "action": "Review and fix the failed operation",
                    "timeline": "immediate"
                })
                continue
            
            if operation_name == "risk_assessment":
                risk_recommendations = result.get("recommendations", [])
                for rec in risk_recommendations:
                    if rec.get("priority") in ["high", "critical"]:
                        recommendations.append({
                            "priority": rec.get("priority", "medium"),
                            "category": "Risk Management",
                            "recommendation": rec.get("recommendation", ""),
                            "action": rec.get("action_plan", []),
                            "timeline": rec.get("timeline", "30 days")
                        })
            
            elif operation_name == "compliance_check":
                compliance_score = result.get("compliance_score", 0)
                if compliance_score < 80:
                    recommendations.append({
                        "priority": "high",
                        "category": "Compliance",
                        "recommendation": f"Improve compliance score from {compliance_score}% to above 80%",
                        "action": "Address non-compliant requirements",
                        "timeline": "90 days"
                    })
        
        return recommendations

    async def _generate_next_steps(self, workflow: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate next steps based on workflow results"""
        next_steps = []
        
        # Schedule follow-up assessments
        next_steps.append({
            "step": "Schedule Follow-up Assessment",
            "description": f"Schedule next {workflow['name']} in 90 days",
            "timeline": "30 days",
            "owner": "GRC Team"
        })
        
        # Address high-priority findings
        for operation_name, result in workflow["results"].items():
            if operation_name == "risk_assessment":
                high_risk_recommendations = [r for r in result.get("recommendations", []) 
                                           if r.get("priority") in ["high", "critical"]]
                if high_risk_recommendations:
                    next_steps.append({
                        "step": "Address High-Risk Findings",
                        "description": f"Implement {len(high_risk_recommendations)} high-priority risk mitigation measures",
                        "timeline": "60 days",
                        "owner": "Risk Management Team"
                    })
        
        return next_steps

    def _calculate_workflow_duration(self, workflow: Dict[str, Any]) -> str:
        """Calculate workflow execution duration"""
        if not workflow["started_at"] or not workflow["completed_at"]:
            return "N/A"
        
        start_time = datetime.fromisoformat(workflow["started_at"])
        end_time = datetime.fromisoformat(workflow["completed_at"])
        duration = end_time - start_time
        
        if duration.days > 0:
            return f"{duration.days} days, {duration.seconds // 3600} hours"
        elif duration.seconds > 3600:
            return f"{duration.seconds // 3600} hours, {(duration.seconds % 3600) // 60} minutes"
        else:
            return f"{duration.seconds // 60} minutes, {duration.seconds % 60} seconds"

    async def get_workflow_templates(self) -> Dict[str, Any]:
        """Get available workflow templates"""
        return self.workflow_templates

    async def create_custom_workflow(self, name: str, description: str, 
                                   industry: IndustryType, operations: List[str],
                                   context: Dict[str, Any]) -> str:
        """Create a custom GRC workflow"""
        workflow_id = f"custom_workflow_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{industry.value}"
        
        workflow = {
            "id": workflow_id,
            "template": "custom",
            "name": name,
            "description": description,
            "industry": industry.value,
            "status": WorkflowStatus.PENDING.value,
            "priority": "medium",
            "created_at": datetime.now().isoformat(),
            "estimated_duration": "1-4 weeks",
            "operations": operations,
            "context": context,
            "results": {},
            "current_step": 0,
            "total_steps": len(operations),
            "progress": 0.0,
            "started_at": None,
            "completed_at": None,
            "error": None
        }
        
        self.workflows[workflow_id] = workflow
        
        logging.info(f"Created custom workflow {workflow_id} for {industry.value}")
        return workflow_id
