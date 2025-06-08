"""Advanced example of using Redoc with templates and custom converters."""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

from redoc import Redoc

class AdvancedRedocExample:
    """Advanced example demonstrating Redoc features."""
    
    def __init__(self):
        """Initialize the example."""
        self.converter = Redoc()
        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)
    
    def load_template(self, template_name: str) -> str:
        """Load a template from the templates directory."""
        template_path = Path("templates") / template_name
        return template_path.read_text(encoding="utf-8")
    
    def generate_report(self, data: Dict[str, Any]) -> Dict[str, str]:
        """Generate a report in multiple formats."""
        # Load the template
        template = self.load_template("report.html")
        
        # Add timestamp
        data["generated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Generate outputs
        outputs = {}
        base_name = f"report_{data.get('report_id', '1')}"
        
        # Generate PDF
        pdf_path = self.output_dir / f"{base_name}.pdf"
        self.converter.convert(
            template,
            pdf_path,
            format="html",
            **data
        )
        outputs["pdf"] = str(pdf_path)
        
        # Generate HTML
        html_path = self.output_dir / f"{base_name}.html"
        self.converter.convert(
            template,
            html_path,
            format="html",
            **data
        )
        outputs["html"] = str(html_path)
        
        # Save data as JSON
        json_path = self.output_dir / f"{base_name}.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        outputs["json"] = str(json_path)
        
        return outputs

def main():
    """Run the advanced example."""
    example = AdvancedRedocExample()
    
    # Sample data for the report
    report_data = {
        "report_id": "001",
        "title": "Quarterly Financial Report",
        "period": "Q2 2025",
        "sections": [
            {"title": "Revenue", "value": "$1,250,000", "trend": "+12%"},
            {"title": "Expenses", "value": "$850,000", "trend": "+5%"},
            {"title": "Profit", "value": "$400,000", "trend": "+25%"},
        ],
        "notes": "All values are in USD. Trend is compared to previous quarter."
    }
    
    try:
        print("Generating report...")
        outputs = example.generate_report(report_data)
        
        print("\nGenerated files:")
        for format_name, path in outputs.items():
            print(f"- {format_name.upper()}: {path}")
            
    except Exception as e:
        print(f"Error generating report: {e}")
        raise

if __name__ == "__main__":
    main()
