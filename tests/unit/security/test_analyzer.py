"""Unit tests for security analyzer module."""

import pytest

from clinkey_cli.security import analyze_password
from clinkey_cli.security.analyzer import SecurityAnalyzer


class TestSecurityAnalyzerImports:
    """Test security module structure."""

    def test_analyze_password_imported(self):
        """Test analyze_password function is available."""
        assert analyze_password is not None
        assert callable(analyze_password)

    def test_security_analyzer_class(self):
        """Test SecurityAnalyzer class is available."""
        analyzer = SecurityAnalyzer()
        assert analyzer is not None
