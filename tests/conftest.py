"""Test configuration file."""
import os
import sys
import tempfile  
import pytest

# Add project root to Python path for test discovery
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Fixture for temporary files
@pytest.fixture
def temp_file():
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        yield tmp.name
        try:
            os.unlink(tmp.name)
        except FileNotFoundError:
            pass  
