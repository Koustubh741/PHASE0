"""
ML-Enhanced AI API Endpoints
RESTful API endpoints for machine learning enhanced AI services
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

from ...core.application.services.ml_enhanced_ai_service import (
    MLEnhancedAIService,
    MLModelType,
    ModelStatus,
    PredictionConfidence
)
from ...core.application.dto.ml_ai_dto import (
    ModelResponse,
    PredictionRequest,
    PredictionResponse,
    TrainingJobRequest,
    TrainingJobResponse,
    FeatureImportanceResponse,
    ModelPerformanceResponse,
    MLMetricsResponse
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/ml-ai", tags=["ML-Enhanced AI"])

# Global service instance
ml_ai_service = MLEnhancedAIService()

@router.get("/models", response_model=List[ModelResponse])
async def get_ml_models():
    """Get all ML models"""
    try:
        models = ml_ai_service.get_models()
        return models
    except Exception as e:
        logger.error(f"Error getting ML models: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/models/{model_id}", response_model=ModelResponse)
async def get_ml_model(model_id: str):
    """Get specific ML model"""
    try:
        models = ml_ai_service.get_models()
        model = next((m for m in models if m["model_id"] == model_id), None)
        
        if not model:
            raise HTTPException(status_code=404, detail="Model not found")
        
        return model
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting ML model: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/models/train", response_model=TrainingJobResponse)
async def train_model(request: TrainingJobRequest):
    """Train a new ML model"""
    try:
        model_id = await ml_ai_service.train_model(
            model_name=request.model_name,
            model_type=MLModelType(request.model_type),
            training_data=request.training_data,
            hyperparameters=request.hyperparameters
        )
        
        return TrainingJobResponse(
            job_id=str(uuid.uuid4()),
            model_id=model_id,
            model_name=request.model_name,
            model_type=request.model_type,
            status="training",
            progress=0.0,
            start_time=datetime.utcnow(),
            hyperparameters=request.hyperparameters
        )
    except Exception as e:
        logger.error(f"Error training model: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/models/{model_id}/predict", response_model=PredictionResponse)
async def make_prediction(model_id: str, request: PredictionRequest):
    """Make a prediction using an ML model"""
    try:
        prediction = await ml_ai_service.predict(model_id, request.input_data)
        
        return PredictionResponse(
            prediction_id=prediction.prediction_id,
            model_id=prediction.model_id,
            input_data=prediction.input_data,
            prediction=prediction.prediction,
            confidence=prediction.confidence,
            confidence_level=prediction.confidence_level.value,
            probability_scores=prediction.probability_scores,
            feature_importance=prediction.feature_importance,
            timestamp=prediction.timestamp,
            processing_time=prediction.processing_time,
            metadata=prediction.metadata
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error making prediction: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/models/{model_id}/batch-predict")
async def batch_predict(model_id: str, batch_data: List[Dict[str, Any]]):
    """Make batch predictions"""
    try:
        predictions = await ml_ai_service.batch_predict(model_id, batch_data)
        return [asdict(prediction) for prediction in predictions]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error making batch predictions: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/models/{model_id}/performance", response_model=ModelPerformanceResponse)
async def get_model_performance(model_id: str):
    """Get model performance metrics"""
    try:
        performance = ml_ai_service.get_model_performance(model_id)
        return performance
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error getting model performance: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/models/{model_id}/feature-importance", response_model=List[FeatureImportanceResponse])
async def get_feature_importance(model_id: str):
    """Get feature importance for a model"""
    try:
        feature_importance = ml_ai_service.get_feature_importance(model_id)
        return [asdict(feature) for feature in feature_importance]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error getting feature importance: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/models/{model_id}/deploy")
async def deploy_model(model_id: str):
    """Deploy a model for predictions"""
    try:
        success = await ml_ai_service.deploy_model(model_id)
        if success:
            return {"message": "Model deployed successfully"}
        else:
            raise HTTPException(status_code=400, detail="Failed to deploy model")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error deploying model: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/models/{model_id}/retire")
async def retire_model(model_id: str):
    """Retire a model"""
    try:
        success = await ml_ai_service.retire_model(model_id)
        if success:
            return {"message": "Model retired successfully"}
        else:
            raise HTTPException(status_code=400, detail="Failed to retire model")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error retiring model: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/predictions", response_model=List[PredictionResponse])
async def get_predictions(model_id: Optional[str] = None):
    """Get predictions"""
    try:
        predictions = ml_ai_service.get_predictions(model_id)
        return predictions
    except Exception as e:
        logger.error(f"Error getting predictions: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/training-jobs", response_model=List[TrainingJobResponse])
async def get_training_jobs():
    """Get training jobs"""
    try:
        jobs = ml_ai_service.get_training_jobs()
        return jobs
    except Exception as e:
        logger.error(f"Error getting training jobs: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/metrics", response_model=MLMetricsResponse)
async def get_ml_metrics():
    """Get ML performance metrics"""
    try:
        metrics = ml_ai_service.get_performance_metrics()
        return metrics
    except Exception as e:
        logger.error(f"Error getting ML metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        metrics = ml_ai_service.get_performance_metrics()
        return {
            "status": "healthy",
            "service": "ml-enhanced-ai",
            "version": "2.0.0",
            "models_loaded": metrics["total_models"],
            "active_models": metrics["active_models"],
            "total_predictions": metrics["total_predictions"],
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "service": "ml-enhanced-ai",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
        )
