"""Configuration management for Clinkey 2.0.

Provides TOML-based configuration with sensible defaults and
environment variable overrides.
"""

from clinkey_cli.config.manager import ConfigManager, DEFAULT_CONFIG

__all__ = ["ConfigManager", "DEFAULT_CONFIG"]
