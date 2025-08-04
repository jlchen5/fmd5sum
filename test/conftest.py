"""Test configuration file."""
import os
import sys
import pytest

# Add project root to Python path for test discovery
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Optional: Disable terminal warnings for cleaner output
def pytest_terminal_summary(terminalreporter, exitstatus, config):
    reports = terminalreporter.getreports("")
    for report in reports:
        if report.when == "call":
            terminalreporter.stats.pop("warnings", None)

# Fixture for temporary files (optional but useful)
@pytest.fixture
def temp_file():
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        yield tmp.name
        try:
            os.unlink(tmp.name)
        except:
            pass
