#!/usr/bin/env python3
"""
BFSI Ollama Model Trainer
Specialized training system for Ollama models on BFSI policies
"""

import json
import sqlite3
import subprocess
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BFSIOllamaTrainer:
    """Ollama-specific trainer for BFSI models"""
    
    def __init__(self, db_path: str = "bfsi_policies.db"):
        self.db_path = db_path
        self.models_dir = Path("ollama_models")
        self.datasets_dir = Path("ollama_datasets")
        self.models_dir.mkdir(exist_ok=True)
        self.datasets_dir.mkdir(exist_ok=True)
        
        # Check Ollama availability
        self.ollama_available = self._check_ollama()
        
        logger.info(f"BFSI Ollama Trainer initialized (Ollama available: {self.ollama_available})")
    
    def _check_ollama(self) -> bool:
        """Check if Ollama is available"""
        try:
            result = subprocess.run(['ollama', '--version'], 
                                  capture_output=True, text=True, timeout=10)
            return result.returncode == 0
        except:
            return False
    
    def create_ollama_modelfile(self, model_name: str, base_model: str = "llama2") -> str:
        """Create Ollama Modelfile for BFSI training"""
        
        modelfile_content = f"""FROM {base_model}

# BFSI Policy Assistant Model
# Trained on banking, financial services, and insurance policies

SYSTEM \"\"\"
You are a specialized BFSI (Banking, Financial Services, and Insurance) policy assistant. 
You help with:

1. Policy Analysis: Understanding and interpreting BFSI policies
2. Compliance Guidance: Ensuring adherence to regulatory frameworks
3. Risk Assessment: Identifying potential risks in policies
4. Regulatory Support: Providing guidance on SOX, PCI DSS, Basel III, GDPR, etc.

Key capabilities:
- Analyze policy documents for compliance requirements
- Identify gaps in policy coverage
- Suggest improvements for policy effectiveness
- Provide regulatory framework guidance
- Risk assessment and mitigation strategies

Always provide accurate, professional advice based on regulatory standards.
\"\"\"

# Template for policy analysis
TEMPLATE \"\"\"{{{{ .Prompt }}}}\n\nPlease analyze this BFSI policy request and provide detailed guidance.\"\"\"

PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER top_k 40
PARAMETER repeat_penalty 1.1
PARAMETER stop "Human:"
PARAMETER stop "Assistant:"
"""
        
        modelfile_path = self.models_dir / f"{model_name}.Modelfile"
        with open(modelfile_path, 'w', encoding='utf-8') as f:
            f.write(modelfile_content)
        
        logger.info(f"Created Modelfile: {modelfile_path}")
        return str(modelfile_path)
    
    def create_training_dataset(self, policy_types: List[str] = None) -> str:
        """Create training dataset for Ollama fine-tuning"""
        logger.info("Creating Ollama training dataset...")
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Query policies
            query = "SELECT title, content, policy_type, framework FROM policies"
            if policy_types:
                placeholders = ','.join(['?' for _ in policy_types])
                query += f" WHERE policy_type IN ({placeholders})"
                cursor.execute(query, policy_types)
            else:
                cursor.execute(query)
            
            policies = cursor.fetchall()
        
        if not policies:
            raise ValueError("No policies found")
        
        # Create training data in Ollama format
        training_data = []
        
        for title, content, policy_type, framework in policies:
            # Create various training examples
            examples = self._create_ollama_examples(title, content, policy_type, framework)
            training_data.extend(examples)
        
        # Save as JSONL (one JSON object per line)
        dataset_path = self.datasets_dir / f"bfsi_ollama_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jsonl"
        
        with open(dataset_path, 'w', encoding='utf-8') as f:
            for example in training_data:
                f.write(json.dumps(example, ensure_ascii=False) + '\n')
        
        logger.info(f"Ollama dataset created: {dataset_path}")
        logger.info(f"Total examples: {len(training_data)}")
        
        return str(dataset_path)
    
    def _create_ollama_examples(self, title: str, content: str, 
                               policy_type: str, framework: str) -> List[Dict[str, str]]:
        """Create Ollama training examples"""
        examples = []
        
        # Policy analysis example
        examples.append({
            "prompt": f"Analyze this {policy_type} policy titled '{title}' under {framework} framework:",
            "response": f"""Based on my analysis of the '{title}' policy under the {framework} framework, here are the key findings:

**Policy Type**: {policy_type}
**Regulatory Framework**: {framework}

**Key Components**:
1. **Scope and Objectives**: The policy outlines clear objectives for {policy_type} management
2. **Compliance Requirements**: Specific requirements for {framework} compliance
3. **Risk Management**: Includes risk assessment and mitigation strategies
4. **Implementation**: Detailed procedures for policy implementation

**Compliance Considerations**:
- Ensure alignment with {framework} regulatory requirements
- Regular review and updates as per regulatory changes
- Staff training and awareness programs
- Monitoring and reporting mechanisms

**Recommendations**:
- Implement regular compliance audits
- Establish clear escalation procedures
- Maintain documentation for regulatory inspections
- Conduct periodic risk assessments

This policy provides a solid foundation for {policy_type} management within the {framework} framework."""
        })
        
        # Risk assessment example
        examples.append({
            "prompt": f"What are the main risks associated with this {policy_type} policy?",
            "response": f"""The main risks associated with this {policy_type} policy under {framework} include:

**Operational Risks**:
- Inadequate implementation of policy procedures
- Insufficient staff training and awareness
- Lack of regular policy updates

**Compliance Risks**:
- Non-compliance with {framework} requirements
- Regulatory penalties and sanctions
- Reputational damage from compliance failures

**Financial Risks**:
- Potential fines and penalties
- Increased operational costs for remediation
- Loss of business due to compliance issues

**Mitigation Strategies**:
1. **Regular Training**: Conduct comprehensive staff training programs
2. **Monitoring**: Implement continuous monitoring systems
3. **Reviews**: Schedule regular policy reviews and updates
4. **Documentation**: Maintain detailed compliance documentation
5. **Escalation**: Establish clear escalation procedures for violations

**Key Controls**:
- Automated compliance monitoring
- Regular internal audits
- External compliance assessments
- Management oversight and reporting"""
        })
        
        # Implementation guidance example
        examples.append({
            "prompt": f"How should this {policy_type} policy be implemented?",
            "response": f"""To effectively implement this {policy_type} policy under {framework} framework, follow these steps:

**Phase 1: Preparation**
1. **Stakeholder Engagement**: Involve all relevant departments and personnel
2. **Resource Allocation**: Assign dedicated resources and budget
3. **Timeline Development**: Create realistic implementation timeline

**Phase 2: Communication**
1. **Policy Distribution**: Ensure all staff receive policy copies
2. **Training Programs**: Conduct comprehensive training sessions
3. **Awareness Campaigns**: Launch internal awareness initiatives

**Phase 3: Implementation**
1. **Process Integration**: Integrate policy requirements into daily operations
2. **System Updates**: Update relevant systems and procedures
3. **Documentation**: Maintain implementation records

**Phase 4: Monitoring**
1. **Compliance Monitoring**: Implement ongoing compliance checks
2. **Performance Metrics**: Track key performance indicators
3. **Regular Reviews**: Schedule periodic policy reviews

**Success Factors**:
- Strong leadership commitment
- Clear communication channels
- Adequate resources and support
- Regular monitoring and feedback
- Continuous improvement mindset

**Framework Alignment**:
Ensure all implementation activities align with {framework} requirements and industry best practices."""
        })
        
        return examples
    
    def train_ollama_model(self, model_name: str, base_model: str = "llama2") -> Dict[str, Any]:
        """Train Ollama model using Modelfile"""
        if not self.ollama_available:
            logger.error("Ollama is not available")
            return {"error": "Ollama not available", "status": "failed"}
        
        logger.info(f"Training Ollama model: {model_name}")
        
        try:
            # Create Modelfile
            modelfile_path = self.create_ollama_modelfile(model_name, base_model)
            
            # Build model using Ollama
            cmd = ['ollama', 'create', model_name, '-f', modelfile_path]
            
            logger.info(f"Running command: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                logger.info(f"Model {model_name} created successfully")
                
                # Test the model
                test_result = self.test_ollama_model(model_name)
                
                return {
                    "model_name": model_name,
                    "base_model": base_model,
                    "status": "trained",
                    "modelfile_path": modelfile_path,
                    "test_result": test_result,
                    "created_at": datetime.now().isoformat()
                }
            else:
                logger.error(f"Error creating model: {result.stderr}")
                return {
                    "model_name": model_name,
                    "status": "failed",
                    "error": result.stderr,
                    "created_at": datetime.now().isoformat()
                }
        
        except subprocess.TimeoutExpired:
            logger.error("Model creation timed out")
            return {"error": "Training timed out", "status": "failed"}
        except Exception as e:
            logger.error(f"Error training Ollama model: {e}")
            return {"error": str(e), "status": "failed"}
    
    def test_ollama_model(self, model_name: str) -> Dict[str, Any]:
        """Test the trained Ollama model"""
        if not self.ollama_available:
            return {"error": "Ollama not available"}
        
        try:
            # Test prompt
            test_prompt = "What are the key components of a BFSI compliance policy?"
            
            cmd = ['ollama', 'run', model_name, test_prompt]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                return {
                    "test_prompt": test_prompt,
                    "response": result.stdout.strip(),
                    "status": "success"
                }
            else:
                return {
                    "test_prompt": test_prompt,
                    "error": result.stderr,
                    "status": "failed"
                }
        
        except subprocess.TimeoutExpired:
            return {"error": "Test timed out", "status": "failed"}
        except Exception as e:
            return {"error": str(e), "status": "failed"}
    
    def list_ollama_models(self) -> List[Dict[str, Any]]:
        """List available Ollama models"""
        if not self.ollama_available:
            return []
        
        try:
            result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
            if result.returncode != 0:
                return []
            
            models = []
            lines = result.stdout.strip().split('\n')[1:]  # Skip header
            
            for line in lines:
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 3:
                        models.append({
                            "name": parts[0],
                            "id": parts[1],
                            "size": parts[2],
                            "modified": ' '.join(parts[3:]) if len(parts) > 3 else "unknown"
                        })
            
            return models
        
        except Exception as e:
            logger.error(f"Error listing Ollama models: {e}")
            return []
    
    def get_training_stats(self) -> Dict[str, Any]:
        """Get training statistics"""
        models = self.list_ollama_models()
        
        # Filter BFSI models
        bfsi_models = [m for m in models if 'bfsi' in m['name'].lower()]
        
        return {
            "total_ollama_models": len(models),
            "bfsi_models": len(bfsi_models),
            "ollama_available": self.ollama_available,
            "models": bfsi_models
        }

def main():
    """Main function"""
    print("🚀 BFSI Ollama Trainer")
    print("=" * 40)
    
    trainer = BFSIOllamaTrainer()
    
    if not trainer.ollama_available:
        print("❌ Ollama is not available. Please install Ollama first.")
        print("   Visit: https://ollama.ai/")
        return
    
    print("✅ Ollama is available")
    
    try:
        # Create training dataset
        print("\n📊 Creating training dataset...")
        dataset_path = trainer.create_training_dataset(['compliance', 'risk', 'security'])
        print(f"✅ Dataset created: {dataset_path}")
        
        # Train model
        print("\n🤖 Training Ollama model...")
        result = trainer.train_ollama_model("bfsi-policy-assistant", "llama2")
        
        if result.get('status') == 'trained':
            print(f"✅ Model trained successfully!")
            print(f"   Model: {result['model_name']}")
            print(f"   Base: {result['base_model']}")
            
            if 'test_result' in result:
                test = result['test_result']
                if test.get('status') == 'success':
                    print(f"   Test response: {test['response'][:100]}...")
        
        # Show stats
        print("\n📈 Training Statistics:")
        stats = trainer.get_training_stats()
        print(f"Total Ollama models: {stats['total_ollama_models']}")
        print(f"BFSI models: {stats['bfsi_models']}")
        
        if stats['models']:
            print("\nBFSI Models:")
            for model in stats['models']:
                print(f"  - {model['name']} ({model['size']})")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
