"""
Real-time Monitoring API Endpoints
RESTful API endpoints for monitoring and alerting system
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

from ...core.application.services.monitoring_service import (
    RealTimeMonitoringService,
    Alert,
    Metric,
    HealthCheck,
    AlertSeverity,
    AlertStatus,
    MetricType
)
from ...core.application.dto.monitoring_dto import (
    AlertResponse,
    MetricResponse,
    HealthCheckResponse,
    MonitoringMetricsResponse,
    AlertCreateRequest,
    AlertUpdateRequest
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/monitoring", tags=["Real-time Monitoring"])

# Global service instance
monitoring_service = RealTimeMonitoringService()

@router.on_event("startup")
async def startup_event():
    """Initialize monitoring service on startup"""
    monitoring_service.start_monitoring()
    logger.info("Real-time monitoring service started")

@router.on_event("shutdown")
async def shutdown_event():
    """Stop monitoring service on shutdown"""
    monitoring_service.stop_monitoring()
    logger.info("Real-time monitoring service stopped")

@router.get("/metrics", response_model=List[MetricResponse])
async def get_metrics(metric_name: Optional[str] = None):
    """Get system metrics"""
    try:
        metrics = monitoring_service.get_metrics(metric_name)
        return [MetricResponse(
            metric_id=metric.metric_id,
            name=metric.name,
            value=metric.value,
            metric_type=metric.metric_type.value,
            labels=metric.labels,
            timestamp=metric.timestamp,
            metadata=metric.metadata
        ) for metric in metrics.values()]
    except Exception as e:
        logger.error(f"Error getting metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/alerts", response_model=List[AlertResponse])
async def get_alerts(status: Optional[AlertStatus] = None):
    """Get alerts"""
    try:
        alerts = monitoring_service.get_alerts(status)
        return [AlertResponse(
            alert_id=alert.alert_id,
            title=alert.title,
            description=alert.description,
            severity=alert.severity.value,
            status=alert.status.value,
            source=alert.source,
            metric_name=alert.metric_name,
            threshold_value=alert.threshold_value,
            current_value=alert.current_value,
            created_at=alert.created_at,
            updated_at=alert.updated_at,
            acknowledged_by=alert.acknowledged_by,
            resolved_at=alert.resolved_at,
            metadata=alert.metadata
        ) for alert in alerts.values()]
    except Exception as e:
        logger.error(f"Error getting alerts: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/alerts/{alert_id}", response_model=AlertResponse)
async def get_alert(alert_id: str):
    """Get specific alert"""
    try:
        alerts = monitoring_service.get_alerts()
        alert = alerts.get(alert_id)
        
        if not alert:
            raise HTTPException(status_code=404, detail="Alert not found")
        
        return AlertResponse(
            alert_id=alert.alert_id,
            title=alert.title,
            description=alert.description,
            severity=alert.severity.value,
            status=alert.status.value,
            source=alert.source,
            metric_name=alert.metric_name,
            threshold_value=alert.threshold_value,
            current_value=alert.current_value,
            created_at=alert.created_at,
            updated_at=alert.updated_at,
            acknowledged_by=alert.acknowledged_by,
            resolved_at=alert.resolved_at,
            metadata=alert.metadata
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting alert: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/alerts/{alert_id}/acknowledge")
async def acknowledge_alert(alert_id: str, user_id: str):
    """Acknowledge an alert"""
    try:
        success = monitoring_service.acknowledge_alert(alert_id, user_id)
        if not success:
            raise HTTPException(status_code=404, detail="Alert not found")
        
        return {"message": "Alert acknowledged successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error acknowledging alert: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/alerts/{alert_id}/resolve")
async def resolve_alert(alert_id: str, user_id: str):
    """Resolve an alert"""
    try:
        success = monitoring_service.resolve_alert(alert_id, user_id)
        if not success:
            raise HTTPException(status_code=404, detail="Alert not found")
        
        return {"message": "Alert resolved successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error resolving alert: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health", response_model=List[HealthCheckResponse])
async def get_health_checks():
    """Get health checks for all services"""
    try:
        health_checks = monitoring_service.get_health_checks()
        return [HealthCheckResponse(
            service_name=health.service_name,
            status=health.status,
            response_time=health.response_time,
            last_check=health.last_check,
            error_message=health.error_message,
            metadata=health.metadata
        ) for health in health_checks.values()]
    except Exception as e:
        logger.error(f"Error getting health checks: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health/{service_name}", response_model=HealthCheckResponse)
async def get_service_health(service_name: str):
    """Get health check for specific service"""
    try:
        health_checks = monitoring_service.get_health_checks()
        health = health_checks.get(service_name)
        
        if not health:
            raise HTTPException(status_code=404, detail="Service not found")
        
        return HealthCheckResponse(
            service_name=health.service_name,
            status=health.status,
            response_time=health.response_time,
            last_check=health.last_check,
            error_message=health.error_message,
            metadata=health.metadata
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting service health: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/metrics/summary", response_model=MonitoringMetricsResponse)
async def get_monitoring_metrics():
    """Get monitoring performance metrics"""
    try:
        metrics = monitoring_service.get_performance_metrics()
        return MonitoringMetricsResponse(
            total_metrics=len(monitoring_service.get_metrics()),
            active_alerts=len([a for a in monitoring_service.get_alerts().values() if a.status == AlertStatus.ACTIVE]),
            total_alerts=len(monitoring_service.get_alerts()),
            health_checks=len(monitoring_service.get_health_checks()),
            monitoring_active=monitoring_service.monitoring_active,
            last_updated=datetime.utcnow().isoformat(),
            **metrics
        )
    except Exception as e:
        logger.error(f"Error getting monitoring metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/alerts", response_model=AlertResponse)
async def create_alert(request: AlertCreateRequest):
    """Create a new alert"""
    try:
        # Create alert (this would typically be done by the monitoring system)
        alert_id = f"manual-{datetime.utcnow().timestamp()}"
        
        # This is a simplified implementation
        # In a real system, alerts would be created by the monitoring system
        return AlertResponse(
            alert_id=alert_id,
            title=request.title,
            description=request.description,
            severity=request.severity,
            status="active",
            source="manual",
            metric_name=request.metric_name,
            threshold_value=request.threshold_value,
            current_value=request.current_value,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            acknowledged_by=None,
            resolved_at=None,
            metadata=request.metadata
        )
    except Exception as e:
        logger.error(f"Error creating alert: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/alerts/{alert_id}", response_model=AlertResponse)
async def update_alert(alert_id: str, request: AlertUpdateRequest):
    """Update an alert"""
    try:
        alerts = monitoring_service.get_alerts()
        alert = alerts.get(alert_id)
        
        if not alert:
            raise HTTPException(status_code=404, detail="Alert not found")
        
        # Update alert fields
        if request.title:
            alert.title = request.title
        if request.description:
            alert.description = request.description
        if request.severity:
            alert.severity = AlertSeverity(request.severity)
        
        alert.updated_at = datetime.utcnow()
        
        return AlertResponse(
            alert_id=alert.alert_id,
            title=alert.title,
            description=alert.description,
            severity=alert.severity.value,
            status=alert.status.value,
            source=alert.source,
            metric_name=alert.metric_name,
            threshold_value=alert.threshold_value,
            current_value=alert.current_value,
            created_at=alert.created_at,
            updated_at=alert.updated_at,
            acknowledged_by=alert.acknowledged_by,
            resolved_at=alert.resolved_at,
            metadata=alert.metadata
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating alert: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status")
async def get_monitoring_status():
    """Get monitoring service status"""
    try:
        return {
            "status": "active" if monitoring_service.monitoring_active else "inactive",
            "service": "real-time-monitoring",
            "version": "2.0.0",
            "monitoring_active": monitoring_service.monitoring_active,
            "metrics_count": len(monitoring_service.get_metrics()),
            "alerts_count": len(monitoring_service.get_alerts()),
            "health_checks_count": len(monitoring_service.get_health_checks()),
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting monitoring status: {e}")
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "service": "real-time-monitoring",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
        )
