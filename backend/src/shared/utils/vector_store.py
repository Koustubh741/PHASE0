"""
Simple Vector Store Implementation
A lightweight vector store that doesn't require ChromaDB or ONNX
"""

import json
import os
import numpy as np
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class SimpleVectorStore:
    """Simple in-memory vector store implementation"""
    
    def __init__(self, collection_name: str = "default", persist_directory: str = "./vector_store"):
        self.collection_name = collection_name
        self.persist_directory = persist_directory
        self.vectors = {}
        self.metadata = {}
        self.embeddings = []
        self.ids = []
        
        # Create persist directory if it doesn't exist
        os.makedirs(persist_directory, exist_ok=True)
        
        # Load existing data if available
        self._load_data()
        
        logger.info(f"SimpleVectorStore initialized for collection: {collection_name}")
    
    def _load_data(self):
        """Load data from disk if available"""
        try:
            data_file = os.path.join(self.persist_directory, f"{self.collection_name}.json")
            if os.path.exists(data_file):
                with open(data_file, 'r') as f:
                    data = json.load(f)
                    self.vectors = data.get('vectors', {})
                    self.metadata = data.get('metadata', {})
                    self.embeddings = data.get('embeddings', [])
                    self.ids = data.get('ids', [])
                logger.info(f"Loaded {len(self.vectors)} vectors from disk")
        except Exception as e:
            logger.warning(f"Failed to load data: {e}")
    
    def _save_data(self):
        """Save data to disk"""
        try:
            data_file = os.path.join(self.persist_directory, f"{self.collection_name}.json")
            data = {
                'vectors': self.vectors,
                'metadata': self.metadata,
                'embeddings': self.embeddings,
                'ids': self.ids
            }
            with open(data_file, 'w') as f:
                json.dump(data, f)
            logger.info(f"Saved {len(self.vectors)} vectors to disk")
        except Exception as e:
            logger.error(f"Failed to save data: {e}")
    
    def add(self, ids: List[str], embeddings: List[List[float]], metadatas: Optional[List[Dict]] = None, documents: Optional[List[str]] = None):
        """Add vectors to the store"""
        try:
            for i, (id_val, embedding) in enumerate(zip(ids, embeddings)):
                self.vectors[id_val] = embedding
                self.embeddings.append(embedding)
                self.ids.append(id_val)
                
                # Store metadata if provided
                if metadatas and i < len(metadatas):
                    self.metadata[id_val] = metadatas[i]
                
                # Store document if provided
                if documents and i < len(documents):
                    if id_val not in self.metadata:
                        self.metadata[id_val] = {}
                    self.metadata[id_val]['document'] = documents[i]
            
            # Save to disk
            self._save_data()
            logger.info(f"Added {len(ids)} vectors to collection {self.collection_name}")
            
        except Exception as e:
            logger.error(f"Failed to add vectors: {e}")
            raise
    
    def query(self, query_embeddings: List[List[float]], n_results: int = 5, where: Optional[Dict] = None) -> Dict[str, Any]:
        """Query the vector store"""
        try:
            if not self.embeddings:
                return {
                    'ids': [[]],
                    'distances': [[]],
                    'metadatas': [[]],
                    'documents': [[]]
                }
            
            results = {
                'ids': [],
                'distances': [],
                'metadatas': [],
                'documents': []
            }
            
            for query_embedding in query_embeddings:
                # Calculate cosine similarity
                similarities = []
                for i, embedding in enumerate(self.embeddings):
                    similarity = self._cosine_similarity(query_embedding, embedding)
                    similarities.append((similarity, i))
                
                # Sort by similarity (descending)
                similarities.sort(key=lambda x: x[0], reverse=True)
                
                # Get top results
                top_results = similarities[:n_results]
                
                result_ids = []
                result_distances = []
                result_metadatas = []
                result_documents = []
                
                for similarity, idx in top_results:
                    id_val = self.ids[idx]
                    result_ids.append(id_val)
                    result_distances.append(1 - similarity)  # Convert to distance
                    
                    # Add metadata
                    metadata = self.metadata.get(id_val, {})
                    result_metadatas.append(metadata)
                    
                    # Add document if available
                    document = metadata.get('document', '')
                    result_documents.append(document)
                
                results['ids'].append(result_ids)
                results['distances'].append(result_distances)
                results['metadatas'].append(result_metadatas)
                results['documents'].append(result_documents)
            
            return results
            
        except Exception as e:
            logger.error(f"Failed to query vectors: {e}")
            raise
    
    def _cosine_similarity(self, a: List[float], b: List[float]) -> float:
        """Calculate cosine similarity between two vectors"""
        try:
            a = np.array(a)
            b = np.array(b)
            
            dot_product = np.dot(a, b)
            norm_a = np.linalg.norm(a)
            norm_b = np.linalg.norm(b)
            
            if norm_a == 0 or norm_b == 0:
                return 0.0
            
            return dot_product / (norm_a * norm_b)
        except Exception as e:
            logger.error(f"Failed to calculate cosine similarity: {e}")
            return 0.0
    
    def get(self, ids: List[str]) -> Dict[str, Any]:
        """Get vectors by IDs"""
        try:
            result = {
                'ids': [],
                'embeddings': [],
                'metadatas': [],
                'documents': []
            }
            
            for id_val in ids:
                if id_val in self.vectors:
                    result['ids'].append(id_val)
                    result['embeddings'].append(self.vectors[id_val])
                    
                    metadata = self.metadata.get(id_val, {})
                    result['metadatas'].append(metadata)
                    
                    document = metadata.get('document', '')
                    result['documents'].append(document)
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to get vectors: {e}")
            raise
    
    def delete(self, ids: List[str]):
        """Delete vectors by IDs"""
        try:
            for id_val in ids:
                if id_val in self.vectors:
                    # Find and remove from embeddings and ids lists
                    if id_val in self.ids:
                        idx = self.ids.index(id_val)
                        self.ids.pop(idx)
                        self.embeddings.pop(idx)
                    
                    # Remove from dictionaries
                    del self.vectors[id_val]
                    if id_val in self.metadata:
                        del self.metadata[id_val]
            
            # Save to disk
            self._save_data()
            logger.info(f"Deleted {len(ids)} vectors from collection {self.collection_name}")
            
        except Exception as e:
            logger.error(f"Failed to delete vectors: {e}")
            raise
    
    def count(self) -> int:
        """Get the number of vectors in the collection"""
        return len(self.vectors)
    
    def reset(self):
        """Reset the collection"""
        self.vectors = {}
        self.metadata = {}
        self.embeddings = []
        self.ids = []
        self._save_data()
        logger.info(f"Reset collection {self.collection_name}")

# Global instance
vector_store = SimpleVectorStore("compliance-policies")

