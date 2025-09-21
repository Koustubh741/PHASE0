"""
BFSI Agent Validation Utilities
===============================

This module provides validation functions for BFSI agent operations.
"""

import re
from typing import Any, Dict, List, Optional, Union
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def validate_operation_context(context: Dict[str, Any]) -> bool:
    """
    Validate operation context for BFSI operations.
    
    Args:
        context: Operation context dictionary
        
    Returns:
        bool: True if valid, False otherwise
    """
    required_fields = ['operation_type', 'timestamp', 'user_id']
    
    for field in required_fields:
        if field not in context:
            logger.error(f"Missing required field: {field}")
            return False
    
    # Validate operation_type
    valid_operation_types = [
        'risk_assessment', 'compliance_check', 'policy_review',
        'transaction_analysis', 'fraud_detection', 'regulatory_reporting'
    ]
    
    if context['operation_type'] not in valid_operation_types:
        logger.error(f"Invalid operation type: {context['operation_type']}")
        return False
    
    # Validate timestamp format
    try:
        if isinstance(context['timestamp'], str):
            datetime.fromisoformat(context['timestamp'].replace('Z', '+00:00'))
        elif not isinstance(context['timestamp'], (int, float)):
            logger.error("Invalid timestamp format")
            return False
    except ValueError:
        logger.error("Invalid timestamp format")
        return False
    
    return True

def validate_reasoning_input(reasoning_data: Dict[str, Any]) -> bool:
    """
    Validate reasoning input data.
    
    Args:
        reasoning_data: Reasoning input dictionary
        
    Returns:
        bool: True if valid, False otherwise
    """
    required_fields = ['input_data', 'reasoning_type', 'context']
    
    for field in required_fields:
        if field not in reasoning_data:
            logger.error(f"Missing required reasoning field: {field}")
            return False
    
    # Validate reasoning_type
    valid_reasoning_types = [
        'logical_analysis', 'risk_evaluation', 'compliance_assessment',
        'pattern_recognition', 'anomaly_detection', 'decision_support'
    ]
    
    if reasoning_data['reasoning_type'] not in valid_reasoning_types:
        logger.error(f"Invalid reasoning type: {reasoning_data['reasoning_type']}")
        return False
    
    # Validate input_data is not empty
    if not reasoning_data['input_data']:
        logger.error("Input data cannot be empty")
        return False
    
    return True

def validate_ml_data(ml_data: Dict[str, Any]) -> bool:
    """
    Validate machine learning data structure.
    
    Args:
        ml_data: ML data dictionary
        
    Returns:
        bool: True if valid, False otherwise
    """
    required_fields = ['features', 'target', 'model_type']
    
    for field in required_fields:
        if field not in ml_data:
            logger.error(f"Missing required ML field: {field}")
            return False
    
    # Validate features
    if not isinstance(ml_data['features'], (list, dict)):
        logger.error("Features must be a list or dictionary")
        return False
    
    # Validate model_type
    valid_model_types = [
        'classification', 'regression', 'clustering', 'anomaly_detection',
        'time_series', 'nlp', 'recommendation'
    ]
    
    if ml_data['model_type'] not in valid_model_types:
        logger.error(f"Invalid model type: {ml_data['model_type']}")
        return False
    
    return True

def validate_financial_data(data: Dict[str, Any]) -> bool:
    """
    Validate financial data structure.
    
    Args:
        data: Financial data dictionary
        
    Returns:
        bool: True if valid, False otherwise
    """
    required_fields = ['amount', 'currency', 'transaction_type', 'timestamp']
    
    for field in required_fields:
        if field not in data:
            logger.error(f"Missing required financial field: {field}")
            return False
    
    # Validate amount is numeric
    try:
        amount = float(data['amount'])
        if amount < 0:
            logger.error("Amount cannot be negative")
            return False
    except (ValueError, TypeError):
        logger.error("Invalid amount format")
        return False
    
    # Validate currency code
    currency_pattern = r'^[A-Z]{3}$'
    if not re.match(currency_pattern, data['currency']):
        logger.error("Invalid currency code format")
        return False
    
    # Validate transaction_type
    valid_transaction_types = [
        'deposit', 'withdrawal', 'transfer', 'payment', 'refund',
        'fee', 'interest', 'dividend', 'loan', 'investment',
        'purchase', 'sale', 'exchange', 'adjustment'
    ]
    
    if data['transaction_type'] not in valid_transaction_types:
        logger.error(f"Invalid transaction type: {data['transaction_type']}")
        return False
    
    # Validate timestamp
    try:
        timestamp = data['timestamp']
        if isinstance(timestamp, str):
            # Try to parse ISO format
            datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        elif isinstance(timestamp, (int, float)):
            # Validate timestamp
            datetime.fromtimestamp(timestamp)
        else:
            logger.error("Invalid timestamp format")
            return False
    except (ValueError, TypeError, OSError) as e:
        logger.error(f"Invalid timestamp: {e}")
        return False
    
    return True

def validate_risk_assessment_data(risk_data: Dict[str, Any]) -> bool:
    """
    Validate risk assessment data.
    
    Args:
        risk_data: Risk assessment data dictionary
        
    Returns:
        bool: True if valid, False otherwise
    """
    required_fields = ['risk_level', 'risk_category', 'assessment_date', 'assessor_id']
    
    for field in required_fields:
        if field not in risk_data:
            logger.error(f"Missing required risk field: {field}")
            return False
    
    # Validate risk_level
    valid_risk_levels = ['low', 'medium', 'high', 'critical']
    if risk_data['risk_level'] not in valid_risk_levels:
        logger.error(f"Invalid risk level: {risk_data['risk_level']}")
        return False
    
    # Validate risk_category
    valid_categories = [
        'credit_risk', 'market_risk', 'operational_risk', 'liquidity_risk',
        'compliance_risk', 'reputational_risk', 'cyber_risk'
    ]
    
    if risk_data['risk_category'] not in valid_categories:
        logger.error(f"Invalid risk category: {risk_data['risk_category']}")
        return False
    
    # Validate assessment_date
    try:
        assessment_date = risk_data['assessment_date']
        if isinstance(assessment_date, str):
            # Try to parse ISO format
            datetime.fromisoformat(assessment_date.replace('Z', '+00:00'))
        elif isinstance(assessment_date, (int, float)):
            # Validate timestamp
            datetime.fromtimestamp(assessment_date)
        else:
            logger.error("Invalid assessment_date format")
            return False
    except (ValueError, TypeError, OSError) as e:
        logger.error(f"Invalid assessment_date: {e}")
        return False
    
    # Validate assessor_id
    assessor_id = risk_data['assessor_id']
    if not isinstance(assessor_id, str) or not assessor_id.strip():
        logger.error("assessor_id must be a non-empty string")
        return False
    
    # Check if assessor_id is alphanumeric (basic validation)
    if not assessor_id.replace('_', '').replace('-', '').isalnum():
        logger.error("assessor_id must be alphanumeric (with optional underscores and hyphens)")
        return False
    
    return True
