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
        cls.output_dir.mkdir(exist_ok=True)
        
        # Path to the main script
        cls.script_path = cls.test_dir / "main.py"
        
        # Test files
        cls.template_path = cls.test_dir / "templates" / "invoice.html"
        cls.data_path = cls.test_dir / "data" / "invoice_data.json"
    
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
        output_file = self.output_dir / "invoice.pdf"
        result = self.run_command([
            "template",
            str(self.data_path),
            "--template", str(self.template_path),
            "-o", str(output_file)
        ])
        
        self.assertEqual(result.returncode, 0)
        self.assertIn("Successfully created", result.stdout)
        self.assertTrue(output_file.exists())
        self.assertGreater(output_file.stat().st_size, 0)
    
    def test_convert_command(self):
        """Test convert command."""
        # First generate a PDF from template
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
        
        # Convert to PDF
        output_file = self.output_dir / "output.pdf"
        result = self.run_command([
            "convert",
            str(html_file),
            str(output_file)
        ])
        
        self.assertEqual(result.returncode, 0)
        self.assertIn("Successfully created", result.stdout)
        self.assertTrue(output_file.exists())
        self.assertGreater(output_file.stat().st_size, 0)


if __name__ == "__main__":
    unittest.main()
