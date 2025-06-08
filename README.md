<div align="center">

# 📄 Redoc - Universal Document Converter

[![PyPI Version](https://img.shields.io/pypi/v/redoc?color=blue&logo=pypi&logoColor=white)](https://pypi.org/project/redoc/)
[![Python Version](https://img.shields.io/pypi/pyversions/redoc?logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/pypi/l/redoc?color=blue)](https://opensource.org/licenses/Apache-2.0)
[![Documentation Status](https://readthedocs.org/projects/redoc/badge/?version=latest)](https://redoc.readthedocs.io/)
[![Build Status](https://github.com/text2doc/redoc/actions/workflows/tests.yml/badge.svg)](https://github.com/text2doc/redoc/actions)
[![Test Coverage](https://codecov.io/gh/text2doc/redoc/branch/main/graph/badge.svg)](https://codecov.io/gh/text2doc/redoc)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Docker Pulls](https://img.shields.io/docker/pulls/text2doc/redoc?logo=docker)](https://hub.docker.com/r/text2doc/redoc)
[![Downloads](https://static.pepy.tech/badge/redoc)](https://pepy.tech/project/redoc)
[![CodeQL](https://github.com/text2doc/redoc/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/text2doc/redoc/actions/workflows/codeql-analysis.yml)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/text2doc/redoc/badge)](https://api.securityscorecards.dev/projects/github.com/text2doc/redoc)
[![Discord](https://img.shields.io/discord/1234567890?logo=discord&label=Discord&color=7289DA)](https://discord.gg/redoc)
[![Twitter Follow](https://img.shields.io/twitter/follow/text2doc?style=social)](https://twitter.com/text2doc)

</div>

Redoc is a powerful, modular document conversion framework that enables seamless transformation between various document formats including PDF, HTML, XML, JSON, DOCX, and EPUB. It features OCR capabilities and AI-powered content generation using Ollama Mistral:7b.

## 🌟 Features

### Core Functionality
- **Multi-format Support**: Bidirectional conversion between PDF, HTML, XML, JSON, DOCX, and EPUB
- **Template System**: JSON+HTML templates for dynamic document generation with bidirectional support
- **OCR Integration**: Extract text from scanned documents and images with Tesseract OCR
- **AI-Powered**: Leverage Ollama Mistral:7b for intelligent content generation and processing

### Advanced Capabilities
- **Bidirectional Conversion**: Convert documents to data and back with templates
- **Batch Processing**: Process multiple documents efficiently with parallel execution
- **Validation**: Built-in data validation with Pydantic models
- **Extensible Architecture**: Plugin system for custom formats and processors
- **Template Variables**: Support for dynamic content and conditional rendering

### Developer Experience
- **Comprehensive API**: Clean, well-documented Python API
- **Command Line Interface**: Intuitive CLI for quick conversions
- **Interactive Shell**: Built-in Python shell for exploration and debugging
- **Logging & Debugging**: Configurable logging and error reporting
- **Type Hints**: Full type annotations for better IDE support

### Enterprise Ready
- **Docker Support**: Containerized deployment with Docker and Docker Compose
- **REST API**: Built with FastAPI for easy integration
- **Asynchronous Processing**: Non-blocking operations for high performance
- **Security**: Input validation, sanitization, and secure defaults
- **Monitoring**: Built-in metrics and health checks

## 🚀 Quick Start

### Installation

#### Using pip
```bash
# Install the latest stable version
pip install redoc

# Install with optional dependencies
pip install "redoc[all]"

# Install specific components
pip install "redoc[cli]"       # CLI tools
pip install "redoc[server]"     # Web server
pip install "redoc[ai]"         # AI features
pip install "redoc[ocr]"        # OCR capabilities
pip install "redoc[templates]"  # Pre-built templates
```

#### Using Docker
```bash
# Pull the latest image
docker pull text2doc/redoc:latest

# Run a conversion
docker run -v $(pwd):/data text2doc/redoc convert input.pdf output.html

# Start the API server
docker run -p 8000:8000 text2doc/redoc serve
```

### Basic Usage

#### Python API
```python
from redoc import Redoc

# Initialize with default settings
converter = Redoc()

# Convert between formats
converter.convert('document.pdf', 'document.html')  # PDF to HTML
converter.convert('data.json', 'report.pdf')       # JSON to PDF with template

# Process multiple files
converter.batch_convert(
    input_glob='invoices/*.json',
    output_dir='output',
    output_format='pdf',
    template='invoice_template.html'
)

# Use the interactive shell
converter.shell()
```

#### Command Line Interface
```bash
# Show help
redoc --help

# Convert a document
redoc convert input.pdf output.html
redoc convert --template invoice.html data.json invoice.pdf

# Start interactive shell
redoc shell

# Start web server
redoc serve --host 0.0.0.0 --port 8000

# Process multiple files
redoc batch "documents/*.pdf" --format html --output-dir html_output
```

#### Using Templates
```python
from redoc import Redoc

converter = Redoc()

# Simple template with variables
template = {
    "template": "invoice.html",
    "data": {
        "invoice": {
            "number": "INV-2023-001",
            "date": "2023-11-15",
            "items": [
                {"description": "Web Design", "quantity": 10, "price": 100},
                {"description": "Hosting", "quantity": 1, "price": 50}
            ]
        }
    }
}

# Generate PDF from template
converter.convert(template, 'pdf', output_file='invoice.pdf')

# Extract data from document
data = converter.extract_data('invoice.pdf', template='invoice_template.html')
```

## 📚 Supported Conversions

| From \ To | PDF | HTML | XML | JSON | DOCX | EPUB |
|-----------|:---:|:----:|:---:|:----:|:----:|:----:|
| **PDF**   | ❌  | ✅   | ✅  | ✅   | ✅   | ✅   |
| **HTML**  | ✅  | ❌  | ✅  | ✅   | ✅   | ✅   |
| **XML**   | ✅  | ✅   | ❌  | ✅   | ✅   | ✅   |
| **JSON**  | ✅  | ✅   | ✅  | ❌   | ✅   | ✅   |
| **DOCX**  | ✅  | ✅   | ✅  | ✅   | ❌   | ✅   |
| **EPUB**  | ✅  | ✅   | ✅  | ✅   | ✅   | ❌   |

### Conversion Features

- **PDF Generation**: High-quality PDF output with support for headers, footers, and page numbers
- **HTML Processing**: Clean HTML output with customizable CSS styling
- **Data Extraction**: Extract structured data from documents using templates
- **Template Variables**: Use Jinja2 syntax for dynamic content
- **Batch Processing**: Process multiple files in parallel
- **OCR Support**: Extract text from scanned documents and images
- **AI-Powered**: Enhance documents with AI-generated content

## 🏗️ Project Structure

```
redoc/
├── src/
│   └── redoc/
│       ├── __init__.py          # Package initialization
│       ├── core.py             # Core conversion logic
│       ├── converters/         # Format-specific converters
│       │   ├── base.py         # Base converter class
│       │   ├── pdf_converter.py
│       │   ├── html_converter.py
│       │   ├── xml_converter.py
│       │   ├── json_converter.py
│       │   ├── docx_converter.py
│       │   └── epub_converter.py
│       ├── ocr/                # OCR functionality
│       ├── templates/          # Default templates
│       └── utils/              # Utility functions
├── tests/                      # Test suite
├── examples/                   # Usage examples
├── docs/                       # Documentation
├── pyproject.toml              # Project configuration
└── README.md                   # This file
```

## 🔧 Advanced Usage

### Using Templates

```python
from redoc import Redoc

converter = Redoc()

# Convert JSON+HTML template to PDF
converter.convert(
    {
        "template": "invoice.html",
        "data": {
            "invoice_number": "INV-2023-001",
            "date": "2023-11-15",
            "items": [
                {"description": "Web Design", "quantity": 1, "price": 1200}
            ],
            "total": 1200
        }
    },
    'pdf',
    output_file='invoice.pdf'
)
```

### OCR Processing

```python
from redoc import Redoc

converter = Redoc()

# Extract text from scanned PDF with OCR
result = converter.ocr('scanned_document.pdf')
print(result['text'])

# Convert scanned document to searchable PDF
converter.ocr('scanned_document.pdf', output_file='searchable.pdf')
```

### AI-Powered Content Generation

```python
from redoc import Redoc

converter = Redoc()

# Generate document using AI
result = converter.generate(
    "Create a professional invoice for web design services",
    format='pdf',
    style='professional',
    output_file='ai_invoice.pdf'
)
```

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) for details on how to contribute to this project.

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 📧 Contact

For any questions or suggestions, please contact [info@softreck.dev](mailto:info@softreck.dev).

---

<div align="center">
  Made with ❤️ by Text2Doc Team
</div>
