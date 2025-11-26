"""Shared pytest fixtures for Clinkey tests."""

import pytest

from clinkey_cli.main import Clinkey


@pytest.fixture
def clinkey():
    """Provide a fresh Clinkey instance for each test."""
    return Clinkey()
