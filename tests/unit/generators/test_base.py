"""Unit tests for base generator abstract class."""

import pytest
from abc import ABC
from clinkey_cli.generators.base import BaseGenerator


class TestBaseGenerator:
    """Test BaseGenerator abstract class."""

    def test_base_generator_is_abstract(self):
        """Test that BaseGenerator cannot be instantiated directly."""
        with pytest.raises(TypeError):
            BaseGenerator()

    def test_base_generator_has_generate_method(self):
        """Test that BaseGenerator defines abstract generate method."""
        assert hasattr(BaseGenerator, 'generate')
        assert getattr(BaseGenerator.generate, '__isabstractmethod__', False)
