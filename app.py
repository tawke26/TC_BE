"""
TechCheck Backend - FDV Thesis Validation API
AI agent-powered thesis validation with PDF annotation
"""

import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional

import uvicorn
from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from ultra_simple_pdf import UltraSimplePDFProcessor as PDFProcessor
from simple_ai_validator import validate_thesis_simple
from fdv_requirements import FDV_REQUIREMENTS
from fastapi.templating import Jinja2Templates
from fastapi import Request

app = FastAPI(
    title="TechCheck FDV Thesis Validator",
    description="AI-powered validation system for FDV thesis formatting requirements",
    version="1.0.0"
)

# CORS middleware for web frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create directories for file storage
templates = Jinja2Templates(directory="templates")
UPLOAD_DIR = Path("uploads")
OUTPUT_DIR = Path("output")
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# Mount static files for downloading results
app.mount("/download", StaticFiles(directory=str(OUTPUT_DIR)), name="download")

# Storage for validation results
validation_results = {}

class ValidationResponse(BaseModel):
    job_id: str
    status: str
    message: str
    download_url: Optional[str] = None
    error_count: Optional[int] = None
    errors: Optional[list] = None

class ValidationStatus(BaseModel):
    job_id: str
    status: str
    progress: str
    error_count: Optional[int] = None
    completed_at: Optional[datetime] = None
@app.get("/", include_in_schema=False)
async def website(request: Request):
    """Main website interface"""
    return templates.TemplateResponse("index.html", {"request": request})



@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

@app.post("/validate", response_model=ValidationResponse)
async def validate_thesis(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    """
    Upload and validate a thesis PDF against FDV requirements
    Returns job ID for checking status and downloading results
    """
    
    # Validate file type
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    # Generate unique job ID
    job_id = str(uuid.uuid4())
    
    # Save uploaded file
    file_path = UPLOAD_DIR / f"{job_id}_{file.filename}"
    try:
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")
    
    # Initialize validation status
    validation_results[job_id] = {
        "status": "processing",
        "progress": "File uploaded, starting validation...",
        "filename": file.filename,
        "file_path": str(file_path),
        "started_at": datetime.now(),
        "error_count": 0,
        "errors": []
    }
    
    # Start validation in background
    background_tasks.add_task(process_validation, job_id, file_path)
    
    return ValidationResponse(
        job_id=job_id,
        status="processing",
        message="Validation started. Use /status/{job_id} to check progress."
    )

async def process_validation(job_id: str, file_path: Path):
    """Background task to process thesis validation"""
    try:
        # Update status
        validation_results[job_id]["progress"] = "Processing PDF..."
        
        # Initialize PDF processor
        pdf_processor = PDFProcessor(file_path)
        
        # Update status
        validation_results[job_id]["progress"] = "Running AI validation agent..."
        
        # Initialize and run validation agent
        # Use simple AI validator instead of complex agent
        errors = validate_thesis_simple(file_path)
        
        # Update status
        validation_results[job_id]["progress"] = "Generating annotated PDF..."
        
        # Generate annotated PDF
        output_filename = f"{job_id}_annotated.pdf"
        output_path = OUTPUT_DIR / output_filename
        
        annotated_pdf_path = pdf_processor.generate_annotated_pdf(errors, output_path)
        
        # Update final results
        validation_results[job_id].update({
            "status": "completed",
            "progress": "Validation completed successfully",
            "error_count": len(errors),
            "errors": errors,
            "output_path": str(annotated_pdf_path),
            "download_url": f"/download/{output_filename}",
            "completed_at": datetime.now()
        })
        
    except Exception as e:
        validation_results[job_id].update({
            "status": "failed",
            "progress": f"Validation failed: {str(e)}",
            "error": str(e),
            "completed_at": datetime.now()
        })

@app.get("/status/{job_id}", response_model=ValidationStatus)
async def get_validation_status(job_id: str):
    """Check the status of a validation job"""
    
    if job_id not in validation_results:
        raise HTTPException(status_code=404, detail="Job ID not found")
    
    result = validation_results[job_id]
    
    return ValidationStatus(
        job_id=job_id,
        status=result["status"],
        progress=result["progress"],
        error_count=result.get("error_count"),
        completed_at=result.get("completed_at")
    )

@app.get("/result/{job_id}")
async def get_validation_result(job_id: str):
    """Get detailed validation results"""
    
    if job_id not in validation_results:
        raise HTTPException(status_code=404, detail="Job ID not found")
    
    result = validation_results[job_id]
    
    if result["status"] != "completed":
        raise HTTPException(status_code=400, detail="Validation not completed yet")
    
    return {
        "job_id": job_id,
        "filename": result["filename"],
        "status": result["status"],
        "error_count": result["error_count"],
        "errors": result["errors"],
        "download_url": result["download_url"],
        "completed_at": result["completed_at"]
    }

@app.get("/download-pdf/{job_id}")
async def download_annotated_pdf(job_id: str):
    """Download the annotated PDF with marked errors"""
    
    if job_id not in validation_results:
        raise HTTPException(status_code=404, detail="Job ID not found")
    
    result = validation_results[job_id]
    
    if result["status"] != "completed":
        raise HTTPException(status_code=400, detail="Validation not completed yet")
    
    output_path = result.get("output_path")
    if not output_path or not Path(output_path).exists():
        raise HTTPException(status_code=404, detail="Annotated PDF not found")
    
    return FileResponse(
        path=output_path,
        filename=f"validated_{result['filename']}",
        media_type="application/pdf"
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)