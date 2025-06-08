# CLI Example

This example demonstrates how to use Redoc from the command line.

## Features

- Convert between document formats
- Generate documents from templates
- Process multiple files
- Configure output options

## Usage

```bash
# Install dependencies
pip install -r requirements.txt

# Show help
python main.py --help

# Convert a document
python main.py convert input.html output.pdf

# Use a template
python main.py template data.json --template template.html -o output.pdf
```

## Examples

### Convert HTML to PDF
```bash
python main.py convert input.html output.pdf
```

### Generate from Template
```bash
python main.py template data.json --template template.html -o output.pdf
```

### Process Multiple Files
```bash
# Convert all HTML files in a directory to PDF
for f in documents/*.html; do
  python main.py convert "$f" "output/$(basename "$f" .html).pdf"
done
```
