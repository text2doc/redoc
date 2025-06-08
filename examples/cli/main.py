"""
Redoc CLI Example

A command-line interface demonstrating Redoc's document conversion capabilities.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, Any, Optional

from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

from redoc import Redoc

# Initialize console for rich output
console = Console()

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Redoc CLI - Document conversion tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  Convert a document:  %(prog)s convert input.html output.pdf
  Use a template:     %(prog)s template data.json --template template.html -o output.pdf
"""
    )
    
    # Subcommands
    subparsers = parser.add_subparsers(dest='command', required=True, help='Command to execute')
    
    # Convert command
    convert_parser = subparsers.add_parser('convert', help='Convert between document formats')
    convert_parser.add_argument('input', help='Input file path')
    convert_parser.add_argument('output', help='Output file path')
    convert_parser.add_argument('--format', help='Output format (default: inferred from output file extension)')
    convert_parser.add_argument('--options', type=json.loads, default={}, 
                              help='Conversion options as JSON string')
    
    # Template command
    template_parser = subparsers.add_parser('template', help='Generate document from template')
    template_parser.add_argument('data_file', help='JSON file with template data')
    template_parser.add_argument('--template', required=True, help='Template file path')
    template_parser.add_argument('-o', '--output', required=True, help='Output file path')
    template_parser.add_argument('--format', help='Output format (default: inferred from output file extension)')
    
    # List formats command
    subparsers.add_parser('formats', help='List supported formats')
    
    return parser.parse_args()

def load_template_data(file_path: str) -> Dict[str, Any]:
    """Load template data from a JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        console.print(f"[red]Error:[/red] Invalid JSON in {file_path}: {e}")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Error loading {file_path}:[/red] {e}")
        sys.exit(1)

def convert_document(args):
    """Handle the convert command."""
    input_path = Path(args.input)
    output_path = Path(args.output)
    
    if not input_path.exists():
        console.print(f"[red]Error:[/red] Input file not found: {input_path}")
        sys.exit(1)
    
    output_format = args.format or output_path.suffix.lstrip('.')
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        task = progress.add_task("Converting document...", total=None)
        
        try:
            converter = Redoc()
            converter.convert(
                str(input_path),
                str(output_path),
                format=output_format,
                **args.options
            )
            progress.stop()
            console.print(f"[green]✓[/green] Successfully created {output_path}")
        except Exception as e:
            progress.stop()
            console.print(f"[red]Error during conversion:[/red] {e}")
            sys.exit(1)

def generate_from_template(args):
    """Handle the template command."""
    template_path = Path(args.template)
    output_path = Path(args.output)
    
    if not template_path.exists():
        console.print(f"[red]Error:[/red] Template file not found: {template_path}")
        sys.exit(1)
    
    output_format = args.format or output_path.suffix.lstrip('.')
    template_data = load_template_data(args.data_file)
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        task = progress.add_task("Generating document from template...", total=None)
        
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                template_content = f.read()
            
            converter = Redoc()
            converter.convert(
                template_content,
                str(output_path),
                format=output_format,
                **template_data
            )
            progress.stop()
            console.print(f"[green]✓[/green] Successfully created {output_path}")
        except Exception as e:
            progress.stop()
            console.print(f"[red]Error during template generation:[/red] {e}")
            sys.exit(1)

def list_formats():
    """List supported formats."""
    # This is a simplified example - in a real app, you would get this from the converter
    formats = [
        {"name": "PDF", "extensions": ["pdf"], "description": "Portable Document Format"},
        {"name": "DOCX", "extensions": ["docx"], "description": "Microsoft Word Document"},
        {"name": "HTML", "extensions": ["html", "htm"], "description": "HyperText Markup Language"},
        {"name": "Markdown", "extensions": ["md", "markdown"], "description": "Lightweight Markup Language"},
        {"name": "Plain Text", "extensions": ["txt"], "description": "Plain Text File"},
    ]
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Format", style="cyan")
    table.add_column("Extensions")
    table.add_column("Description")
    
    for fmt in formats:
        table.add_row(
            fmt["name"],
            ", ".join(fmt["extensions"]),
            fmt["description"]
        )
    
    console.print("\n[bold]Supported Formats:[/bold]")
    console.print(table)

def main():
    """Main entry point."""
    try:
        args = parse_arguments()
        
        if args.command == 'convert':
            convert_document(args)
        elif args.command == 'template':
            generate_from_template(args)
        elif args.command == 'formats':
            list_formats()
            
    except KeyboardInterrupt:
        console.print("\n[red]Operation cancelled by user.[/red]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
