"""Unit tests for dictionary analyzer."""

import pytest

from clinkey_cli.security.dictionary import (
    check_common_password,
    check_dictionary_words,
    analyze_dictionary,
)


class TestCommonPasswordCheck:
    """Test common password detection."""

    def test_detect_common_password(self):
        """Test detection of common passwords."""
        result = check_common_password("password")
        assert result["is_common"] is True
        assert "password" in result["matches"]

    def test_detect_password123(self):
        """Test detection of password123."""
        result = check_common_password("password123")
        assert result["is_common"] is True

    def test_safe_password(self):
        """Test non-common password."""
        result = check_common_password("Xk9mP2qR7!")
        assert result["is_common"] is False
        assert len(result["matches"]) == 0


class TestDictionaryWordCheck:
    """Test dictionary word detection."""

    def test_detect_single_word(self):
        """Test detection of dictionary word."""
        result = check_dictionary_words("elephant")
        assert len(result["words"]) > 0

    def test_detect_multiple_words(self):
        """Test detection of multiple words."""
        result = check_dictionary_words("bluesky")
        assert len(result["words"]) >= 1

    def test_no_dictionary_words(self):
        """Test password with no dictionary words."""
        result = check_dictionary_words("X9mK2pQ7")
        assert len(result["words"]) == 0


class TestAnalyzeDictionary:
    """Test comprehensive dictionary analysis."""

    def test_analyze_dictionary_structure(self):
        """Test dictionary analysis returns expected structure."""
        result = analyze_dictionary("password123")
        assert "is_common" in result
        assert "common_matches" in result
        assert "dictionary_words" in result
        assert "word_count" in result
        assert "score_penalty" in result

    def test_analyze_common_password_penalty(self):
        """Test common password gets high penalty."""
        result = analyze_dictionary("password")
        assert result["score_penalty"] >= 50

    def test_analyze_dictionary_word_penalty(self):
        """Test dictionary words get penalty."""
        result = analyze_dictionary("elephant2024")
        assert result["score_penalty"] > 0

    def test_analyze_strong_password_no_penalty(self):
        """Test strong password gets minimal penalty."""
        result = analyze_dictionary("Xk9mP2qR7!")
        assert result["score_penalty"] < 10
