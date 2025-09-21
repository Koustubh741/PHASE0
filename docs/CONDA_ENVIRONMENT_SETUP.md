# GRC Platform - Conda Environment Setup Guide

This guide will help you set up a conda environment for the GRC (Governance, Risk, and Compliance) Platform project.

## Prerequisites

Before setting up the conda environment, ensure you have:

1. **Anaconda or Miniconda installed** on your system
   - Download from: https://www.anaconda.com/products/distribution
   - Or Miniconda: https://docs.conda.io/en/latest/miniconda.html

2. **Git** (if cloning the repository)
3. **CUDA Toolkit** (optional, for GPU acceleration with PyTorch)

## Quick Setup (Automated)

The easiest way to set up the conda environment is using our automated script:

```bash
# Run the setup script
python setup_conda_env.py
```

This script will:
- Check if conda is installed
- Detect CUDA availability
- Create the conda environment with all dependencies
- Set up environment variables
- Create activation scripts
- Verify the installation

## Manual Setup

If you prefer to set up the environment manually:

### 1. Create the Environment

```bash
# Create environment from environment.yml
conda env create -f environment.yml

# Or create manually with Python 3.11
conda create -n grc-platform python=3.11
conda activate grc-platform
```

### 2. Install Dependencies

```bash
# Activate the environment
conda activate grc-platform

# Install core dependencies
conda install -c conda-forge numpy pandas scikit-learn
conda install -c pytorch pytorch torchvision torchaudio
conda install -c huggingface transformers tokenizers datasets

# Install additional packages via pip
pip install -r requirements.txt
pip install -r requirements_huggingface_local.txt
```

## Environment Details

### Python Version
- **Python 3.11** (required for the project)

### Key Dependencies

#### Core Framework
- **FastAPI** (0.115.6+) - Web framework
- **Uvicorn** - ASGI server
- **Pydantic** (2.9.2+) - Data validation

#### Database & Caching
- **SQLAlchemy** (2.0.35+) - ORM
- **PostgreSQL** - Primary database
- **Redis** (5.2.1+) - Caching and session storage

#### AI/ML Libraries
- **PyTorch** (2.0.0+) - Deep learning framework
- **Transformers** (4.35.0+) - Hugging Face transformers
- **LangChain** (0.3.7+) - LLM framework
- **ChromaDB** (0.5.23+) - Vector database
- **Ollama** (0.4.2+) - Local LLM runner

#### Data Processing
- **NumPy** (1.26.4+) - Numerical computing
- **Pandas** (2.2.3+) - Data manipulation
- **Scikit-learn** (1.3.0+) - Machine learning

## GPU Support

The environment is configured to support both CPU and GPU computation:

### CUDA Support
If you have an NVIDIA GPU with CUDA support:
- PyTorch will be installed with CUDA support
- GPU acceleration will be available for model training and inference

### CPU-Only
If no CUDA is detected:
- CPU-only PyTorch will be installed
- All functionality remains available (slower for large models)

## Environment Variables

The setup script creates a `.env` file with the following variables:

```bash
GRC_PLATFORM_ENV=development
PYTHONPATH=/path/to/your/project
CUDA_VISIBLE_DEVICES=0
```

## Activation Scripts

After setup, you can use the provided activation scripts:

### Windows
```cmd
activate_grc_env.bat
```

### Linux/macOS
```bash
source activate_grc_env.sh
```

### Manual Activation
```bash
conda activate grc-platform
```

## Running the Platform

Once the environment is set up and activated, you can start the GRC platform services:

```bash
# Start the main integration service
python start_bfsi_integration.py

# Start local AI services
python start_local_ai_services.py

# Start the frontend
python start_bfsi_frontend.py
```

## Troubleshooting

### Common Issues

1. **Conda not found**
   - Ensure Anaconda/Miniconda is installed and in your PATH
   - Try restarting your terminal

2. **CUDA issues**
   - Check if you have NVIDIA drivers installed
   - Verify CUDA toolkit version compatibility
   - Use CPU-only version if GPU is not available

3. **Package conflicts**
   - Try creating a fresh environment
   - Use `conda env remove -n grc-platform` to remove existing environment

4. **Memory issues**
   - Some models require significant RAM
   - Consider using smaller models for development

### Environment Management

```bash
# List environments
conda env list

# Remove environment
conda env remove -n grc-platform

# Update environment
conda env update -f environment.yml

# Export environment
conda env export > environment_backup.yml
```

## Development Tools

The environment includes development tools:

- **Jupyter Lab** - Interactive development
- **Black** - Code formatting
- **Flake8** - Linting
- **MyPy** - Type checking
- **Pytest** - Testing framework

## Performance Optimization

### For Development
- Use CPU-only PyTorch for faster startup
- Enable model caching
- Use smaller models for testing

### For Production
- Use GPU acceleration
- Enable model quantization
- Configure proper memory management

## Support

If you encounter issues:

1. Check the troubleshooting section above
2. Verify all prerequisites are installed
3. Check the project's GitHub issues
4. Review the logs for specific error messages

## Next Steps

After setting up the conda environment:

1. **Configure the database** - Set up PostgreSQL
2. **Set up Redis** - Configure caching
3. **Configure AI models** - Set up Ollama or Hugging Face models
4. **Run tests** - Verify everything works
5. **Start development** - Begin working on the platform

For more detailed information, see the main project documentation.
