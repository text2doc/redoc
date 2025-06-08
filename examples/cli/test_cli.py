"""Tests for the CLI example."""

import json
import os
import subprocess
import sys
import unittest
from pathlib import Path


class TestCLI(unittest.TestCase):
    """Test cases for the CLI example."""

    @classmethod
    def setUpClass(cls):
        """Set up test environment."""
        cls.test_dir = Path(__file__).parent
        cls.output_dir = cls.test_dir / "output"
        cls.output_dir.mkdir(exist_ok=True, parents=True)  # Create parent directories if needed
        
        # Path to the main script
        cls.script_path = cls.test_dir / "main.py"
        
        # Test files
        cls.template_path = cls.test_dir / "templates" / "invoice.html"
        cls.data_path = cls.test_dir / "data" / "invoice_data.json"
        
        # Ensure test files exist
        if not cls.template_path.exists():
            raise FileNotFoundError(f"Template file not found: {cls.template_path}")
        if not cls.data_path.exists():
            raise FileNotFoundError(f"Data file not found: {cls.data_path}")
    
    def setUp(self):
        """Set up before each test."""
        # Clear output directory before each test
        for file in self.output_dir.glob("*"):
            if file.is_file():
                file.unlink()
    
    def run_command(self, args):
        """Run a command and return the result."""
        cmd = [sys.executable, str(self.script_path)] + args
        result = subprocess.run(
            cmd,
            cwd=str(self.test_dir),
            capture_output=True,
            text=True,
            check=False
        )
        return result
    
    def test_help(self):
        """Test help command."""
        result = self.run_command(["--help"])
        self.assertEqual(result.returncode, 0)
        self.assertIn("usage:", result.stdout)
    
    def test_formats_command(self):
        """Test formats command."""
        result = self.run_command(["formats"])
        self.assertEqual(result.returncode, 0)
        self.assertIn("Supported Formats", result.stdout)
    
    def test_template_command(self):
        """Test template command."""
        # Use HTML output instead of PDF
        output_file = self.output_dir / "invoice.html"
        
        # Ensure output directory exists
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        result = self.run_command([
            "template",
            str(self.data_path),
            "--template", str(self.template_path),
            "-o", str(output_file)
        ])
        
        # Print debug info
        print(f"Command output: {result.stdout}")
        if result.stderr:
            print(f"Command error: {result.stderr}")
        
        # Check if the command failed because of missing dependencies
        if "No module named 'weasyprint'" in result.stderr:
            self.skipTest("WeasyPrint is required for PDF generation")
        
        self.assertEqual(result.returncode, 0, 
                         f"Command failed with return code {result.returncode}")
        self.assertIn("Successfully created", result.stdout)
        self.assertTrue(output_file.exists(), 
                      f"Output file was not created: {output_file}")
        self.assertGreater(output_file.stat().st_size, 0, 
                         f"Output file is empty: {output_file}")
    
    def test_convert_command(self):
        """Test convert command."""
        # First create a test HTML file
        html_file = self.output_dir / "test.html"
        html_content = """
        <!DOCTYPE html>
        <html>
        <body>
            <h1>Test Document</h1>
            <p>This is a test document.</p>
        </body>
        </html>
        """
        html_file.write_text(html_content)
        
        # Convert to another format (using HTML to HTML as a simple test)
        output_file = self.output_dir / "output.html"
        
        # Ensure output directory exists
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        result = self.run_command([
            "convert",
            str(html_file),
            str(output_file)
        ])
        
        # Print debug info
        print(f"Command output: {result.stdout}")
        if result.stderr:
            print(f"Command error: {result.stderr}")
        
        # Check if the command failed because of missing dependencies
        if "No module named 'weasyprint'" in result.stderr:
            self.skipTest("WeasyPrint is required for PDF generation")
        
        self.assertEqual(result.returncode, 0, 
                         f"Command failed with return code {result.returncode}")
        self.assertIn("Successfully created", result.stdout)
        self.assertTrue(output_file.exists(), 
                      f"Output file was not created: {output_file}")
        self.assertGreater(output_file.stat().st_size, 0, 
                         f"Output file is empty: {output_file}")


if __name__ == "__main__":
    unittest.main()
