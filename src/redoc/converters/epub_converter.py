"""EPUB converter implementation for Redoc."""

import json
import os
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union, BinaryIO

from . import register_converter, BaseConverter
from ..exceptions import ConversionError


@register_converter('epub')
class EpubConverter(BaseConverter):
    """Converter for EPUB e-book format."""
    
    def __init__(self):
        self.supported_formats = ['pdf', 'html', 'txt', 'mobi', 'azw3']
    
    def convert(
        self,
        source: Union[str, Path, Dict],
        output_file: Optional[Union[str, Path]] = None,
        **kwargs
    ) -> Any:
        """Convert to/from EPUB format.
        
        Args:
            source: Source file path or template dictionary
            output_file: Optional output file path
            **kwargs: Additional conversion options
                - from_format: Source format if not inferrable from source
                - to_format: Target format if not inferrable from output_file
                - title: Title for the EPUB (when creating new)
                - author: Author for the EPUB (when creating new)
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
            from_format = kwargs.get('from_format', 'epub' if source_path.suffix.lower() == '.epub' else None)
            to_format = kwargs.get('to_format', output_path.suffix[1:].lower())
            
            if from_format == 'epub':
                return self._convert_from_epub(source_path, output_path, to_format, **kwargs)
            else:
                return self._convert_to_epub(source_path, output_path, from_format, **kwargs)
                
        except Exception as e:
            raise ConversionError(f"EPUB conversion failed: {str(e)}") from e
    
    def _convert_from_epub(
        self,
        source_path: Path,
        output_path: Path,
        to_format: str,
        **kwargs
    ) -> Path:
        """Convert from EPUB to another format."""
        try:
            if to_format == 'pdf':
                # Convert EPUB to PDF using ebook-convert (Calibre)
                return self._convert_with_calibre(source_path, output_path, 'pdf', **kwargs)
                
            elif to_format == 'html':
                # Convert EPUB to HTML
                return self._epub_to_html(source_path, output_path, **kwargs)
                
            elif to_format == 'txt':
                # Convert EPUB to plain text
                return self._epub_to_text(source_path, output_path, **kwargs)
                
            elif to_format in ['mobi', 'azw3']:
                # Convert between ebook formats using Calibre
                return self._convert_with_calibre(source_path, output_path, to_format, **kwargs)
                
            else:
                raise ConversionError(f"Conversion from EPUB to {to_format} not supported")
            
        except Exception as e:
            raise ConversionError(f"Failed to convert EPUB to {to_format}: {str(e)}") from e
    
    def _convert_to_epub(
        self,
        source_path: Path,
        output_path: Path,
        from_format: str,
        **kwargs
    ) -> Path:
        """Convert from another format to EPUB."""
        try:
            if from_format == 'html':
                # Convert HTML to EPUB
                return self._html_to_epub(source_path, output_path, **kwargs)
                
            elif from_format == 'txt':
                # Convert plain text to EPUB
                return self._text_to_epub(source_path, output_path, **kwargs)
                
            elif from_format in ['pdf', 'docx', 'mobi', 'azw3']:
                # Convert between formats using Calibre
                return self._convert_with_calibre(source_path, output_path, 'epub', **kwargs)
                
            else:
                raise ConversionError(f"Conversion from {from_format} to EPUB not implemented")
                
        except Exception as e:
            raise ConversionError(f"Failed to convert {from_format} to EPUB: {str(e)}") from e
    
    def _epub_to_html(
        self,
        source_path: Path,
        output_path: Path,
        **kwargs
    ) -> Path:
        """Convert EPUB to HTML."""
        try:
            import ebooklib
            from ebooklib import epub
            from bs4 import BeautifulSoup
            
            # Read the EPUB file
            book = epub.read_epub(str(source_path))
            
            # Create a new BeautifulSoup document for the output
            soup = BeautifulSoup('', 'html.parser')
            html = soup.new_tag('html')
            soup.append(html)
            
            # Add head and body
            head = soup.new_tag('head')
            html.append(head)
            
            title = soup.new_tag('title')
            title.string = book.get_metadata('DC', 'title')[0][0] if book.get_metadata('DC', 'title') else 'EPUB Export'
            head.append(title)
            
            # Add CSS
            style = soup.new_tag('style')
            style.string = """
                body { font-family: Arial, sans-serif; line-height: 1.6; margin: 40px; max-width: 800px; margin: 0 auto; }
                h1, h2, h3, h4, h5, h6 { color: #2c3e50; margin-top: 1.5em; }
                p { margin: 1em 0; text-align: justify; }
                img { max-width: 100%; height: auto; }
                .toc { margin: 20px 0; padding: 10px; background: #f5f5f5; border-radius: 5px; }
                .toc ul { list-style-type: none; padding-left: 20px; }
                .toc a { text-decoration: none; color: #3498db; }
                .toc a:hover { text-decoration: underline; }
                .page-break { page-break-after: always; }
            """
            head.append(style)
            
            body = soup.new_tag('body')
            html.append(body)
            
            # Add title
            if title.string:
                h1 = soup.new_tag('h1')
                h1.string = title.string
                body.append(h1)
            
            # Add author if available
            authors = book.get_metadata('DC', 'creator')
            if authors:
                p = soup.new_tag('p', style='font-style: italic; color: #666;')
                p.string = f"Author: {', '.join(a[0] for a in authors)}"
                body.append(p)
            
            # Add table of contents
            self._add_epub_toc(book, body, soup)
            
            # Add content
            for item in book.get_items():
                if item.get_type() == ebooklib.ITEM_DOCUMENT:
                    # Parse the content
                    item_soup = BeautifulSoup(item.get_content(), 'html.parser')
                    
                    # Add a page break before each chapter
                    if body.contents:  # Don't add at the very beginning
                        hr = soup.new_tag('hr', **{'class': 'page-break'})
                        body.append(hr)
                    
                    # Add the content
                    body.append(item_soup)
            
            # Write the output file
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(soup.prettify())
            
            return output_path
            
        except ImportError as e:
            raise ConversionError(
                "Required packages not found. Install with: "
                "pip install EbookLib beautifulsoup4"
            ) from e
        except Exception as e:
            raise ConversionError(f"Failed to convert EPUB to HTML: {str(e)}") from e
    
    def _add_epub_toc(
        self,
        book: 'epub.EpubBook',
        body: 'BeautifulSoup',
        soup: 'BeautifulSoup'
    ) -> None:
        """Add table of contents to the HTML output."""
        try:
            # Create TOC div
            toc_div = soup.new_tag('div', **{'class': 'toc'})
            h2 = soup.new_tag('h2')
            h2.string = 'Table of Contents'
            toc_div.append(h2)
            
            # Create TOC list
            toc_list = soup.new_tag('ul')
            
            # Add TOC items
            for item in book.toc:
                self._add_toc_item(item, toc_list, soup)
            
            toc_div.append(toc_list)
            body.append(toc_div)
            
        except Exception as e:
            # If TOC generation fails, just continue without it
            pass
    
    def _add_toc_item(
        self,
        item: Any,
        parent: 'BeautifulSoup',
        soup: 'BeautifulSoup'
    ) -> None:
        """Recursively add TOC items."""
        li = soup.new_tag('li')
        
        # Create link if href exists
        if hasattr(item, 'href') and item.href:
            a = soup.new_tag('a', href=f"#{item.href}")
            a.string = item.title
            li.append(a)
        else:
            span = soup.new_tag('span')
            span.string = item.title if hasattr(item, 'title') else 'Untitled'
            li.append(span)
        
        # Add sub-items if they exist
        if hasattr(item, 'items') and item.items:
            sub_ul = soup.new_tag('ul')
            for sub_item in item.items:
                self._add_toc_item(sub_item, sub_ul, soup)
            li.append(sub_ul)
        
        parent.append(li)
    
    def _epub_to_text(
        self,
        source_path: Path,
        output_path: Path,
        **kwargs
    ) -> Path:
        """Convert EPUB to plain text."""
        try:
            # First convert to HTML
            temp_html = output_path.with_suffix('.html')
            self._epub_to_html(source_path, temp_html, **kwargs)
            
            # Then convert HTML to text
            from bs4 import BeautifulSoup
            
            with open(temp_html, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f, 'html.parser')
            
            # Remove scripts and styles
            for script in soup(['script', 'style']):
                script.decompose()
            
            # Get text
            text = soup.get_text()
            
            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split('  '))
            text = '\n'.join(chunk for chunk in chunks if chunk)
            
            # Write to output file
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(text)
            
            # Clean up temporary file
            try:
                temp_html.unlink()
            except:
                pass
            
            return output_path
            
        except Exception as e:
            # If HTML conversion fails, try a simpler approach
            try:
                import ebooklib
                from ebooklib import epub
                
                # Read the EPUB file
                book = epub.read_epub(str(source_path))
                
                # Extract text from all items
                text_parts = []
                for item in book.get_items():
                    if item.get_type() == ebooklib.ITEM_DOCUMENT:
                        from bs4 import BeautifulSoup
                        soup = BeautifulSoup(item.get_content(), 'html.parser')
                        text_parts.append(soup.get_text('\n', strip=True))
                
                # Combine text parts
                text = '\n\n'.join(text_parts)
                
                # Write to output file
                output_path.parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(text)
                
                return output_path
                
            except Exception as e2:
                raise ConversionError(
                    f"Failed to convert EPUB to text: {str(e)}; Fallback also failed: {str(e2)}"
                ) from e2
    
    def _html_to_epub(
        self,
        source_path: Path,
        output_path: Path,
        **kwargs
    ) -> Path:
        """Convert HTML to EPUB."""
        try:
            from ebooklib import epub
            from bs4 import BeautifulSoup
            
            # Read HTML content
            with open(source_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Parse HTML
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Create a new EPUB book
            book = epub.EpubBook()
            
            # Set metadata
            title = kwargs.get('title', soup.title.string if soup.title else 'Untitled Document')
            book.set_title(title)
            
            author = kwargs.get('author', 'Unknown')
            book.add_author(author)
            
            book.set_identifier('id' + str(hash(title)))
            book.set_language(kwargs.get('language', 'en'))
            
            # Create a chapter
            chapter = epub.EpubHtml(
                title='Content',
                file_name='content.xhtml',
                lang=kwargs.get('language', 'en')
            )
            
            # Set the content (preserve the HTML structure)
            chapter.content = str(soup.body) if soup.body else str(soup)
            
            # Add the chapter to the book
            book.add_item(chapter)
            
            # Add table of contents
            book.toc = (epub.Link('content.xhtml', 'Content', 'content'),)
            
            # Add navigation files
            book.add_item(epub.EpubNcx())
            book.add_item(epub.EpubNav())
            
            # Create spine
            book.spine = ['nav', chapter]
            
            # Write the EPUB file
            output_path.parent.mkdir(parents=True, exist_ok=True)
            epub.write_epub(str(output_path), book, {})
            
            return output_path
            
        except ImportError as e:
            raise ConversionError(
                "Required packages not found. Install with: "
                "pip install EbookLib beautifulsoup4"
            ) from e
        except Exception as e:
            raise ConversionError(f"Failed to convert HTML to EPUB: {str(e)}") from e
    
    def _text_to_epub(
        self,
        source_path: Path,
        output_path: Path,
        **kwargs
    ) -> Path:
        """Convert plain text to EPUB."""
        try:
            # Read text content
            with open(source_path, 'r', encoding='utf-8') as f:
                text_content = f.read()
            
            # Create a temporary HTML file
            with tempfile.NamedTemporaryFile(suffix='.html', mode='w', delete=False, encoding='utf-8') as f:
                f.write(f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>{kwargs.get('title', 'Text Document')}</title>
                    <meta charset="utf-8">
                </head>
                <body>
                    <pre>{text_content}</pre>
                </body>
                </html>
                """)
                temp_html = f.name
            
            try:
                # Convert HTML to EPUB
                return self._html_to_epub(
                    Path(temp_html),
                    output_path,
                    **kwargs
                )
            finally:
                # Clean up temporary file
                try:
                    os.unlink(temp_html)
                except:
                    pass
                    
        except Exception as e:
            raise ConversionError(f"Failed to convert text to EPUB: {str(e)}") from e
    
    def _convert_with_calibre(
        self,
        source_path: Path,
        output_path: Path,
        target_format: str,
        **kwargs
    ) -> Path:
        """Convert between ebook formats using Calibre's ebook-convert."""
        try:
            import subprocess
            
            # Check if ebook-convert is available
            try:
                subprocess.run(
                    ['ebook-convert', '--version'],
                    check=True,
                    capture_output=True,
                    text=True
                )
            except (FileNotFoundError, subprocess.CalledProcessError):
                raise ConversionError(
                    "Calibre's ebook-convert tool is required for this conversion. "
                    "Please install Calibre from https://calibre-ebook.com/"
                )
            
            # Create output directory if it doesn't exist
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Run ebook-convert
            cmd = [
                'ebook-convert',
                str(source_path),
                str(output_path),
                '--output-profile', 'tablet',  # Optimize for tablet reading
            ]
            
            # Add title if provided
            if 'title' in kwargs:
                cmd.extend(['--title', str(kwargs['title'])])
            
            # Add author if provided
            if 'author' in kwargs:
                cmd.extend(['--authors', str(kwargs['author'])])
            
            # Run the command
            result = subprocess.run(
                cmd,
                check=True,
                capture_output=True,
                text=True
            )
            
            if not output_path.exists():
                raise ConversionError(
                    f"Conversion failed: {result.stderr or 'Unknown error'}"
                )
            
            return output_path
            
        except subprocess.CalledProcessError as e:
            raise ConversionError(
                f"ebook-convert failed with return code {e.returncode}: {e.stderr}"
            ) from e
        except Exception as e:
            raise ConversionError(f"Failed to convert with Calibre: {str(e)}") from e
    
    def _convert_from_template(
        self,
        template: Dict[str, Any],
        output_file: Optional[Union[str, Path]] = None,
        **kwargs
    ) -> Path:
        """Convert a template to EPUB."""
        try:
            from ebooklib import epub
            from bs4 import BeautifulSoup
            
            # Create a new EPUB book
            book = epub.EpubBook()
            
            # Set metadata
            title = template.get('title', 'Untitled Document')
            book.set_title(title)
            
            authors = template.get('authors', [])
            if isinstance(authors, str):
                authors = [authors]
            for author in authors:
                book.add_author(author)
            
            book.set_identifier(template.get('id', f'id{hash(title)}'))
            book.set_language(template.get('language', 'en'))
            
            # Add cover image if provided
            if 'cover_image' in template:
                try:
                    cover_path = Path(template['cover_image'])
                    if cover_path.exists():
                        with open(cover_path, 'rb') as f:
                            book.set_cover('cover.jpg', f.read())
                except Exception as e:
                    # If cover image can't be added, continue without it
                    pass
            
            # Create chapters from content
            chapters = []
            toc = []
            
            for i, chapter_data in enumerate(template.get('chapters', [])):
                if not isinstance(chapter_data, dict):
                    continue
                
                chapter_title = chapter_data.get('title', f'Chapter {i+1}')
                chapter_content = chapter_data.get('content', '')
                
                # Create chapter
                chapter = epub.EpubHtml(
                    title=chapter_title,
                    file_name=f'chapter_{i+1}.xhtml',
                    lang=template.get('language', 'en')
                )
                
                # Add content (wrap in proper HTML structure)
                soup = BeautifulSoup('<div>', 'html.parser')
                div = soup.div
                
                # Add title
                h1 = soup.new_tag('h1')
                h1.string = chapter_title
                div.append(h1)
                
                # Add content
                content_soup = BeautifulSoup(chapter_content, 'html.parser')
                div.append(content_soup)
                
                chapter.content = str(soup)
                
                # Add to book
                book.add_item(chapter)
                chapters.append(chapter)
                
                # Add to TOC
                toc.append(chapter)
            
            # Add table of contents
            book.toc = tuple(toc)
            
            # Add navigation files
            book.add_item(epub.EpubNcx())
            book.add_item(epub.EpubNav())
            
            # Create spine
            book.spine = ['nav']
            book.spine.extend(chapters)
            
            # Write the EPUB file
            if output_file is None:
                output_file = 'output.epub'
            
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            epub.write_epub(str(output_path), book, {})
            
            return output_path
            
        except ImportError as e:
            raise ConversionError(
                "Required packages not found. Install with: "
                "pip install EbookLib beautifulsoup4"
            ) from e
        except Exception as e:
            raise ConversionError(f"Template conversion failed: {str(e)}") from e
    
    def get_supported_formats(self) -> list:
        """Get a list of formats this converter can handle."""
        return self.supported_formats
