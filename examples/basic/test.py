"""Tests for the basic example."""

import unittest
from pathlib import Path
import subprocess

class TestBasicExample(unittest.TestCase):
    """Test cases for basic example."""

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

    def test_output_file_created(self):
        """Test that the output PDF is created."""
        output_file = Path(__file__).parent / "output" / "sample.pdf"
        self.assertTrue(output_file.exists(), 
                      f"Output file {output_file} was not created")

if __name__ == "__main__":
    unittest.main()
