"""
Redoc Invoice Template Demo

This script demonstrates bidirectional document conversion using Redoc's template system.
It shows how to:
1. Generate a PDF invoice from a JSON data file and HTML template
2. Extract data from an existing PDF invoice
3. Convert between different document formats
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any, Optional

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from redoc.templates.pdf_handler import PDFTemplateHandler
from redoc.templates.base import TemplateError

# Paths
TEMPLATE_DIR = Path(__file__).parent / "templates"
DATA_DIR = Path(__file__).parent / "data"
OUTPUT_DIR = Path(__file__).parent / "output"

# Ensure output directory exists
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def load_json_data(file_path: Path) -> Dict[str, Any]:
    """Load JSON data from a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading JSON file {file_path}: {e}")
        sys.exit(1)

def generate_invoice() -> None:
    """Generate a PDF invoice from a template and data file."""
    print("\n=== Generating Invoice ===")
    
    # Load invoice data
    data_file = DATA_DIR / "sample_invoice.json"
    print(f"Loading data from {data_file}")
    invoice_data = load_json_data(data_file)
    
    # Initialize PDF template handler
    handler = PDFTemplateHandler(template_dir=str(TEMPLATE_DIR))
    
    # Generate PDF
    output_pdf = OUTPUT_DIR / "generated_invoice.pdf"
    print(f"Generating PDF: {output_pdf}")
    
    try:
        # Add calculated fields to the data
        subtotal = sum(item['quantity'] * item['unit_price'] for item in invoice_data['items'])
        tax_amount = sum(item['quantity'] * item['unit_price'] * item['tax_rate'] 
                        for item in invoice_data['items'])
        total = subtotal + tax_amount - invoice_data.get('discount', 0)
        
        invoice_data.update({
            'subtotal': subtotal,
            'tax_amount': tax_amount,
            'total': total
        })
        
        # Render the template and generate PDF
        handler.render_pdf(
            template_name="invoice.html",
            data=invoice_data,
            output_pdf=str(output_pdf)
        )
        print(f"Successfully generated: {output_pdf}")
        
        # Also generate HTML for reference
        html_output = OUTPUT_DIR / "generated_invoice.html"
        with open(html_output, 'w', encoding='utf-8') as f:
            template = handler.renderer.get_template("invoice.html")
            html_content = template.render(**invoice_data)
            f.write(html_content)
        print(f"Generated HTML version: {html_output}")
        
        return output_pdf
        
    except TemplateError as e:
        print(f"Error generating invoice: {e}")
        sys.exit(1)

def extract_invoice_data(pdf_path: Path) -> Dict[str, Any]:
    """Extract structured data from a PDF invoice."""
    print("\n=== Extracting Data from Invoice ===")
    print(f"Processing PDF: {pdf_path}")
    
    if not pdf_path.exists():
        print(f"Error: File not found: {pdf_path}")
        return {}
    
    try:
        handler = PDFTemplateHandler()
        extracted_data = handler.extract_data(str(pdf_path))
        
        # Save extracted data to JSON
        output_json = OUTPUT_DIR / "extracted_invoice_data.json"
        with open(output_json, 'w', encoding='utf-8') as f:
            json.dump(extracted_data, f, indent=2)
        
        print(f"Extracted data saved to: {output_json}")
        return extracted_data
        
    except Exception as e:
        print(f"Error extracting data from PDF: {e}")
        return {}

def convert_document(
    input_path: Path, 
    output_path: Path, 
    from_format: str = 'pdf', 
    to_format: str = 'html'
) -> None:
    """Convert a document between different formats."""
    print(f"\n=== Converting {from_format.upper()} to {to_format.upper()} ===")
    print(f"Input: {input_path}")
    print(f"Output: {output_path}")
    
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}")
        return
    
    try:
        # In a real implementation, you would use the appropriate converter
        # based on the input and output formats
        if from_format == 'pdf' and to_format == 'html':
            # Simple conversion using pdf2htmlEX or similar
            # This is a placeholder - you'd need to implement the actual conversion
            print(f"Converting {input_path} to HTML (simulated)")
            with open(input_path, 'rb') as f_in, open(output_path, 'w', encoding='utf-8') as f_out:
                f_out.write(f"<!-- Converted from {input_path.name} -->\n")
                f_out.write("<html><body>")
                f_out.write("<h1>Converted Document</h1>")
                f_out.write(f"<p>This is a simulated conversion from {from_format} to {to_format}.</p>")
                f_out.write("</body></html>")
        else:
            print(f"Conversion from {from_format} to {to_format} not implemented in this demo.")
            return
            
        print(f"Successfully converted to: {output_path}")
        
    except Exception as e:
        print(f"Error during conversion: {e}")

def main():
    """Run the demo script."""
    print("=" * 50)
    print("Redoc Document Conversion Demo")
    print("=" * 50)
    
    # 1. Generate a PDF invoice from template and data
    pdf_path = generate_invoice()
    
    # 2. Extract data from the generated PDF
    if pdf_path and pdf_path.exists():
        extracted_data = extract_invoice_data(pdf_path)
        
        # 3. Demonstrate document conversion
        if extracted_data:
            # Convert the extracted data to a different format
            output_html = OUTPUT_DIR / "converted_invoice.html"
            convert_document(pdf_path, output_html, 'pdf', 'html')
    
    print("\nDemo completed!")
    print(f"Check the '{OUTPUT_DIR}' directory for generated files.")

if __name__ == "__main__":
    main()
