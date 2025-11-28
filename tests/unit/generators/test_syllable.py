"""Unit tests for syllable-based password generator."""

import re

import pytest

from clinkey_cli.generators.syllable import SyllableGenerator


def _assert_word_pattern(password: str, gen: SyllableGenerator):
    """Ensure password follows four CV words joined by hyphens.
    
    Checks that the password structure matches the expected format (4 words)
    and that each word is composed of valid syllables (simple or complex).
    """

    letters_only = re.sub(r"[^A-Z-]", "", password)
    parts = letters_only.split("-")

    assert len(parts) == 4
    assert all(parts)
    assert all(len(part) >= 2 for part in parts)
    
    # We expect at least one word to be longer than 2 chars usually, 
    # but strictly speaking with random choice it's possible to have all simple syllables (len 2).
    # However, the generator guarantees: "Guarantees at least one word uses multiple CV pairs" 
    # OR now multiple syllables.
    # The old test checked: assert any(len(part) > 2 for part in parts)
    # With complex syllables (len 3), this is even more likely.
    assert any(len(part) > 2 for part in parts)
    
    # Check variability in length
    assert len({len(part) for part in parts}) > 1

    # Build regex for valid syllables
    # Simple are defined as lowercase, complex as uppercase in generator
    # We normalize to uppercase for matching
    simple = [s.upper() for s in gen._simple_syllables]
    complex_syl = [s.upper() for s in gen._complex_syllables]
    
    # Sort by length descending to ensure greedy matching correct order (longest first)
    all_syl = sorted(simple + complex_syl, key=len, reverse=True)
    
    # Escape just in case, though they are letters
    pattern_str = "|".join(re.escape(s) for s in all_syl)
    regex = re.compile(f"(?:{pattern_str})+")

    for part in parts:
        assert regex.fullmatch(part), f"Word part '{part}' is not composed of valid syllables"


def _extract_words(password: str) -> list[str]:
    """Return the list of letter-only words from a password."""

    letters_only = re.sub(r"[^A-Z-]", "", password)
    return [part for part in letters_only.split("-") if part]


def _assert_unique_words(password: str):
    """Ensure no word is repeated inside the password."""

    words = _extract_words(password)
    assert len(words) == len(set(words))


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
        password = gen.normal()
        _assert_word_pattern(password, gen)

    def test_generate_strong_type(self, gen):
        """Test strong type includes digits."""
        password = gen.strong()
        _assert_word_pattern(password, gen)
        assert any(c.isdigit() for c in password)
        _assert_unique_words(password)

    def test_generate_super_strong_type(self, gen):
        """Test super_strong type includes specials."""
        password = gen.super_strong()
        _assert_word_pattern(password, gen)
        assert any(c.isalpha() for c in password)
        assert any(c.isdigit() for c in password)
        _assert_unique_words(password)

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

    def test_generate_unique_words_normal(self, gen):
        """Ensure normal passwords never repeat a word."""
        password = gen.normal()
        _assert_unique_words(password)


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
