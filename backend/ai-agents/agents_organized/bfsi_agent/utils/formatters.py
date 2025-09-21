"""
BFSI Agent Formatting Utilities
===============================

This module provides formatting and transformation utilities for BFSI agent operations.
"""

import json
from typing import Any, Dict, List, Optional, Union
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def format_reasoning_result(reasoning_data: Dict[str, Any], format_type: str = "standard") -> Dict[str, Any]:
    """
    Format reasoning result for display or storage.
    
    Args:
        reasoning_data: Raw reasoning data
        format_type: Output format type ('standard', 'detailed', 'summary')
        
    Returns:
        Dict: Formatted reasoning result
    """
    base_result = {
        "reasoning_id": reasoning_data.get("reasoning_id", "unknown"),
        "timestamp": datetime.now().isoformat(),
        "status": reasoning_data.get("status", "completed"),
        "confidence_score": reasoning_data.get("confidence_score", 0.0)
    }
    
    if format_type == "standard":
        return {
            **base_result,
            "conclusion": reasoning_data.get("conclusion", ""),
            "key_factors": reasoning_data.get("key_factors", []),
            "recommendations": reasoning_data.get("recommendations", [])
        }
    
    elif format_type == "detailed":
        return {
            **base_result,
            "conclusion": reasoning_data.get("conclusion", ""),
            "key_factors": reasoning_data.get("key_factors", []),
            "recommendations": reasoning_data.get("recommendations", []),
            "reasoning_steps": reasoning_data.get("reasoning_steps", []),
            "evidence": reasoning_data.get("evidence", []),
            "assumptions": reasoning_data.get("assumptions", []),
            "limitations": reasoning_data.get("limitations", [])
        }
    
    elif format_type == "summary":
        return {
            "reasoning_id": base_result["reasoning_id"],
            "timestamp": base_result["timestamp"],
            "conclusion": reasoning_data.get("conclusion", ""),
            "confidence": base_result["confidence_score"]
        }
    
    return base_result

def format_decision_result(decision_data: Dict[str, Any], include_rationale: bool = True) -> Dict[str, Any]:
    """
    Format decision result for display or storage.
    
    Args:
        decision_data: Raw decision data
        include_rationale: Whether to include decision rationale
        
    Returns:
        Dict: Formatted decision result
    """
    formatted_result = {
        "decision_id": decision_data.get("decision_id", "unknown"),
        "timestamp": datetime.now().isoformat(),
        "decision": decision_data.get("decision", ""),
        "decision_type": decision_data.get("decision_type", "unknown"),
        "confidence": decision_data.get("confidence", 0.0),
        "status": decision_data.get("status", "completed")
    }
    
    if include_rationale:
        formatted_result.update({
            "rationale": decision_data.get("rationale", ""),
            "factors_considered": decision_data.get("factors_considered", []),
            "risk_assessment": decision_data.get("risk_assessment", {}),
            "compliance_check": decision_data.get("compliance_check", {})
        })
    
    return formatted_result

def format_ml_prediction(prediction_data: Dict[str, Any], format_type: str = "standard") -> Dict[str, Any]:
    """
    Format ML prediction result.
    
    Args:
        prediction_data: Raw prediction data
        format_type: Output format type ('standard', 'detailed', 'technical')
        
    Returns:
        Dict: Formatted prediction result
    """
    base_result = {
        "prediction_id": prediction_data.get("prediction_id", "unknown"),
        "timestamp": datetime.now().isoformat(),
        "model_name": prediction_data.get("model_name", "unknown"),
        "prediction": prediction_data.get("prediction", None),
        "confidence": prediction_data.get("confidence", 0.0),
        "model_version": prediction_data.get("model_version", "1.0")
    }
    
    if format_type == "standard":
        return base_result
    
    elif format_type == "detailed":
        return {
            **base_result,
            "feature_importance": prediction_data.get("feature_importance", {}),
            "prediction_probability": prediction_data.get("prediction_probability", {}),
            "model_metadata": prediction_data.get("model_metadata", {}),
            "data_quality_score": prediction_data.get("data_quality_score", 0.0)
        }
    
    elif format_type == "technical":
        return {
            **base_result,
            "feature_importance": prediction_data.get("feature_importance", {}),
            "prediction_probability": prediction_data.get("prediction_probability", {}),
            "model_metadata": prediction_data.get("model_metadata", {}),
            "data_quality_score": prediction_data.get("data_quality_score", 0.0),
            "model_parameters": prediction_data.get("model_parameters", {}),
            "training_metrics": prediction_data.get("training_metrics", {}),
            "validation_metrics": prediction_data.get("validation_metrics", {})
        }
    
    return base_result

def format_financial_data(financial_data: Dict[str, Any], currency: str = "USD") -> Dict[str, Any]:
    """
    Format financial data for display.
    
    Args:
        financial_data: Raw financial data
        currency: Target currency for formatting
        
    Returns:
        Dict: Formatted financial data
    """
    formatted_data = {
        "transaction_id": financial_data.get("transaction_id", "unknown"),
        "timestamp": datetime.now().isoformat(),
        "amount": financial_data.get("amount", 0.0),
        "currency": currency,
        "transaction_type": financial_data.get("transaction_type", "unknown"),
        "status": financial_data.get("status", "pending")
    }
    
    # Format amount with currency symbol
    if currency == "USD":
        formatted_data["formatted_amount"] = f"${financial_data.get('amount', 0.0):,.2f}"
    elif currency == "EUR":
        formatted_data["formatted_amount"] = f"€{financial_data.get('amount', 0.0):,.2f}"
    else:
        formatted_data["formatted_amount"] = f"{financial_data.get('amount', 0.0):,.2f} {currency}"
    
    return formatted_data

def format_risk_assessment(risk_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Format risk assessment data.
    
    Args:
        risk_data: Raw risk assessment data
        
    Returns:
        Dict: Formatted risk assessment
    """
    risk_level = risk_data.get("risk_level", "unknown")
    risk_color = {
        "low": "green",
        "medium": "yellow", 
        "high": "orange",
        "critical": "red"
    }.get(risk_level, "gray")
    
    return {
        "assessment_id": risk_data.get("assessment_id", "unknown"),
        "timestamp": datetime.now().isoformat(),
        "risk_level": risk_level,
        "risk_color": risk_color,
        "risk_category": risk_data.get("risk_category", "unknown"),
        "risk_score": risk_data.get("risk_score", 0.0),
        "description": risk_data.get("description", ""),
        "mitigation_actions": risk_data.get("mitigation_actions", []),
        "assessor": risk_data.get("assessor", "unknown")
    }

def format_compliance_report(compliance_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Format compliance report data.
    
    Args:
        compliance_data: Raw compliance data
        
    Returns:
        Dict: Formatted compliance report
    """
    compliance_status = compliance_data.get("compliance_status", "unknown")
    status_color = {
        "compliant": "green",
        "non_compliant": "red",
        "partially_compliant": "yellow",
        "under_review": "blue"
    }.get(compliance_status, "gray")
    
    return {
        "report_id": compliance_data.get("report_id", "unknown"),
        "timestamp": datetime.now().isoformat(),
        "compliance_status": compliance_status,
        "status_color": status_color,
        "regulation": compliance_data.get("regulation", "unknown"),
        "compliance_score": compliance_data.get("compliance_score", 0.0),
        "violations": compliance_data.get("violations", []),
        "recommendations": compliance_data.get("recommendations", []),
        "next_review_date": compliance_data.get("next_review_date", ""),
        "reviewer": compliance_data.get("reviewer", "unknown")
    }

def format_json_output(data: Any, indent: int = 2) -> str:
    """
    Format data as JSON string.
    
    Args:
        data: Data to format
        indent: JSON indentation
        
    Returns:
        str: Formatted JSON string
    """
    try:
        return json.dumps(data, indent=indent, default=str)
    except (TypeError, ValueError) as e:
        logger.error(f"Error formatting JSON: {e}")
        return json.dumps({"error": "Failed to format data as JSON"})
