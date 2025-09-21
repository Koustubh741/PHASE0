#!/usr/bin/env python3
"""
BFSI Policy Upload API
FastAPI service for uploading and managing BFSI policies
"""

import os
import json
import logging
import secrets
from datetime import datetime
from typing import Dict, List, Any, Optional
from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn
import aiofiles

from bfsi_policy_uploader import policy_manager, upload_policy_file, upload_policy_text, create_training_dataset, get_policy_statistics

def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename by removing unsafe characters and extensions.
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename without extension and unsafe characters
    """
    import re
    
    if not filename:
        return "untitled"
    
    # Remove file extension (everything after the last dot)
    name_without_ext = os.path.splitext(filename)[0]
    
    # Remove or replace unsafe characters
    # Keep only alphanumeric, spaces, hyphens, underscores, and dots
    sanitized = re.sub(r'[^\w\s\-\.]', '', name_without_ext)
    
    # Replace multiple spaces with single space
    sanitized = re.sub(r'\s+', ' ', sanitized)
    
    # Strip leading/trailing whitespace
    sanitized = sanitized.strip()
    
    # If empty after sanitization, use default name
    if not sanitized:
        sanitized = "untitled"
    
    return sanitized

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="BFSI Policy Upload API",
    description="API for uploading and managing BFSI policies for LLM training",
    version="1.0.0"
)

# Add CORS middleware with secure configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Frontend development server
        "http://localhost:8080",  # Alternative frontend port
        "https://yourdomain.com", # Replace with your production domain
    ],
    allow_credentials=False,  # Set to True only if you need cookies/auth headers
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # Only necessary HTTP methods
    allow_headers=[
        "Accept",
        "Accept-Language",
        "Content-Language",
        "Content-Type",
        "Authorization",  # Only if you need auth headers
    ],
)

# Security headers middleware
@app.middleware("http")
async def security_headers_middleware(request: Request, call_next):
    """Add security headers to all responses"""
    response = await call_next(request)
    
    # Generate nonce for this request
    nonce = secrets.token_urlsafe(32)
    
    # Strict Content Security Policy
    csp_policy = (
        f"default-src 'self'; "
        f"script-src 'self' 'nonce-{nonce}' 'strict-dynamic'; "
        f"style-src 'self' 'unsafe-inline'; "  # CSS-in-JS may require unsafe-inline
        f"img-src 'self' data: blob:; "
        f"font-src 'self'; "
        f"connect-src 'self'; "
        f"object-src 'none'; "
        f"base-uri 'none'; "
        f"frame-ancestors 'none'; "
        f"form-action 'self'; "
        f"upgrade-insecure-requests; "
        f"report-uri /csp-report"
    )
    
    # Add security headers
    response.headers["Content-Security-Policy"] = csp_policy
    response.headers["Content-Security-Policy-Report-Only"] = csp_policy  # Start in report-only mode
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
    
    # Add nonce to response for use in templates
    response.headers["X-Nonce"] = nonce
    
    return response

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Pydantic models
class PolicyUploadRequest(BaseModel):
    """Policy upload request"""
    title: str
    content: str
    policy_type: str
    framework: str
    version: str = "1.0"
    metadata: Optional[Dict[str, Any]] = None

class TrainingDatasetRequest(BaseModel):
    """Training dataset creation request"""
    name: str
    description: str
    policy_ids: Optional[List[str]] = None
    framework_filter: Optional[List[str]] = None

class PolicyResponse(BaseModel):
    """Policy response"""
    policy_id: str
    title: str
    policy_type: str
    framework: str
    version: str
    upload_date: str
    status: str
    content_preview: str

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "BFSI Policy Upload API",
        "version": "1.0.0",
        "description": "API for uploading and managing BFSI policies for LLM training",
        "endpoints": {
            "health": "/health",
            "policies": "/api/policies",
            "upload": "/api/policies/upload",
            "statistics": "/api/policies/statistics",
            "training": "/api/training/datasets"
        }
    }

@app.post("/csp-report")
async def csp_report(request: Request):
    """Handle CSP violation reports"""
    try:
        report_data = await request.json()
        logging.warning(f"CSP Violation Report: {json.dumps(report_data, indent=2)}")
        return {"status": "received"}
    except Exception as e:
        logging.error(f"Error processing CSP report: {e}")
        return {"status": "error", "message": str(e)}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        return {
            "service": "BFSI Policy Upload API",
            "status": "healthy",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/policies")
async def get_policies():
    """Get all policies"""
    try:
        policies = policy_manager.get_all_policies()
        
        policy_responses = []
        for policy in policies:
            policy_responses.append(PolicyResponse(
                policy_id=policy.policy_id,
                title=policy.title,
                policy_type=policy.policy_type,
                framework=policy.framework,
                version=policy.version,
                upload_date=policy.upload_date.isoformat(),
                status=policy.status,
                content_preview=policy.content[:200] + "..." if len(policy.content) > 200 else policy.content
            ))
        
        return {
            "policies": policy_responses,
            "total_count": len(policy_responses),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting policies: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/policies/{policy_id}")
async def get_policy(policy_id: str):
    """Get specific policy by ID"""
    try:
        policies = policy_manager.get_all_policies()
        policy = next((p for p in policies if p.policy_id == policy_id), None)
        
        if not policy:
            raise HTTPException(status_code=404, detail="Policy not found")
        
        return {
            "policy_id": policy.policy_id,
            "title": policy.title,
            "policy_type": policy.policy_type,
            "framework": policy.framework,
            "version": policy.version,
            "upload_date": policy.upload_date.isoformat(),
            "status": policy.status,
            "content": policy.content,
            "metadata": policy.metadata
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting policy {policy_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/policies/upload")
async def upload_policy_text_endpoint(request: PolicyUploadRequest):
    """Upload policy content as text"""
    try:
        policy_id = upload_policy_text(
            title=request.title,
            content=request.content,
            policy_type=request.policy_type,
            framework=request.framework,
            version=request.version,
            metadata=request.metadata
        )
        
        return {
            "message": "Policy uploaded successfully",
            "policy_id": policy_id,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error uploading policy: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/policies/upload-file")
async def upload_policy_file_endpoint(
    file: UploadFile = File(...),
    policy_type: str = Form(...),
    framework: str = Form(...),
    version: str = Form("1.0"),
    metadata: str = Form("{}")
):
    """Upload policy file"""
    try:
        # Read file content
        content = await file.read()
        content_str = content.decode('utf-8')
        
        # Parse metadata
        try:
            metadata_dict = json.loads(metadata) if metadata else {}
        except json.JSONDecodeError:
            metadata_dict = {}
        
        policy_id = upload_policy_text(
            title=sanitize_filename(file.filename),
            content=content_str,
            policy_type=policy_type,
            framework=framework,
            version=version,
            metadata=metadata_dict
        )
        
        return {
            "message": "Policy file uploaded successfully",
            "policy_id": policy_id,
            "filename": file.filename,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error uploading policy file: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/policies/statistics")
async def get_statistics():
    """Get policy statistics"""
    try:
        stats = get_policy_statistics()
        return {
            "statistics": stats,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting statistics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/training/datasets")
async def get_training_datasets():
    """Get all training datasets"""
    try:
        # This would need to be implemented in the policy_manager
        # For now, return empty list
        return {
            "datasets": [],
            "total_count": 0,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting training datasets: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/training/datasets")
async def create_training_dataset_endpoint(request: TrainingDatasetRequest):
    """Create a new training dataset"""
    try:
        dataset_id = create_training_dataset(
            name=request.name,
            description=request.description,
            policy_ids=request.policy_ids,
            framework_filter=request.framework_filter
        )
        
        return {
            "message": "Training dataset created successfully",
            "dataset_id": dataset_id,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error creating training dataset: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/training/datasets/{dataset_id}")
async def get_training_dataset(dataset_id: str):
    """Get specific training dataset"""
    try:
        chunks = policy_manager.get_training_chunks(dataset_id)
        
        return {
            "dataset_id": dataset_id,
            "chunks": chunks,
            "total_chunks": len(chunks),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting training dataset {dataset_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/training/datasets/{dataset_id}/export")
async def export_training_dataset(dataset_id: str, format: str = "json"):
    """Export training dataset"""
    try:
        if format not in ["json", "txt", "jsonl"]:
            raise HTTPException(status_code=400, detail="Invalid format. Use: json, txt, jsonl")
        
        output_file = policy_manager.export_training_data(dataset_id, format)
        
        return {
            "message": "Training data exported successfully",
            "output_file": output_file,
            "format": format,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error exporting training dataset {dataset_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/policies/{policy_id}")
async def delete_policy(policy_id: str):
    """Delete a policy"""
    try:
        # Check if policy exists first
        policies = policy_manager.get_all_policies()
        policy = next((p for p in policies if p.policy_id == policy_id), None)
        
        if not policy:
            raise HTTPException(status_code=404, detail="Policy not found")
        
        # Attempt to delete the policy
        deletion_successful = policy_manager.delete_policy(policy_id)
        
        if not deletion_successful:
            raise HTTPException(status_code=500, detail="Failed to delete policy")
        
        return {
            "message": "Policy deleted successfully",
            "policy_id": policy_id,
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        # Re-raise HTTP exceptions (404, 500)
        raise
    except Exception as e:
        logger.error(f"Error deleting policy {policy_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Serve the HTML interface
@app.get("/interface")
async def serve_interface(request: Request):
    """Serve the policy upload interface with CSP nonce injection"""
    try:
        with open("bfsi_policy_upload_interface.html", "r", encoding="utf-8") as f:
            html_content = f.read()
        
        # Get nonce from request headers (set by middleware)
        nonce = request.headers.get("X-Nonce", "")
        
        # Inject nonce into script tags
        html_content = html_content.replace(
            '<script>',
            f'<script nonce="{nonce}">'
        )
        
        # Also inject nonce into inline event handlers if any
        html_content = html_content.replace(
            'onclick="',
            f'nonce="{nonce}" onclick="'
        )
        
        return HTMLResponse(content=html_content)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Interface file not found")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8010))
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    )
