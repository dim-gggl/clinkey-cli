"""Unit tests for passphrase generator."""

import pytest

from clinkey_cli.generators.passphrase import PassphraseGenerator


class TestPassphraseGeneratorInit:
    """Test PassphraseGenerator initialization."""

    def test_passphrase_generator_creation(self):
        """Test PassphraseGenerator instance creation."""
        gen = PassphraseGenerator()
        assert gen is not None

    def test_passphrase_generator_default_wordlist(self):
        """Test default wordlist is loaded."""
        gen = PassphraseGenerator()
        assert len(gen._wordlist) > 0
        assert gen.wordlist_name == "eff_large"

    def test_passphrase_generator_has_wordlist(self):
        """Test wordlist contains expected number of words."""
        gen = PassphraseGenerator(wordlist="eff_large")
        # EFF large wordlist has 7,776 words
        assert len(gen._wordlist) == 7776


class TestPassphraseGeneration:
    """Test passphrase generation."""

    @pytest.fixture
    def gen(self):
        """Provide PassphraseGenerator instance."""
        return PassphraseGenerator()

    def test_generate_default_passphrase(self, gen):
        """Test generate with default parameters."""
        passphrase = gen.generate(word_count=4)
        words = passphrase.split("-")
        assert len(words) == 4
        assert all(len(word) > 0 for word in words)
        assert all(word[0].isupper() for word in words)  # Capitalized

    def test_generate_custom_word_count(self, gen):
        """Test generate with custom word count."""
        for count in [3, 5, 6, 8]:
            passphrase = gen.generate(word_count=count)
            words = passphrase.split("-")
            assert len(words) == count

    def test_generate_custom_separator(self, gen):
        """Test generate with custom separator."""
        passphrase = gen.generate(word_count=4, separator="@")
        assert "@" in passphrase
        words = passphrase.split("@")
        assert len(words) == 4

    def test_generate_no_separator(self, gen):
        """Test generate with no separator."""
        passphrase = gen.generate(word_count=4, separator="")
        assert "-" not in passphrase
        assert len(passphrase) > 10  # Multiple words concatenated

    def test_generate_capitalize(self, gen):
        """Test capitalize option."""
        passphrase = gen.generate(word_count=4, capitalize=True)
        words = passphrase.split("-")
        assert all(word[0].isupper() for word in words)

    def test_generate_no_capitalize(self, gen):
        """Test no capitalize option."""
        passphrase = gen.generate(word_count=4, capitalize=False)
        words = passphrase.split("-")
        assert all(word.islower() for word in words)

    def test_generate_length_parameter(self, gen):
        """Test generate with length parameter (for BaseGenerator compatibility)."""
        # Length parameter should be ignored for passphrases
        # but method should still work
        passphrase = gen.generate(length=20, word_count=4)
        words = passphrase.split("-")
        assert len(words) == 4


class TestPassphraseValidation:
    """Test input validation."""

    @pytest.fixture
    def gen(self):
        """Provide PassphraseGenerator instance."""
        return PassphraseGenerator()

    def test_invalid_word_count_too_low(self, gen):
        """Test word count below minimum."""
        with pytest.raises(ValueError, match="word_count must be at least"):
            gen.generate(word_count=2)

    def test_invalid_word_count_too_high(self, gen):
        """Test word count above maximum."""
        with pytest.raises(ValueError, match="word_count cannot exceed"):
            gen.generate(word_count=11)

    def test_invalid_wordlist(self):
        """Test invalid wordlist name."""
        with pytest.raises(ValueError, match="Unknown wordlist"):
            PassphraseGenerator(wordlist="invalid")
