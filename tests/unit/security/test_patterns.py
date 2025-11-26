"""Unit tests for pattern detector."""

import pytest

from clinkey_cli.security.patterns import (
    detect_keyboard_walks,
    detect_sequences,
    detect_repetitions,
    analyze_patterns,
)


class TestKeyboardWalks:
    """Test keyboard walk pattern detection."""

    def test_detect_qwerty_row(self):
        """Test detection of QWERTY row walk."""
        patterns = detect_keyboard_walks("qwerty123")
        assert len(patterns) > 0
        assert any(p["type"] == "keyboard_walk" for p in patterns)

    def test_detect_asdf_walk(self):
        """Test detection of home row walk."""
        patterns = detect_keyboard_walks("asdfgh")
        assert len(patterns) > 0

    def test_no_keyboard_walk(self):
        """Test no detection for non-walk password."""
        patterns = detect_keyboard_walks("xqzmpr")
        assert len(patterns) == 0


class TestSequences:
    """Test sequential pattern detection."""

    def test_detect_alphabet_sequence(self):
        """Test detection of alphabetic sequence."""
        patterns = detect_sequences("abc123xyz")
        assert len(patterns) > 0
        assert any("abc" in str(p) for p in patterns)

    def test_detect_numeric_sequence(self):
        """Test detection of numeric sequence."""
        patterns = detect_sequences("pass123word")
        assert len(patterns) > 0

    def test_no_sequences(self):
        """Test no detection for non-sequential password."""
        patterns = detect_sequences("p4s5w6r7d")
        assert len(patterns) == 0


class TestRepetitions:
    """Test repetition pattern detection."""

    def test_detect_char_repetition(self):
        """Test detection of character repetition."""
        patterns = detect_repetitions("passssword")
        assert len(patterns) > 0
        assert any("ssss" in str(p) for p in patterns)

    def test_detect_sequence_repetition(self):
        """Test detection of sequence repetition."""
        patterns = detect_repetitions("123123abc")
        assert len(patterns) > 0

    def test_no_repetitions(self):
        """Test no detection for non-repetitive password."""
        patterns = detect_repetitions("p4s5w0rd")
        assert len(patterns) == 0


class TestAnalyzePatterns:
    """Test comprehensive pattern analysis."""

    def test_analyze_patterns_structure(self):
        """Test pattern analysis returns expected structure."""
        result = analyze_patterns("password123")
        assert "keyboard_walks" in result
        assert "sequences" in result
        assert "repetitions" in result
        assert "pattern_count" in result
        assert "entropy_reduction" in result

    def test_analyze_patterns_clean(self):
        """Test analysis of clean password with no patterns."""
        result = analyze_patterns("X9m2K7p4")
        assert result["pattern_count"] == 0

    def test_analyze_patterns_weak(self):
        """Test analysis of weak password with many patterns."""
        result = analyze_patterns("qwerty123123")
        assert result["pattern_count"] > 0
