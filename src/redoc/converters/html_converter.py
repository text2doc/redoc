"""HTML converter implementation for Redoc."""

from pathlib import Path
from typing import Any, Dict, Optional, Union

from . import register_converter, BaseConverter
from ..exceptions import ConversionError


@register_converter('html')
class HtmlConverter(BaseConverter):
    """Converter for HTML documents."""
    
    def __init__(self):
        self.supported_formats = ['pdf', 'xml', 'json', 'docx', 'epub']
    
    def convert(
        self,
        source: Union[str, Path, Dict],
        output_file: Optional[Union[str, Path]] = None,
        **kwargs
    ) -> Any:
        """Convert to/from HTML format.
        
        Args:
            source: Source file path or template dictionary
            output_file: Optional output file path
            **kwargs: Additional conversion options
                - from_format: Source format if not inferrable from source
                - to_format: Target format if not inferrable from output_file
        """
        try:
            # Handle template input
            if isinstance(source, dict):
                return self._convert_from_template(source, output_file, **kwargs)
                
            source_path = Path(source)
            
            # If output_file is not specified, determine from source
            if output_file is None:
                if 'to_format' not in kwargs:
                    raise ValueError("Either output_file or to_format must be specified")
                to_format = kwargs['to_format']
                output_file = source_path.with_suffix(f'.{to_format}')
            
            output_path = Path(output_file)
            from_format = kwargs.get('from_format', 'html')
            to_format = kwargs.get('to_format', output_path.suffix[1:].lower())
            
            if from_format == 'html':
                return self._convert_from_html(source_path, output_path, to_format, **kwargs)
            else:
                return self._convert_to_html(source_path, output_path, from_format, **kwargs)
                
        except Exception as e:
            raise ConversionError(f"HTML conversion failed: {str(e)}") from e
    
    def _convert_from_html(
        self,
        source_path: Path,
        output_path: Path,
        to_format: str,
        **kwargs
    ) -> Path:
        """Convert from HTML to another format."""
        try:
            from bs4 import BeautifulSoup
            
            # Read the HTML content
            with open(source_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Parse HTML with BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')
            
            if to_format == 'pdf':
                # Convert HTML to PDF using WeasyPrint
                from weasyprint import HTML
                HTML(string=html_content).write_pdf(output_path)
                
            elif to_format == 'docx':
                # Convert HTML to DOCX using python-docx
                from docx import Document
                from docx.shared import Pt
                from htmldocx import HtmlToDocx
                
                doc = Document()
                doc.add_paragraph()  # Add empty paragraph to avoid errors
                
                # Convert HTML to DOCX
                html_parser = HtmlToDocx()
                html_parser.add_html_to_document(html_content, doc)
                
                # Save the document
                doc.save(output_path)
                
            elif to_format == 'epub':
                # Convert HTML to EPUB using ebooklib
                from ebooklib import epub
                from bs4 import BeautifulSoup
                
                # Create a new EPUB book
                book = epub.EpubBook()
                
                # Set metadata
                title = soup.title.string if soup.title else 'Untitled Document'
                book.set_identifier('id123456')
                book.set_title(title)
                book.set_language('en')
                
                # Add content
                chapter = epub.EpubHtml(
                    title='Content',
                    file_name='content.xhtml',
                    lang='en'
                )
                chapter.content = html_content
                book.add_item(chapter)
                
                # Add table of contents
                book.toc = (epub.Link('content.xhtml', 'Content', 'content'),)
                
                # Add navigation files
                book.add_item(epub.EpubNcx())
                book.add_item(epub.EpubNav())
                
                # Create spine
                book.spine = [chapter]
                
                # Write the EPUB file
                epub.write_epub(output_path, book, {})
                
            elif to_format == 'json':
                # Convert HTML to JSON
                import json
                
                # Extract text content and metadata
                result = {
                    'title': soup.title.string if soup.title else None,
                    'text': soup.get_text('\n', strip=True),
                    'links': [a.get('href') for a in soup.find_all('a', href=True)],
                    'images': [img.get('src') for img in soup.find_all('img', src=True)],
                }
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)
                
            elif to_format == 'xml':
                # Convert HTML to well-formed XML
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(str(soup))
            
            return output_path
            
        except ImportError as e:
            raise ConversionError(f"Required dependency not found: {str(e)}") from e
        except Exception as e:
            raise ConversionError(f"Failed to convert HTML to {to_format}: {str(e)}") from e
    
    def _convert_to_html(
        self,
        source_path: Path,
        output_path: Path,
        from_format: str,
        **kwargs
    ) -> Path:
        """Convert from another format to HTML."""
        # This would be implemented by other converters
        raise ConversionError(f"Conversion from {from_format} to HTML not implemented yet")
    
    def _convert_from_template(
        self,
        template: Dict[str, Any],
        output_file: Optional[Union[str, Path]] = None,
        **kwargs
    ) -> Path:
        """Convert a template to HTML."""
        try:
            from jinja2 import Environment, FileSystemLoader
            import json
            
            # Validate template
            if 'template' not in template:
                raise ValueError("Template must contain a 'template' key")
            if 'data' not in template:
                raise ValueError("Template must contain a 'data' key with template variables")
            
            # Set up Jinja2 environment
            template_path = Path(template['template']).parent
            env = Environment(loader=FileSystemLoader(str(template_path)))
            
            # Load template
            template_name = Path(template['template']).name
            jinja_template = env.get_template(template_name)
            
            # Render template with data
            html_content = jinja_template.render(**template['data'])
            
            # If no output file specified, return the HTML content
            if output_file is None:
                return html_content
            
            # Otherwise, write to file
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            return output_path
            
        except Exception as e:
            raise ConversionError(f"Template conversion failed: {str(e)}") from e
    
    def get_supported_formats(self) -> list:
        """Get a list of formats this converter can handle."""
        return self.supported_formats
