"""Tests for the advanced example."""

import unittest
import json
from pathlib import Path
import subprocess

class TestAdvancedExample(unittest.TestCase):
    """Test cases for advanced example."""

    @classmethod
    def setUpClass(cls):
        """Set up test environment."""
        cls.output_dir = Path(__file__).parent / "output"
        cls.output_dir.mkdir(exist_ok=True)

    def test_main_script_runs(self):
        """Test that the main script runs without errors."""
        result = subprocess.run(
            ["python", "main.py"],
            cwd=Path(__file__).parent,
            capture_output=True,
            text=True,
            check=False
        )
        self.assertEqual(result.returncode, 0, 
                        f"Script failed with error: {result.stderr}")

    def test_output_files_created(self):
        """Test that all output files are created."""
        # Run the main script
        subprocess.run(
            ["python", "main.py"],
            cwd=Path(__file__).parent,
            capture_output=True,
            check=True
        )
        
        # Check for expected output files
        expected_files = [
            self.output_dir / "report_001.pdf",
            self.output_dir / "report_001.html",
            self.output_dir / "report_001.json"
        ]
        
        for file_path in expected_files:
            with self.subTest(file=file_path.name):
                self.assertTrue(file_path.exists(), 
                              f"Expected file {file_path} was not created")
