"""Base template handler for document generation."""

import json
from pathlib import Path
from typing import Dict, Any, Optional, Type, TypeVar, Generic
from dataclasses import dataclass, asdict
import jinja2
from pydantic import BaseModel, ValidationError

T = TypeVar('T', bound=BaseModel)

class TemplateError(Exception):
    """Base exception for template-related errors."""
    pass

class TemplateValidationError(TemplateError):
    """Raised when template data validation fails."""
    pass

class TemplateRenderer:
    """Base class for rendering templates with data."""
    
    def __init__(self, template_dir: Optional[str] = None):
        """Initialize template renderer with optional template directory.
        
        Args:
            template_dir: Directory containing template files
        """
        self.template_dir = Path(template_dir) if template_dir else None
        self.env = self._create_environment()
    
    def _create_environment(self) -> jinja2.Environment:
        """Create and configure Jinja2 environment."""
        loader = jinja2.FileSystemLoader(str(self.template_dir)) if self.template_dir else None
        env = jinja2.Environment(
            loader=loader,
            autoescape=jinja2.select_autoescape(),
            trim_blocks=True,
            lstrip_blocks=True
        )
        
        # Add custom filters and globals here
        env.filters['tojson'] = json.dumps
        
        return env
    
    def get_template(self, template_name: str) -> jinja2.Template:
        """Get a template by name.
        
        Args:
            template_name: Name of the template file
            
        Returns:
            jinja2.Template: Loaded template
            
        Raises:
            TemplateError: If template cannot be loaded
        """
        try:
            return self.env.get_template(template_name)
        except jinja2.TemplateNotFound as e:
            raise TemplateError(f"Template not found: {template_name}") from e
        except Exception as e:
            raise TemplateError(f"Error loading template {template_name}: {str(e)}") from e


class TemplateManager(Generic[T]):
    """Manages templates and their associated data models."""
    
    def __init__(self, model_class: Type[T], template_dir: Optional[str] = None):
        """Initialize template manager with data model and template directory.
        
        Args:
            model_class: Pydantic model class for data validation
            template_dir: Directory containing template files
        """
        self.model_class = model_class
        self.renderer = TemplateRenderer(template_dir)
    
    def validate_data(self, data: Dict[str, Any]) -> T:
        """Validate input data against the model.
        
        Args:
            data: Input data to validate
            
        Returns:
            Validated model instance
            
        Raises:
            TemplateValidationError: If validation fails
        """
        try:
            return self.model_class(**data)
        except ValidationError as e:
            raise TemplateValidationError(f"Data validation failed: {str(e)}") from e
    
    def render_template(
        self,
        template_name: str,
        data: Dict[str, Any],
        output_path: Optional[str] = None
    ) -> str:
        """Render a template with the provided data.
        
        Args:
            template_name: Name of the template file
            data: Data to render the template with
            output_path: Optional path to save rendered output
            
        Returns:
            Rendered template as string
            
        Raises:
            TemplateError: If template rendering fails
        """
        try:
            # Validate input data
            model = self.validate_data(data)
            
            # Get and render template
            template = self.renderer.get_template(template_name)
            rendered = template.render(**model.dict())
            
            # Save to file if output path is provided
            if output_path:
                output_path = Path(output_path)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_text(rendered, encoding='utf-8')
                
            return rendered
            
        except Exception as e:
            raise TemplateError(f"Error rendering template {template_name}: {str(e)}") from e
    
    def extract_data(self, document_path: str) -> Dict[str, Any]:
        """Extract structured data from a document.
        
        Args:
            document_path: Path to the document file
            
        Returns:
            Extracted data as dictionary
            
        Raises:
            NotImplementedError: Must be implemented by subclasses
        """
        raise NotImplementedError("Data extraction must be implemented by subclasses")
