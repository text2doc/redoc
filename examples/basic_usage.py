"""
Basic usage example for the Redoc document conversion library.

This example demonstrates how to:
1. Convert between different document formats
2. Use OCR to extract text from images/PDFs
3. Process documents using templates
"""

import os
import sys
from pathlib import Path

# Add the parent directory to the path so we can import redoc
sys.path.insert(0, str(Path(__file__).parent.parent))

from redoc import Redoc

def main():
    # Initialize the Redoc converter
    converter = Redoc()
    
    # Create an examples directory if it doesn't exist
    examples_dir = Path("examples_output")
    examples_dir.mkdir(exist_ok=True)
    
    print("Redoc Document Conversion Examples")
    print("=" * 30)
    
    # Example 1: Convert PDF to text using OCR
    print("\nExample 1: Extracting text from a PDF with OCR")
    print("-" * 50)
    try:
        # This assumes you have a sample PDF in the examples directory
        pdf_path = "samples/sample.pdf"
        if os.path.exists(pdf_path):
            print(f"Processing {pdf_path} with OCR...")
            result = converter.ocr(pdf_path)
            print(f"Extracted text: {result['text'][:200]}...")
            
            # Save the searchable PDF
            output_pdf = examples_dir / "searchable_sample.pdf"
            converter.ocr(pdf_path, output_file=output_pdf)
            print(f"Searchable PDF saved to: {output_pdf}")
        else:
            print(f"Sample PDF not found at {pdf_path}")
            print("Please add a sample PDF to the samples/ directory.")
    except Exception as e:
        print(f"Error in Example 1: {e}")
    
    # Example 2: Convert between formats
    print("\nExample 2: Converting between document formats")
    print("-" * 50)
    try:
        # This would convert a document if the source file exists
        # In a real scenario, you'd have actual files to convert
        print("Conversion example (placeholder - no actual files converted)")
        print("Use: converter.convert('input.pdf', 'html', output_file='output.html')")
    except Exception as e:
        print(f"Error in Example 2: {e}")
    
    # Example 3: Using templates
    print("\nExample 3: Using templates for document generation")
    print("-" * 50)
    try:
        template = {
            "template": "templates/invoice.html",
            "data": {
                "invoice_number": "INV-2023-001",
                "date": "2023-11-15",
                "client": "Acme Corp",
                "items": [
                    {"description": "Web Design Services", "quantity": 10, "price": 100.00},
                    {"description": "Hosting (Annual)", "quantity": 1, "price": 500.00}
                ],
                "tax_rate": 0.23,
                "notes": "Thank you for your business!"
            }
        }
        
        # In a real scenario, you'd have the template file
        print("Template example (placeholder - template file not created)")
        print("Use: converter.convert(template, 'pdf', output_file='invoice.pdf')")
    except Exception as e:
        print(f"Error in Example 3: {e}")
    
    print("\nExamples completed. Check the 'examples_output' directory for results.")

if __name__ == "__main__":
    main()
