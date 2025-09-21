#!/usr/bin/env python3
"""
BFSI Model Deployment System
Deploy trained models to the BFSI system for production use
"""

import json
import sqlite3
import subprocess
import logging
import re
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import asyncio

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BFSIModelDeployment:
    """Deploy trained models to BFSI system"""
    
    def __init__(self, db_path: str = "bfsi_policies.db"):
        self.db_path = db_path
        self.deployment_dir = Path("deployed_models")
        self.config_dir = Path("deployment_configs")
        self.deployment_dir.mkdir(exist_ok=True)
        self.config_dir.mkdir(exist_ok=True)
        
        # Define allowed base directories for model paths (security measure)
        self.allowed_base_dirs = [
            Path.cwd() / "trained_models",
            Path.cwd() / "models",
            Path.cwd() / "deployed_models",
            Path.cwd() / "backend" / "models"
        ]
        
        # Initialize deployment database
        self._init_deployment_db()
        
        logger.info("BFSI Model Deployment System initialized")
    
    def _validate_deployment_path(self, deployment_path: str) -> bool:
        """
        Validate deployment path for security.
        Ensures the path is within allowed directories and is safe for import.
        
        Args:
            deployment_path: Path to validate
            
        Returns:
            bool: True if path is valid and safe, False otherwise
            
        Raises:
            ValueError: If path is invalid or potentially malicious
        """
        try:
            # Convert to Path object and resolve to absolute path
            path = Path(deployment_path).resolve()
            
            # Check if path exists
            if not path.exists():
                raise ValueError(f"Deployment path does not exist: {deployment_path}")
            
            # Check if it's a file (not directory)
            if not path.is_file():
                raise ValueError(f"Deployment path must be a file, not directory: {deployment_path}")
            
            # Check if file has .py extension
            if path.suffix != '.py':
                raise ValueError(f"Deployment path must be a Python file (.py): {deployment_path}")
            
            # Check if path is within allowed base directories
            is_allowed = False
            for allowed_dir in self.allowed_base_dirs:
                try:
                    # Resolve both paths to absolute
                    allowed_abs = allowed_dir.resolve()
                    if path.is_relative_to(allowed_abs):
                        is_allowed = True
                        break
                except (OSError, ValueError):
                    # Skip invalid allowed directories
                    continue
            
            if not is_allowed:
                raise ValueError(f"Deployment path is not within allowed directories: {deployment_path}")
            
            # Additional security checks
            # Check for path traversal attempts
            if '..' in str(path) or path.is_absolute() and not any(str(path).startswith(str(allowed_dir.resolve())) for allowed_dir in self.allowed_base_dirs):
                raise ValueError(f"Deployment path contains suspicious patterns: {deployment_path}")
            
            # Check file size (prevent loading extremely large files)
            file_size = path.stat().st_size
            max_size = 10 * 1024 * 1024  # 10MB limit
            if file_size > max_size:
                raise ValueError(f"Deployment file too large ({file_size} bytes): {deployment_path}")
            
            logger.info(f"Deployment path validated successfully: {deployment_path}")
            return True
            
        except Exception as e:
            logger.error(f"Deployment path validation failed: {e}")
            raise ValueError(f"Invalid deployment path: {e}")
    
    def _init_deployment_db(self):
        """Initialize deployment database with proper error handling and context managers"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                try:
                    # Create deployment history table
                    cursor.execute('''
                        CREATE TABLE IF NOT EXISTS model_deployments (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            model_name TEXT NOT NULL,
                            model_type TEXT NOT NULL,
                            deployment_status TEXT NOT NULL,
                            deployment_path TEXT NOT NULL,
                            config_path TEXT,
                            validation_score REAL,
                            deployment_timestamp TEXT NOT NULL,
                            last_accessed TEXT,
                            access_count INTEGER DEFAULT 0,
                            is_active BOOLEAN DEFAULT 1
                        )
                    ''')
                    
                    conn.commit()
                    logger.info("Deployment database initialized successfully")
                finally:
                    cursor.close()
                    
        except sqlite3.Error as e:
            logger.error(f"Database error during initialization: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during database initialization: {e}")
            raise
    
    def _validate_model_path(self, model_path: str) -> tuple[bool, str]:
        """
        Validate model path to prevent directory traversal attacks.
        
        Args:
            model_path: The path to validate
            
        Returns:
            tuple: (is_valid, error_message)
        """
        try:
            # Additional security checks first - check for suspicious patterns
            suspicious_patterns = [
                '../',
                '..\\',
                '~/',
                '~\\',
                '//',
                '\\\\'
            ]
            
            model_path_normalized = model_path.replace('\\', '/')
            for pattern in suspicious_patterns:
                if pattern in model_path_normalized:
                    return False, f"Model path contains suspicious pattern: {pattern}"
            
            # Convert to Path object and resolve any relative paths
            try:
                path = Path(model_path).resolve()
            except (OSError, ValueError) as e:
                # Handle cases where path resolution fails (e.g., network paths)
                return False, f"Cannot resolve path: {model_path} - {str(e)}"
            
            # Check if path exists
            if not path.exists():
                return False, f"Model path does not exist: {model_path}"
            
            # Check if path is a file (models should be files or directories)
            if not (path.is_file() or path.is_dir()):
                return False, f"Model path is not a valid file or directory: {model_path}"
            
            # Security check: Ensure the resolved path is within allowed directories
            is_within_allowed = False
            for allowed_dir in self.allowed_base_dirs:
                try:
                    # Resolve the allowed directory to absolute path
                    allowed_dir_resolved = allowed_dir.resolve()
                    
                    # Check if the model path is within the allowed directory
                    if path.is_relative_to(allowed_dir_resolved):
                        is_within_allowed = True
                        break
                except Exception:
                    # If we can't resolve the allowed directory, skip it
                    continue
            
            if not is_within_allowed:
                allowed_dirs_str = ", ".join([str(d) for d in self.allowed_base_dirs])
                return False, f"Model path '{model_path}' is outside allowed directories: {allowed_dirs_str}"
            
            logger.info(f"Model path validation passed: {model_path}")
            return True, ""
            
        except Exception as e:
            logger.error(f"Error validating model path '{model_path}': {e}")
            return False, f"Error validating model path: {str(e)}"
    
    def deploy_ollama_model(self, model_name: str, validation_score: float = None) -> Dict[str, Any]:
        """Deploy Ollama model to production"""
        logger.info(f"Deploying Ollama model: {model_name}")
        
        # Validate model_name parameter to prevent command injection and path traversal
        if not model_name or not isinstance(model_name, str):
            return {"error": "Model name cannot be empty or non-string", "status": "failed"}
        
        # Only allow alphanumeric characters, hyphens, underscores, and periods
        if not re.match(r'^[a-zA-Z0-9._-]+$', model_name):
            return {"error": "Model name contains invalid characters. Only alphanumeric characters, hyphens, underscores, and periods are allowed", "status": "failed"}
        
        # Additional length check to prevent excessively long names
        if len(model_name) > 100:
            return {"error": "Model name is too long (maximum 100 characters)", "status": "failed"}
        
        try:
            # Check if model exists
            result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
            if result.returncode != 0:
                return {"error": f"Failed to list Ollama models: {result.stderr}", "status": "failed"}
            
            # Parse ollama list output to get discrete model names
            # ollama list output format: "NAME    ID    SIZE    MODIFIED"
            # We need to extract just the model names from the first column
            available_models = []
            for line in result.stdout.strip().split('\n')[1:]:  # Skip header line
                if line.strip():  # Skip empty lines
                    # Split by whitespace and take the first column (model name)
                    model_name_from_list = line.split()[0] if line.split() else ""
                    if model_name_from_list:
                        available_models.append(model_name_from_list)
            
            # Check for exact match instead of substring match
            if model_name not in available_models:
                return {"error": f"Model {model_name} not found. Available models: {', '.join(available_models)}", "status": "failed"}
            
            # Create deployment configuration
            deployment_config = {
                "model_name": model_name,
                "model_type": "ollama",
                "deployment_method": "ollama_api",
                "endpoint": f"http://localhost:11434/api/generate",
                "model_parameters": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "max_tokens": 512
                },
                "bfsi_config": {
                    "supported_tasks": [
                        "policy_analysis",
                        "risk_assessment", 
                        "compliance_guidance",
                        "implementation_advice",
                        "regulatory_framework_analysis"
                    ],
                    "specializations": ["BFSI", "compliance", "risk_management"],
                    "max_context_length": 4096
                },
                "deployment_timestamp": datetime.now().isoformat(),
                "validation_score": validation_score
            }
            
            # Save deployment config
            config_path = self.config_dir / f"{model_name}_deployment_config.json"
            with open(config_path, 'w') as f:
                json.dump(deployment_config, f, indent=2)
            
            # Create deployment wrapper
            wrapper_path = self.deployment_dir / f"{model_name}_deployment.py"
            self._create_ollama_wrapper(model_name, wrapper_path, deployment_config)
            
            # Record deployment
            deployment_info = {
                "model_name": model_name,
                "model_type": "ollama",
                "status": "deployed",
                "deployment_path": str(wrapper_path),
                "config_path": str(config_path),
                "validation_score": validation_score,
                "timestamp": datetime.now().isoformat()
            }
            
            self._record_deployment(deployment_info)
            
            logger.info(f"Ollama model {model_name} deployed successfully")
            return deployment_info
            
        except Exception as e:
            logger.error(f"Error deploying Ollama model: {e}")
            return {"error": str(e), "status": "failed"}
    
    def deploy_huggingface_model(self, model_path: str, model_name: str = None, 
                                validation_score: float = None) -> Dict[str, Any]:
        """Deploy Hugging Face model to production"""
        if not model_name:
            model_name = Path(model_path).name
        
        logger.info(f"Deploying Hugging Face model: {model_name}")
        
        try:
            # Validate model path to prevent directory traversal attacks
            is_valid, error_msg = self._validate_model_path(model_path)
            if not is_valid:
                logger.error(f"Model path validation failed: {error_msg}")
                return {"error": f"Invalid model path: {error_msg}", "status": "failed"}
            
            # Check if model path exists (redundant but kept for clarity)
            if not Path(model_path).exists():
                return {"error": f"Model path {model_path} not found", "status": "failed"}
            
            # Create deployment configuration
            deployment_config = {
                "model_name": model_name,
                "model_type": "huggingface",
                "model_path": str(model_path),
                "deployment_method": "local_api",
                "endpoint": f"http://localhost:8000/api/generate",
                "model_parameters": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "max_length": 512,
                    "do_sample": True
                },
                "bfsi_config": {
                    "supported_tasks": [
                        "policy_analysis",
                        "risk_assessment",
                        "compliance_guidance", 
                        "implementation_advice",
                        "regulatory_framework_analysis"
                    ],
                    "specializations": ["BFSI", "compliance", "risk_management"],
                    "max_context_length": 1024
                },
                "deployment_timestamp": datetime.now().isoformat(),
                "validation_score": validation_score
            }
            
            # Save deployment config
            config_path = self.config_dir / f"{model_name}_deployment_config.json"
            with open(config_path, 'w') as f:
                json.dump(deployment_config, f, indent=2)
            
            # Create deployment wrapper
            wrapper_path = self.deployment_dir / f"{model_name}_deployment.py"
            self._create_huggingface_wrapper(model_name, wrapper_path, deployment_config)
            
            # Record deployment
            deployment_info = {
                "model_name": model_name,
                "model_type": "huggingface",
                "status": "deployed",
                "deployment_path": str(wrapper_path),
                "config_path": str(config_path),
                "validation_score": validation_score,
                "timestamp": datetime.now().isoformat()
            }
            
            self._record_deployment(deployment_info)
            
            logger.info(f"Hugging Face model {model_name} deployed successfully")
            return deployment_info
            
        except Exception as e:
            logger.error(f"Error deploying Hugging Face model: {e}")
            return {"error": str(e), "status": "failed"}
    
    def _create_ollama_wrapper(self, model_name: str, wrapper_path: Path, config: Dict[str, Any]):
        """Create Ollama deployment wrapper"""
        wrapper_code = f'''#!/usr/bin/env python3
"""
Ollama Model Deployment Wrapper for {model_name}
Production-ready wrapper for BFSI model deployment
"""

import requests
import json
import logging
from typing import Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class BFSIModelAPI:
    """BFSI Model API wrapper for {model_name}"""
    
    def __init__(self):
        self.model_name = "{model_name}"
        self.endpoint = "{config['endpoint']}"
        self.config = {json.dumps(config, indent=8)}
        
    def analyze_policy(self, policy_text: str, policy_type: str = "compliance") -> Dict[str, Any]:
        """Analyze BFSI policy"""
        prompt = f"""Analyze this {{{policy_type}}} policy and provide detailed insights:

Policy Text: {{{policy_text}}}

Please provide:
1. Key compliance requirements
2. Risk assessment
3. Implementation recommendations
4. Regulatory framework alignment
"""
        
        return self._query_model(prompt)
    
    def assess_risk(self, risk_description: str) -> Dict[str, Any]:
        """Assess BFSI risks"""
        prompt = f"""Assess the following BFSI risk scenario:

Risk Description: {{{risk_description}}}

Please provide:
1. Risk level assessment
2. Potential impact analysis
3. Mitigation strategies
4. Monitoring recommendations
"""
        
        return self._query_model(prompt)
    
    def compliance_guidance(self, compliance_question: str) -> Dict[str, Any]:
        """Provide compliance guidance"""
        prompt = f"""Provide compliance guidance for this BFSI question:

Question: {{{compliance_question}}}

Please provide:
1. Regulatory requirements
2. Compliance procedures
3. Best practices
4. Implementation steps
"""
        
        return self._query_model(prompt)
    
    def _query_model(self, prompt: str) -> Dict[str, Any]:
        """Query the deployed model"""
        try:
            payload = {{
                "model": self.model_name,
                "prompt": prompt,
                "stream": False,
                "options": self.config["model_parameters"]
            }}
            
            response = requests.post(self.endpoint, json=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            
            return {{
                "success": True,
                "response": result.get("response", ""),
                "model": self.model_name,
                "timestamp": datetime.now().isoformat()
            }}
            
        except Exception as e:
            logger.error(f"Error querying model: {{{e}}}")
            return {{
                "success": False,
                "error": str(e),
                "model": self.model_name,
                "timestamp": datetime.now().isoformat()
            }}

# Global instance
bfsi_model = BFSIModelAPI()

# Convenience functions
def analyze_policy(policy_text: str, policy_type: str = "compliance") -> Dict[str, Any]:
    return bfsi_model.analyze_policy(policy_text, policy_type)

def assess_risk(risk_description: str) -> Dict[str, Any]:
    return bfsi_model.assess_risk(risk_description)

def get_compliance_guidance(question: str) -> Dict[str, Any]:
    return bfsi_model.compliance_guidance(question)

if __name__ == "__main__":
    # Test the deployed model
    test_policy = "This policy outlines data protection requirements for financial institutions under GDPR framework."
    
    print("Testing deployed BFSI model...")
    result = analyze_policy(test_policy)
    
    if result["success"]:
        print("✅ Model is working correctly")
        print(f"Response: {{{result['response'][:200]}}}...")
    else:
        print(f"❌ Model error: {{{result['error']}}}")
'''
        
        with open(wrapper_path, 'w', encoding='utf-8') as f:
            f.write(wrapper_code)
    
    def _create_huggingface_wrapper(self, model_name: str, wrapper_path: Path, config: Dict[str, Any]):
        """Create Hugging Face deployment wrapper"""
        wrapper_code = f'''#!/usr/bin/env python3
"""
Hugging Face Model Deployment Wrapper for {model_name}
Production-ready wrapper for BFSI model deployment
"""

import json
import logging
from typing import Dict, Any, Optional
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BFSIModelAPI:
    """BFSI Model API wrapper for {model_name}"""
    
    def __init__(self):
        self.model_name = "{model_name}"
        self.model_path = "{config['model_path']}"
        self.config = {json.dumps(config, indent=8)}
        
        # Load model (with error handling)
        self.model = None
        self.tokenizer = None
        self._load_model()
        
    def _load_model(self):
        """Load the Hugging Face model"""
        try:
            from transformers import pipeline, AutoTokenizer
            
            # Try to load custom model first
            try:
                self.model = pipeline("text-generation", model=self.model_path)
                logger.info(f"Loaded custom model from {{{self.model_path}}}")
            except OSError as e:
                logger.error(f"Model file not found or corrupted at {self.model_path}: {e}")
                raise
            except ValueError as e:
                logger.error(f"Invalid model configuration for {self.model_path}: {e}")
                raise
            except RuntimeError as e:
                logger.error(f"Runtime error loading model {self.model_path}: {e}")
                raise
            except Exception as e:
                logger.error(f"Unexpected error loading model {self.model_path}: {e}")
                raise
                
        except ImportError:
            logger.error("transformers library not available")
        except Exception as e:
            logger.error(f"Error loading model: {{{e}}}")
    
    def analyze_policy(self, policy_text: str, policy_type: str = "compliance") -> Dict[str, Any]:
        """Analyze BFSI policy"""
        if not self.model:
            return {{"success": False, "error": "Model not loaded"}}
        
        prompt = f"Analyze this {{{policy_type}}} policy: {{{policy_text[:200]}}}... Key requirements:"
        
        try:
            result = self.model(prompt, max_length=200, num_return_sequences=1, 
                              temperature=0.7, do_sample=True)
            
            response = result[0]["generated_text"][len(prompt):].strip()
            
            return {{
                "success": True,
                "response": response,
                "model": self.model_name,
                "timestamp": datetime.now().isoformat()
            }}
            
        except Exception as e:
            logger.error(f"Error analyzing policy: {{{e}}}")
            return {{
                "success": False,
                "error": str(e),
                "model": self.model_name,
                "timestamp": datetime.now().isoformat()
            }}
    
    def assess_risk(self, risk_description: str) -> Dict[str, Any]:
        """Assess BFSI risks"""
        if not self.model:
            return {{"success": False, "error": "Model not loaded"}}
        
        prompt = f"Assess this BFSI risk: {{{risk_description[:150]}}}... Risk level:"
        
        try:
            result = self.model(prompt, max_length=150, num_return_sequences=1,
                              temperature=0.7, do_sample=True)
            
            response = result[0]["generated_text"][len(prompt):].strip()
            
            return {{
                "success": True,
                "response": response,
                "model": self.model_name,
                "timestamp": datetime.now().isoformat()
            }}
            
        except Exception as e:
            logger.error(f"Error assessing risk: {{{e}}}")
            return {{
                "success": False,
                "error": str(e),
                "model": self.model_name,
                "timestamp": datetime.now().isoformat()
            }}
    
    def compliance_guidance(self, compliance_question: str) -> Dict[str, Any]:
        """Provide compliance guidance"""
        if not self.model:
            return {{"success": False, "error": "Model not loaded"}}
        
        prompt = f"Compliance guidance for: {{{compliance_question[:150]}}}... Answer:"
        
        try:
            result = self.model(prompt, max_length=150, num_return_sequences=1,
                              temperature=0.7, do_sample=True)
            
            response = result[0]["generated_text"][len(prompt):].strip()
            
            return {{
                "success": True,
                "response": response,
                "model": self.model_name,
                "timestamp": datetime.now().isoformat()
            }}
            
        except Exception as e:
            logger.error(f"Error providing guidance: {{{e}}}")
            return {{
                "success": False,
                "error": str(e),
                "model": self.model_name,
                "timestamp": datetime.now().isoformat()
            }}

# Global instance
bfsi_model = BFSIModelAPI()

# Convenience functions
def analyze_policy(policy_text: str, policy_type: str = "compliance") -> Dict[str, Any]:
    return bfsi_model.analyze_policy(policy_text, policy_type)

def assess_risk(risk_description: str) -> Dict[str, Any]:
    return bfsi_model.assess_risk(risk_description)

def get_compliance_guidance(question: str) -> Dict[str, Any]:
    return bfsi_model.compliance_guidance(question)

if __name__ == "__main__":
    # Test the deployed model
    test_policy = "This policy outlines data protection requirements for financial institutions under GDPR framework."
    
    print("Testing deployed BFSI model...")
    result = analyze_policy(test_policy)
    
    if result["success"]:
        print("✅ Model is working correctly")
        print(f"Response: {{{result['response'][:200]}}}...")
    else:
        print(f"❌ Model error: {{{result['error']}}}")
'''
        
        with open(wrapper_path, 'w', encoding='utf-8') as f:
            f.write(wrapper_code)
    
    def _record_deployment(self, deployment_info: Dict[str, Any]):
        """Record deployment in database with proper error handling and context managers"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                try:
                    cursor.execute('''
                        INSERT INTO model_deployments 
                        (model_name, model_type, deployment_status, deployment_path, 
                         config_path, validation_score, deployment_timestamp)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        deployment_info['model_name'],
                        deployment_info['model_type'],
                        deployment_info['status'],
                        deployment_info['deployment_path'],
                        deployment_info['config_path'],
                        deployment_info.get('validation_score'),
                        deployment_info['timestamp']
                    ))
                    
                    conn.commit()
                    logger.info(f"Deployment recorded for model: {deployment_info['model_name']}")
                finally:
                    cursor.close()
                    
        except sqlite3.Error as e:
            logger.error(f"Database error recording deployment: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error recording deployment: {e}")
            raise
    
    def list_deployments(self) -> List[Dict[str, Any]]:
        """List all model deployments with proper error handling and context managers"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                try:
                    cursor.execute('''
                        SELECT model_name, model_type, deployment_status, deployment_path,
                               config_path, validation_score, deployment_timestamp, 
                               last_accessed, access_count, is_active
                        FROM model_deployments
                        ORDER BY deployment_timestamp DESC
                    ''')
                    
                    deployments = []
                    for row in cursor.fetchall():
                        deployments.append({
                            'model_name': row[0],
                            'model_type': row[1],
                            'status': row[2],
                            'deployment_path': row[3],
                            'config_path': row[4],
                            'validation_score': row[5],
                            'deployment_timestamp': row[6],
                            'last_accessed': row[7],
                            'access_count': row[8],
                            'is_active': bool(row[9])
                        })
                    
                    logger.info(f"Retrieved {len(deployments)} deployments from database")
                    return deployments
                finally:
                    cursor.close()
                    
        except sqlite3.Error as e:
            logger.error(f"Database error listing deployments: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error listing deployments: {e}")
            raise
    
    def get_deployment_stats(self) -> Dict[str, Any]:
        """Get deployment statistics"""
        deployments = self.list_deployments()
        
        if not deployments:
            return {"total_deployments": 0}
        
        active_deployments = [d for d in deployments if d['is_active']]
        model_types = list(set(d['model_type'] for d in deployments))
        
        avg_score = None
        scored_deployments = [d for d in deployments if d['validation_score'] is not None]
        if scored_deployments:
            avg_score = sum(d['validation_score'] for d in scored_deployments) / len(scored_deployments)
        
        stats = {
            "total_deployments": len(deployments),
            "active_deployments": len(active_deployments),
            "model_types": model_types,
            "average_validation_score": avg_score
        }
        
        if deployments:
            stats["latest_deployment"] = deployments[0]
        
        return stats
    
    def test_deployment(self, model_name: str) -> Dict[str, Any]:
        """Test a deployed model"""
        deployments = self.list_deployments()
        deployment = next((d for d in deployments if d['model_name'] == model_name), None)
        
        if not deployment:
            return {"error": f"Model {model_name} not found in deployments"}
        
        try:
            # SECURITY: Validate deployment path before importing
            deployment_path = deployment['deployment_path']
            self._validate_deployment_path(deployment_path)
            
            # Import and test the deployment wrapper
            import importlib.util
            spec = importlib.util.spec_from_file_location("deployment", deployment_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Test the model
            test_policy = "This policy outlines data protection requirements for financial institutions under GDPR framework."
            result = module.analyze_policy(test_policy)
            
            # Update access count
            self._update_access_stats(model_name)
            
            return {
                "model_name": model_name,
                "test_result": result,
                "deployment_path": deployment['deployment_path'],
                "test_timestamp": datetime.now().isoformat()
            }
            
        except ValueError as ve:
            # Security validation error
            logger.error(f"Security validation failed for deployment {model_name}: {ve}")
            return {"error": f"Security validation failed: {ve}", "model_name": model_name}
        except Exception as e:
            logger.error(f"Error testing deployment {model_name}: {e}")
            return {"error": str(e), "model_name": model_name}
    
    def _update_access_stats(self, model_name: str):
        """Update access statistics for a model with proper error handling and context managers"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                try:
                    cursor.execute('''
                        UPDATE model_deployments 
                        SET access_count = access_count + 1, last_accessed = ?
                        WHERE model_name = ?
                    ''', (datetime.now().isoformat(), model_name))
                    
                    conn.commit()
                    logger.info(f"Updated access stats for model: {model_name}")
                finally:
                    cursor.close()
                    
        except sqlite3.Error as e:
            logger.error(f"Database error updating access stats: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error updating access stats: {e}")
            raise

def test_path_validation():
    """Test the path validation security feature"""
    print("🔒 Testing Path Validation Security...")
    
    deployer = BFSIModelDeployment()
    
    # Test cases for path validation
    test_cases = [
        # Invalid paths (should fail) - these are the main security tests
        ("../../../etc/passwd", False, "Directory traversal attack"),
        ("..\\..\\windows\\system32", False, "Windows directory traversal"),
        ("~/secret_files", False, "Home directory access"),
        ("/etc/passwd", False, "Absolute path outside allowed directories"),
        ("//network/path", False, "Network path with double slashes"),
        ("\\\\server\\share", False, "UNC network path"),
        ("C:\\Windows\\System32", False, "Windows system directory"),
        ("/usr/bin", False, "Unix system directory"),
        ("../config/secrets", False, "Parent directory traversal"),
        ("models/../../../etc/passwd", False, "Mixed traversal attempt"),
    ]
    
    passed_tests = 0
    total_tests = len(test_cases)
    
    for test_path, should_pass, description in test_cases:
        is_valid, error_msg = deployer._validate_model_path(test_path)
        
        if not should_pass and not is_valid:
            print(f"✅ PASS: {description} - '{test_path}' (correctly blocked)")
            passed_tests += 1
        else:
            print(f"❌ FAIL: {description} - '{test_path}' (Expected: blocked, Got: {'allowed' if is_valid else 'blocked'})")
            if error_msg:
                print(f"   Error: {error_msg}")
    
    print(f"\n📊 Security Test Results: {passed_tests}/{total_tests} tests passed")
    if passed_tests == total_tests:
        print("🔒 All security tests PASSED - Path traversal protection is working!")
    else:
        print("⚠️ Some security tests FAILED - Review path validation logic")

def main():
    """Main function"""
    print("🚀 BFSI Model Deployment System")
    print("=" * 50)
    
    # Run security tests first
    test_path_validation()
    print("\n" + "="*50 + "\n")
    
    deployer = BFSIModelDeployment()
    
    try:
        # Deploy Ollama model
        print("\n🤖 Deploying Ollama model...")
        ollama_deployment = deployer.deploy_ollama_model("bfsi-policy-assistant", validation_score=7.06)
        
        if "error" not in ollama_deployment:
            print(f"✅ Ollama model deployed: {ollama_deployment['model_name']}")
        else:
            print(f"⚠️ Ollama deployment: {ollama_deployment['error']}")
        
        # Deploy Hugging Face models
        print("\n🤖 Deploying Hugging Face models...")
        hf_models = [
            ("trained_models/bfsi-transformers-model", "bfsi-transformers-deployed"),
            ("trained_models/bfsi-quick-transformers", "bfsi-quick-deployed")
        ]
        
        for model_path, model_name in hf_models:
            if Path(model_path).exists():
                hf_deployment = deployer.deploy_huggingface_model(model_path, model_name)
                if "error" not in hf_deployment:
                    print(f"✅ Hugging Face model deployed: {hf_deployment['model_name']}")
                else:
                    print(f"⚠️ {model_name} deployment: {hf_deployment['error']}")
        
        # Show deployment statistics
        print("\n📈 Deployment Statistics:")
        stats = deployer.get_deployment_stats()
        print(f"Total deployments: {stats['total_deployments']}")
        print(f"Active deployments: {stats['active_deployments']}")
        print(f"Model types: {', '.join(stats['model_types'])}")
        
        if stats['average_validation_score']:
            print(f"Average validation score: {stats['average_validation_score']:.2f}/10")
        
        # Test a deployment
        print("\n🧪 Testing deployed model...")
        if stats['total_deployments'] > 0:
            latest_model = stats['latest_deployment']['model_name']
            test_result = deployer.test_deployment(latest_model)
            
            if "error" not in test_result:
                print(f"✅ Model test successful: {latest_model}")
                if test_result['test_result']['success']:
                    print(f"Response: {test_result['test_result']['response'][:100]}...")
            else:
                print(f"⚠️ Model test failed: {test_result['error']}")
        
        # List all deployments
        print("\n📋 Deployed Models:")
        deployments = deployer.list_deployments()
        for deployment in deployments[:5]:  # Show first 5
            status_icon = "✅" if deployment['is_active'] else "❌"
            score_info = f" (Score: {deployment['validation_score']:.1f})" if deployment['validation_score'] else ""
            print(f"  {status_icon} {deployment['model_name']} ({deployment['model_type']}){score_info}")
        
        print("\n✅ Model deployment completed!")
        print("\n🎯 Next Steps:")
        print("   1. Models are ready for production use")
        print("   2. Integrate with BFSI agent system")
        print("   3. Set up monitoring and logging")
        print("   4. Configure API endpoints")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
