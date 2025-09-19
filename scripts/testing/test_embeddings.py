#!/usr/bin/env python3
"""
Test script to debug embeddings issue
"""

import torch
from transformers import pipeline

def test_embeddings():
    print("Testing embeddings generation...")
    
    # Create the pipeline
    pipe = pipeline(
        "feature-extraction",
        model="sentence-transformers/all-MiniLM-L6-v2",
        device=-1  # CPU
    )
    
    # Test text
    text = "This is a test sentence for embedding generation."
    
    # Generate embeddings
    embeddings = pipe(text)
    
    print(f"Embeddings type: {type(embeddings)}")
    print(f"Embeddings length: {len(embeddings)}")
    print(f"First element type: {type(embeddings[0])}")
    print(f"First element shape: {embeddings[0].shape if hasattr(embeddings[0], 'shape') else 'No shape'}")
    
    # Try to extract the vector
    try:
        # Method 1: Mean pooling
        if hasattr(embeddings[0], 'mean'):
            result = embeddings[0].mean(dim=0)
            print(f"Mean pooling result type: {type(result)}")
            print(f"Mean pooling result shape: {result.shape}")
            print(f"Mean pooling result (first 5): {result[:5].tolist()}")
        else:
            print("No mean method available")
            
        # Method 2: Direct access
        if hasattr(embeddings[0], 'tolist'):
            result = embeddings[0].tolist()
            print(f"Direct tolist result type: {type(result)}")
            print(f"Direct tolist result length: {len(result)}")
        else:
            print("No tolist method available")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_embeddings()

