"""Unit tests for entropy calculator."""

import pytest
import math

from clinkey_cli.security.entropy import (
    calculate_shannon_entropy,
    calculate_charset_entropy,
    get_entropy_score,
)


class TestShannonEntropy:
    """Test Shannon entropy calculation."""

    def test_shannon_entropy_uniform(self):
        """Test Shannon entropy for uniform distribution."""
        # "aaaa" has 0 entropy (all same character)
        entropy = calculate_shannon_entropy("aaaa")
        assert entropy == 0.0

    def test_shannon_entropy_binary(self):
        """Test Shannon entropy for binary distribution."""
        # "abab" has 1 bit per character
        entropy = calculate_shannon_entropy("abab")
        assert abs(entropy - 1.0) < 0.01

    def test_shannon_entropy_varied(self):
        """Test Shannon entropy for varied distribution."""
        # "abcdefgh" has maximum entropy for 8 chars
        entropy = calculate_shannon_entropy("abcdefgh")
        assert entropy > 2.5  # log2(8) = 3.0


class TestCharsetEntropy:
    """Test character set entropy calculation."""

    def test_charset_entropy_lowercase(self):
        """Test entropy for lowercase-only password."""
        # 26 lowercase letters, length 8
        entropy = calculate_charset_entropy("abcdefgh", 8)
        expected = math.log2(26) * 8  # ~37.6 bits
        assert abs(entropy - expected) < 0.1

    def test_charset_entropy_alphanumeric(self):
        """Test entropy for alphanumeric password."""
        # 62 characters (26+26+10), length 10
        entropy = calculate_charset_entropy("Abc123Xyz0", 10)
        expected = math.log2(62) * 10  # ~59.5 bits
        assert abs(entropy - expected) < 0.1

    def test_charset_entropy_full(self):
        """Test entropy for password with all character types."""
        # ~95 printable ASCII characters
        entropy = calculate_charset_entropy("Abc123!@#", 9)
        expected = math.log2(95) * 9  # ~59.0 bits
        assert entropy > 55


class TestEntropyScore:
    """Test comprehensive entropy scoring."""

    def test_entropy_score_weak(self):
        """Test entropy score for weak password."""
        score = get_entropy_score("password")
        assert "shannon_entropy" in score
        assert "charset_entropy" in score
        assert "bits_per_char" in score
        assert score["charset_entropy"] < 40  # Weak

    def test_entropy_score_strong(self):
        """Test entropy score for strong password."""
        score = get_entropy_score("Tr0ub4dor&3-X")
        assert score["charset_entropy"] > 60  # Strong

    def test_entropy_score_structure(self):
        """Test entropy score has expected structure."""
        score = get_entropy_score("test")
        assert "shannon_entropy" in score
        assert "charset_entropy" in score
        assert "bits_per_char" in score
        assert "charset_size" in score
        assert "length" in score
