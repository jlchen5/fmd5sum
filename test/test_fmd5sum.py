import os
import pytest
import hashlib
import tempfile
from fmd5sum import md5sum

@pytest.fixture
def create_test_file():
    """Creates a temporary test file with known content."""
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(b"Test content for MD5 calculation")
        tmp_path = tmp.name
    yield tmp_path
    os.unlink(tmp_path)

def test_md5sum_correctness(create_test_file):
    """Test the MD5 calculation correctness."""
    # Expected hash of "Test content for MD5 calculation"
    expected_hash = "ee4f7c3b32e3c9dfb01bb9f9b1acf1c0"
    assert md5sum(create_test_file) == expected_hash

def test_md5sum_large_file():
    """Test large file handling."""
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        # Write 5MB of random data
        data = os.urandom(5 * 1024 * 1024)
        tmp.write(data)
        tmp_path = tmp.name
        expected_hash = hashlib.md5(data).hexdigest()
    
    try:
        assert md5sum(tmp_path) == expected_hash
    finally:
        os.unlink(tmp_path)

def test_md5sum_nonexistent_file():
    """Test handling of non-existent files."""
    assert md5sum("/path/to/nonexistent/file") is None

def test_empty_file():
    """Test MD5 calculation for empty files."""
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp_path = tmp.name
    
    try:
        expected_hash = "d41d8cd98f00b204e9800998ecf8427e"  # MD5 of empty file
        assert md5sum(tmp_path) == expected_hash
    finally:
        os.unlink(tmp_path)

def test_binary_file():
    """Test handling of binary files."""
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        # Binary data (PDF signature)
        binary_data = b"%PDF-1.4\x0A%\xE2\xE3\xCF\xD3\x0A"
        tmp.write(binary_data)
        tmp_path = tmp.name
        expected_hash = hashlib.md5(binary_data).hexdigest()
    
    try:
        assert md5sum(tmp_path) == expected_hash
    finally:
        os.unlink(tmp_path)
