# 📦 Installation Guide

## System Requirements

- **Python 3.8 or higher**
- **Required Dependencies**:
  - `poppler-utils` (for PDF processing)
  - `libreoffice` (for DOCX/ODT support)
  - `tesseract-ocr` (for OCR functionality)
  - `libreoffice-headless` (for server environments)
- **Disk Space**: ~500MB (more for large document processing)
- **Memory**: 2GB minimum (4GB recommended for large documents)

## Installing System Dependencies

### Ubuntu/Debian
```bash
sudo apt update
sudo apt install -y \
    poppler-utils \
    libreoffice \
    tesseract-ocr \
    tesseract-ocr-eng \
    libreoffice-headless
```

### macOS (using Homebrew)
```bash
brew install poppler tesseract tesseract-lang libreoffice
```

### Windows
1. Download and install [Poppler for Windows](https://github.com/oschwartz10612/poppler-windows/releases/)
2. Download and install [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki)
3. Download and install [LibreOffice](https://www.libreoffice.org/)
4. Add all installation directories to your system PATH

## Installing Redoc

### Using pip (Recommended)
```bash
# Basic installation
pip install redoc

# Install with all optional dependencies
pip install "redoc[all]"

# Or install specific components
pip install "redoc[cli]"       # Command line interface
pip install "redoc[server]"     # Web server and API
pip install "redoc[ai]"         # AI features (requires Ollama)
pip install "redoc[ocr]"        # OCR capabilities (Tesseract)
pip install "redoc[templates]"  # Pre-built templates
```

### Using Docker (Recommended for Production)
```bash
# Pull the latest image
docker pull text2doc/redoc:latest

# Run a conversion
docker run -v $(pwd):/data text2doc/redoc convert input.pdf output.html

# Start the web interface
docker run -p 8000:8000 -v $(pwd)/templates:/app/templates text2doc/redoc serve
```

### Development Installation
```bash
# Clone the repository
git clone https://github.com/text2doc/redoc.git
cd redoc

# Install in development mode with all dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Run tests
pytest
```

## Verifying Installation

```bash
# Check Redoc installation
redoc --version

# Verify basic functionality
redoc convert --help

# Run self-tests
redoc test
```

## Configuration

Redoc can be configured using environment variables or a configuration file:

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
default_output_format: pdf

templates:
  search_paths:
    - ~/.config/redoc/templates
    - /usr/local/share/redoc/templates
```

## Troubleshooting

### Common Issues

1. **Missing Dependencies**
   ```bash
   # Check for missing system dependencies
   which pdftohtml tesseract libreoffice
   ```
   
2. **Permission Errors**
   ```bash
   # Fix permission issues for temporary files
   chmod 777 /tmp/redoc  # Or your configured temp directory
   ```

3. **Docker Issues**
   ```bash
   # Check if Docker is running
   docker ps
   
   # Check container logs
   docker logs <container_id>
   ```

4. **OCR Problems**
   - Ensure Tesseract language packs are installed
   - Check image quality and resolution
   - Try with `--preprocess image` option for better OCR results

## Next Steps

- Try the [Quick Start Guide](quick-start.md) for basic usage
- Learn about [Templates](templates.md) for document generation
- Explore [AI Features](ai.md) for smart document processing
- Check the [API Reference](api.md) for programmatic usage
- Join our [Community](https://github.com/text2doc/redoc/discussions) for support
