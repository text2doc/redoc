"""Web example using FastAPI and Redoc."""

import os
import uuid
from pathlib import Path
from typing import Dict, List, Optional

from fastapi import FastAPI, File, Form, HTTPException, UploadFile, status
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from redoc import Redoc

# Configuration
DEBUG = os.getenv("REDOC_DEBUG", "0") == "1"
UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", "uploads"))
ALLOWED_EXTENSIONS = {"pdf", "docx", "html", "txt", "md"}

# Ensure upload directory exists
UPLOAD_DIR.mkdir(exist_ok=True, parents=True)

# Initialize FastAPI
app = FastAPI(
    title="Redoc Web API",
    description="Web interface for Redoc document conversion",
    version="0.1.0",
    debug=DEBUG
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Redoc
converter = Redoc()

# Models
class ConvertRequest(BaseModel):
    """Request model for document conversion."""
    input_format: str
    output_format: str
    options: Optional[Dict] = None

class TemplateRequest(BaseModel):
    """Request model for template rendering."""
    template: str
    data: Dict
    output_format: str = "pdf"

class FormatInfo(BaseModel):
    """Information about a supported format."""
    name: str
    description: str
    extensions: List[str]

# Helper functions
def get_file_extension(filename: str) -> str:
    """Get the file extension from a filename."""
    return Path(filename).suffix[1:].lower()

def allowed_file(filename: str) -> bool:
    """Check if the file has an allowed extension."""
    return '.' in filename and get_file_extension(filename) in ALLOWED_EXTENSIONS

async def save_upload_file(upload_file: UploadFile) -> Path:
    """Save an uploaded file to the upload directory."""
    if not allowed_file(upload_file.filename):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # Generate a unique filename
    file_ext = get_file_extension(upload_file.filename)
    filename = f"{uuid.uuid4()}.{file_ext}"
    file_path = UPLOAD_DIR / filename
    
    # Save the file
    try:
        contents = await upload_file.read()
        file_path.write_bytes(contents)
        return file_path
    except Exception as e:
        if file_path.exists():
            file_path.unlink()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save file: {str(e)}"
        ) from e

# Routes
@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "Redoc Web API",
        "version": "0.1.0",
        "documentation": "/docs",
        "endpoints": [
            {"path": "/convert", "methods": ["POST"], "description": "Convert a document"},
            {"path": "/template", "methods": ["POST"], "description": "Generate from template"},
            {"path": "/formats", "methods": ["GET"], "description": "List supported formats"}
        ]
    }

@app.post("/convert")
async def convert_document(
    file: UploadFile = File(...),
    output_format: str = Form(...),
    options: str = Form("{}")
):
    """Convert a document to another format."""
    # Save uploaded file
    try:
        input_path = await save_upload_file(file)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process file: {str(e)}"
        ) from e
    
    # Parse options
    try:
        options_dict = eval(options) if options else {}
    except Exception as e:
        options_dict = {}
    
    # Generate output filename
    output_filename = f"{input_path.stem}.{output_format}"
    output_path = UPLOAD_DIR / output_filename
    
    try:
        # Convert the document
        converter.convert(
            str(input_path),
            str(output_path),
            format=output_format,
            **options_dict
        )
        
        # Return the converted file
        return FileResponse(
            output_path,
            media_type=f"application/{output_format}",
            filename=output_filename
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Conversion failed: {str(e)}"
        ) from e
    finally:
        # Clean up input file
        if input_path.exists():
            input_path.unlink()
        # Clean up output file if it exists and there was an error
        if output_path.exists() and not output_path.is_file():
            output_path.unlink()

@app.post("/template")
async def generate_from_template(request: TemplateRequest):
    """Generate a document from a template."""
    output_filename = f"template_output.{request.output_format}"
    output_path = UPLOAD_DIR / output_filename
    
    try:
        # Generate document from template
        converter.convert(
            request.template,
            str(output_path),
            format=request.output_format,
            **request.data
        )
        
        # Return the generated file
        return FileResponse(
            output_path,
            media_type=f"application/{request.output_format}",
            filename=output_filename
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Template processing failed: {str(e)}"
        ) from e
    finally:
        # Clean up output file if it exists and there was an error
        if output_path.exists() and not output_path.is_file():
            output_path.unlink()

@app.get("/formats", response_model=List[FormatInfo])
async def list_formats():
    """List all supported formats and their details."""
    # This is a simplified example - in a real app, you would get this from the converter
    return [
        FormatInfo(
            name="PDF",
            description="Portable Document Format",
            extensions=["pdf"]
        ),
        FormatInfo(
            name="DOCX",
            description="Microsoft Word Document",
            extensions=["docx"]
        ),
        FormatInfo(
            name="HTML",
            description="HyperText Markup Language",
            extensions=["html", "htm"]
        ),
        FormatInfo(
            name="Markdown",
            description="Lightweight Markup Language",
            extensions=["md", "markdown"]
        ),
        FormatInfo(
            name="Plain Text",
            description="Plain Text File",
            extensions=["txt"]
        )
    ]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
