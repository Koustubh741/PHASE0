"""
Real-time Monitoring Data Transfer Objects
DTOs for monitoring and alerting operations
"""

from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum


class AlertSeverity(str, Enum):
    """Alert severity enumeration"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AlertStatus(str, Enum):
    """Alert status enumeration"""
    ACTIVE = "active"
    ACKNOWLEDGED = "acknowledged"
    RESOLVED = "resolved"
    SUPPRESSED = "suppressed"


class MetricType(str, Enum):
    """Metric type enumeration"""
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    SUMMARY = "summary"


class AlertResponse(BaseModel):
    """Alert response"""
    alert_id: str = Field(..., description="Alert ID")
    title: str = Field(..., description="Alert title")
    description: str = Field(..., description="Alert description")
    severity: str = Field(..., description="Alert severity")
    status: str = Field(..., description="Alert status")
    source: str = Field(..., description="Alert source")
    metric_name: str = Field(..., description="Metric name")
    threshold_value: float = Field(..., description="Threshold value")
    current_value: float = Field(..., description="Current value")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    acknowledged_by: Optional[str] = Field(None, description="User who acknowledged")
    resolved_at: Optional[datetime] = Field(None, description="Resolution timestamp")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    
    class Config:
        json_schema_extra = {
            "example": {
                "alert_id": "123e4567-e89b-12d3-a456-426614174000",
                "title": "High CPU Usage",
                "description": "CPU usage is above 80%",
                "severity": "high",
                "status": "active",
                "source": "monitoring-service",
                "metric_name": "system_cpu_usage",
                "threshold_value": 80.0,
                "current_value": 85.5,
                "created_at": "2024-01-15T10:30:00Z",
                "updated_at": "2024-01-15T10:30:00Z",
                "acknowledged_by": None,
                "resolved_at": None,
                "metadata": {}
            }
        }


class MetricResponse(BaseModel):
    """Metric response"""
    metric_id: str = Field(..., description="Metric ID")
    name: str = Field(..., description="Metric name")
    value: float = Field(..., description="Metric value")
    metric_type: str = Field(..., description="Metric type")
    labels: Dict[str, str] = Field(default_factory=dict, description="Metric labels")
    timestamp: datetime = Field(..., description="Metric timestamp")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    
    class Config:
        json_schema_extra = {
            "example": {
                "metric_id": "123e4567-e89b-12d3-a456-426614174000",
                "name": "system_cpu_usage",
                "value": 75.5,
                "metric_type": "gauge",
                "labels": {"instance": "server-01", "environment": "production"},
                "timestamp": "2024-01-15T10:30:00Z",
                "metadata": {"unit": "percent"}
            }
        }


class HealthCheckResponse(BaseModel):
    """Health check response"""
    service_name: str = Field(..., description="Service name")
    status: str = Field(..., description="Health status")
    response_time: float = Field(..., description="Response time in milliseconds")
    last_check: datetime = Field(..., description="Last check timestamp")
    error_message: Optional[str] = Field(None, description="Error message if unhealthy")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    
    class Config:
        json_schema_extra = {
            "example": {
                "service_name": "database",
                "status": "healthy",
                "response_time": 45.2,
                "last_check": "2024-01-15T10:30:00Z",
                "error_message": None,
                "metadata": {"version": "13.4", "connections": 15}
            }
        }


class MonitoringMetricsResponse(BaseModel):
    """Monitoring metrics response"""
    total_metrics: int = Field(..., description="Total number of metrics")
    active_alerts: int = Field(..., description="Number of active alerts")
    total_alerts: int = Field(..., description="Total number of alerts")
    health_checks: int = Field(..., description="Number of health checks")
    monitoring_active: bool = Field(..., description="Whether monitoring is active")
    last_updated: str = Field(..., description="Last update timestamp")
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_metrics": 25,
                "active_alerts": 3,
                "total_alerts": 15,
                "health_checks": 5,
                "monitoring_active": True,
                "last_updated": "2024-01-15T10:30:00Z"
            }
        }


class AlertCreateRequest(BaseModel):
    """Request to create an alert"""
    title: str = Field(..., description="Alert title")
    description: str = Field(..., description="Alert description")
    severity: str = Field(..., description="Alert severity")
    metric_name: str = Field(..., description="Metric name")
    threshold_value: float = Field(..., description="Threshold value")
    current_value: float = Field(..., description="Current value")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "High Memory Usage",
                "description": "Memory usage is above 85%",
                "severity": "high",
                "metric_name": "system_memory_usage",
                "threshold_value": 85.0,
                "current_value": 87.5,
                "metadata": {"instance": "server-01"}
            }
        }


class AlertUpdateRequest(BaseModel):
    """Request to update an alert"""
    title: Optional[str] = Field(None, description="Alert title")
    description: Optional[str] = Field(None, description="Alert description")
    severity: Optional[str] = Field(None, description="Alert severity")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Updated High Memory Usage",
                "description": "Memory usage is above 85% - Updated",
                "severity": "critical",
                "metadata": {"updated_by": "admin"}
            }
        }
