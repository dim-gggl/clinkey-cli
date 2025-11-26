"""Unit tests for configuration manager."""

import pathlib
import tempfile

from clinkey_cli.config.manager import DEFAULT_CONFIG, ConfigManager


class TestConfigManager:
    """Test ConfigManager class."""

    def test_config_manager_creation(self):
        """Test ConfigManager instance creation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = pathlib.Path(tmpdir) / "config.toml"
            manager = ConfigManager(config_path)
            assert manager is not None

    def test_default_config_structure(self):
        """Test default config has expected structure."""
        assert "general" in DEFAULT_CONFIG
        assert "security" in DEFAULT_CONFIG
        assert "vault" in DEFAULT_CONFIG
        assert "generators" in DEFAULT_CONFIG

    def test_get_default_value(self):
        """Test get() returns default values."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = pathlib.Path(tmpdir) / "config.toml"
            manager = ConfigManager(config_path)
            value = manager.get("general.default_length")
            assert value == 16

    def test_get_nested_value(self):
        """Test get() handles nested keys."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = pathlib.Path(tmpdir) / "config.toml"
            manager = ConfigManager(config_path)
            value = manager.get("generators.syllable.default_language")
            assert value == "english"

    def test_get_nonexistent_key(self):
        """Test get() returns None for missing keys."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = pathlib.Path(tmpdir) / "config.toml"
            manager = ConfigManager(config_path)
            value = manager.get("nonexistent.key")
            assert value is None

    def test_get_with_default(self):
        """Test get() returns default for missing keys."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = pathlib.Path(tmpdir) / "config.toml"
            manager = ConfigManager(config_path)
            value = manager.get("nonexistent.key", default="fallback")
            assert value == "fallback"
