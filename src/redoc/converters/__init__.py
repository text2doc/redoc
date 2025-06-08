"""Document format converters for Redoc."""

from typing import Dict, Type, Optional, Union
from pathlib import Path
import importlib
import pkgutil
import inspect
import logging

from ..exceptions import UnsupportedFormatError, ConversionError

logger = logging.getLogger(__name__)

# Dictionary to store registered converters
_CONVERTERS: Dict[str, Type['BaseConverter']] = {}


def register_converter(format_name: str):
    """Decorator to register a converter class for a specific format.
    
    Args:
        format_name: The format name this converter handles (e.g., 'pdf', 'html')
    """
    def decorator(converter_class):
        _CONVERTERS[format_name.lower()] = converter_class
        return converter_class
    return decorator


def get_converter(format_name: str) -> 'BaseConverter':
    """Get a converter instance for the specified format.
    
    Args:
        format_name: The format to get a converter for
        
    Returns:
        An instance of the appropriate converter
        
    Raises:
        UnsupportedFormatError: If no converter is available for the format
    """
    format_name = format_name.lower()
    if format_name not in _CONVERTERS:
        raise UnsupportedFormatError(f"No converter available for format: {format_name}")
    return _CONVERTERS[format_name]()


class BaseConverter:
    """Base class for all document converters.
    
    Subclasses should implement the convert_from and convert_to methods.
    """
    
    def convert(
        self,
        source: Union[str, Path, Dict],
        output_file: Optional[Union[str, Path]] = None,
        **kwargs
    ) -> Any:
        """Convert the source to the target format.
        
        Args:
            source: Source file path or template dictionary
            output_file: Optional output file path
            **kwargs: Additional conversion options
            
        Returns:
            Converted content or path to output file
        """
        raise NotImplementedError("Subclasses must implement convert method")
    
    def get_supported_formats(self) -> list:
        """Get a list of formats this converter can handle."""
        raise NotImplementedError("Subclasses must implement get_supported_formats method")
