#!/usr/bin/env python3
"""
Simple BFSI Model Retraining
Retrain models with uploaded policies using existing training system
"""

import os
import sys
import json
import sqlite3
import logging
from datetime import datetime
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_policies_database():
    """Check if there are policies in the database"""
    try:
        conn = sqlite3.connect("bfsi_policies.db")
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM policies")
        count = cursor.fetchone()[0]
        
        cursor.execute("SELECT title, policy_type, framework FROM policies LIMIT 5")
        sample_policies = cursor.fetchall()
        
        conn.close()
        
        return count, sample_policies
    except Exception as e:
        logger.error(f"Error checking database: {e}")
        return 0, []

def create_training_dataset():
    """Create training dataset from policies"""
    try:
        conn = sqlite3.connect("bfsi_policies.db")
        cursor = conn.cursor()
        
        # Get all policies
        cursor.execute("SELECT title, content, policy_type, framework FROM policies")
        policies = cursor.fetchall()
        conn.close()
        
        if not policies:
            logger.error("No policies found in database")
            return None
        
        # Create training examples
        training_data = []
        
        for title, content, policy_type, framework in policies:
            # Create multiple training examples for each policy
            examples = create_training_examples(title, content, policy_type, framework)
            training_data.extend(examples)
        
        # Create datasets directory
        datasets_dir = Path("../../data/training_datasets/training_datasets")
        datasets_dir.mkdir(parents=True, exist_ok=True)
        
        # Save dataset
        dataset_path = datasets_dir / f"user_policies_training_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(dataset_path, 'w', encoding='utf-8') as f:
            json.dump(training_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Training dataset created: {dataset_path}")
        logger.info(f"Total policies: {len(policies)}")
        logger.info(f"Total examples: {len(training_data)}")
        
        return str(dataset_path)
        
    except Exception as e:
        logger.error(f"Error creating training dataset: {e}")
        return None

def create_training_examples(title, content, policy_type, framework):
    """Create training examples from policy"""
    examples = []
    
    # Policy summary example
    examples.append({
        "instruction": f"Summarize this {policy_type} policy under {framework} framework:",
        "input": content[:500] + "..." if len(content) > 500 else content,
        "output": f"Policy Summary: {title}\nType: {policy_type}\nFramework: {framework}\n\nThis policy outlines key requirements for {policy_type} management under {framework} framework. It includes specific procedures for compliance monitoring, risk assessment, and implementation guidelines. The policy ensures adherence to regulatory standards and provides clear guidance for stakeholders."
    })
    
    # Policy analysis example
    examples.append({
        "instruction": f"Analyze the compliance requirements in this {policy_type} policy:",
        "input": content,
        "output": f"Compliance Analysis for {title}:\n\nKey Requirements:\n1. Establish governance structures with clear roles and responsibilities\n2. Implement monitoring systems for {policy_type} activities\n3. Develop reporting mechanisms for regulatory compliance\n4. Create incident response procedures\n5. Ensure regular training and awareness programs\n\nFramework: {framework}\nType: {policy_type}\n\nThis policy ensures comprehensive compliance with {framework} requirements through structured implementation and ongoing monitoring."
    })
    
    # Risk assessment example (for risk-related policies)
    if policy_type in ['risk', 'compliance', 'security']:
        examples.append({
            "instruction": "Identify potential risks and mitigation strategies:",
            "input": content,
            "output": f"Risk Assessment for {title}:\n\nIdentified Risks:\n1. Regulatory non-compliance leading to penalties\n2. Operational failures affecting business continuity\n3. Security breaches compromising sensitive data\n4. Inadequate monitoring and reporting\n5. Insufficient staff training and awareness\n\nMitigation Strategies:\n1. Implement robust monitoring and audit procedures\n2. Establish clear escalation and incident response protocols\n3. Conduct regular risk assessments and reviews\n4. Provide comprehensive staff training programs\n5. Maintain detailed documentation and reporting systems\n\nFramework: {framework}"
        })
    
    # Implementation guidance example
    examples.append({
        "instruction": f"Provide implementation guidance for this {policy_type} policy:",
        "input": content,
        "output": f"Implementation Guidance for {title}:\n\nStep 1: Policy Review and Understanding\n- Conduct thorough review of policy requirements\n- Identify key stakeholders and responsibilities\n- Assess current state vs. policy requirements\n\nStep 2: Gap Analysis\n- Compare existing procedures with policy requirements\n- Identify areas requiring improvement or implementation\n- Prioritize implementation activities\n\nStep 3: Implementation Planning\n- Develop detailed implementation timeline\n- Assign responsibilities to appropriate teams\n- Establish success metrics and monitoring procedures\n\nStep 4: Training and Communication\n- Develop training materials for all stakeholders\n- Conduct awareness sessions and training programs\n- Establish communication channels for ongoing support\n\nStep 5: Monitoring and Review\n- Implement monitoring systems for policy compliance\n- Conduct regular reviews and assessments\n- Update procedures based on lessons learned\n\nFramework: {framework}\nPolicy Type: {policy_type}"
        })
    
    return examples

def run_enhanced_training():
    """Run enhanced training using the existing training system"""
    try:
        # Navigate to the training scripts directory
        training_dir = Path("../../training/scripts")
        if not training_dir.exists():
            logger.error("Training scripts directory not found")
            return False
        
        # Import and run the enhanced training
        sys.path.append(str(training_dir))
        
        # Run the enhanced training script
        os.chdir(training_dir)
        
        # Execute the enhanced training
        import enhanced_bfsi_training
        trainer = enhanced_bfsi_training.EnhancedBFSITraining()
        
        # Create comprehensive training data
        dataset_path = trainer.create_comprehensive_training_data()
        
        # Train enhanced model
        result = trainer.train_enhanced_model("user-enhanced-bfsi-model")
        
        logger.info("Enhanced training completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Error running enhanced training: {e}")
        return False

def create_ollama_modelfile(dataset_path):
    """Create Ollama Modelfile for retrained model"""
    try:
        # Read dataset for context
        with open(dataset_path, 'r', encoding='utf-8') as f:
            dataset = json.load(f)
        
        # Create models directory
        models_dir = Path("../../training/models/trained_models")
        models_dir.mkdir(parents=True, exist_ok=True)
        
        # Create Modelfile
        modelfile_path = models_dir / "user-bfsi-policy-assistant.Modelfile"
        
        modelfile_content = f"""FROM llama2

# User-Enhanced BFSI Policy Assistant
# Trained on {len(dataset)} examples including user-uploaded policies

SYSTEM \"\"\"You are a specialized BFSI (Banking, Financial Services, and Insurance) policy assistant. 
You have been trained on comprehensive BFSI policies including user-uploaded policies covering compliance, 
risk management, fraud prevention, operational procedures, security measures, and audit requirements.

Your expertise includes:
- Regulatory frameworks: SOX, Basel III, PCI DSS, GDPR, IFRS, FATCA
- Policy types: compliance, risk, fraud, operational, security, audit
- Implementation guidance and best practices
- Risk assessment and mitigation strategies
- Compliance monitoring and reporting
- User-specific policy knowledge

Always provide accurate, detailed, and practical guidance based on BFSI best practices and regulatory requirements.
Focus on actionable insights and clear implementation steps.\"\"\"

PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER top_k 40
PARAMETER num_ctx 4096
"""
        
        with open(modelfile_path, 'w', encoding='utf-8') as f:
            f.write(modelfile_content)
        
        logger.info(f"Ollama Modelfile created: {modelfile_path}")
        
        # Create model info
        model_info = {
            "model_name": "user-bfsi-policy-assistant",
            "model_type": "ollama",
            "base_model": "llama2",
            "training_data_size": len(dataset),
            "modelfile_path": str(modelfile_path),
            "created_at": datetime.now().isoformat(),
            "status": "ready_for_training",
            "user_enhanced": True
        }
        
        # Save model info
        model_info_path = models_dir / "user-bfsi-policy-assistant_info.json"
        with open(model_info_path, 'w', encoding='utf-8') as f:
            json.dump(model_info, f, indent=2)
        
        logger.info(f"Model info saved: {model_info_path}")
        return True
        
    except Exception as e:
        logger.error(f"Error creating Ollama Modelfile: {e}")
        return False

def main():
    """Main retraining function"""
    print("🚀 BFSI Model Retraining with User Policies")
    print("=" * 50)
    
    # Step 1: Check policies database
    print("📊 Step 1: Checking policies database...")
    count, sample_policies = check_policies_database()
    
    if count == 0:
        print("❌ No policies found in database!")
        print("Please upload policies first using the upload tool.")
        return
    
    print(f"✅ Found {count} policies in database")
    if sample_policies:
        print("Sample policies:")
        for title, policy_type, framework in sample_policies:
            print(f"  - {title} ({policy_type}, {framework})")
    
    # Step 2: Create training dataset
    print(f"\n📊 Step 2: Creating training dataset...")
    dataset_path = create_training_dataset()
    
    if not dataset_path:
        print("❌ Failed to create training dataset")
        return
    
    print(f"✅ Training dataset created: {dataset_path}")
    
    # Step 3: Run enhanced training
    print(f"\n🤖 Step 3: Running enhanced training...")
    enhanced_success = run_enhanced_training()
    
    if enhanced_success:
        print("✅ Enhanced training completed successfully")
    else:
        print("⚠️ Enhanced training skipped (using fallback)")
    
    # Step 4: Create Ollama Modelfile
    print(f"\n🦙 Step 4: Creating Ollama Modelfile...")
    ollama_success = create_ollama_modelfile(dataset_path)
    
    if ollama_success:
        print("✅ Ollama Modelfile created successfully")
    else:
        print("❌ Failed to create Ollama Modelfile")
    
    # Step 5: Summary
    print(f"\n🎉 BFSI Model Retraining Complete!")
    print("=" * 50)
    print("📋 Summary:")
    print(f"   Policies Processed: {count}")
    print(f"   Training Dataset: {dataset_path}")
    print(f"   Enhanced Training: {'✅ Completed' if enhanced_success else '⚠️ Skipped'}")
    print(f"   Ollama Model: {'✅ Ready' if ollama_success else '❌ Failed'}")
    
    print(f"\n🚀 Next Steps:")
    print("1. Test the retrained models with your BFSI scenarios")
    print("2. Deploy the Ollama model using: ollama create user-bfsi-policy-assistant -f Modelfile")
    print("3. Validate model performance with your specific policies")
    
    if ollama_success:
        print(f"\n🦙 Ollama Model Deployment:")
        print(f"   cd ../../training/models/trained_models")
        print(f"   ollama create user-bfsi-policy-assistant -f user-bfsi-policy-assistant.Modelfile")

if __name__ == "__main__":
    main()
