"""
Unit tests for SimpleVectorStore.
"""

import pytest
import numpy as np
from unittest.mock import patch, MagicMock
import tempfile
import os

# Import the SimpleVectorStore
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'shared', 'utils'))
from vector_store import SimpleVectorStore


class TestSimpleVectorStore:
    """Test cases for SimpleVectorStore."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.store = SimpleVectorStore("test_collection", self.temp_dir)
    
    def teardown_method(self):
        """Clean up test fixtures."""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_initialization(self):
        """Test store initialization."""
        assert self.store.collection_name == "test_collection"
        assert self.store.persist_directory == self.temp_dir
        assert len(self.store.vectors) == 0
        assert len(self.store.embeddings) == 0
    
    def test_add_vectors(self):
        """Test adding vectors to the store."""
        ids = ["1", "2"]
        embeddings = [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]
        metadatas = [{"type": "policy"}, {"type": "risk"}]
        documents = ["Policy document 1", "Risk document 1"]
        
        self.store.add(ids, embeddings, metadatas, documents)
        
        assert len(self.store.vectors) == 2
        assert len(self.store.embeddings) == 2
        assert "1" in self.store.vectors
        assert "2" in self.store.vectors
    
    def test_query_vectors(self):
        """Test querying vectors."""
        # Add test vectors
        ids = ["1", "2"]
        embeddings = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]
        self.store.add(ids, embeddings)
        
        # Query with similar vector
        query_embeddings = [[1.0, 0.0, 0.0]]
        results = self.store.query(query_embeddings, n_results=2)
        
        assert len(results['ids']) == 1
        assert len(results['ids'][0]) == 2
        assert "1" in results['ids'][0]
    
    def test_get_vectors(self):
        """Test getting vectors by IDs."""
        ids = ["1", "2"]
        embeddings = [[1.0, 2.0], [3.0, 4.0]]
        self.store.add(ids, embeddings)
        
        result = self.store.get(["1"])
        assert len(result['ids']) == 1
        assert result['ids'][0] == "1"
    
    def test_delete_vectors(self):
        """Test deleting vectors."""
        ids = ["1", "2"]
        embeddings = [[1.0, 2.0], [3.0, 4.0]]
        self.store.add(ids, embeddings)
        
        assert len(self.store.vectors) == 2
        self.store.delete(["1"])
        assert len(self.store.vectors) == 1
        assert "1" not in self.store.vectors
    
    def test_count(self):
        """Test counting vectors."""
        assert self.store.count() == 0
        
        ids = ["1", "2"]
        embeddings = [[1.0, 2.0], [3.0, 4.0]]
        self.store.add(ids, embeddings)
        
        assert self.store.count() == 2
    
    def test_reset(self):
        """Test resetting the store."""
        ids = ["1", "2"]
        embeddings = [[1.0, 2.0], [3.0, 4.0]]
        self.store.add(ids, embeddings)
        
        assert self.store.count() == 2
        self.store.reset()
        assert self.store.count() == 0


if __name__ == "__main__":
    pytest.main([__file__])
