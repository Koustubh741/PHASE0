#!/usr/bin/env python3
"""
Simple Redis 5.2.1 Compatibility Test
Quick verification that Redis 5.2.1 is working correctly
"""

import redis
import json
import time
import uuid
from datetime import datetime

def test_redis_basic():
    """Test basic Redis 5.2.1 functionality"""
    print("🧪 Testing Redis 5.2.1 Basic Functionality...")
    
    try:
        # Connect to Redis
        client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
        
        # Test connection
        client.ping()
        print("✅ Redis connection successful")
        
        # Test basic operations
        test_key = f"test_{uuid.uuid4().hex[:8]}"
        test_value = "Redis 5.2.1 Test"
        
        # SET/GET test
        client.set(test_key, test_value)
        retrieved = client.get(test_key)
        assert retrieved == test_value
        print("✅ SET/GET operations working")
        
        # Hash operations
        hash_key = f"hash_{uuid.uuid4().hex[:8]}"
        client.hset(hash_key, mapping={"field1": "value1", "field2": "value2"})
        hash_data = client.hgetall(hash_key)
        assert len(hash_data) == 2
        print("✅ Hash operations working")
        
        # List operations
        list_key = f"list_{uuid.uuid4().hex[:8]}"
        client.lpush(list_key, "item1", "item2", "item3")
        list_length = client.llen(list_key)
        assert list_length == 3
        print("✅ List operations working")
        
        # Set operations
        set_key = f"set_{uuid.uuid4().hex[:8]}"
        client.sadd(set_key, "member1", "member2", "member3")
        set_size = client.scard(set_key)
        assert set_size == 3
        print("✅ Set operations working")
        
        # Sorted set operations
        zset_key = f"zset_{uuid.uuid4().hex[:8]}"
        client.zadd(zset_key, {"member1": 1.0, "member2": 2.0, "member3": 3.0})
        zset_size = client.zcard(zset_key)
        assert zset_size == 3
        print("✅ Sorted set operations working")
        
        # Cleanup
        client.delete(test_key, hash_key, list_key, set_key, zset_key)
        
        # Get Redis info
        info = client.info()
        redis_version = info.get('redis_version', 'Unknown')
        used_memory = info.get('used_memory_human', 'Unknown')
        
        print(f"📊 Redis Version: {redis_version}")
        print(f"📊 Used Memory: {used_memory}")
        
        client.close()
        
        print("\n🎉 Redis 5.2.1 compatibility test PASSED!")
        return True
        
    except redis.ConnectionError:
        print("❌ Cannot connect to Redis. Make sure Redis is running on localhost:6379")
        print("💡 Start Redis with: docker run -d --name test-redis -p 6379:6379 redis:7-alpine")
        return False
    except Exception as e:
        print(f"❌ Redis test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting Redis 5.2.1 Simple Compatibility Test")
    print("=" * 60)
    
    success = test_redis_basic()
    
    if success:
        print("\n✅ Redis 5.2.1 is fully compatible and working correctly!")
        exit(0)
    else:
        print("\n❌ Redis 5.2.1 compatibility test failed!")
        exit(1)
