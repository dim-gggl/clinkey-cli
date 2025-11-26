"""Unit tests for context analyzer."""

import pytest

from clinkey_cli.security.context import (
    analyze_character_diversity,
    analyze_positional_patterns,
    analyze_context,
)


class TestCharacterDiversity:
    """Test character diversity analysis."""

    def test_diversity_all_types(self):
        """Test password with all character types."""
        result = analyze_character_diversity("Abc123!@#")
        assert result["has_lowercase"] is True
        assert result["has_uppercase"] is True
        assert result["has_digits"] is True
        assert result["has_special"] is True
        assert result["diversity_score"] == 4

    def test_diversity_lowercase_only(self):
        """Test password with only lowercase."""
        result = analyze_character_diversity("abcdefgh")
        assert result["has_lowercase"] is True
        assert result["has_uppercase"] is False
        assert result["has_digits"] is False
        assert result["has_special"] is False
        assert result["diversity_score"] == 1

    def test_diversity_alphanumeric(self):
        """Test password with alphanumeric only."""
        result = analyze_character_diversity("Abc123")
        assert result["diversity_score"] == 3


class TestPositionalPatterns:
    """Test positional pattern detection."""

    def test_detect_digits_at_end(self):
        """Test detection of digits at end."""
        result = analyze_positional_patterns("password123")
        assert "digits_at_end" in result["patterns"]

    def test_detect_special_at_end(self):
        """Test detection of special chars at end."""
        result = analyze_positional_patterns("password!@#")
        assert "special_at_end" in result["patterns"]

    def test_detect_uppercase_at_start(self):
        """Test detection of uppercase at start."""
        result = analyze_positional_patterns("Password123")
        assert "uppercase_at_start" in result["patterns"]

    def test_no_positional_patterns(self):
        """Test password with good mixing."""
        result = analyze_positional_patterns("P4s5w0r!d")
        assert len(result["patterns"]) == 0


class TestAnalyzeContext:
    """Test comprehensive context analysis."""

    def test_analyze_context_structure(self):
        """Test context analysis returns expected structure."""
        result = analyze_context("Password123!")
        assert "character_diversity" in result
        assert "positional_patterns" in result
        assert "mixing_score" in result

    def test_analyze_well_mixed_password(self):
        """Test well-mixed password gets high score."""
        result = analyze_context("P4s5w0r!d")
        assert result["mixing_score"] >= 80

    def test_analyze_poorly_mixed_password(self):
        """Test poorly mixed password gets low score."""
        result = analyze_context("Password123")
        assert result["mixing_score"] < 60
