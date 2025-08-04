import os
import pytest
import hashlib
import tempfile
from fmd5sum import md5sum

def test_md5sum_correctness():
    """Test the MD5 calculation correctness."""
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        content = b"Test content for MD5 calculation"
        tmp.write(content)
        tmp_path = tmp.name
        
    try:
        # Expected hash of "Test content for MD5 calculation"
        expected_hash = hashlib.md5(content).hexdigest()
        assert md5sum(tmp_path) == expected_hash
    finally:
        os.unlink(tmp_path)

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
        expected_hash = hashlib.md5().hexdigest()  # MD5 of empty file
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

# Add test for parallel processing
def test_parallel_processing(capsys):
    """Test the parallel processing functionality."""
    files = []
    try:
        # Create 5 temporary test files
        for i in range(5):
            with tempfile.NamedTemporaryFile(delete=False) as tmp:
                content = f"Test file {i}".encode()
                tmp.write(content)
                files.append(tmp.name)
        
        # Import and run the parallel process function
        from fmd5sum import process_files
        process_files(files, max_workers=2)
        
        captured = capsys.readouterr()
        outputs = captured.out.splitlines()
        assert len(outputs) == len(files)
        
        # Verify each file has an output line
        for filename in files:
            assert any(filename in line for line in outputs)
    finally:
        for filename in files:
            os.unlink(filename)
