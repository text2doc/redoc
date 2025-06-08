"""Tests for the web example."""

import os
import tempfile
import unittest
from pathlib import Path
from typing import Dict, Any

import pytest
from fastapi.testclient import TestClient

from main import app, UPLOAD_DIR

# Test client
client = TestClient(app)

# Test data
SAMPLE_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Test Document</title>
</head>
<body>
    <h1>Test Document</h1>
    <p>This is a test document.</p>
</body>
</html>
"""

SAMPLE_TEMPLATE = """
# {{ title }}

Hello, {{ name }}!

This is a test template.
"""

class TestWebApp(unittest.TestCase):
    """Test cases for the web application."""

    @classmethod
    def setUpClass(cls):
        """Set up test environment."""
        cls.client = TestClient(app)
        cls.upload_dir = Path("test_uploads")
        os.environ["UPLOAD_DIR"] = str(cls.upload_dir)
        cls.upload_dir.mkdir(exist_ok=True)

    def setUp(self):
        """Set up before each test."""
        # Clear upload directory before each test
        for file in self.upload_dir.glob("*"):
            if file.is_file():
                file.unlink()

    def test_root_endpoint(self):
        """Test the root endpoint."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["name"], "Redoc Web API")
        self.assertIn("endpoints", data)

    def test_convert_endpoint(self):
        """Test the convert endpoint."""
        # Create a test HTML file
        test_file = self.upload_dir / "test.html"
        test_file.write_text(SAMPLE_HTML)

        # Test conversion to PDF
        with open(test_file, "rb") as f:
            response = self.client.post(
                "/convert",
                files={"file": ("test.html", f, "text/html")},
                data={"output_format": "pdf"}
            )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["content-type"], "application/pdf")
        self.assertIn("test.pdf", response.headers["content-disposition"])

    def test_template_endpoint(self):
        """Test the template endpoint."""
        # Test template rendering
        response = self.client.post(
            "/template",
            json={
                "template": SAMPLE_TEMPLATE,
                "data": {"title": "Test Document", "name": "Tester"},
                "output_format": "txt"
            }
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["content-type"], "application/txt")
        self.assertIn(b"Hello, Tester!", response.content)

    def test_formats_endpoint(self):
        """Test the formats endpoint."""
        response = self.client.get("/formats")
        self.assertEqual(response.status_code, 200)
        formats = response.json()
        self.assertIsInstance(formats, list)
        self.assertGreater(len(formats), 0)
        self.assertIn("name", formats[0])
        self.assertIn("extensions", formats[0])

    @classmethod
    def tearDownClass(cls):
        """Clean up after tests."""
        # Clean up test upload directory
        for file in cls.upload_dir.glob("*"):
            if file.is_file():
                file.unlink()
        cls.upload_dir.rmdir()

if __name__ == "__main__":
    unittest.main()
