"""XML converter implementation for Redoc."""

import json
from pathlib import Path
from typing import Any, Dict, Optional, Union
import xml.etree.ElementTree as ET

from . import register_converter, BaseConverter
from ..exceptions import ConversionError


@register_converter('xml')
class XmlConverter(BaseConverter):
    """Converter for XML documents."""
    
    def __init__(self):
        self.supported_formats = ['json', 'html', 'yaml', 'csv', 'pdf']
    
    def convert(
        self,
        source: Union[str, Path, Dict],
        output_file: Optional[Union[str, Path]] = None,
        **kwargs
    ) -> Any:
        """Convert to/from XML format.
        
        Args:
            source: Source file path or dictionary
            output_file: Optional output file path
            **kwargs: Additional conversion options
                - from_format: Source format if not inferrable from source
                - to_format: Target format if not inferrable from output_file
                - root_tag: Root tag name for XML output (default: 'root')
                - item_tag: Item tag name for XML arrays (default: 'item')
        """
        try:
            # If source is a dictionary, convert it to XML
            if isinstance(source, dict):
                if output_file is None:
                    output_file = 'output.xml'
                output_path = Path(output_file)
                return self._dict_to_xml(source, output_path, **kwargs)
                
            source_path = Path(source)
            
            # If output_file is not specified, determine from source
            if output_file is None:
                if 'to_format' not in kwargs:
                    raise ValueError("Either output_file or to_format must be specified")
                to_format = kwargs['to_format']
                output_file = source_path.with_suffix(f'.{to_format}')
            
            output_path = Path(output_file)
            from_format = kwargs.get('from_format', 'xml' if source_path.suffix.lower() == '.xml' else None)
            to_format = kwargs.get('to_format', output_path.suffix[1:].lower())
            
            if from_format == 'xml':
                return self._convert_from_xml(source_path, output_path, to_format, **kwargs)
            else:
                return self._convert_to_xml(source_path, output_path, from_format, **kwargs)
                
        except Exception as e:
            raise ConversionError(f"XML conversion failed: {str(e)}") from e
    
    def _convert_from_xml(
        self,
        source_path: Path,
        output_path: Path,
        to_format: str,
        **kwargs
    ) -> Path:
        """Convert from XML to another format."""
        try:
            # Parse XML
            tree = ET.parse(source_path)
            root = tree.getroot()
            
            # Convert XML to dictionary
            data = self._xml_to_dict(root)
            
            if to_format == 'json':
                # Convert to JSON
                import json
                output_path.parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                    
            elif to_format == 'yaml':
                # Convert to YAML
                import yaml
                output_path.parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, 'w', encoding='utf-8') as f:
                    yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
                    
            elif to_format == 'html':
                # Convert to HTML
                from .html_converter import HtmlConverter
                html = self._xml_to_html(root, **kwargs)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(html)
                    
            elif to_format == 'csv':
                # Convert to CSV (for tabular data)
                self._xml_to_csv(root, output_path, **kwargs)
                
            elif to_format == 'pdf':
                # Convert to PDF via HTML
                from .html_converter import HtmlConverter
                html = self._xml_to_html(root, **kwargs)
                temp_html = output_path.with_suffix('.html')
                with open(temp_html, 'w', encoding='utf-8') as f:
                    f.write(html)
                
                # Use HTML to PDF conversion
                html_converter = HtmlConverter()
                html_converter.convert(temp_html, output_path, from_format='html', to_format='pdf')
                temp_html.unlink()  # Clean up temporary file
            
            return output_path
            
        except ET.ParseError as e:
            raise ConversionError(f"Invalid XML: {str(e)}") from e
        except ImportError as e:
            raise ConversionError(f"Required dependency not found: {str(e)}") from e
        except Exception as e:
            raise ConversionError(f"Failed to convert XML to {to_format}: {str(e)}") from e
    
    def _convert_to_xml(
        self,
        source_path: Path,
        output_path: Path,
        from_format: str,
        **kwargs
    ) -> Path:
        """Convert from another format to XML."""
        try:
            if from_format == 'json':
                # Convert JSON to XML
                import json
                
                with open(source_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                return self._dict_to_xml(data, output_path, **kwargs)
                
            elif from_format == 'yaml':
                # Convert YAML to XML
                import yaml
                
                with open(source_path, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                
                return self._dict_to_xml(data, output_path, **kwargs)
                
            elif from_format == 'csv':
                # Convert CSV to XML
                import csv
                
                with open(source_path, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    data = {'row': list(reader)}
                
                return self._dict_to_xml(data, output_path, **kwargs)
                
            else:
                raise ConversionError(f"Conversion from {from_format} to XML not implemented")
                
        except ImportError as e:
            raise ConversionError(f"Required dependency not found: {str(e)}") from e
        except Exception as e:
            raise ConversionError(f"Failed to convert {from_format} to XML: {str(e)}") from e
    
    def _xml_to_dict(self, element: ET.Element) -> Any:
        """Convert XML element to a Python dictionary."""
        result = {}
        
        # Handle attributes
        if element.attrib:
            result['@attributes'] = element.attrib
        
        # Handle child elements
        children = {}
        
        for child in element:
            child_data = self._xml_to_dict(child)
            
            # If this tag already exists, make it a list
            if child.tag in children:
                if not isinstance(children[child.tag], list):
                    children[child.tag] = [children[child.tag]]
                children[child.tag].append(child_data)
            else:
                children[child.tag] = child_data
        
        # If there are child elements, add them to the result
        if children:
            result.update(children)
        # If no children but there is text content, add it
        elif element.text and element.text.strip():
            result['#text'] = element.text.strip()
        
        return result
    
    def _dict_to_xml(
        self,
        data: Any,
        output_path: Path,
        **kwargs
    ) -> Path:
        """Convert a dictionary to XML and save to file."""
        root_tag = kwargs.get('root_tag', 'root')
        item_tag = kwargs.get('item_tag', 'item')
        
        # Create root element
        root = ET.Element(root_tag)
        
        # Add data to the root
        self._add_dict_to_element(root, data, item_tag=item_tag)
        
        # Create element tree and write to file
        tree = ET.ElementTree(root)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Pretty print XML
        self._indent(root)
        tree.write(
            str(output_path),
            encoding='utf-8',
            xml_declaration=True,
            method='xml',
            short_empty_elements=False
        )
        
        return output_path
    
    def _add_dict_to_element(self, parent: ET.Element, data: Any, item_tag: str = 'item') -> None:
        """Recursively add dictionary data to an XML element."""
        if isinstance(data, dict):
            for key, value in data.items():
                # Handle attributes
                if key == '@attributes':
                    for attr, val in value.items():
                        parent.set(attr, str(val))
                # Handle text content
                elif key == '#text':
                    parent.text = str(value)
                # Handle nested elements
                else:
                    if isinstance(value, list):
                        for item in value:
                            element = ET.SubElement(parent, key)
                            self._add_dict_to_element(element, item, item_tag)
                    else:
                        element = ET.SubElement(parent, key)
                        self._add_dict_to_element(element, value, item_tag)
        elif isinstance(data, list):
            for item in data:
                element = ET.SubElement(parent, item_tag)
                self._add_dict_to_element(element, item, item_tag)
        else:
            parent.text = str(data) if data is not None else ''
    
    def _indent(self, elem: ET.Element, level: int = 0, indent: str = '  ') -> None:
        """Pretty-print XML with proper indentation."""
        i = "\n" + level * indent
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + indent
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                self._indent(elem, level + 1, indent)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i
    
    def _xml_to_html(self, root: ET.Element, **kwargs) -> str:
        """Convert XML to an HTML representation."""
        from jinja2 import Environment, PackageLoader
        
        # Convert XML to a dictionary for templating
        data = self._xml_to_dict(root)
        
        env = Environment(loader=PackageLoader('redoc', 'templates'))
        template = env.get_template('xml_viewer.html')
        
        return template.render(
            data=data,
            title=kwargs.get('title', 'XML Viewer'),
            style=kwargs.get('style', 'default')
        )
    
    def _xml_to_csv(self, root: Path, output_path: Path, **kwargs) -> None:
        """Convert XML to CSV (for tabular data)."""
        import csv
        
        # Find all unique field names
        fieldnames = set()
        rows = []
        
        # For each row element
        for row in root.findall('.//row'):
            row_data = {}
            for child in row:
                fieldnames.add(child.tag)
                row_data[child.tag] = child.text or ''
            rows.append(row_data)
        
        fieldnames = sorted(fieldnames)
        
        # Write CSV
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
    
    def get_supported_formats(self) -> list:
        """Get a list of formats this converter can handle."""
        return self.supported_formats
