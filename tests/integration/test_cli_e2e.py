"""End-to-end CLI integration tests."""

import subprocess
import tempfile
from pathlib import Path


class TestBackwardCompatibility:
    """Test that existing CLI commands work identically."""

    def test_basic_generation(self):
        """Test basic password generation."""
        result = subprocess.run(
            ["clinkey", "-l", "20", "-t", "strong"],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        password = result.stdout.strip()
        # Syllable-based passwords may be within 1 character of target length
        assert 19 <= len(password) <= 21

    def test_batch_generation(self):
        """Test generating multiple passwords."""
        result = subprocess.run(
            ["clinkey", "-l", "16", "-t", "normal", "-n", "5"],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        passwords = result.stdout.strip().split("\n")
        assert len(passwords) == 5
        for password in passwords:
            # Syllable-based passwords may be within 1 character of target length
            assert 15 <= len(password) <= 17

    def test_output_to_file(self):
        """Test writing passwords to file."""
        with tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix=".txt"
        ) as f:
            output_path = f.name

        try:
            result = subprocess.run(
                ["clinkey", "-l", "20", "-n", "3", "-o", output_path],
                capture_output=True,
                text=True,
            )

            assert result.returncode == 0
            # Path might be resolved (e.g., /private/var on macOS)
            assert "Passwords saved to" in result.stdout
            assert output_path.split("/")[-1] in result.stdout

            # Verify file contents
            passwords = Path(output_path).read_text().strip().split("\n")
            assert len(passwords) == 3
            for password in passwords:
                # Syllable-based passwords may be within 1 character of target length
                assert 19 <= len(password) <= 21
        finally:
            Path(output_path).unlink(missing_ok=True)


class TestPassphraseCLI:
    """Test passphrase generation via CLI."""

    def test_passphrase_default(self):
        """Test default passphrase generation."""
        result = subprocess.run(
            ["clinkey", "-t", "passphrase"],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        password = result.stdout.strip()
        words = password.split("-")
        assert len(words) == 4  # Default word count

    def test_passphrase_custom_word_count(self):
        """Test passphrase with custom word count."""
        result = subprocess.run(
            ["clinkey", "-t", "passphrase", "--word-count", "6"],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        password = result.stdout.strip()
        words = password.split("-")
        assert len(words) == 6

    def test_passphrase_custom_separator(self):
        """Test passphrase with custom separator."""
        result = subprocess.run(
            ["clinkey", "-t", "passphrase", "-s", "_"],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        password = result.stdout.strip()
        assert "_" in password
        assert "-" not in password

    def test_passphrase_no_capitalize(self):
        """Test passphrase without capitalization."""
        result = subprocess.run(
            ["clinkey", "-t", "passphrase", "--no-capitalize"],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        password = result.stdout.strip()
        # All words should be lowercase
        for word in password.split("-"):
            assert word.islower()

    def test_passphrase_batch(self):
        """Test generating multiple passphrases."""
        result = subprocess.run(
            ["clinkey", "-t", "passphrase", "-n", "3"],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        passwords = result.stdout.strip().split("\n")
        assert len(passwords) == 3


class TestPatternCLI:
    """Test pattern generation via CLI."""

    def test_pattern_simple(self):
        """Test simple pattern generation."""
        result = subprocess.run(
            ["clinkey", "-t", "pattern", "--pattern", "DDDD"],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        password = result.stdout.strip()
        assert len(password) == 4
        assert password.isdigit()

    def test_pattern_complex(self):
        """Test complex pattern generation."""
        result = subprocess.run(
            ["clinkey", "-t", "pattern", "--pattern", "Cvvc-9999-Cvvc"],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        password = result.stdout.strip()
        # Pattern length: 4 + 1 + 4 + 1 + 4 = 14
        assert len(password) == 14
        assert password.count("-") == 2

    def test_pattern_missing_template_error(self):
        """Test that pattern without template shows error."""
        result = subprocess.run(
            ["clinkey", "-t", "pattern"],
            capture_output=True,
            text=True,
        )

        assert result.returncode != 0
        assert "Pattern template required" in result.stderr

    def test_pattern_batch(self):
        """Test generating multiple patterns."""
        result = subprocess.run(
            ["clinkey", "-t", "pattern", "--pattern", "LLLL-DDDD", "-n", "5"],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        passwords = result.stdout.strip().split("\n")
        assert len(passwords) == 5


class TestHelpText:
    """Test CLI help output."""

    def test_help_shows_new_options(self):
        """Test that --help shows all new options."""
        result = subprocess.run(
            ["clinkey", "--help"],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        help_text = result.stdout

        # Check type options
        assert "passphrase" in help_text
        assert "pattern" in help_text

        # Check new flags
        assert "--word-count" in help_text
        assert "--capitalize" in help_text
        assert "--pattern" in help_text
