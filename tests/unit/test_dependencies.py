"""Test that required dependencies are available."""

import pytest


def test_pytest_installed():
    """Test pytest is available."""
    import pytest

    assert pytest is not None


def test_pytest_asyncio_installed():
    """Test pytest-asyncio is available for Phase 2."""
    try:
        import pytest_asyncio

        assert pytest_asyncio is not None
    except ImportError:
        pytest.skip("pytest-asyncio not yet installed (expected in Phase 1)")


def test_hypothesis_installed():
    """Test hypothesis is available for property-based testing."""
    import hypothesis

    assert hypothesis is not None
