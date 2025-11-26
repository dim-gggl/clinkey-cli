"""Unit tests for compliance validator."""

import pytest

from clinkey_cli.security.compliance import (
    check_nist_compliance,
    check_owasp_compliance,
    validate_compliance,
)


class TestNISTCompliance:
    """Test NIST SP 800-63B compliance."""

    def test_nist_compliant_password(self):
        """Test NIST compliant password."""
        result = check_nist_compliance("MySecurePass123!")
        assert result["compliant"] is True
        assert len(result["violations"]) == 0

    def test_nist_too_short(self):
        """Test NIST violation for short password."""
        result = check_nist_compliance("Pass1!")
        assert result["compliant"] is False
        assert "min_length" in result["violations"]

    def test_nist_minimum_length(self):
        """Test NIST minimum length (8 chars)."""
        result = check_nist_compliance("Pass123!")
        assert result["compliant"] is True

    def test_nist_exactly_8_chars(self):
        """Test NIST boundary - exactly 8 characters."""
        result = check_nist_compliance("12345678")
        assert result["compliant"] is True
        assert len(result["violations"]) == 0

    def test_nist_non_string_input(self):
        """Test NIST raises ValueError for non-string input."""
        with pytest.raises(ValueError, match="password must be a string"):
            check_nist_compliance(12345678)

        with pytest.raises(ValueError, match="password must be a string"):
            check_nist_compliance(None)

        with pytest.raises(ValueError, match="password must be a string"):
            check_nist_compliance(["password"])


class TestOWASPCompliance:
    """Test OWASP compliance."""

    def test_owasp_compliant_password(self):
        """Test OWASP compliant password."""
        result = check_owasp_compliance("MySecurePass123!")
        assert result["compliant"] is True
        assert len(result["violations"]) == 0

    def test_owasp_requires_complexity(self):
        """Test OWASP requires character complexity."""
        result = check_owasp_compliance("passwordonly")
        assert result["compliant"] is False
        assert "complexity" in result["violations"]

    def test_owasp_minimum_length(self):
        """Test OWASP minimum length (10 chars)."""
        result = check_owasp_compliance("Pass123!")
        assert result["compliant"] is False
        assert "min_length" in result["violations"]

    def test_owasp_exactly_10_chars(self):
        """Test OWASP boundary - exactly 10 characters."""
        result = check_owasp_compliance("Pass123!@#")
        assert result["compliant"] is True
        assert len(result["violations"]) == 0

    def test_owasp_non_string_input(self):
        """Test OWASP raises ValueError for non-string input."""
        with pytest.raises(ValueError, match="password must be a string"):
            check_owasp_compliance(1234567890)

        with pytest.raises(ValueError, match="password must be a string"):
            check_owasp_compliance(None)

        with pytest.raises(ValueError, match="password must be a string"):
            check_owasp_compliance({"password": "test"})


class TestValidateCompliance:
    """Test comprehensive compliance validation."""

    def test_validate_compliance_structure(self):
        """Test compliance validation returns expected structure."""
        result = validate_compliance("MySecurePass123!")
        assert "nist" in result
        assert "owasp" in result
        assert "overall_compliant" in result
        assert "standards_met" in result

    def test_validate_strong_password_compliant(self):
        """Test strong password meets all standards."""
        result = validate_compliance("MySecureP@ssw0rd!")
        assert result["overall_compliant"] is True
        assert result["standards_met"] >= 2

    def test_validate_weak_password_not_compliant(self):
        """Test weak password fails standards."""
        result = validate_compliance("pass")
        assert result["overall_compliant"] is False
        assert result["standards_met"] < 2

    def test_validate_nist_compliant_owasp_noncompliant(self):
        """Test password that meets NIST but not OWASP standards."""
        # 9 chars: meets NIST (8+) but not OWASP (10+)
        result = validate_compliance("Pass123!@")
        assert result["nist"]["compliant"] is True
        assert result["owasp"]["compliant"] is False
        assert result["overall_compliant"] is False
        assert result["standards_met"] == 1

    def test_validate_non_string_input(self):
        """Test validate_compliance raises ValueError for non-string input."""
        with pytest.raises(ValueError, match="password must be a string"):
            validate_compliance(12345)

        with pytest.raises(ValueError, match="password must be a string"):
            validate_compliance(None)

        with pytest.raises(ValueError, match="password must be a string"):
            validate_compliance([])
