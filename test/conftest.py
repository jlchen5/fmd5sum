"""Test configuration file."""
import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Disable terminal warnings for cleaner output
def pytest_terminal_summary(terminalreporter, exitstatus, config):
    reports = terminalreporter.getreports("")
    for report in reports:
        if report.when == "call":
            terminalreporter.stats.pop("warnings", None)
