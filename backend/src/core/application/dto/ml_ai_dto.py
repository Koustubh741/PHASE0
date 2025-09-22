"""
ML-Enhanced AI Data Transfer Objects
DTOs for machine learning enhanced AI operations
"""

from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum


class MLModelType(str, Enum):
    """ML model type enumeration"""
    CLASSIFICATION = "classification"
    REGRESSION = "regression"
    CLUSTERING = "clustering"
    ANOMALY_DETECTION = "anomaly_detection"
    TIME_SERIES = "time_series"
    NLP = "nlp"
    RECOMMENDATION = "recommendation"


class ModelStatus(str, Enum):
    """Model status enumeration"""
    TRAINING = "training"
    TRAINED = "trained"
    DEPLOYED = "deployed"
    RETIRING = "retiring"
    RETIRED = "retired"
    FAILED = "failed"


class PredictionConfidence(str, Enum):
    """Prediction confidence enumeration"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"


class ModelResponse(BaseModel):
    """ML model response"""
    model_id: str = Field(..., description="Model ID")
    name: str = Field(..., description="Model name")
    model_type: str = Field(..., description="Model type")
    version: str = Field(..., description="Model version")
    status: str = Field(..., description="Model status")
    accuracy: float = Field(..., description="Model accuracy")
    precision: float = Field(..., description="Model precision")
    recall: float = Field(..., description="Model recall")
    f1_score: float = Field(..., description="Model F1 score")
    created_at: datetime = Field(..., description="Creation timestamp")
    last_trained: datetime = Field(..., description="Last training timestamp")
    last_prediction: Optional[datetime] = Field(None, description="Last prediction timestamp")
    training_data_size: int = Field(..., description="Training data size")
    features: List[str] = Field(..., description="Model features")
    hyperparameters: Dict[str, Any] = Field(..., description="Model hyperparameters")
    performance_metrics: Dict[str, Any] = Field(..., description="Performance metrics")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    
    class Config:
        json_schema_extra = {
            "example": {
                "model_id": "123e4567-e89b-12d3-a456-426614174000",
                "name": "Risk Assessment Classifier",
                "model_type": "classification",
                "version": "1.0.0",
                "status": "deployed",
                "accuracy": 0.92,
                "precision": 0.89,
                "recall": 0.91,
                "f1_score": 0.90,
                "created_at": "2024-01-15T10:30:00Z",
                "last_trained": "2024-01-15T10:30:00Z",
                "last_prediction": "2024-01-15T11:30:00Z",
                "training_data_size": 10000,
                "features": ["credit_score", "debt_ratio", "income_stability"],
                "hyperparameters": {"n_estimators": 100, "max_depth": 10},
                "performance_metrics": {"auc": 0.94, "log_loss": 0.25},
                "metadata": {"domain": "risk_assessment"}
            }
        }


class PredictionRequest(BaseModel):
    """Request to make a prediction"""
    input_data: Dict[str, Any] = Field(..., description="Input data for prediction")
    
    class Config:
        json_schema_extra = {
            "example": {
                "input_data": {
                    "credit_score": 750,
                    "debt_ratio": 0.3,
                    "income_stability": 0.8,
                    "employment_history": 5
                }
            }
        }


class PredictionResponse(BaseModel):
    """ML prediction response"""
    prediction_id: str = Field(..., description="Prediction ID")
    model_id: str = Field(..., description="Model ID")
    input_data: Dict[str, Any] = Field(..., description="Input data")
    prediction: Any = Field(..., description="Prediction result")
    confidence: float = Field(..., description="Prediction confidence")
    confidence_level: str = Field(..., description="Confidence level")
    probability_scores: Dict[str, float] = Field(..., description="Probability scores")
    feature_importance: Dict[str, float] = Field(..., description="Feature importance")
    timestamp: datetime = Field(..., description="Prediction timestamp")
    processing_time: float = Field(..., description="Processing time in seconds")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    
    class Config:
        json_schema_extra = {
            "example": {
                "prediction_id": "456e7890-e89b-12d3-a456-426614174000",
                "model_id": "123e4567-e89b-12d3-a456-426614174000",
                "input_data": {"credit_score": 750, "debt_ratio": 0.3},
                "prediction": "low_risk",
                "confidence": 0.92,
                "confidence_level": "high",
                "probability_scores": {"low_risk": 0.85, "medium_risk": 0.12, "high_risk": 0.03},
                "feature_importance": {"credit_score": 0.45, "debt_ratio": 0.35},
                "timestamp": "2024-01-15T11:30:00Z",
                "processing_time": 0.15,
                "metadata": {"model_version": "1.0.0"}
            }
        }


class TrainingJobRequest(BaseModel):
    """Request to train a model"""
    model_name: str = Field(..., description="Model name")
    model_type: str = Field(..., description="Model type")
    training_data: Dict[str, Any] = Field(..., description="Training data")
    hyperparameters: Dict[str, Any] = Field(default_factory=dict, description="Model hyperparameters")
    
    class Config:
        json_schema_extra = {
            "example": {
                "model_name": "Fraud Detection Model",
                "model_type": "classification",
                "training_data": {
                    "features": [[1, 2, 3], [4, 5, 6]],
                    "labels": [0, 1],
                    "feature_names": ["amount", "frequency", "location"]
                },
                "hyperparameters": {"n_estimators": 100, "max_depth": 10}
            }
        }


class TrainingJobResponse(BaseModel):
    """Training job response"""
    job_id: str = Field(..., description="Job ID")
    model_id: str = Field(..., description="Model ID")
    model_name: str = Field(..., description="Model name")
    model_type: str = Field(..., description="Model type")
    status: str = Field(..., description="Job status")
    progress: float = Field(..., description="Training progress")
    start_time: datetime = Field(..., description="Start time")
    end_time: Optional[datetime] = Field(None, description="End time")
    hyperparameters: Dict[str, Any] = Field(..., description="Hyperparameters")
    metrics: Dict[str, Any] = Field(default_factory=dict, description="Training metrics")
    error_message: Optional[str] = Field(None, description="Error message")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    
    class Config:
        json_schema_extra = {
            "example": {
                "job_id": "789e0123-e89b-12d3-a456-426614174000",
                "model_id": "123e4567-e89b-12d3-a456-426614174000",
                "model_name": "Fraud Detection Model",
                "model_type": "classification",
                "status": "training",
                "progress": 0.5,
                "start_time": "2024-01-15T10:30:00Z",
                "end_time": None,
                "hyperparameters": {"n_estimators": 100, "max_depth": 10},
                "metrics": {},
                "error_message": None,
                "metadata": {}
            }
        }


class FeatureImportanceResponse(BaseModel):
    """Feature importance response"""
    feature_name: str = Field(..., description="Feature name")
    importance_score: float = Field(..., description="Importance score")
    rank: int = Field(..., description="Feature rank")
    category: str = Field(..., description="Feature category")
    description: str = Field(..., description="Feature description")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    
    class Config:
        json_schema_extra = {
            "example": {
                "feature_name": "credit_score",
                "importance_score": 0.45,
                "rank": 1,
                "category": "input",
                "description": "Importance of credit_score for predictions",
                "metadata": {"model_id": "123e4567-e89b-12d3-a456-426614174000"}
            }
        }


class ModelPerformanceResponse(BaseModel):
    """Model performance response"""
    model_id: str = Field(..., description="Model ID")
    name: str = Field(..., description="Model name")
    version: str = Field(..., description="Model version")
    status: str = Field(..., description="Model status")
    accuracy: float = Field(..., description="Model accuracy")
    precision: float = Field(..., description="Model precision")
    recall: float = Field(..., description="Model recall")
    f1_score: float = Field(..., description="Model F1 score")
    total_predictions: int = Field(..., description="Total predictions")
    average_confidence: float = Field(..., description="Average confidence")
    last_prediction: Optional[str] = Field(None, description="Last prediction timestamp")
    performance_metrics: Dict[str, Any] = Field(..., description="Performance metrics")
    
    class Config:
        json_schema_extra = {
            "example": {
                "model_id": "123e4567-e89b-12d3-a456-426614174000",
                "name": "Risk Assessment Classifier",
                "version": "1.0.0",
                "status": "deployed",
                "accuracy": 0.92,
                "precision": 0.89,
                "recall": 0.91,
                "f1_score": 0.90,
                "total_predictions": 150,
                "average_confidence": 0.88,
                "last_prediction": "2024-01-15T11:30:00Z",
                "performance_metrics": {"auc": 0.94, "log_loss": 0.25}
            }
        }


class MLMetricsResponse(BaseModel):
    """ML performance metrics response"""
    total_models: int = Field(..., description="Total models")
    active_models: int = Field(..., description="Active models")
    total_predictions: int = Field(..., description="Total predictions")
    average_accuracy: float = Field(..., description="Average accuracy")
    training_jobs_completed: int = Field(..., description="Training jobs completed")
    prediction_latency: float = Field(..., description="Prediction latency")
    deployed_models: int = Field(..., description="Deployed models")
    training_jobs_running: int = Field(..., description="Training jobs running")
    last_updated: str = Field(..., description="Last update timestamp")
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_models": 5,
                "active_models": 3,
                "total_predictions": 1250,
                "average_accuracy": 0.89,
                "training_jobs_completed": 8,
                "prediction_latency": 0.15,
                "deployed_models": 3,
                "training_jobs_running": 1,
                "last_updated": "2024-01-15T10:30:00Z"
            }
        }
