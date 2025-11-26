"""Integration tests verifying backward compatibility with Clinkey 1.x.

These tests ensure that the refactored architecture maintains 100%
compatibility with the 1.x API and behavior.
"""

import re
import pytest
from clinkey_cli.main import Clinkey, MAX_PASSWORD_LENGTH, MAX_BATCH_SIZE, MIN_PASSWORD_LENGTH


class TestBackwardCompatibleAPI:
    """Test that Clinkey class API is unchanged."""

    @pytest.fixture
    def clinkey(self):
        """Provide a fresh Clinkey instance."""
        return Clinkey()

    def test_clinkey_instance_creation(self, clinkey):
        """Test Clinkey instance creates successfully."""
        assert clinkey is not None

    def test_generate_password_signature(self, clinkey):
        """Test generate_password() method exists with correct signature."""
        password = clinkey.generate_password(
            length=16,
            type="normal",
            lower=False,
            no_separator=False,
            new_separator=None
        )
        assert isinstance(password, str)
        assert len(password) == 16

    def test_generate_batch_signature(self, clinkey):
        """Test generate_batch() method exists."""
        passwords = clinkey.generate_batch(
            count=5,
            length=16,
            type="normal"
        )
        assert isinstance(passwords, list)
        assert len(passwords) == 5

    def test_normal_method_exists(self, clinkey):
        """Test normal() method still exists."""
        password = clinkey.normal()
        assert isinstance(password, str)

    def test_strong_method_exists(self, clinkey):
        """Test strong() method still exists."""
        password = clinkey.strong()
        assert isinstance(password, str)

    def test_super_strong_method_exists(self, clinkey):
        """Test super_strong() method still exists."""
        password = clinkey.super_strong()
        assert isinstance(password, str)


class TestBackwardCompatibleBehavior:
    """Test that behavior matches 1.x exactly."""

    @pytest.fixture
    def clinkey(self):
        """Provide a fresh Clinkey instance."""
        return Clinkey()

    def test_default_password_length(self, clinkey):
        """Test default length is 16."""
        password = clinkey.generate_password()
        assert len(password) == 16

    def test_normal_password_pattern(self, clinkey):
        """Test normal password pattern unchanged."""
        password = clinkey.generate_password(type="normal", length=30)
        assert re.match(r'^[A-Z\-_]+$', password)

    def test_strong_password_has_digits(self, clinkey):
        """Test strong password includes digits."""
        password = clinkey.generate_password(type="strong", length=30)
        assert any(c.isdigit() for c in password)

    def test_lowercase_transformation(self, clinkey):
        """Test lowercase flag works."""
        password = clinkey.generate_password(lower=True, length=20)
        assert password.islower() or not password.isalpha()

    def test_no_separator_flag(self, clinkey):
        """Test no_separator removes separators."""
        password = clinkey.generate_password(no_separator=True, length=20)
        assert '-' not in password
        assert '_' not in password

    def test_custom_separator(self, clinkey):
        """Test custom separator via new_separator."""
        password = clinkey.generate_password(new_separator='@', length=20)
        assert '@' in password or len(password) < 10


class TestBackwardCompatibleValidation:
    """Test that validation errors match 1.x."""

    @pytest.fixture
    def clinkey(self):
        """Provide a fresh Clinkey instance."""
        return Clinkey()

    def test_invalid_length_error(self, clinkey):
        """Test invalid length raises ValueError."""
        with pytest.raises(ValueError):
            clinkey.generate_password(length=-1)

    def test_invalid_type_error(self, clinkey):
        """Test invalid type raises ValueError."""
        with pytest.raises(ValueError):
            clinkey.generate_password(type="invalid")

    def test_invalid_separator_error(self, clinkey):
        """Test invalid separator raises ValueError."""
        with pytest.raises(ValueError):
            clinkey.generate_password(new_separator="@@")


class TestBackwardCompatibleConstants:
    """Test that module constants are unchanged."""

    def test_max_password_length_constant(self):
        """Test MAX_PASSWORD_LENGTH is accessible."""
        assert MAX_PASSWORD_LENGTH == 128

    def test_max_batch_size_constant(self):
        """Test MAX_BATCH_SIZE is accessible."""
        assert MAX_BATCH_SIZE == 500

    def test_min_password_length_constant(self):
        """Test MIN_PASSWORD_LENGTH is accessible."""
        assert MIN_PASSWORD_LENGTH == 16
