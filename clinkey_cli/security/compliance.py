"""Compliance validation against security standards.

Validates passwords against NIST SP 800-63B and OWASP password guidelines.
"""

from typing import Any


def check_nist_compliance(password: str) -> dict[str, Any]:
    """Check NIST SP 800-63B compliance.

    NIST Requirements:
    - Minimum 8 characters
    - Maximum 64+ characters (we allow unlimited)
    - Allow all printable ASCII + Unicode
    - No composition rules (we check but don't require)

    Parameters
    ----------
    password : str
        Password to validate.

    Returns
    -------
    dict[str, Any]
        NIST compliance results.

    Raises
    ------
    ValueError
        If password is not a string.

    Examples
    --------
    >>> result = check_nist_compliance("MySecurePass123!")
    >>> result["compliant"]
    True
    """
    if not isinstance(password, str):
        raise ValueError("password must be a string")

    violations = []

    # Minimum length: 8 characters
    if len(password) < 8:
        violations.append("min_length")

    # NIST doesn't require composition, but we note if it's simple
    # (this is informational, not a violation)

    return {
        "compliant": len(violations) == 0,
        "violations": violations,
        "standard": "NIST SP 800-63B",
    }


def check_owasp_compliance(password: str) -> dict[str, Any]:
    """Check OWASP password guidelines compliance.

    OWASP Requirements:
    - Minimum 10 characters (recommended)
    - At least 3 of 4 character types (uppercase, lowercase, digits, special)

    Parameters
    ----------
    password : str
        Password to validate.

    Returns
    -------
    dict[str, Any]
        OWASP compliance results.

    Raises
    ------
    ValueError
        If password is not a string.

    Examples
    --------
    >>> result = check_owasp_compliance("MySecurePass123!")
    >>> result["compliant"]
    True
    """
    if not isinstance(password, str):
        raise ValueError("password must be a string")

    violations = []

    # Minimum length: 10 characters
    if len(password) < 10:
        violations.append("min_length")

    # Character complexity: at least 3 of 4 types
    has_lowercase = any(c.islower() for c in password)
    has_uppercase = any(c.isupper() for c in password)
    has_digits = any(c.isdigit() for c in password)
    has_special = any(not c.isalnum() for c in password)

    char_types = sum([has_lowercase, has_uppercase, has_digits, has_special])
    if char_types < 3:
        violations.append("complexity")

    return {
        "compliant": len(violations) == 0,
        "violations": violations,
        "standard": "OWASP",
    }


def validate_compliance(password: str) -> dict[str, Any]:
    """Comprehensive compliance validation.

    Parameters
    ----------
    password : str
        Password to validate.

    Returns
    -------
    dict[str, Any]
        Compliance validation results for all standards.

    Raises
    ------
    ValueError
        If password is not a string.

    Examples
    --------
    >>> result = validate_compliance("MySecureP@ssw0rd!")
    >>> result["overall_compliant"]
    True
    """
    if not isinstance(password, str):
        raise ValueError("password must be a string")

    nist = check_nist_compliance(password)
    owasp = check_owasp_compliance(password)

    # Count standards met
    standards_met = sum([nist["compliant"], owasp["compliant"]])
    overall_compliant = standards_met >= 2  # Both standards

    return {
        "nist": nist,
        "owasp": owasp,
        "overall_compliant": overall_compliant,
        "standards_met": standards_met,
        "total_standards": 2,
    }
