"""JSON converter implementation for Redoc."""

import json
from pathlib import Path
from typing import Any, Dict, Optional, Union

from . import register_converter, BaseConverter
from ..exceptions import ConversionError


@register_converter('json')
class JsonConverter(BaseConverter):
    """Converter for JSON documents."""
    
    def __init__(self):
        self.supported_formats = ['pdf', 'html', 'xml', 'yaml', 'csv']
    
    def convert(
        self,
        source: Union[str, Path, Dict],
        output_file: Optional[Union[str, Path]] = None,
        **kwargs
    ) -> Any:
        """Convert to/from JSON format.
        
        Args:
            source: Source file path or dictionary
            output_file: Optional output file path
            **kwargs: Additional conversion options
                - from_format: Source format if not inferrable from source
                - to_format: Target format if not inferrable from output_file
                - indent: Indentation for JSON output
        """
        try:
            # If source is a dictionary, convert it to JSON
            if isinstance(source, dict):
                if output_file is None:
                    output_file = 'output.json'
                output_path = Path(output_file)
                return self._save_json(source, output_path, **kwargs)
                
            source_path = Path(source)
            
            # If output_file is not specified, determine from source
            if output_file is None:
                if 'to_format' not in kwargs:
                    raise ValueError("Either output_file or to_format must be specified")
                to_format = kwargs['to_format']
                output_file = source_path.with_suffix(f'.{to_format}')
            
            output_path = Path(output_file)
            from_format = kwargs.get('from_format', 'json' if source_path.suffix.lower() == '.json' else None)
            to_format = kwargs.get('to_format', output_path.suffix[1:].lower())
            
            if from_format == 'json':
                return self._convert_from_json(source_path, output_path, to_format, **kwargs)
            else:
                return self._convert_to_json(source_path, output_path, from_format, **kwargs)
                
        except Exception as e:
            raise ConversionError(f"JSON conversion failed: {str(e)}") from e
    
    def _convert_from_json(
        self,
        source_path: Path,
        output_path: Path,
        to_format: str,
        **kwargs
    ) -> Path:
        """Convert from JSON to another format."""
        try:
            # Load JSON data
            with open(source_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if to_format == 'html':
                # Convert JSON to HTML table
                from .html_converter import HtmlConverter
                html = self._json_to_html(data, **kwargs)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(html)
                    
            elif to_format == 'pdf':
                # Convert JSON to PDF via HTML
                from .html_converter import HtmlConverter
                html = self._json_to_html(data, **kwargs)
                temp_html = output_path.with_suffix('.html')
                with open(temp_html, 'w', encoding='utf-8') as f:
                    f.write(html)
                
                # Use HTML to PDF conversion
                html_converter = HtmlConverter()
                html_converter.convert(temp_html, output_path, from_format='html', to_format='pdf')
                temp_html.unlink()  # Clean up temporary file
                
            elif to_format == 'xml':
                # Convert JSON to XML
                from dicttoxml import dicttoxml
                from xml.dom.minidom import parseString
                
                xml = dicttoxml(data, custom_root='document', attr_type=False)
                dom = parseString(xml)
                pretty_xml = dom.toprettyxml()
                
                output_path.parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(pretty_xml)
                    
            elif to_format == 'yaml':
                # Convert JSON to YAML
                import yaml
                
                output_path.parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, 'w', encoding='utf-8') as f:
                    yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
                    
            elif to_format == 'csv':
                # Convert JSON to CSV (handles array of flat objects)
                import csv
                
                if not isinstance(data, list):
                    data = [data]
                
                if not data:  # Empty list
                    with open(output_path, 'w', newline='', encoding='utf-8') as f:
                        f.write("")
                    return output_path
                
                # Get fieldnames from the first object
                fieldnames = set()
                for item in data:
                    if isinstance(item, dict):
                        fieldnames.update(item.keys())
                
                fieldnames = sorted(fieldnames)
                
                with open(output_path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    
                    for item in data:
                        if isinstance(item, dict):
                            # Ensure all fields are present
                            row = {field: item.get(field, '') for field in fieldnames}
                            writer.writerow(row)
            
            return output_path
            
        except ImportError as e:
            raise ConversionError(f"Required dependency not found: {str(e)}") from e
        except Exception as e:
            raise ConversionError(f"Failed to convert JSON to {to_format}: {str(e)}") from e
    
    def _convert_to_json(
        self,
        source_path: Path,
        output_path: Path,
        from_format: str,
        **kwargs
    ) -> Path:
        """Convert from another format to JSON."""
        try:
            if from_format == 'csv':
                # Convert CSV to JSON
                import csv
                import json
                
                with open(source_path, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    data = list(reader)
                
                return self._save_json(data, output_path, **kwargs)
                
            elif from_format == 'yaml':
                # Convert YAML to JSON
                import yaml
                
                with open(source_path, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                
                return self._save_json(data, output_path, **kwargs)
                
            elif from_format == 'xml':
                # Convert XML to JSON
                import xmltodict
                
                with open(source_path, 'r', encoding='utf-8') as f:
                    data = xmltodict.parse(f.read())
                
                return self._save_json(data, output_path, **kwargs)
                
            else:
                raise ConversionError(f"Conversion from {from_format} to JSON not implemented")
                
        except ImportError as e:
            raise ConversionError(f"Required dependency not found: {str(e)}") from e
        except Exception as e:
            raise ConversionError(f"Failed to convert {from_format} to JSON: {str(e)}") from e
    
    def _json_to_html(self, data: Any, **kwargs) -> str:
        """Convert JSON data to an HTML representation."""
        from jinja2 import Environment, PackageLoader
        
        env = Environment(loader=PackageLoader('redoc', 'templates'))
        template = env.get_template('json_viewer.html')
        
        return template.render(
            data=data,
            title=kwargs.get('title', 'JSON Viewer'),
            style=kwargs.get('style', 'default')
        )
    
    def _save_json(
        self,
        data: Any,
        output_path: Path,
        **kwargs
    ) -> Path:
        """Save data as JSON to the specified path."""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        indent = kwargs.get('indent', 2)
        ensure_ascii = kwargs.get('ensure_ascii', False)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent, ensure_ascii=ensure_ascii)
        
        return output_path
    
    def get_supported_formats(self) -> list:
        """Get a list of formats this converter can handle."""
        return self.supported_formats
