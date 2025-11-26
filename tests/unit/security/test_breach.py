"""Unit tests for breach checker."""

import pytest
from unittest.mock import AsyncMock, Mock, patch

from clinkey_cli.security.breach import (
    hash_password_sha1,
    get_hash_prefix_suffix,
    check_breach_api,
    analyze_breach,
)


class TestPasswordHashing:
    """Test password hashing for k-anonymity."""

    def test_hash_password_sha1(self):
        """Test SHA-1 hashing of password."""
        # "password" -> 5BAA61E4C9B93F3F0682250B6CF8331B7EE68FD8
        hash_val = hash_password_sha1("password")
        assert hash_val == "5BAA61E4C9B93F3F0682250B6CF8331B7EE68FD8"
        assert len(hash_val) == 40

    def test_get_hash_prefix_suffix(self):
        """Test splitting hash into prefix and suffix."""
        hash_val = "5BAA61E4C9B93F3F0682250B6CF8331B7EE68FD8"
        prefix, suffix = get_hash_prefix_suffix(hash_val)
        assert prefix == "5BAA6"
        assert suffix == "1E4C9B93F3F0682250B6CF8331B7EE68FD8"
        assert len(prefix) == 5
        assert len(suffix) == 35


class TestBreachAPICheck:
    """Test breach API checking."""

    @pytest.mark.asyncio
    async def test_check_breach_api_mock_found(self):
        """Test breach check with mocked API (found)."""
        # Mock API response
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.text = "1E4C9B93F3F0682250B6CF8331B7EE68FD8:3861493"
        mock_response.raise_for_status = Mock()

        with patch("httpx.AsyncClient.get", return_value=mock_response):
            result = await check_breach_api("password")
            assert result["is_breached"] is True
            assert result["breach_count"] > 0

    @pytest.mark.asyncio
    async def test_check_breach_api_mock_not_found(self):
        """Test breach check with mocked API (not found)."""
        # Mock API response without our hash
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.text = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA:123"
        mock_response.raise_for_status = Mock()

        with patch("httpx.AsyncClient.get", return_value=mock_response):
            result = await check_breach_api("Xk9mP2qR7!")
            assert result["is_breached"] is False
            assert result["breach_count"] == 0


class TestAnalyzeBreach:
    """Test comprehensive breach analysis."""

    @pytest.mark.asyncio
    async def test_analyze_breach_structure(self):
        """Test breach analysis returns expected structure."""
        # Mock to avoid actual API call
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.text = ""
        mock_response.raise_for_status = Mock()

        with patch("httpx.AsyncClient.get", return_value=mock_response):
            result = await analyze_breach("testpass")
            assert "is_breached" in result
            assert "breach_count" in result
            assert "score_penalty" in result
            assert "checked" in result

    @pytest.mark.asyncio
    async def test_analyze_breach_penalty(self):
        """Test breached password gets penalty."""
        # Mock breached password
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.text = "1E4C9B93F3F0682250B6CF8331B7EE68FD8:1000000"
        mock_response.raise_for_status = Mock()

        with patch("httpx.AsyncClient.get", return_value=mock_response):
            result = await analyze_breach("password")
            assert result["is_breached"] is True
            assert result["score_penalty"] == 100
