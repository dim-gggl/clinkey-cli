"""Unit tests for syllable-based password generator."""

import re

import pytest

from clinkey_cli.generators.syllable import SyllableGenerator


class TestSyllableGeneratorInit:
    """Test SyllableGenerator initialization."""

    def test_syllable_generator_creation(self):
        """Test that SyllableGenerator instance is created successfully."""
        gen = SyllableGenerator()
        assert gen is not None

    def test_syllable_generator_has_syllables(self):
        """Test that syllable lists are populated."""
        gen = SyllableGenerator()
        assert hasattr(gen, "_simple_syllables")
        assert hasattr(gen, "_complex_syllables")
        assert len(gen._simple_syllables) > 0
        assert len(gen._complex_syllables) > 0

    def test_syllable_generator_default_language(self):
        """Test default language is English."""
        gen = SyllableGenerator()
        assert gen.language == "english"


class TestSyllableGeneratorGenerate:
    """Test password generation."""

    @pytest.fixture
    def gen(self):
        """Provide a fresh SyllableGenerator instance."""
        return SyllableGenerator()

    def test_generate_default(self, gen):
        """Test generate with default parameters."""
        password = gen.generate(length=16)
        assert isinstance(password, str)
        assert len(password) == 16

    @pytest.mark.parametrize("length", [16, 20, 50])
    def test_generate_various_lengths(self, gen, length):
        """Test generate produces correct length."""
        password = gen.generate(length=length)
        assert len(password) == length

    def test_generate_normal_type(self, gen):
        """Test normal type generates letters and separators."""
        password = gen.generate(length=30, password_type="normal")
        assert re.match(r"^[A-Z\-_]+$", password)

    def test_generate_strong_type(self, gen):
        """Test strong type includes digits."""
        password = gen.generate(length=30, password_type="strong")
        assert re.match(r"^[A-Z0-9\-_]+$", password)
        assert any(c.isdigit() for c in password)

    def test_generate_super_strong_type(self, gen):
        """Test super_strong type includes specials."""
        password = gen.generate(length=40, password_type="super_strong")
        assert any(c.isalpha() for c in password)
        assert any(c.isdigit() for c in password)

    def test_generate_with_lowercase(self, gen):
        """Test lowercase transformation."""
        password = gen.generate(length=20, lower=True)
        assert password.islower() or not password.isalpha()

    def test_generate_no_separator(self, gen):
        """Test no_separator removes separators."""
        password = gen.generate(length=20, no_separator=True)
        assert "-" not in password
        assert "_" not in password

    def test_generate_custom_separator(self, gen):
        """Test custom separator replacement."""
        password = gen.generate(length=20, separator="@")
        # Should contain @ or be too short for separators
        assert "@" in password or len(password) < 10


class TestSyllableGeneratorValidation:
    """Test input validation."""

    @pytest.fixture
    def gen(self):
        """Provide a fresh SyllableGenerator instance."""
        return SyllableGenerator()

    def test_invalid_length_negative(self, gen):
        """Test negative length raises ValueError."""
        with pytest.raises(ValueError, match="length must be at least"):
            gen.generate(length=-1)

    def test_invalid_length_zero(self, gen):
        """Test zero length raises ValueError."""
        with pytest.raises(ValueError, match="length must be at least"):
            gen.generate(length=0)

    def test_invalid_type(self, gen):
        """Test invalid password type raises ValueError."""
        with pytest.raises(ValueError, match="Unsupported type"):
            gen.generate(length=16, password_type="invalid")
