# Production-Ready GRC LLM Fine-tuning System

This system provides production-ready Python code for fine-tuning a locally hosted LLM for Governance, Risk, and Compliance (GRC) platforms using Mistral-7B with QLoRA and SFTTrainer.

## Features

- **Base Model**: Mistral-7B-v0.1 from Hugging Face
- **Quantization**: 4-bit QLoRA for memory efficiency
- **Training**: SFTTrainer from TRL for supervised fine-tuning
- **LoRA**: Parameter-efficient fine-tuning with configurable parameters
- **Production Ready**: Comprehensive logging, error handling, and validation

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements-training.txt
```

### 2. Prepare Dataset

Create a `grc_dataset.json` file with the following schema:

```json
[
  {
    "instruction": "Your instruction here",
    "input": "Optional input context",
    "output": "Expected response"
  }
]
```

### 3. Run Training

```bash
python train_grc_llm.py --dataset grc_dataset.json --output ./grc-llm-finetuned
```

## Configuration

### Default Parameters

- **Model**: `mistralai/Mistral-7B-v0.1`
- **LoRA**: r=16, alpha=32, dropout=0.1
- **Training**: 3 epochs, batch_size=2, learning_rate=2e-4
- **Quantization**: 4-bit QLoRA with bfloat16

### Custom Configuration

```python
config = GRCTrainingConfig(
    base_model="mistralai/Mistral-7B-v0.1",
    output_dir="./grc-llm-finetuned",
    dataset_path="grc_dataset.json",
    lora_r=16,
    lora_alpha=32,
    lora_dropout=0.1,
    batch_size_per_device=2,
    gradient_accumulation_steps=8,
    learning_rate=2e-4,
    num_epochs=3,
    max_length=512,
    use_bf16=True
)
```

## Command Line Options

```bash
python train_grc_llm.py \
    --dataset grc_dataset.json \
    --output ./grc-llm-finetuned \
    --base-model mistralai/Mistral-7B-v0.1 \
    --epochs 3 \
    --batch-size 2 \
    --learning-rate 2e-4 \
    --lora-r 16 \
    --lora-alpha 32 \
    --max-length 512
```

## System Requirements

### Hardware
- **GPU**: NVIDIA GPU with 16GB+ VRAM (recommended)
- **RAM**: 32GB+ system RAM
- **Storage**: 50GB+ free space

### Software
- Python 3.8+
- CUDA 11.8+ (for GPU training)
- PyTorch 2.0+

## Dataset Format

The training system expects a JSON file with the following structure:

```json
[
  {
    "instruction": "Analyze the compliance risk for this banking transaction",
    "input": "A customer is requesting to transfer $50,000 to an offshore account...",
    "output": "This transaction presents a medium-high compliance risk due to..."
  }
]
```

### Dataset Guidelines

1. **Instruction**: Clear, specific task description
2. **Input**: Context or scenario (optional)
3. **Output**: Expected response with detailed analysis

## Training Process

### 1. Model Loading
- Loads Mistral-7B with 4-bit quantization
- Configures BitsAndBytesConfig for efficiency
- Sets up tokenizer with proper padding

### 2. Dataset Preparation
- Loads JSON dataset
- Formats instruction + input as training prompt
- Creates Hugging Face Dataset object

### 3. LoRA Setup
- Applies LoRA to target modules
- Configures rank, alpha, and dropout
- Prints trainable parameters

### 4. Training
- Uses SFTTrainer for supervised fine-tuning
- Implements mixed precision training
- Saves model at each epoch

## Output

The training process saves:

- **Model**: Fine-tuned model weights
- **Tokenizer**: Associated tokenizer files
- **Config**: Training configuration
- **Logs**: Detailed training logs

## Monitoring

### Training Progress
- Real-time loss monitoring
- Parameter count tracking
- Memory usage optimization

### Logging
- Comprehensive logging with timestamps
- Error handling and recovery
- Training summary

## Best Practices

### 1. Dataset Quality
- Ensure high-quality, diverse examples
- Balance different GRC scenarios
- Include edge cases and complex scenarios

### 2. Training Configuration
- Start with default parameters
- Adjust learning rate based on convergence
- Monitor for overfitting

### 3. Resource Management
- Use gradient accumulation for large batches
- Monitor GPU memory usage
- Implement checkpointing for long training runs

## Troubleshooting

### Common Issues

1. **CUDA Out of Memory**
   - Reduce batch size
   - Increase gradient accumulation steps
   - Use CPU offloading

2. **Dataset Loading Errors**
   - Verify JSON format
   - Check file encoding (UTF-8)
   - Validate required fields

3. **Training Convergence**
   - Adjust learning rate
   - Increase training epochs
   - Check dataset quality

### Performance Optimization

1. **Memory Optimization**
   - Use 4-bit quantization
   - Enable gradient checkpointing
   - Optimize data loading

2. **Training Speed**
   - Use mixed precision training
   - Enable data parallelism
   - Optimize data preprocessing

## Example Usage

```python
from bfsi_llm_training_system import (
    GRCTrainingConfig,
    load_model,
    load_dataset,
    setup_lora,
    train_model
)

# Configure training
config = GRCTrainingConfig(
    dataset_path="grc_dataset.json",
    output_dir="./grc-llm-finetuned"
)

# Load components
model, tokenizer = load_model(config)
dataset = load_dataset(config)
model = setup_lora(model, config)

# Train model
train_model(model, tokenizer, dataset, config)
```

## Production Deployment

### Model Serving
- Use the fine-tuned model for inference
- Implement proper error handling
- Add monitoring and logging

### Integration
- Integrate with existing GRC systems
- Implement API endpoints
- Add authentication and authorization

## Support

For issues and questions:
1. Check the logs for error messages
2. Verify system requirements
3. Review dataset format
4. Test with smaller datasets first

## License

This training system is part of the GRC Platform and follows the same licensing terms.
