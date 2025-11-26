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


class TestSecurityAnalyzerIntegration:
    """Test integrated security analysis."""

    def test_analyze_includes_entropy(self):
        """Test analysis includes entropy data."""
        result = analyze_password("TestPassword123!")
        assert "entropy" in result
        assert "shannon_entropy" in result["entropy"]
        assert "charset_entropy" in result["entropy"]

    def test_analyze_includes_patterns(self):
        """Test analysis includes pattern detection."""
        result = analyze_password("qwerty123", check_patterns=True)
        assert "patterns" in result
        assert "pattern_count" in result["patterns"]

    def test_analyze_skip_patterns(self):
        """Test analysis can skip pattern detection."""
        result = analyze_password("test", check_patterns=False)
        assert result["patterns"] == {}

    def test_analyze_calculates_strength_score(self):
        """Test analysis calculates strength score."""
        result = analyze_password("Tr0ub4dor&3")
        assert "strength_score" in result
        assert 0 <= result["strength_score"] <= 100

    def test_analyze_provides_strength_label(self):
        """Test analysis provides strength label."""
        result = analyze_password("Abc123!@#")
        assert "strength_label" in result
        assert result["strength_label"] in [
            "Very Weak",
            "Weak",
            "Moderate",
            "Strong",
            "Very Strong",
        ]

    def test_analyze_weak_password(self):
        """Test analysis of weak password."""
        result = analyze_password("abc123")
        assert result["strength_score"] < 40

    def test_analyze_strong_password(self):
        """Test analysis of strong password."""
        result = analyze_password("Tr0ub4dor&3-Xy9Pq2")
        assert result["strength_score"] > 60
