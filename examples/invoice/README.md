# Redoc Invoice Example

This example demonstrates how to use Redoc's template system to generate professional invoices with bidirectional document conversion capabilities.

## Features

- Generate PDF and HTML invoices from JSON data
- Customizable invoice template using HTML/CSS
- Extract structured data from existing invoices
- Convert between different document formats (PDF, HTML, JSON)
- Support for multiple line items, taxes, and discounts
- Professional styling with responsive design

## Prerequisites

- Python 3.9+
- Redoc package installed
- Required dependencies (will be installed automatically with Redoc)

## Installation

1. Clone the Redoc repository:
   ```bash
   git clone https://github.com/text2doc/redoc.git
   cd redoc
   ```

2. Install the package in development mode:
   ```bash
   pip install -e .
   ```

3. Install additional development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

## Directory Structure

```
invoice/
├── README.md                 # This file
├── demo.py                   # Demo script
├── data/
│   └── sample_invoice.json  # Sample invoice data
├── templates/
│   └── invoice.html        # Invoice HTML template
└── output/                  # Generated files will be saved here
```

## Usage

### 1. Generate an Invoice

Run the demo script to generate a PDF invoice from the sample data:

```bash
python examples/invoice/demo.py
```

This will:
1. Load the sample invoice data from `data/sample_invoice.json`
2. Generate a PDF invoice in the `output/` directory
3. Create an HTML version of the invoice
4. Attempt to extract data from the generated PDF
5. Demonstrate document format conversion

### 2. Customize the Template

Edit the template file at `templates/invoice.html` to customize the invoice design. The template uses:

- **Jinja2** templating syntax
- **CSS** for styling
- **Responsive design** that works on different screen sizes

### 3. Use Your Own Data

1. Create a JSON file with your invoice data following the same structure as `sample_invoice.json`
2. Update the `demo.py` script to use your data file
3. Run the script to generate your custom invoice

### 4. Extract Data from Existing Invoices

The example includes a basic implementation for extracting data from PDF invoices. To use it:

```python
from redoc.templates.pdf_handler import PDFTemplateHandler

handler = PDFTemplateHandler()
extracted_data = handler.extract_data("path/to/your/invoice.pdf")
print(extracted_data)
```

## Template Variables

The invoice template expects the following variables:

### Required Variables
- `invoice_number`: Unique invoice identifier
- `issue_date`: Date the invoice was issued
- `due_date`: Payment due date
- `company`: Dictionary with company details (name, address, etc.)
- `client`: Dictionary with client details
- `items`: List of invoice line items

### Optional Variables
- `status`: Invoice status (draft, sent, paid, etc.)
- `currency`: Currency symbol (default: '$')
- `notes`: Additional notes
- `terms`: Payment terms
- `discount`: Discount amount
- `payment_instructions`: Instructions for payment
- `bank_info`: Bank account details

## Extending the Example

### Add New Templates
1. Create a new HTML template in the `templates/` directory
2. Update the demo script to use your new template

### Support Additional Formats
1. Create a new template handler class (similar to `PDFTemplateHandler`)
2. Implement the required methods for your format
3. Update the demo script to use your new handler

## License

This example is part of the Redoc project and is licensed under the Apache 2.0 License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
