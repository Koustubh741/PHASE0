"""
Industry-Specific Multi-Agent Strategy with Ollama and Chroma
Enhanced multi-agent orchestration for each industry department
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import uuid
import json
import requests
from dataclasses import dataclass

# Import existing components
from multi_agent_strategy import MultiAgentOrchestrator, Task, TaskPriority, TaskStatus
from advanced_mcp_protocol import AdvancedMCPBroker, MessageType, MessagePriority
from vector_db.chroma_service import ChromaService

# Import BFSI agent only - other industry agents disabled
from agents.bfsi.bfsi_grc_agent import BFSIGRCAgent
# COMMENTED OUT - Other industry agents disabled
# from agents.telecom.telecom_grc_agent import TelecomGRCAgent
# from agents.manufacturing.manufacturing_grc_agent import ManufacturingGRCAgent
# from agents.healthcare.healthcare_grc_agent import HealthcareGRCAgent

logger = logging.getLogger(__name__)

@dataclass
class IndustryAgentCapability:
    """Industry-specific agent capability"""
    agent_id: str
    industry: str
    capabilities: List[str]
    ollama_model: str
    chroma_collection: str
    performance_score: float
    specialization: str

class OllamaIntegration:
    """Ollama LLM integration for local AI processing"""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.available_models = []
        self._load_available_models()
    
    def _load_available_models(self):
        """Load available Ollama models"""
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            if response.status_code == 200:
                models_data = response.json()
                self.available_models = [model["name"] for model in models_data.get("models", [])]
                logger.info(f"Available Ollama models: {self.available_models}")
            else:
                logger.warning("Could not fetch Ollama models")
        except Exception as e:
            logger.error(f"Failed to load Ollama models: {e}")
    
    async def generate_response(self, model: str, prompt: str, context: str = "") -> str:
        """Generate response using Ollama model"""
        try:
            full_prompt = f"{context}\n\n{prompt}" if context else prompt
            
            payload = {
                "model": model,
                "prompt": full_prompt,
                "stream": False,
                "options": {
                    "temperature": 0.1,
                    "top_p": 0.9,
                    "max_tokens": 2000
                }
            }
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("response", "")
            else:
                logger.error(f"Ollama API error: {response.status_code}")
                return ""
                
        except Exception as e:
            logger.error(f"Failed to generate response with Ollama: {e}")
            return ""
    
    async def analyze_compliance(self, model: str, content: str, regulations: List[str]) -> Dict[str, Any]:
        """Analyze compliance using Ollama"""
        try:
            regulations_text = "\n".join([f"- {reg}" for reg in regulations])
            
            prompt = f"""
            Analyze the following content for compliance against these regulations:
            
            Regulations:
            {regulations_text}
            
            Content to analyze:
            {content}
            
            Provide a JSON response with:
            {{
                "compliance_status": "compliant|non-compliant|partially-compliant",
                "violations": ["list of specific violations"],
                "recommendations": ["list of recommendations"],
                "confidence": 0.95,
                "regulations_checked": ["list of regulations checked"]
            }}
            """
            
            response = await self.generate_response(model, prompt)
            
            # Try to parse JSON response
            try:
                # Extract JSON from response if it's wrapped in text
                start_idx = response.find('{')
                end_idx = response.rfind('}') + 1
                if start_idx != -1 and end_idx != 0:
                    json_str = response[start_idx:end_idx]
                    return json.loads(json_str)
                else:
                    return json.loads(response)
            except json.JSONDecodeError:
                return {
                    "compliance_status": "partially-compliant",
                    "violations": ["Unable to parse AI response"],
                    "recommendations": ["Manual review recommended"],
                    "confidence": 0.5,
                    "regulations_checked": regulations
                }
                
        except Exception as e:
            logger.error(f"Compliance analysis failed: {e}")
            return {
                "compliance_status": "error",
                "violations": [],
                "recommendations": [f"Analysis failed: {str(e)}"],
                "confidence": 0.0,
                "regulations_checked": regulations
            }
    
    async def assess_risk(self, model: str, risk_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess risk using Ollama"""
        try:
            prompt = f"""
            Assess the following risk data and provide a comprehensive risk analysis:
            
            Risk Data:
            {json.dumps(risk_data, indent=2)}
            
            Provide a JSON response with:
            {{
                "risk_level": "low|medium|high|critical",
                "impact_score": 1-10,
                "probability_score": 1-10,
                "mitigation_strategies": ["list of mitigation strategies"],
                "monitoring_recommendations": ["list of monitoring recommendations"],
                "confidence": 0.95
            }}
            """
            
            response = await self.generate_response(model, prompt)
            
            try:
                start_idx = response.find('{')
                end_idx = response.rfind('}') + 1
                if start_idx != -1 and end_idx != 0:
                    json_str = response[start_idx:end_idx]
                    return json.loads(json_str)
                else:
                    return json.loads(response)
            except json.JSONDecodeError:
                return {
                    "risk_level": "medium",
                    "impact_score": 5,
                    "probability_score": 5,
                    "mitigation_strategies": ["Manual review recommended"],
                    "monitoring_recommendations": ["Regular monitoring required"],
                    "confidence": 0.5
                }
                
        except Exception as e:
            logger.error(f"Risk assessment failed: {e}")
            return {
                "risk_level": "medium",
                "impact_score": 5,
                "probability_score": 5,
                "mitigation_strategies": [f"Assessment failed: {str(e)}"],
                "monitoring_recommendations": ["Manual review required"],
                "confidence": 0.0
            }

class IndustryMultiAgentOrchestrator:
    """
    Industry-Specific Multi-Agent Orchestrator
    Enhanced with Ollama and Chroma for each industry
    """
    
    def __init__(self, industry: str):
        self.industry = industry
        self.ollama = OllamaIntegration()
        self.chroma_service = ChromaService()
        self.mcp_broker = AdvancedMCPBroker()
        self.agents = {}
        self.agent_capabilities = {}
        self.industry_specific_models = self._get_industry_models()
        self.chroma_collections = self._get_industry_collections()
        
    def _get_industry_models(self) -> Dict[str, str]:
        """Get BFSI-specific Ollama models only"""
        models = {
            "bfsi": "llama2:13b",  # Good for financial analysis
            # COMMENTED OUT - Other industry models disabled
            # "telecom": "mistral:7b",  # Good for technical analysis
            # "manufacturing": "codellama:7b",  # Good for technical specifications
            # "healthcare": "llama2:13b"  # Good for regulatory analysis
        }
        return models.get(self.industry, "llama2:7b")
    
    def _get_industry_collections(self) -> Dict[str, str]:
        """Get BFSI-specific Chroma collections only"""
        collections = {
            "bfsi": "bfsi_regulations",
            # COMMENTED OUT - Other industry collections disabled
            # "telecom": "telecom_standards", 
            # "manufacturing": "manufacturing_standards",
            # "healthcare": "healthcare_regulations"
        }
        return collections.get(self.industry, f"{self.industry}_documents")
    
    async def initialize(self):
        """Initialize industry-specific multi-agent orchestrator"""
        try:
            # Initialize MCP broker
            await self.mcp_broker.initialize()
            
            # Initialize Chroma collections
            await self._initialize_chroma_collections()
            
            # Initialize industry-specific agents
            await self._initialize_industry_agents()
            
            # Register agents with MCP broker
            await self._register_industry_agents()
            
            logger.info(f"Industry Multi-Agent Orchestrator for {self.industry} initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize {self.industry} orchestrator: {e}")
            raise
    
    async def _initialize_chroma_collections(self):
        """Initialize Chroma collections for industry"""
        try:
            # Create main industry collection
            main_collection = self.chroma_service.get_or_create_collection(
                self.chroma_collections
            )
            
            # Create specialized collections
            specialized_collections = {
                f"{self.industry}_policies": "Industry policies and procedures",
                f"{self.industry}_risks": "Risk assessments and scenarios",
                f"{self.industry}_compliance": "Compliance requirements and frameworks",
                f"{self.industry}_incidents": "Incident reports and lessons learned"
            }
            
            for collection_name, description in specialized_collections.items():
                self.chroma_service.get_or_create_collection(collection_name)
                logger.info(f"Created Chroma collection: {collection_name}")
            
        except Exception as e:
            logger.error(f"Failed to initialize Chroma collections: {e}")
    
    async def _initialize_industry_agents(self):
        """Initialize BFSI agents only - other industries disabled"""
        try:
            if self.industry == "bfsi":
                await self._initialize_bfsi_agents()
            # COMMENTED OUT - Other industry agents disabled
            # elif self.industry == "telecom":
            #     await self._initialize_telecom_agents()
            # elif self.industry == "manufacturing":
            #     await self._initialize_manufacturing_agents()
            # elif self.industry == "healthcare":
            #     await self._initialize_healthcare_agents()
            else:
                logger.warning(f"Industry {self.industry} not supported - only BFSI is active")
                
        except Exception as e:
            logger.error(f"Failed to initialize BFSI agents: {e}")
    
    async def _initialize_bfsi_agents(self):
        """Initialize BFSI-specific agents"""
        self.agents = {
            "bfsi_compliance_coordinator": BFSIComplianceCoordinatorAgent(),
            "bfsi_risk_analyzer": BFSIRiskAnalyzerAgent(),
            "bfsi_regulatory_monitor": BFSIRegulatoryMonitorAgent(),
            "bfsi_aml_analyzer": BFSIAMLAnalyzerAgent(),
            "bfsi_capital_adequacy": BFSICapitalAdequacyAgent(),
            "bfsi_operational_risk": BFSIOperationalRiskAgent(),
            "bfsi_cyber_security": BFSICyberSecurityAgent(),
            "bfsi_fraud_detection": BFSIFraudDetectionAgent()
        }
        
        # Define capabilities
        self.agent_capabilities = {
            "bfsi_compliance_coordinator": IndustryAgentCapability(
                agent_id="bfsi_compliance_coordinator",
                industry="bfsi",
                capabilities=["compliance_management", "regulatory_coordination", "stakeholder_communication"],
                ollama_model=self.industry_specific_models,
                chroma_collection="bfsi_compliance",
                performance_score=0.95,
                specialization="compliance_coordination"
            ),
            "bfsi_risk_analyzer": IndustryAgentCapability(
                agent_id="bfsi_risk_analyzer",
                industry="bfsi",
                capabilities=["risk_modeling", "statistical_analysis", "stress_testing"],
                ollama_model=self.industry_specific_models,
                chroma_collection="bfsi_risks",
                performance_score=0.92,
                specialization="risk_analysis"
            ),
            "bfsi_aml_analyzer": IndustryAgentCapability(
                agent_id="bfsi_aml_analyzer",
                industry="bfsi",
                capabilities=["aml_analysis", "transaction_monitoring", "suspicious_activity_detection"],
                ollama_model=self.industry_specific_models,
                chroma_collection="bfsi_aml",
                performance_score=0.90,
                specialization="aml_compliance"
            )
        }
    
    async def _initialize_telecom_agents(self):
        """Initialize Telecom-specific agents"""
        self.agents = {
            "telecom_compliance_coordinator": TelecomComplianceCoordinatorAgent(),
            "telecom_network_security": TelecomNetworkSecurityAgent(),
            "telecom_spectrum_management": TelecomSpectrumManagementAgent(),
            "telecom_service_quality": TelecomServiceQualityAgent(),
            "telecom_privacy_compliance": TelecomPrivacyComplianceAgent(),
            "telecom_cyber_security": TelecomCyberSecurityAgent(),
            "telecom_incident_response": TelecomIncidentResponseAgent()
        }
        
        # Define capabilities
        self.agent_capabilities = {
            "telecom_compliance_coordinator": IndustryAgentCapability(
                agent_id="telecom_compliance_coordinator",
                industry="telecom",
                capabilities=["fcc_compliance", "spectrum_management", "service_quality"],
                ollama_model=self.industry_specific_models,
                chroma_collection="telecom_compliance",
                performance_score=0.93,
                specialization="telecom_compliance"
            ),
            "telecom_network_security": IndustryAgentCapability(
                agent_id="telecom_network_security",
                industry="telecom",
                capabilities=["network_security", "vulnerability_assessment", "threat_detection"],
                ollama_model=self.industry_specific_models,
                chroma_collection="telecom_security",
                performance_score=0.91,
                specialization="network_security"
            )
        }
    
    async def _initialize_manufacturing_agents(self):
        """Initialize Manufacturing-specific agents"""
        self.agents = {
            "manufacturing_compliance_coordinator": ManufacturingComplianceCoordinatorAgent(),
            "manufacturing_quality_control": ManufacturingQualityControlAgent(),
            "manufacturing_safety_compliance": ManufacturingSafetyComplianceAgent(),
            "manufacturing_supply_chain": ManufacturingSupplyChainAgent(),
            "manufacturing_environmental": ManufacturingEnvironmentalAgent(),
            "manufacturing_cyber_security": ManufacturingCyberSecurityAgent(),
            "manufacturing_incident_response": ManufacturingIncidentResponseAgent()
        }
        
        # Define capabilities
        self.agent_capabilities = {
            "manufacturing_compliance_coordinator": IndustryAgentCapability(
                agent_id="manufacturing_compliance_coordinator",
                industry="manufacturing",
                capabilities=["iso_compliance", "quality_management", "safety_standards"],
                ollama_model=self.industry_specific_models,
                chroma_collection="manufacturing_compliance",
                performance_score=0.94,
                specialization="manufacturing_compliance"
            ),
            "manufacturing_quality_control": IndustryAgentCapability(
                agent_id="manufacturing_quality_control",
                industry="manufacturing",
                capabilities=["quality_assurance", "statistical_process_control", "defect_analysis"],
                ollama_model=self.industry_specific_models,
                chroma_collection="manufacturing_quality",
                performance_score=0.89,
                specialization="quality_control"
            )
        }
    
    async def _initialize_healthcare_agents(self):
        """Initialize Healthcare-specific agents"""
        self.agents = {
            "healthcare_compliance_coordinator": HealthcareComplianceCoordinatorAgent(),
            "healthcare_hipaa_compliance": HealthcareHIPAAComplianceAgent(),
            "healthcare_patient_safety": HealthcarePatientSafetyAgent(),
            "healthcare_clinical_risk": HealthcareClinicalRiskAgent(),
            "healthcare_data_privacy": HealthcareDataPrivacyAgent(),
            "healthcare_cyber_security": HealthcareCyberSecurityAgent(),
            "healthcare_incident_response": HealthcareIncidentResponseAgent()
        }
        
        # Define capabilities
        self.agent_capabilities = {
            "healthcare_compliance_coordinator": IndustryAgentCapability(
                agent_id="healthcare_compliance_coordinator",
                industry="healthcare",
                capabilities=["hipaa_compliance", "fda_regulations", "patient_safety"],
                ollama_model=self.industry_specific_models,
                chroma_collection="healthcare_compliance",
                performance_score=0.96,
                specialization="healthcare_compliance"
            ),
            "healthcare_hipaa_compliance": IndustryAgentCapability(
                agent_id="healthcare_hipaa_compliance",
                industry="healthcare",
                capabilities=["hipaa_analysis", "phi_protection", "breach_assessment"],
                ollama_model=self.industry_specific_models,
                chroma_collection="healthcare_hipaa",
                performance_score=0.92,
                specialization="hipaa_compliance"
            )
        }
    
    async def _register_industry_agents(self):
        """Register industry agents with MCP broker"""
        for agent_id, agent in self.agents.items():
            capabilities = self.agent_capabilities.get(agent_id, IndustryAgentCapability(
                agent_id=agent_id,
                industry=self.industry,
                capabilities=["general_processing"],
                ollama_model=self.industry_specific_models,
                chroma_collection=self.chroma_collections,
                performance_score=0.8,
                specialization="general"
            ))
            
            await self.mcp_broker.register_agent(
                agent_id, 
                agent, 
                capabilities.capabilities
            )
            logger.info(f"Registered {self.industry} agent: {agent_id}")
    
    async def execute_industry_analysis(self, 
                                      organization_id: str,
                                      analysis_type: str = "comprehensive") -> Dict[str, Any]:
        """
        Execute industry-specific analysis using multi-agent strategy
        """
        try:
            logger.info(f"Starting {self.industry} industry analysis for organization {organization_id}")
            
            # Create industry-specific analysis scope
            analysis_scope = {
                "organization_id": organization_id,
                "industry": self.industry,
                "analysis_type": analysis_type,
                "ollama_model": self.industry_specific_models,
                "chroma_collections": list(self.chroma_collections.keys()) if isinstance(self.chroma_collections, dict) else [self.chroma_collections]
            }
            
            # Create industry-specific tasks
            tasks = await self._create_industry_tasks(organization_id, analysis_scope)
            
            # Execute tasks using multi-agent strategy
            start_time = datetime.now()
            results = await self._execute_industry_tasks(tasks)
            end_time = datetime.now()
            
            # Synthesize results using Ollama
            synthesized_results = await self._synthesize_industry_results(results, analysis_scope)
            
            return {
                "industry": self.industry,
                "organization_id": organization_id,
                "analysis_results": synthesized_results,
                "performance_metrics": {
                    "execution_time": (end_time - start_time).total_seconds(),
                    "agents_used": len(self.agents),
                    "tasks_completed": len(results),
                    "ollama_model": self.industry_specific_models,
                    "chroma_collections": analysis_scope["chroma_collections"]
                },
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to execute {self.industry} industry analysis: {e}")
            raise
    
    async def _create_industry_tasks(self, organization_id: str, scope: Dict[str, Any]) -> List[Task]:
        """Create industry-specific tasks"""
        tasks = []
        base_context = {
            "organization_id": organization_id,
            "industry": self.industry,
            "scope": scope
        }
        
        if self.industry == "bfsi":
            tasks.extend([
                Task(
                    task_id=f"bfsi_basel_compliance_{uuid.uuid4()}",
                    task_type="basel_compliance_check",
                    priority=TaskPriority.HIGH,
                    complexity=0.9,
                    required_capabilities=["compliance_management", "regulatory_analysis"],
                    deadline=datetime.now() + timedelta(minutes=30),
                    context={**base_context, "regulation": "Basel III"},
                    dependencies=[],
                    created_at=datetime.now()
                ),
                Task(
                    task_id=f"bfsi_aml_analysis_{uuid.uuid4()}",
                    task_type="aml_analysis",
                    priority=TaskPriority.HIGH,
                    complexity=0.8,
                    required_capabilities=["aml_analysis", "transaction_monitoring"],
                    deadline=datetime.now() + timedelta(minutes=25),
                    context=base_context,
                    dependencies=[],
                    created_at=datetime.now()
                ),
                Task(
                    task_id=f"bfsi_risk_assessment_{uuid.uuid4()}",
                    task_type="risk_assessment",
                    priority=TaskPriority.CRITICAL,
                    complexity=1.0,
                    required_capabilities=["risk_modeling", "statistical_analysis"],
                    deadline=datetime.now() + timedelta(minutes=40),
                    context=base_context,
                    dependencies=[],
                    created_at=datetime.now()
                )
            ])
        
        elif self.industry == "telecom":
            tasks.extend([
                Task(
                    task_id=f"telecom_fcc_compliance_{uuid.uuid4()}",
                    task_type="fcc_compliance_check",
                    priority=TaskPriority.HIGH,
                    complexity=0.8,
                    required_capabilities=["fcc_compliance", "spectrum_management"],
                    deadline=datetime.now() + timedelta(minutes=30),
                    context={**base_context, "regulation": "FCC"},
                    dependencies=[],
                    created_at=datetime.now()
                ),
                Task(
                    task_id=f"telecom_network_security_{uuid.uuid4()}",
                    task_type="network_security_assessment",
                    priority=TaskPriority.HIGH,
                    complexity=0.9,
                    required_capabilities=["network_security", "vulnerability_assessment"],
                    deadline=datetime.now() + timedelta(minutes=35),
                    context=base_context,
                    dependencies=[],
                    created_at=datetime.now()
                )
            ])
        
        elif self.industry == "manufacturing":
            tasks.extend([
                Task(
                    task_id=f"manufacturing_iso_compliance_{uuid.uuid4()}",
                    task_type="iso_compliance_check",
                    priority=TaskPriority.HIGH,
                    complexity=0.8,
                    required_capabilities=["iso_compliance", "quality_management"],
                    deadline=datetime.now() + timedelta(minutes=30),
                    context={**base_context, "standard": "ISO 9001"},
                    dependencies=[],
                    created_at=datetime.now()
                ),
                Task(
                    task_id=f"manufacturing_safety_assessment_{uuid.uuid4()}",
                    task_type="safety_assessment",
                    priority=TaskPriority.CRITICAL,
                    complexity=0.9,
                    required_capabilities=["safety_standards", "risk_assessment"],
                    deadline=datetime.now() + timedelta(minutes=35),
                    context=base_context,
                    dependencies=[],
                    created_at=datetime.now()
                )
            ])
        
        elif self.industry == "healthcare":
            tasks.extend([
                Task(
                    task_id=f"healthcare_hipaa_compliance_{uuid.uuid4()}",
                    task_type="hipaa_compliance_check",
                    priority=TaskPriority.CRITICAL,
                    complexity=0.9,
                    required_capabilities=["hipaa_compliance", "phi_protection"],
                    deadline=datetime.now() + timedelta(minutes=30),
                    context={**base_context, "regulation": "HIPAA"},
                    dependencies=[],
                    created_at=datetime.now()
                ),
                Task(
                    task_id=f"healthcare_patient_safety_{uuid.uuid4()}",
                    task_type="patient_safety_assessment",
                    priority=TaskPriority.CRITICAL,
                    complexity=1.0,
                    required_capabilities=["patient_safety", "clinical_risk"],
                    deadline=datetime.now() + timedelta(minutes=40),
                    context=base_context,
                    dependencies=[],
                    created_at=datetime.now()
                )
            ])
        
        return tasks
    
    async def _execute_industry_tasks(self, tasks: List[Task]) -> Dict[str, Any]:
        """Execute industry-specific tasks using agents"""
        results = {}
        
        for task in tasks:
            try:
                # Find best agent for task
                best_agent_id = self._find_best_agent_for_task(task)
                
                if best_agent_id and best_agent_id in self.agents:
                    agent = self.agents[best_agent_id]
                    capability = self.agent_capabilities.get(best_agent_id)
                    
                    # Execute task with Ollama and Chroma integration
                    result = await self._execute_task_with_ollama_chroma(
                        agent, task, capability
                    )
                    
                    results[task.task_id] = result
                    logger.info(f"Task {task.task_id} completed by {best_agent_id}")
                else:
                    logger.warning(f"No suitable agent found for task {task.task_id}")
                    results[task.task_id] = {"error": "No suitable agent found"}
                    
            except Exception as e:
                logger.error(f"Failed to execute task {task.task_id}: {e}")
                results[task.task_id] = {"error": str(e)}
        
        return results
    
    async def _execute_task_with_ollama_chroma(self, 
                                             agent, 
                                             task: Task, 
                                             capability: IndustryAgentCapability) -> Dict[str, Any]:
        """Execute task using Ollama and Chroma integration"""
        try:
            # Get relevant documents from Chroma
            relevant_docs = await self._get_relevant_documents_from_chroma(
                task, capability.chroma_collection
            )
            
            # Prepare context for Ollama
            context = self._prepare_ollama_context(task, relevant_docs)
            
            # Execute task using Ollama
            if "compliance" in task.task_type:
                result = await self.ollama.analyze_compliance(
                    capability.ollama_model,
                    context.get("content", ""),
                    context.get("regulations", [])
                )
            elif "risk" in task.task_type:
                result = await self.ollama.assess_risk(
                    capability.ollama_model,
                    context
                )
            else:
                # General analysis
                prompt = f"Analyze the following {self.industry} industry data: {json.dumps(context, indent=2)}"
                response = await self.ollama.generate_response(
                    capability.ollama_model, prompt
                )
                result = {"analysis": response, "confidence": 0.8}
            
            # Add metadata
            result.update({
                "task_id": task.task_id,
                "agent_id": capability.agent_id,
                "industry": self.industry,
                "ollama_model": capability.ollama_model,
                "chroma_collection": capability.chroma_collection,
                "executed_at": datetime.now().isoformat()
            })
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to execute task with Ollama/Chroma: {e}")
            return {"error": str(e)}
    
    async def _get_relevant_documents_from_chroma(self, 
                                                task: Task, 
                                                collection_name: str) -> List[str]:
        """Get relevant documents from Chroma collection"""
        try:
            # Query Chroma for relevant documents
            query_text = f"{task.task_type} {self.industry} {task.context.get('organization_id', '')}"
            
            results = self.chroma_service.query_documents(
                query_texts=[query_text],
                n_results=5,
                collection_name=collection_name
            )
            
            if results and results.get('documents'):
                return results['documents'][0]
            else:
                return []
                
        except Exception as e:
            logger.error(f"Failed to get documents from Chroma: {e}")
            return []
    
    def _prepare_ollama_context(self, task: Task, relevant_docs: List[str]) -> Dict[str, Any]:
        """Prepare context for Ollama analysis"""
        context = {
            "task_type": task.task_type,
            "industry": self.industry,
            "organization_id": task.context.get("organization_id"),
            "content": task.context.get("content", ""),
            "relevant_documents": relevant_docs
        }
        
        # Add industry-specific context
        if self.industry == "bfsi":
            context["regulations"] = ["Basel III", "SOX", "PCI DSS", "AML/KYC"]
        elif self.industry == "telecom":
            context["regulations"] = ["FCC", "ITU", "ETSI", "3GPP"]
        elif self.industry == "manufacturing":
            context["regulations"] = ["ISO 9001", "ISO 14001", "OSHA", "EPA"]
        elif self.industry == "healthcare":
            context["regulations"] = ["HIPAA", "FDA", "CMS", "JCAHO"]
        
        return context
    
    async def _synthesize_industry_results(self, 
                                         results: Dict[str, Any], 
                                         scope: Dict[str, Any]) -> Dict[str, Any]:
        """Synthesize results using Ollama"""
        try:
            # Prepare synthesis prompt
            results_summary = json.dumps(results, indent=2)
            
            prompt = f"""
            Synthesize the following {self.industry} industry analysis results:
            
            Results:
            {results_summary}
            
            Provide a comprehensive synthesis with:
            {{
                "overall_assessment": "summary of overall findings",
                "key_findings": ["list of key findings"],
                "critical_issues": ["list of critical issues"],
                "recommendations": ["list of prioritized recommendations"],
                "compliance_status": "overall compliance status",
                "risk_level": "overall risk level",
                "confidence_score": 0.95
            }}
            """
            
            synthesis = await self.ollama.generate_response(
                self.industry_specific_models, prompt
            )
            
            # Try to parse JSON response
            try:
                start_idx = synthesis.find('{')
                end_idx = synthesis.rfind('}') + 1
                if start_idx != -1 and end_idx != 0:
                    json_str = synthesis[start_idx:end_idx]
                    return json.loads(json_str)
                else:
                    return json.loads(synthesis)
            except json.JSONDecodeError:
                return {
                    "overall_assessment": synthesis,
                    "key_findings": ["Analysis completed"],
                    "critical_issues": [],
                    "recommendations": ["Manual review recommended"],
                    "compliance_status": "unknown",
                    "risk_level": "medium",
                    "confidence_score": 0.7
                }
                
        except Exception as e:
            logger.error(f"Failed to synthesize results: {e}")
            return {
                "overall_assessment": f"Synthesis failed: {str(e)}",
                "key_findings": [],
                "critical_issues": [],
                "recommendations": ["Manual review required"],
                "compliance_status": "unknown",
                "risk_level": "unknown",
                "confidence_score": 0.0
            }
    
    def _find_best_agent_for_task(self, task: Task) -> Optional[str]:
        """Find the best agent for a given task"""
        suitable_agents = []
        
        for agent_id, capability in self.agent_capabilities.items():
            if all(cap in capability.capabilities for cap in task.required_capabilities):
                score = capability.performance_score
                suitable_agents.append((agent_id, score))
        
        if not suitable_agents:
            return None
        
        # Return agent with highest score
        suitable_agents.sort(key=lambda x: x[1], reverse=True)
        return suitable_agents[0][0]

# Industry-Specific Agent Classes
class BFSIComplianceCoordinatorAgent(BFSIGRCAgent):
    def __init__(self):
        super().__init__("bfsi_compliance_coordinator", "BFSI Compliance Coordinator")

class BFSIRiskAnalyzerAgent(BFSIGRCAgent):
    def __init__(self):
        super().__init__("bfsi_risk_analyzer", "BFSI Risk Analyzer")

class BFSIRegulatoryMonitorAgent(BFSIGRCAgent):
    def __init__(self):
        super().__init__("bfsi_regulatory_monitor", "BFSI Regulatory Monitor")

class BFSIAMLAnalyzerAgent(BFSIGRCAgent):
    def __init__(self):
        super().__init__("bfsi_aml_analyzer", "BFSI AML Analyzer")

class BFSICapitalAdequacyAgent(BFSIGRCAgent):
    def __init__(self):
        super().__init__("bfsi_capital_adequacy", "BFSI Capital Adequacy")

class BFSIOperationalRiskAgent(BFSIGRCAgent):
    def __init__(self):
        super().__init__("bfsi_operational_risk", "BFSI Operational Risk")

class BFSICyberSecurityAgent(BFSIGRCAgent):
    def __init__(self):
        super().__init__("bfsi_cyber_security", "BFSI Cyber Security")

class BFSIFraudDetectionAgent(BFSIGRCAgent):
    def __init__(self):
        super().__init__("bfsi_fraud_detection", "BFSI Fraud Detection")

# Telecom Agents
class TelecomComplianceCoordinatorAgent(TelecomGRCAgent):
    def __init__(self):
        super().__init__("telecom_compliance_coordinator", "Telecom Compliance Coordinator")

class TelecomNetworkSecurityAgent(TelecomGRCAgent):
    def __init__(self):
        super().__init__("telecom_network_security", "Telecom Network Security")

class TelecomSpectrumManagementAgent(TelecomGRCAgent):
    def __init__(self):
        super().__init__("telecom_spectrum_management", "Telecom Spectrum Management")

class TelecomServiceQualityAgent(TelecomGRCAgent):
    def __init__(self):
        super().__init__("telecom_service_quality", "Telecom Service Quality")

class TelecomPrivacyComplianceAgent(TelecomGRCAgent):
    def __init__(self):
        super().__init__("telecom_privacy_compliance", "Telecom Privacy Compliance")

class TelecomCyberSecurityAgent(TelecomGRCAgent):
    def __init__(self):
        super().__init__("telecom_cyber_security", "Telecom Cyber Security")

class TelecomIncidentResponseAgent(TelecomGRCAgent):
    def __init__(self):
        super().__init__("telecom_incident_response", "Telecom Incident Response")

# Manufacturing Agents
class ManufacturingComplianceCoordinatorAgent(ManufacturingGRCAgent):
    def __init__(self):
        super().__init__("manufacturing_compliance_coordinator", "Manufacturing Compliance Coordinator")

class ManufacturingQualityControlAgent(ManufacturingGRCAgent):
    def __init__(self):
        super().__init__("manufacturing_quality_control", "Manufacturing Quality Control")

class ManufacturingSafetyComplianceAgent(ManufacturingGRCAgent):
    def __init__(self):
        super().__init__("manufacturing_safety_compliance", "Manufacturing Safety Compliance")

class ManufacturingSupplyChainAgent(ManufacturingGRCAgent):
    def __init__(self):
        super().__init__("manufacturing_supply_chain", "Manufacturing Supply Chain")

class ManufacturingEnvironmentalAgent(ManufacturingGRCAgent):
    def __init__(self):
        super().__init__("manufacturing_environmental", "Manufacturing Environmental")

class ManufacturingCyberSecurityAgent(ManufacturingGRCAgent):
    def __init__(self):
        super().__init__("manufacturing_cyber_security", "Manufacturing Cyber Security")

class ManufacturingIncidentResponseAgent(ManufacturingGRCAgent):
    def __init__(self):
        super().__init__("manufacturing_incident_response", "Manufacturing Incident Response")

# Healthcare Agents
class HealthcareComplianceCoordinatorAgent(HealthcareGRCAgent):
    def __init__(self):
        super().__init__("healthcare_compliance_coordinator", "Healthcare Compliance Coordinator")

class HealthcareHIPAAComplianceAgent(HealthcareGRCAgent):
    def __init__(self):
        super().__init__("healthcare_hipaa_compliance", "Healthcare HIPAA Compliance")

class HealthcarePatientSafetyAgent(HealthcareGRCAgent):
    def __init__(self):
        super().__init__("healthcare_patient_safety", "Healthcare Patient Safety")

class HealthcareClinicalRiskAgent(HealthcareGRCAgent):
    def __init__(self):
        super().__init__("healthcare_clinical_risk", "Healthcare Clinical Risk")

class HealthcareDataPrivacyAgent(HealthcareGRCAgent):
    def __init__(self):
        super().__init__("healthcare_data_privacy", "Healthcare Data Privacy")

class HealthcareCyberSecurityAgent(HealthcareGRCAgent):
    def __init__(self):
        super().__init__("healthcare_cyber_security", "Healthcare Cyber Security")

class HealthcareIncidentResponseAgent(HealthcareGRCAgent):
    def __init__(self):
        super().__init__("healthcare_incident_response", "Healthcare Incident Response")
