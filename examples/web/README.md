# Web Example

This example shows how to use Redoc in a web application with FastAPI.

## Features

- REST API for document conversion
- File upload support
- Template rendering
- Asynchronous processing

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the web server:
   ```bash
   uvicorn main:app --reload
   ```

3. Open http://localhost:8000/docs for the interactive API documentation.

## API Endpoints

- `POST /convert`: Convert a document to another format
- `POST /template`: Generate a document from a template
- `GET /formats`: List supported formats

## Environment Variables

- `REDOC_DEBUG`: Set to `1` to enable debug mode
- `UPLOAD_DIR`: Directory to store uploaded files (default: `./uploads`)
