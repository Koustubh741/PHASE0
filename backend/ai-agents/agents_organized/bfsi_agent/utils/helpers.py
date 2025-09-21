"""
BFSI Agent Helper Utilities
==========================

This module provides general helper functions and utilities for the BFSI agent system.
"""

import uuid
import hashlib
import json
from typing import Any, Dict, List, Optional, Union
from datetime import datetime, timezone
import logging

logger = logging.getLogger(__name__)

def generate_operation_id(prefix: str = "bfsi", include_timestamp: bool = True) -> str:
    """
    Generate a unique operation ID.
    
    Args:
        prefix: Prefix for the operation ID
        include_timestamp: Whether to include timestamp in the ID
        
    Returns:
        str: Unique operation ID
    """
    base_id = str(uuid.uuid4())[:8]
    
    if include_timestamp:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"{prefix}_{timestamp}_{base_id}"
    else:
        return f"{prefix}_{base_id}"

def format_timestamp(timestamp: Optional[Union[str, float, datetime]] = None, 
                    format_type: str = "iso") -> str:
    """
    Format timestamp in various formats.
    
    Args:
        timestamp: Timestamp to format (defaults to current time)
        format_type: Format type ('iso', 'readable', 'unix', 'custom')
        
    Returns:
        str: Formatted timestamp
    """
    if timestamp is None:
        dt = datetime.now(timezone.utc)
    elif isinstance(timestamp, str):
        try:
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        except ValueError:
            dt = datetime.now(timezone.utc)
    elif isinstance(timestamp, (int, float)):
        dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
    elif isinstance(timestamp, datetime):
        dt = timestamp
    else:
        dt = datetime.now(timezone.utc)
    
    if format_type == "iso":
        return dt.isoformat()
    elif format_type == "readable":
        return dt.strftime("%Y-%m-%d %H:%M:%S UTC")
    elif format_type == "unix":
        return str(int(dt.timestamp()))
    elif format_type == "custom":
        return dt.strftime("%Y%m%d_%H%M%S")
    else:
        return dt.isoformat()

def create_context_summary(context: Dict[str, Any], max_length: int = 500) -> str:
    """
    Create a summary of operation context.
    
    Args:
        context: Operation context dictionary
        max_length: Maximum length of summary
        
    Returns:
        str: Context summary
    """
    summary_parts = []
    
    # Add key context information
    if "operation_type" in context:
        summary_parts.append(f"Operation: {context['operation_type']}")
    
    if "user_id" in context:
        summary_parts.append(f"User: {context['user_id']}")
    
    if "timestamp" in context:
        formatted_time = format_timestamp(context['timestamp'], "readable")
        summary_parts.append(f"Time: {formatted_time}")
    
    if "priority" in context:
        summary_parts.append(f"Priority: {context['priority']}")
    
    # Add additional context if available
    additional_info = []
    for key, value in context.items():
        if key not in ["operation_type", "user_id", "timestamp", "priority"]:
            if isinstance(value, (str, int, float, bool)):
                additional_info.append(f"{key}: {value}")
            elif isinstance(value, (list, dict)) and len(str(value)) < 100:
                additional_info.append(f"{key}: {value}")
    
    if additional_info:
        summary_parts.append("Additional: " + ", ".join(additional_info[:3]))
    
    summary = " | ".join(summary_parts)
    
    # Truncate if too long
    if len(summary) > max_length:
        summary = summary[:max_length-3] + "..."
    
    return summary

def generate_hash(data: Union[str, Dict, List], algorithm: str = "sha256") -> str:
    """
    Generate hash for data using secure algorithms only.
    
    Args:
        data: Data to hash
        algorithm: Hash algorithm ('sha256', 'sha512', 'blake2b', 'blake2s')
        
    Returns:
        str: Hash string
        
    Note:
        Only secure hash algorithms are supported for BFSI security requirements.
        MD5 and SHA1 are not supported due to security vulnerabilities.
    """
    if isinstance(data, (dict, list)):
        data_str = json.dumps(data, sort_keys=True)
    else:
        data_str = str(data)
    
    data_bytes = data_str.encode('utf-8')
    
    if algorithm == "sha256":
        return hashlib.sha256(data_bytes).hexdigest()
    elif algorithm == "sha512":
        return hashlib.sha512(data_bytes).hexdigest()
    elif algorithm == "blake2b":
        return hashlib.blake2b(data_bytes).hexdigest()
    elif algorithm == "blake2s":
        return hashlib.blake2s(data_bytes).hexdigest()
    else:
        # Default to SHA256 for security
        logger.warning(f"Unsupported algorithm '{algorithm}', using SHA256")
        return hashlib.sha256(data_bytes).hexdigest()

def safe_json_serialize(data: Any, default: str = "Unable to serialize") -> str:
    """
    Safely serialize data to JSON string.
    
    Args:
        data: Data to serialize
        default: Default value for non-serializable data
        
    Returns:
        str: JSON string
    """
    try:
        return json.dumps(data, default=str, indent=2)
    except (TypeError, ValueError) as e:
        logger.warning(f"Failed to serialize data: {e}")
        return json.dumps({"error": default, "original_type": str(type(data))})

def extract_key_value_pairs(data: Dict[str, Any], 
                           key_patterns: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Extract key-value pairs from dictionary based on patterns.
    
    Args:
        data: Dictionary to extract from
        key_patterns: List of key patterns to match (None for all keys)
        
    Returns:
        Dict: Extracted key-value pairs
    """
    if key_patterns is None:
        return data.copy()
    
    extracted = {}
    for pattern in key_patterns:
        for key, value in data.items():
            if pattern.lower() in key.lower():
                extracted[key] = value
    
    return extracted

def merge_dictionaries(*dicts: Dict[str, Any], 
                      overwrite: bool = True) -> Dict[str, Any]:
    """
    Merge multiple dictionaries.
    
    Args:
        *dicts: Dictionaries to merge
        overwrite: Whether to overwrite existing keys
        
    Returns:
        Dict: Merged dictionary
    """
    if not dicts:
        return {}
    
    result = dicts[0].copy()
    
    for d in dicts[1:]:
        for key, value in d.items():
            if overwrite or key not in result:
                result[key] = value
    
    return result

def validate_data_structure(data: Any, expected_structure: Dict[str, type]) -> bool:
    """
    Validate data structure against expected types.
    
    Args:
        data: Data to validate
        expected_structure: Dictionary mapping keys to expected types
        
    Returns:
        bool: True if structure is valid
    """
    if not isinstance(data, dict):
        return False
    
    for key, expected_type in expected_structure.items():
        if key not in data:
            logger.warning(f"Missing required key: {key}")
            return False
        
        if not isinstance(data[key], expected_type):
            logger.warning(f"Key '{key}' has wrong type. Expected {expected_type}, got {type(data[key])}")
            return False
    
    return True

def create_operation_log(operation_id: str, 
                        operation_type: str,
                        status: str,
                        details: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Create a standardized operation log entry.
    
    Args:
        operation_id: Unique operation identifier
        operation_type: Type of operation
        status: Operation status
        details: Additional operation details
        
    Returns:
        Dict: Operation log entry
    """
    log_entry = {
        "operation_id": operation_id,
        "operation_type": operation_type,
        "status": status,
        "timestamp": format_timestamp(),
        "details": details or {}
    }
    
    return log_entry

def sanitize_string(text: str, max_length: int = 1000) -> str:
    """
    Sanitize string for safe storage/display.
    
    Args:
        text: Text to sanitize
        max_length: Maximum length of sanitized text
        
    Returns:
        str: Sanitized text
    """
    if not isinstance(text, str):
        text = str(text)
    
    # Remove or replace potentially problematic characters
    sanitized = text.replace('\x00', '').replace('\r', '').replace('\n', ' ')
    
    # Truncate if too long
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length-3] + "..."
    
    return sanitized.strip()

def create_batch_operation_id(batch_size: int, prefix: str = "batch") -> List[str]:
    """
    Create a list of operation IDs for batch operations.
    
    Args:
        batch_size: Number of operation IDs to generate
        prefix: Prefix for operation IDs
        
    Returns:
        List[str]: List of operation IDs
    """
    return [generate_operation_id(prefix) for _ in range(batch_size)]
