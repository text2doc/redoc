# Redoc - Universal Document Converter

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Redoc is a powerful, modular document conversion framework that enables seamless transformation between various document formats including PDF, HTML, XML, JSON, DOCX, and EPUB. It features OCR capabilities and AI-powered content generation using Ollama Mistral:7b.

## 🌟 Features

- **Multi-format Support**: Convert between PDF, HTML, XML, JSON, DOCX, and EPUB
- **Template-based Processing**: Use JSON+HTML templates for dynamic document generation
- **OCR Integration**: Extract text from scanned documents and images
- **Modular Architecture**: Easily extendable with custom converters and processors
- **AI-Powered**: Leverage Ollama Mistral:7b for intelligent content generation
- **Batch Processing**: Process multiple documents efficiently
- **CLI & API**: Command-line interface and Python API for easy integration

## 🚀 Quick Start

### Installation

```bash
# Install with pip
pip install redoc

# Or install from source
git clone https://github.com/text2doc/redoc.git
cd redoc
pip install -e .
```

### Basic Usage

```python
from redoc import Redoc

# Initialize the converter
converter = Redoc()

# Convert PDF to JSON
result = converter.convert('document.pdf', 'json')

# Convert HTML+JSON template to PDF
template = {
    "template": "invoice.html",
    "data": {
        "invoice_number": "INV-2023-001",
        "date": "2023-11-15",
        "total": "$1,200.00"
    }
}
converter.convert(template, 'pdf', output_file='invoice.pdf')
```

## 📚 Supported Conversions

| From \ To | PDF | HTML | XML | JSON | DOCX | EPUB |
|-----------|-----|------|-----|------|------|------|
| PDF       | ❌  | ✅   | ✅  | ✅   | ✅   | ✅   |
| HTML      | ✅  | ❌  | ✅  | ✅   | ✅   | ✅   |
| XML       | ✅  | ✅   | ❌  | ✅   | ✅   | ✅   |
| JSON      | ✅  | ✅   | ✅  | ❌   | ✅   | ✅   |
| DOCX      | ✅  | ✅   | ✅  | ✅   | ❌   | ✅   |
| EPUB      | ✅  | ✅   | ✅  | ✅   | ✅   | ❌   |

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
