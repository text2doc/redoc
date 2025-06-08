"""PDF template handler with bidirectional document-data conversion."""

import json
import tempfile
from pathlib import Path
from typing import Dict, Any, Optional, Type, Union
from dataclasses import dataclass, field
from pydantic import BaseModel, Field

from ..converters.pdf_converter import PDFConverter
from .base import TemplateManager, TemplateError, TemplateValidationError

class PDFTemplateData(BaseModel):
    """Base model for PDF template data."""
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Document metadata (author, title, etc.)"
    )
    content: Dict[str, Any] = Field(
        default_factory=dict,
        description="Main content sections of the document"
    )
    styles: Dict[str, Any] = Field(
        default_factory=dict,
        description="Styling information"
    )


class PDFTemplateHandler(TemplateManager[PDFTemplateData]):
    """Handler for PDF templates with bidirectional conversion."""
    
    def __init__(self, template_dir: Optional[str] = None):
        """Initialize PDF template handler.
        
        Args:
            template_dir: Directory containing PDF templates
        """
        super().__init__(PDFTemplateData, template_dir)
        self.pdf_converter = PDFConverter()
    
    def render_pdf(
        self,
        template_name: str,
        data: Dict[str, Any],
        output_pdf: str,
        **kwargs
    ) -> str:
        """Render a PDF from a template and data.
        
        Args:
            template_name: Name of the HTML template file
            data: Data to render in the template
            output_pdf: Path to save the generated PDF
            **kwargs: Additional arguments for PDF conversion
            
        Returns:
            Path to the generated PDF file
        """
        # First render HTML from template
        html_content = self.render_template(template_name, data)
        
        # Save HTML to temp file
        with tempfile.NamedTemporaryFile(suffix='.html', delete=False, mode='w') as f:
            f.write(html_content)
            temp_html = f.name
        
        try:
            # Convert HTML to PDF
            self.pdf_converter.convert(
                temp_html,
                output_pdf,
                from_format='html',
                to_format='pdf',
                **kwargs
            )
            return output_pdf
        finally:
            # Clean up temp file
            Path(temp_html).unlink(missing_ok=True)
    
    def extract_data(
        self,
        pdf_path: str,
        template_name: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Extract structured data from a PDF document.
        
        Args:
            pdf_path: Path to the PDF file
            template_name: Optional template name to guide extraction
            **kwargs: Additional arguments for PDF processing
            
        Returns:
            Extracted data as dictionary
        """
        try:
            # First convert PDF to HTML
            with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as f:
                temp_html = f.name
            
            self.pdf_converter.convert(
                pdf_path,
                temp_html,
                from_format='pdf',
                to_format='html',
                **kwargs
            )
            
            # Read the HTML content
            html_content = Path(temp_html).read_text(encoding='utf-8')
            
            # Here you would parse the HTML and extract structured data
            # This is a simplified example - you might want to use BeautifulSoup
            # or another HTML parser for more complex documents
            
            # For now, just return the HTML content in a structured format
            return {
                "metadata": {
                    "source": pdf_path,
                    "pages": self._count_pdf_pages(pdf_path)
                },
                "content": {
                    "html": html_content,
                    "text": self._extract_text_from_html(html_content)
                }
            }
            
        except Exception as e:
            raise TemplateError(f"Failed to extract data from PDF: {str(e)}") from e
        finally:
            # Clean up temp file
            Path(temp_html).unlink(missing_ok=True)
    
    def _count_pdf_pages(self, pdf_path: str) -> int:
        """Count the number of pages in a PDF file."""
        try:
            # This is a placeholder - you might want to use PyPDF2 or similar
            # for more accurate page counting
            return 1
        except Exception:
            return 0
    
    def _extract_text_from_html(self, html_content: str) -> str:
        """Extract plain text from HTML content."""
        try:
            # This is a simplified example - consider using BeautifulSoup
            # for more robust HTML parsing
            import re
            from html import unescape
            
            # Remove script and style elements
            text = re.sub(r'<script.*?>.*?</script>', '', html_content, flags=re.DOTALL)
            text = re.sub(r'<style.*?>.*?</style>', '', text, flags=re.DOTALL)
            
            # Remove HTML tags
            text = re.sub(r'<[^>]+>', ' ', text)
            
            # Convert HTML entities
            text = unescape(text)
            
            # Normalize whitespace
            text = ' '.join(text.split())
            
            return text
        except Exception:
            return ""
