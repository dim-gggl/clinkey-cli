"""Unit tests for generator registry."""

import pytest

from clinkey_cli.generators.base import BaseGenerator
from clinkey_cli.generators.passphrase import PassphraseGenerator
from clinkey_cli.generators.pattern import PatternGenerator
from clinkey_cli.generators.registry import GeneratorRegistry
from clinkey_cli.generators.syllable import SyllableGenerator


class TestGeneratorRegistry:
    """Test GeneratorRegistry class."""

    def test_registry_creation(self):
        """Test registry instance creation."""
        registry = GeneratorRegistry()
        assert registry is not None

    def test_register_generator(self):
        """Test registering a generator."""
        registry = GeneratorRegistry()
        registry.register("test", SyllableGenerator)
        assert "test" in registry.list_generators()

    def test_get_registered_generator(self):
        """Test retrieving registered generator."""
        registry = GeneratorRegistry()
        registry.register("syllable", SyllableGenerator)
        gen_class = registry.get("syllable")
        assert gen_class == SyllableGenerator

    def test_get_unregistered_generator(self):
        """Test retrieving unregistered generator raises error."""
        registry = GeneratorRegistry()
        with pytest.raises(ValueError, match="Unknown generator"):
            registry.get("nonexistent")

    def test_list_generators_empty(self):
        """Test listing generators when registry is empty."""
        registry = GeneratorRegistry()
        assert registry.list_generators() == []

    def test_list_generators_multiple(self):
        """Test listing multiple registered generators."""
        registry = GeneratorRegistry()
        registry.register("syllable", SyllableGenerator)
        registry.register("passphrase", PassphraseGenerator)
        registry.register("pattern", PatternGenerator)
        generators = registry.list_generators()
        assert len(generators) == 3
        assert "syllable" in generators
        assert "passphrase" in generators
        assert "pattern" in generators


class TestDefaultRegistry:
    """Test default global registry."""

    def test_default_registry_has_syllable_generators(self):
        """Test default registry includes syllable generators."""
        from clinkey_cli.generators.registry import registry

        generators = registry.list_generators()
        assert "normal" in generators
        assert "strong" in generators
        assert "super_strong" in generators

    def test_default_registry_has_passphrase(self):
        """Test default registry includes passphrase generator."""
        from clinkey_cli.generators.registry import registry

        generators = registry.list_generators()
        assert "passphrase" in generators

    def test_default_registry_has_pattern(self):
        """Test default registry includes pattern generator."""
        from clinkey_cli.generators.registry import registry

        generators = registry.list_generators()
        assert "pattern" in generators

    def test_get_generator_from_default_registry(self):
        """Test retrieving generators from default registry."""
        from clinkey_cli.generators.registry import registry

        syllable_gen = registry.get("normal")
        assert syllable_gen == SyllableGenerator

        passphrase_gen = registry.get("passphrase")
        assert passphrase_gen == PassphraseGenerator

        pattern_gen = registry.get("pattern")
        assert pattern_gen == PatternGenerator
