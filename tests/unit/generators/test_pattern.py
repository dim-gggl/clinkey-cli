"""Unit tests for pattern-based password generator."""

import re

import pytest

from clinkey_cli.generators.pattern import PatternGenerator


class TestPatternGeneratorInit:
    """Test PatternGenerator initialization."""

    def test_pattern_generator_creation(self):
        """Test PatternGenerator instance creation."""
        gen = PatternGenerator()
        assert gen is not None

    def test_pattern_generator_has_character_sets(self):
        """Test character sets are defined."""
        gen = PatternGenerator()
        assert hasattr(gen, "_consonants")
        assert hasattr(gen, "_vowels")
        assert hasattr(gen, "_digits")
        assert hasattr(gen, "_specials")


class TestPatternValidation:
    """Test pattern validation."""

    @pytest.fixture
    def gen(self):
        """Provide PatternGenerator instance."""
        return PatternGenerator()

    def test_validate_valid_pattern(self, gen):
        """Test validation of valid patterns."""
        assert gen.validate_pattern("LLLL") is True
        assert gen.validate_pattern("Cvvc-9999") is True
        assert gen.validate_pattern("SSS-LLL-DDD") is True

    def test_validate_invalid_pattern_empty(self, gen):
        """Test validation rejects empty pattern."""
        assert gen.validate_pattern("") is False

    def test_validate_invalid_pattern_unknown_char(self, gen):
        """Test validation rejects unknown character class."""
        assert gen.validate_pattern("XYZ") is False

    def test_validate_pattern_with_custom_set(self, gen):
        """Test validation accepts custom character sets."""
        assert gen.validate_pattern("[abc]DDD") is True
        assert gen.validate_pattern("LL[123]LL") is True


class TestPatternLength:
    """Test pattern length calculation."""

    @pytest.fixture
    def gen(self):
        """Provide PatternGenerator instance."""
        return PatternGenerator()

    def test_get_pattern_length_simple(self, gen):
        """Test length calculation for simple patterns."""
        assert gen.get_pattern_length("LLLL") == 4
        assert gen.get_pattern_length("DDDD") == 4
        assert gen.get_pattern_length("SSSS") == 4

    def test_get_pattern_length_with_literals(self, gen):
        """Test length calculation with literal characters."""
        assert gen.get_pattern_length("LL-LL") == 5
        assert gen.get_pattern_length("DDD@DDD") == 7

    def test_get_pattern_length_with_custom_sets(self, gen):
        """Test length calculation with custom character sets."""
        assert gen.get_pattern_length("[abc]DDD") == 4
        assert gen.get_pattern_length("LL[123]LL") == 5


class TestPatternGeneration:
    """Test password generation from patterns."""

    @pytest.fixture
    def gen(self):
        """Provide PatternGenerator instance."""
        return PatternGenerator()

    def test_generate_consonant_pattern(self, gen):
        """Test generation with consonant pattern."""
        password = gen.generate(pattern="CCCC")
        assert len(password) == 4
        assert all(c.isalpha() and c.isupper() for c in password)

    def test_generate_vowel_pattern(self, gen):
        """Test generation with vowel pattern."""
        password = gen.generate(pattern="VVVV")
        assert len(password) == 4
        assert all(c in "AEIOUY" for c in password)

    def test_generate_digit_pattern(self, gen):
        """Test generation with digit pattern."""
        password = gen.generate(pattern="DDDD")
        assert len(password) == 4
        assert password.isdigit()

    def test_generate_special_pattern(self, gen):
        """Test generation with special character pattern."""
        password = gen.generate(pattern="SSSS")
        assert len(password) == 4
        assert all(not c.isalnum() for c in password)

    def test_generate_letter_pattern(self, gen):
        """Test generation with any letter pattern."""
        password = gen.generate(pattern="LLLL")
        assert len(password) == 4
        assert password.isalpha()

    def test_generate_mixed_pattern(self, gen):
        """Test generation with mixed pattern."""
        password = gen.generate(pattern="Cvvc-9999-Cvvc")
        assert len(password) == 14
        assert password[4] == "-"
        assert password[9] == "-"
        assert password[5:9].isdigit()

    def test_generate_with_literals(self, gen):
        """Test generation preserves literal characters."""
        password = gen.generate(pattern="LL@LL")
        assert password[2] == "@"
        assert len(password) == 5

    def test_generate_custom_character_set(self, gen):
        """Test generation with custom character set."""
        password = gen.generate(pattern="[abc]DDD")
        assert password[0] in "abc"
        assert password[1:4].isdigit()

    def test_generate_length_parameter(self, gen):
        """Test generate with length parameter (for BaseGenerator compatibility)."""
        # Length parameter should be ignored when pattern is provided
        password = gen.generate(length=20, pattern="LLLL")
        assert len(password) == 4


class TestPatternGeneratorValidation:
    """Test error handling."""

    @pytest.fixture
    def gen(self):
        """Provide PatternGenerator instance."""
        return PatternGenerator()

    def test_generate_invalid_pattern(self, gen):
        """Test generation with invalid pattern."""
        with pytest.raises(ValueError, match="Invalid pattern"):
            gen.generate(pattern="XYZ")

    def test_generate_empty_pattern(self, gen):
        """Test generation with empty pattern."""
        with pytest.raises(ValueError, match="pattern cannot be empty"):
            gen.generate(pattern="")

    def test_generate_no_pattern_no_length(self, gen):
        """Test generation requires either pattern or length."""
        with pytest.raises(ValueError, match="must provide either pattern or length"):
            gen.generate()
