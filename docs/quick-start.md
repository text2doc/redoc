# 🚀 Quick Start Guide

Welcome to Redoc, the universal document converter! This guide will help you get started with converting documents between various formats in just a few minutes.

## Prerequisites

- Python 3.8 or higher
- Basic familiarity with command line
- (Optional) Docker for containerized deployment
- (Optional) Tesseract OCR for image text extraction

## Your First Conversion

### Convert a document
```bash
# Convert PDF to HTML
redoc convert document.pdf document.html

# Convert HTML to PDF
redoc convert page.html output.pdf
```

### Interactive Mode
```bash
# Start interactive shell
redoc shell
```

## Basic Commands

### Document Conversion
```bash
# Basic conversion
redoc convert input.pdf output.html

# Convert with a specific format
redoc convert --from pdf --to html input.pdf output.html

# Process multiple files
redoc batch "documents/*.pdf" --format html --output-dir html_output
```

### Interactive Shell Commands
```bash
redoc shell

# In the shell:
> help                 # Show available commands
> convert input.pdf output.html  # Convert files
> batch "*.pdf" --format html   # Batch process files
> templates list      # List available templates
> exit                # Exit the shell
```

## Example Workflow: Invoice Generation

1. **Prepare your data** (data.json):
   ```json
   {
     "invoice": {
       "number": "INV-2023-001",
       "date": "2023-11-15",
       "items": [
         {"description": "Web Design", "quantity": 10, "price": 100},
         {"description": "Hosting", "quantity": 1, "price": 50}
       ]
     }
   }
   ```

2. **Convert JSON to PDF using a template**:
   ```bash
   redoc convert --template invoice.html data.json invoice.pdf
   ```

3. **Extract data from an existing document**:
   ```bash
   redoc extract --template invoice_schema.json scanned_invoice.pdf extracted_data.json
   ```

## Advanced Examples

### Batch Processing
```bash
# Convert all PDFs in a directory to HTML
redoc batch "invoices/*.pdf" --format html --output-dir html_output

# Convert with a template
redoc batch "data/*.json" --template invoice.html --output-dir pdf_invoices
```

### Using Docker
```bash
# Run a conversion with Docker
docker run -v $(pwd):/data text2doc/redoc convert input.pdf output.html

# Start the web interface
docker run -p 8000:8000 -v $(pwd)/templates:/app/templates text2doc/redoc serve
```

## Next Steps

- Learn about [templates](templates.md) for custom document generation
- Explore [AI-powered features](ai.md) for smart document processing
- Check the [API Reference](api.md) for programmatic usage
- Review the [installation guide](installation.md) for advanced setup

## Getting Help

- Run `redoc --help` for command-line options
- [Open an issue](https://github.com/text2doc/redoc/issues) for bugs or feature requests
