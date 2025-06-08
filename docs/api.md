# 📚 Redoc API Reference

This document provides a comprehensive reference for the Redoc Python API, command-line interface, and web API.

## Table of Contents
- [Core Classes](#core-classes)
- [Document Conversion](#document-conversion)
- [Templates](#templates)
- [AI Integration](#ai-integration)
- [Command Line Interface](#command-line-interface)
- [Web API](#web-api)
- [Configuration](#configuration)
- [Exceptions](#exceptions)

## Core Classes

### `Redoc` Class

The main class for interacting with Redoc programmatically.

```python
from redoc import Redoc

# Basic initialization
redoc = Redoc()

# With custom configuration
redoc = Redoc(
    templates_dir="templates",
    cache_dir=".cache",
    debug=False
)
```

#### Methods

- `convert(input_file, output_file, **options)` - Convert between document formats
- `batch_convert(input_glob, output_dir, **options)` - Process multiple files
- `extract_data(input_file, schema=None, **options)` - Extract data from documents
- `generate_document(template, data, output_file, **options)` - Generate documents from templates
- `validate_document(file_path, schema=None)` - Validate document against a schema
- `get_available_formats()` - List supported input/output formats

## Document Conversion

### Basic Conversion

```python
# Convert PDF to HTML
redoc.convert("input.pdf", "output.html")

# Convert with options
redoc.convert(
    "input.pdf",
    "output.html",
    dpi=300,
    page_range="1-5,7,9-12"
)
```

### Batch Processing

```python
# Process multiple files
results = redoc.batch_convert(
    "documents/*.pdf",
    "output/",
    output_format="html",
    recursive=True
)

for result in results:
    print(f"Processed {result.input} -> {result.output}")
```

## Templates

### Using Templates

```python
# Generate document from template
data = {
    "title": "Sample Document",
    "sections": ["Introduction", "Main Content", "Conclusion"]
}

redoc.generate_document(
    template="basic.html",
    data=data,
    output_file="output.pdf"
)
```

### Template Helpers

```python
# Register custom filters
@redoc.template_filter('currency')
def format_currency(value):
    return f"${value:,.2f}"

# Add global variables
redoc.template_globals['version'] = '1.0.0'
redoc.template_globals['current_year'] = lambda: datetime.now().year
```

## AI Integration

### Basic AI Operations

```python
# Summarize text
summary = redoc.ai.summarize("long_document.txt")

# Extract entities
entities = redoc.ai.extract_entities("document.pdf")

# Answer questions about a document
answer = redoc.ai.ask("document.pdf", "What is the main topic?")
```

### Custom AI Providers

```python
from redoc.ai.base import AIProvider

class MyAIProvider(AIProvider):
    def summarize(self, text: str, **kwargs) -> str:
        # Your implementation here
        return summary

# Use custom provider
redoc = Redoc(ai_provider=MyAIProvider())
```

## Command Line Interface

### Basic Commands

```bash
# Convert document
redoc convert input.pdf output.html

# Batch process files
redoc batch "documents/*.pdf" --format html --output-dir output

# Start interactive shell
redoc shell

# Start web server
redoc serve --host 0.0.0.0 --port 8000
```

### Common Options

- `--format, -f`: Output format (default: auto-detect)
- `--template, -t`: Template to use
- `--output-dir, -o`: Output directory
- `--recursive, -r`: Process directories recursively
- `--workers, -w`: Number of worker processes
- `--debug`: Enable debug mode

## Web API

### Endpoints

- `POST /api/convert` - Convert document
- `POST /api/batch` - Batch process documents
- `POST /api/extract` - Extract data from document
- `GET /api/formats` - List supported formats
- `GET /api/health` - Health check

### Example Request

```bash
curl -X POST http://localhost:8000/api/convert \
  -F "file=@document.pdf" \
  -F "output_format=html" \
  -o output.html
```

## Configuration

### Environment Variables

```bash
export REDOC_LOG_LEVEL=INFO
export REDOC_WORKERS=4
export REDOC_TEMP_DIR=/tmp/redoc
```

### Configuration File

Create `~/.config/redoc/config.yaml`:

```yaml
log_level: INFO
workers: 4
temp_dir: /tmp/redoc

templates:
  search_paths:
    - ~/.config/redoc/templates
    - /usr/local/share/redoc/templates

ai:
  provider: ollama
  model: mistral:7b
  temperature: 0.7
```

## Exceptions

### Common Exceptions

- `RedocError` - Base exception for all Redoc errors
- `ConversionError` - Document conversion failed
- `TemplateError` - Template rendering error
- `ValidationError` - Data validation failed
- `UnsupportedFormatError` - Unsupported file format
- `AIServiceError` - AI service error

### Error Handling

```python
try:
    redoc.convert("input.pdf", "output.html")
except redoc.RedocError as e:
    print(f"Error: {e}")
    if hasattr(e, 'details'):
        print(f"Details: {e.details}")
```

## Examples

### Convert and Process

```python
# Convert and process the result
with redoc.convert_to_memory("input.pdf", "html") as html_content:
    # Process HTML content
    processed = process_html(html_content)
    
    # Save result
    with open("processed.html", "w") as f:
        f.write(processed)
```

### Custom Document Processor

```python
from redoc.processors import DocumentProcessor

class MyProcessor(DocumentProcessor):
    def process(self, content, **kwargs):
        # Process document content
        return processed_content

# Register processor
redoc.register_processor("my_format", MyProcessor())
```

## Contributing

For contributing to Redoc, see our [Contributing Guide](https://github.com/text2doc/redoc/blob/main/CONTRIBUTING.md).