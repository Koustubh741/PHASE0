#!/usr/bin/env python3
"""
BFSI Model Training CLI
Interactive command-line interface for training BFSI models
"""

import sys
import json
from pathlib import Path
from simple_bfsi_training import SimpleBFSITraining

def print_banner():
    """Print application banner"""
    print("=" * 60)
    print("🚀 BFSI LLM MODEL TRAINING SYSTEM")
    print("=" * 60)
    print("Train language models on your BFSI policies")
    print("Supports: Ollama, Hugging Face Transformers")
    print("BFSI Models: FinBERT, DistilBERT, BART, BERT NER")
    print("Training Data: 25,000 samples")
    print("=" * 60)

def print_menu():
    """Print main menu"""
    print("\n📋 MAIN MENU:")
    print("1. Prepare training dataset (25K samples)")
    print("2. Train Ollama model")
    print("3. Train Hugging Face model (FinBERT)")
    print("4. Train BFSI model stack (all models)")
    print("5. List trained models")
    print("6. View training statistics")
    print("7. Quick train (all models)")
    print("8. Exit")
    print("-" * 30)

def get_policy_types():
    """Get policy types from user"""
    print("\n📝 Select policy types to include:")
    print("1. compliance")
    print("2. risk")
    print("3. fraud")
    print("4. operational")
    print("5. security")
    print("6. audit")
    print("7. all")
    
    choice = input("Enter choice (1-7): ").strip()
    
    type_map = {
        "1": ["compliance"],
        "2": ["risk"],
        "3": ["fraud"],
        "4": ["operational"],
        "5": ["security"],
        "6": ["audit"],
        "7": ["compliance", "risk", "fraud", "operational", "security", "audit"]
    }
    
    return type_map.get(choice, ["compliance", "risk", "security"])

def prepare_dataset(trainer):
    """Prepare training dataset"""
    print("\n📊 PREPARE TRAINING DATASET")
    print("-" * 30)
    
    try:
        policy_types = get_policy_types()
        print(f"Selected policy types: {policy_types}")
        
        dataset_path = trainer.prepare_training_data(policy_types)
        
        print(f"✅ Dataset created successfully!")
        print(f"📁 Path: {dataset_path}")
        
        # Show dataset info
        with open(dataset_path, 'r') as f:
            data = json.load(f)
        
        print(f"📊 Total examples: {len(data)}")
        
        return dataset_path
        
    except Exception as e:
        print(f"❌ Error preparing dataset: {e}")
        return None

def train_ollama_model(trainer, dataset_path=None):
    """Train Ollama model"""
    print("\n🤖 TRAIN OLLAMA MODEL")
    print("-" * 30)
    
    if not dataset_path:
        print("No dataset provided. Preparing new dataset...")
        dataset_path = prepare_dataset(trainer)
        if not dataset_path:
            return
    
    model_name = input("Enter model name (default: bfsi-ollama-model): ").strip()
    if not model_name:
        model_name = "bfsi-ollama-model"
    
    print(f"🚀 Training Ollama model: {model_name}")
    print("This may take a few minutes...")
    
    try:
        result = trainer.train_with_ollama(model_name, dataset_path)
        
        if "error" in result:
            print(f"❌ Training failed: {result['error']}")
        else:
            print(f"✅ Training completed!")
            print(f"   Model: {result['model_name']}")
            print(f"   Status: {result['status']}")
            print(f"   Training time: {result.get('training_time', 'N/A')}s")
            print(f"   Data size: {result.get('training_data_size', 'N/A')} examples")
    
    except Exception as e:
        print(f"❌ Error training Ollama model: {e}")

def train_transformers_model(trainer, dataset_path=None):
    """Train Hugging Face model"""
    print("\n🤖 TRAIN HUGGING FACE MODEL (FinBERT)")
    print("-" * 30)
    
    if not dataset_path:
        print("No dataset provided. Preparing new dataset...")
        dataset_path = prepare_dataset(trainer)
        if not dataset_path:
            return
    
    model_name = input("Enter model name (default: bfsi-transformers-model): ").strip()
    if not model_name:
        model_name = "bfsi-transformers-model"
    
    print(f"🚀 Training Hugging Face model: {model_name}")
    print("Base model: ProsusAI/finbert")
    print("Training data: 25,000 samples")
    print("This may take a few minutes...")
    
    try:
        result = trainer.train_with_transformers(model_name, dataset_path)
        
        if "error" in result:
            print(f"❌ Training failed: {result['error']}")
        else:
            print(f"✅ Training completed!")
            print(f"   Model: {result['model_name']}")
            print(f"   Status: {result['status']}")
            print(f"   Base model: {result.get('base_model', 'N/A')}")
            print(f"   Data size: {result.get('training_data_size', 'N/A')} examples")
            
            if 'bfsi_model_stack' in result:
                print(f"   BFSI Models: {len(result['bfsi_model_stack'])} specialized models")
            
            if 'test_output' in result:
                print(f"   Test output: {result['test_output'][:100]}...")
    
    except Exception as e:
        print(f"❌ Error training Hugging Face model: {e}")

def train_bfsi_model_stack(trainer, dataset_path=None):
    """Train complete BFSI model stack"""
    print("\n🏦 TRAIN BFSI MODEL STACK")
    print("-" * 30)
    print("Training all specialized BFSI models:")
    print("• FinBERT (Financial analysis)")
    print("• DistilBERT (Document classification)")
    print("• BART (Summarization)")
    print("• BERT NER (Entity recognition)")
    print("• DistilBERT Q&A (Question answering)")
    print("• DialoGPT (Conversational AI)")
    
    if not dataset_path:
        print("\nNo dataset provided. Preparing new dataset...")
        dataset_path = prepare_dataset(trainer)
        if not dataset_path:
            return
    
    model_name = input("Enter model name (default: bfsi-complete-stack): ").strip()
    if not model_name:
        model_name = "bfsi-complete-stack"
    
    print(f"\n🚀 Training BFSI model stack: {model_name}")
    print("Training data: 25,000 samples")
    print("This will take several minutes...")
    
    try:
        # Train the main transformers model with BFSI stack
        result = trainer.train_with_transformers(model_name, dataset_path)
        
        if "error" in result:
            print(f"❌ Training failed: {result['error']}")
        else:
            print(f"✅ BFSI Model Stack Training Completed!")
            print(f"   Model: {result['model_name']}")
            print(f"   Status: {result['status']}")
            print(f"   Base model: {result.get('base_model', 'N/A')}")
            print(f"   Data size: {result.get('training_data_size', 'N/A')} examples")
            
            if 'bfsi_model_stack' in result:
                print(f"\n📋 BFSI Model Stack:")
                for model_type, model_name in result['bfsi_model_stack'].items():
                    print(f"   {model_type}: {model_name}")
            
            if 'test_output' in result:
                print(f"\n🧪 Test output: {result['test_output'][:100]}...")
    
    except Exception as e:
        print(f"❌ Error training BFSI model stack: {e}")

def list_models(trainer):
    """List trained models"""
    print("\n📋 TRAINED MODELS")
    print("-" * 30)
    
    try:
        models = trainer.list_models()
        
        if not models:
            print("No trained models found.")
            return
        
        for i, model in enumerate(models, 1):
            print(f"\n{i}. {model['model_name']}")
            print(f"   Type: {model.get('model_type', 'unknown')}")
            print(f"   Status: {model.get('status', 'unknown')}")
            print(f"   Created: {model.get('created_at', 'unknown')}")
            
            if 'training_data_size' in model:
                print(f"   Training data: {model['training_data_size']} examples")
            
            if 'base_model' in model:
                print(f"   Base model: {model['base_model']}")
    
    except Exception as e:
        print(f"❌ Error listing models: {e}")

def show_statistics(trainer):
    """Show training statistics"""
    print("\n📈 TRAINING STATISTICS")
    print("-" * 30)
    
    try:
        stats = trainer.get_training_stats()
        
        print(f"Total models: {stats['total_models']}")
        print(f"Model types: {', '.join(stats['model_types'])}")
        print(f"Successful models: {stats['successful_models']}")
        
        if stats['latest_model']:
            print(f"\nLatest model: {stats['latest_model']['model_name']}")
            print(f"Type: {stats['latest_model'].get('model_type', 'unknown')}")
            print(f"Status: {stats['latest_model'].get('status', 'unknown')}")
        
        # Show model directory info
        models_dir = Path("trained_models")
        if models_dir.exists():
            model_files = list(models_dir.glob("*"))
            print(f"\nModel files: {len(model_files)}")
            
            total_size = sum(f.stat().st_size for f in model_files if f.is_file())
            print(f"Total size: {total_size / 1024 / 1024:.2f} MB")
    
    except Exception as e:
        print(f"❌ Error getting statistics: {e}")

def quick_train(trainer):
    """Quick train all models"""
    print("\n⚡ QUICK TRAIN ALL MODELS")
    print("-" * 30)
    print("This will prepare a dataset and train both Ollama and Hugging Face models.")
    
    confirm = input("Continue? (y/N): ").strip().lower()
    if confirm != 'y':
        print("Cancelled.")
        return
    
    try:
        # Prepare dataset
        print("\n📊 Preparing dataset...")
        dataset_path = trainer.prepare_training_data(['compliance', 'risk', 'security'])
        print(f"✅ Dataset ready: {dataset_path}")
        
        # Train Ollama model
        print("\n🤖 Training Ollama model...")
        ollama_result = trainer.train_with_ollama("bfsi-quick-ollama", dataset_path)
        if "error" not in ollama_result:
            print("✅ Ollama model trained successfully!")
        else:
            print(f"⚠️ Ollama training: {ollama_result['error']}")
        
        # Train Transformers model
        print("\n🤖 Training Hugging Face model...")
        transformers_result = trainer.train_with_transformers("bfsi-quick-transformers", dataset_path)
        if "error" not in transformers_result:
            print("✅ Hugging Face model trained successfully!")
        else:
            print(f"⚠️ Transformers training: {transformers_result['error']}")
        
        # Show final stats
        print("\n📈 Final Statistics:")
        stats = trainer.get_training_stats()
        print(f"Total models: {stats['total_models']}")
        print(f"Successful models: {stats['successful_models']}")
        
        print("\n✅ Quick training completed!")
    
    except Exception as e:
        print(f"❌ Error in quick training: {e}")

def main():
    """Main function"""
    print_banner()
    
    # Initialize trainer
    try:
        trainer = SimpleBFSITraining()
        print("✅ Training system initialized")
    except Exception as e:
        print(f"❌ Failed to initialize training system: {e}")
        sys.exit(1)
    
    dataset_path = None
    
    while True:
        print_menu()
        choice = input("Enter your choice (1-8): ").strip()
        
        if choice == "1":
            dataset_path = prepare_dataset(trainer)
        
        elif choice == "2":
            train_ollama_model(trainer, dataset_path)
        
        elif choice == "3":
            train_transformers_model(trainer, dataset_path)
        
        elif choice == "4":
            train_bfsi_model_stack(trainer, dataset_path)
        
        elif choice == "5":
            list_models(trainer)
        
        elif choice == "6":
            show_statistics(trainer)
        
        elif choice == "7":
            quick_train(trainer)
        
        elif choice == "8":
            print("\n👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice. Please try again.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
