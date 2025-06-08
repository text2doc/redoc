"""Utility functions for the Redoc package."""

from pathlib import Path
from typing import Any, Dict, Optional, Union
import mimetypes
import logging

logger = logging.getLogger(__name__)


def get_file_extension(file_path: Union[str, Path]) -> str:
    """Get the file extension in lowercase without the dot.
    
    Args:
        file_path: Path to the file
        
    Returns:
        File extension in lowercase
    """
    return Path(file_path).suffix[1:].lower()


def guess_file_format(file_path: Union[str, Path]) -> Optional[str]:
    """Guess the file format based on its extension.
    
    Args:
        file_path: Path to the file
        
    Returns:
        Guessed format (e.g., 'pdf', 'html') or None if unknown
    """
    ext = get_file_extension(file_path)
    if not ext:
        return None
    
    # Map of common extensions to formats
    extension_map = {
        'pdf': 'pdf',
        'html': 'html',
        'htm': 'html',
        'xml': 'xml',
        'json': 'json',
        'docx': 'docx',
        'doc': 'doc',
        'epub': 'epub',
        'jpg': 'image',
        'jpeg': 'image',
        'png': 'image',
        'tiff': 'image',
        'tif': 'image',
        'bmp': 'image',
    }
    
    return extension_map.get(ext)


def is_binary_file(file_path: Union[str, Path]) -> bool:
    """Check if a file is binary.
    
    Args:
        file_path: Path to the file
        
    Returns:
        True if the file is binary, False otherwise
    """
    try:
        with open(file_path, 'rb') as f:
            # Read first 1024 bytes to check for binary content
            chunk = f.read(1024)
            # Check for null bytes in text files
            if b'\x00' in chunk:
                return True
            # Check for non-printable bytes
            text_characters = (
                b''.join(bytes((i,)) for i in range(32, 127)) + b'\n\r\t\b\f'
            )
            # Check if any byte is not in text characters
            return bool(chunk.translate(None, text_characters))
    except Exception:
        return True


def validate_template(template: Dict[str, Any]) -> bool:
    """Validate a document template.
    
    Args:
        template: Template dictionary to validate
        
    Returns:
        True if the template is valid
        
    Raises:
        ValueError: If the template is invalid
    """
    if not isinstance(template, dict):
        raise ValueError("Template must be a dictionary")
    
    if 'template' not in template:
        raise ValueError("Template must contain a 'template' key")
    
    template_path = Path(template['template'])
    if not template_path.exists():
        raise ValueError(f"Template file not found: {template_path}")
    
    if 'data' not in template:
        raise ValueError("Template must contain a 'data' key with template variables")
    
    if not isinstance(template['data'], dict):
        raise ValueError("Template data must be a dictionary")
    
    return True


def ensure_directory_exists(path: Union[str, Path]) -> Path:
    """Ensure that the directory for a file path exists.
    
    Args:
        path: File path
        
    Returns:
        Path object with ensured parent directory
    """
    path = Path(path).resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    return path
