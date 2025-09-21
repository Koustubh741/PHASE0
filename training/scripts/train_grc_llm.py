#!/usr/bin/env python3
"""
Production-Ready GRC LLM Fine-tuning Script
Optimized for Mistral-7B with QLoRA and SFTTrainer

Usage:
    python train_grc_llm.py --dataset grc_dataset.json --output ./grc-llm-finetuned
"""

import argparse
import logging
import os
import sys
from pathlib import Path

# Add the current directory to Python path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from bfsi_llm_training_system import (
    GRCTrainingConfig,
    load_model,
    load_dataset,
    setup_lora,
    train_model
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Fine-tune GRC LLM with Mistral-7B")
    
    parser.add_argument(
        "--dataset",
        type=str,
        default="grc_dataset.json",
        help="Path to the GRC dataset JSON file"
    )
    
    parser.add_argument(
        "--output",
        type=str,
        default="./grc-llm-finetuned",
        help="Output directory for the fine-tuned model"
    )
    
    parser.add_argument(
        "--base-model",
        type=str,
        default="mistralai/Mistral-7B-v0.1",
        help="Base model to fine-tune"
    )
    
    parser.add_argument(
        "--epochs",
        type=int,
        default=3,
        help="Number of training epochs"
    )
    
    parser.add_argument(
        "--batch-size",
        type=int,
        default=2,
        help="Batch size per device"
    )
    
    parser.add_argument(
        "--learning-rate",
        type=float,
        default=2e-4,
        help="Learning rate"
    )
    
    parser.add_argument(
        "--lora-r",
        type=int,
        default=16,
        help="LoRA rank"
    )
    
    parser.add_argument(
        "--lora-alpha",
        type=int,
        default=32,
        help="LoRA alpha"
    )
    
    parser.add_argument(
        "--max-length",
        type=int,
        default=512,
        help="Maximum sequence length"
    )
    
    return parser.parse_args()


def validate_environment():
    """Validate the training environment."""
    logger.info("Validating training environment...")
    
    # Check CUDA availability
    import torch
    if torch.cuda.is_available():
        logger.info(f"CUDA available: {torch.cuda.get_device_name(0)}")
        logger.info(f"CUDA memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
    else:
        logger.warning("CUDA not available. Training will be slower on CPU.")
    
    # Check required packages
    required_packages = [
        'transformers', 'datasets', 'peft', 'trl', 
        'accelerate', 'bitsandbytes'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        logger.error(f"Missing required packages: {missing_packages}")
        logger.error("Please install requirements: pip install -r requirements-training.txt")
        sys.exit(1)
    
    logger.info("Environment validation completed successfully")


def main():
    """Main training function."""
    args = parse_args()
    
    # Validate environment
    validate_environment()
    
    # Check dataset file
    if not os.path.exists(args.dataset):
        logger.error(f"Dataset file not found: {args.dataset}")
        sys.exit(1)
    
    # Create output directory
    os.makedirs(args.output, exist_ok=True)
    
    # Initialize configuration
    config = GRCTrainingConfig(
        base_model=args.base_model,
        output_dir=args.output,
        dataset_path=args.dataset,
        num_epochs=args.epochs,
        batch_size_per_device=args.batch_size,
        learning_rate=args.learning_rate,
        lora_r=args.lora_r,
        lora_alpha=args.lora_alpha,
        max_length=args.max_length
    )
    
    logger.info("Starting GRC LLM fine-tuning process")
    logger.info(f"Configuration: {config}")
    
    try:
        # Load model and tokenizer
        logger.info("Loading model and tokenizer...")
        model, tokenizer = load_model(config)
        
        # Load dataset
        logger.info("Loading and preparing dataset...")
        dataset = load_dataset(config)
        
        # Setup LoRA
        logger.info("Setting up LoRA configuration...")
        model = setup_lora(model, config)
        
        # Train model
        logger.info("Starting training...")
        train_model(model, tokenizer, dataset, config)
        
        logger.info("GRC LLM fine-tuning completed successfully!")
        logger.info(f"Model saved to: {config.output_dir}")
        
        # Print final summary
        print("\n" + "="*50)
        print("TRAINING COMPLETED SUCCESSFULLY!")
        print("="*50)
        print(f"Model saved to: {config.output_dir}")
        print(f"Dataset used: {config.dataset_path}")
        print(f"Training epochs: {config.num_epochs}")
        print(f"LoRA configuration: r={config.lora_r}, alpha={config.lora_alpha}")
        print("="*50)
        
    except Exception as e:
        logger.error(f"Training failed: {str(e)}")
        raise


if __name__ == "__main__":
    main()
