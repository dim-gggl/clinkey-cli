"""Main security analyzer coordinating all analysis components."""

from typing import Any

from clinkey_cli.security.entropy import get_entropy_score
from clinkey_cli.security.patterns import analyze_patterns


class SecurityAnalyzer:
    """Coordinate all security analysis components.

    Combines entropy, pattern, dictionary, breach, context, and compliance
    analysis into a unified security assessment.

    Methods
    -------
    analyze(password: str, **options) -> dict
        Perform comprehensive security analysis.
    """

    def __init__(self):
        """Initialize security analyzer."""
        pass

    def analyze(
        self,
        password: str,
        check_breach: bool = False,
        check_dictionary: bool = True,
        check_patterns: bool = True,
    ) -> dict[str, Any]:
        """Analyze password security.

        Parameters
        ----------
        password : str
            Password to analyze.
        check_breach : bool, default False
            Check against breach databases.
        check_dictionary : bool, default True
            Check against common password dictionaries.
        check_patterns : bool, default True
            Detect security-weakening patterns.

        Returns
        -------
        dict
            Comprehensive security analysis results.
        """
        # Entropy analysis (always performed)
        entropy = get_entropy_score(password)

        # Pattern analysis (optional)
        patterns = analyze_patterns(password) if check_patterns else {}

        # Dictionary analysis (Phase 2 Task 5)
        dictionary = {} if not check_dictionary else {}

        # Breach check (Phase 2 Task 6)
        breach = {} if not check_breach else {}

        # Context analysis (Phase 2 Task 7)
        context = {}

        # Compliance validation (Phase 2 Task 8)
        compliance = {}

        # Calculate overall strength score
        strength_score = self._calculate_strength_score(
            entropy, patterns, dictionary, breach
        )

        # Determine strength label
        strength_label = self._get_strength_label(strength_score)

        # Generate recommendations
        recommendations = self._generate_recommendations(
            entropy, patterns, dictionary, breach, strength_score
        )

        return {
            "entropy": entropy,
            "patterns": patterns,
            "dictionary": dictionary,
            "breach": breach,
            "context": context,
            "compliance": compliance,
            "strength_score": strength_score,
            "strength_label": strength_label,
            "recommendations": recommendations,
        }

    def _calculate_strength_score(
        self,
        entropy: dict,
        patterns: dict,
        dictionary: dict,
        breach: dict,
    ) -> int:
        """Calculate overall strength score (0-100).

        Parameters
        ----------
        entropy : dict
            Entropy analysis results.
        patterns : dict
            Pattern analysis results.
        dictionary : dict
            Dictionary analysis results.
        breach : dict
            Breach check results.

        Returns
        -------
        int
            Strength score from 0 (very weak) to 100 (very strong).
        """
        # Base score from charset entropy
        charset_entropy = entropy.get("charset_entropy", 0)
        base_score = min(charset_entropy * 1.5, 100)

        # Deduct for patterns
        if patterns:
            pattern_penalty = patterns.get("entropy_reduction", 0)
            base_score -= pattern_penalty

        # Deduct for dictionary matches (Phase 2 Task 5)
        # Deduct for breaches (Phase 2 Task 6)

        # Ensure score is in range [0, 100]
        return max(0, min(100, int(base_score)))

    def _get_strength_label(self, score: int) -> str:
        """Get human-readable strength label.

        Parameters
        ----------
        score : int
            Strength score 0-100.

        Returns
        -------
        str
            Strength label.
        """
        if score < 20:
            return "Very Weak"
        elif score < 40:
            return "Weak"
        elif score < 60:
            return "Moderate"
        elif score < 80:
            return "Strong"
        else:
            return "Very Strong"

    def _generate_recommendations(
        self,
        entropy: dict,
        patterns: dict,
        dictionary: dict,
        breach: dict,
        score: int,
    ) -> list[str]:
        """Generate actionable security recommendations.

        Parameters
        ----------
        entropy : dict
            Entropy analysis.
        patterns : dict
            Pattern analysis.
        dictionary : dict
            Dictionary analysis.
        breach : dict
            Breach check.
        score : int
            Overall strength score.

        Returns
        -------
        list[str]
            List of recommendations.
        """
        recommendations = []

        # Length recommendations
        length = entropy.get("length", 0)
        if length < 12:
            recommendations.append(
                f"Increase length to at least 12 characters (current: {length})"
            )
        elif length < 16:
            recommendations.append(
                f"Consider increasing length to 16+ characters (current: {length})"
            )

        # Character set recommendations
        charset_size = entropy.get("charset_size", 0)
        if charset_size < 62:
            recommendations.append(
                "Use a mix of uppercase, lowercase, digits, and symbols"
            )

        # Pattern recommendations
        if patterns:
            pattern_count = patterns.get("pattern_count", 0)
            if pattern_count > 0:
                recommendations.append(
                    f"Avoid predictable patterns ({pattern_count} detected)"
                )

        # Overall score recommendation
        if score < 60:
            recommendations.append(
                "Consider using a password generator for stronger passwords"
            )

        return recommendations


def analyze_password(
    password: str,
    check_breach: bool = False,
    check_dictionary: bool = True,
    check_patterns: bool = True,
) -> dict[str, Any]:
    """Convenience function for password analysis.

    Parameters
    ----------
    password : str
        Password to analyze.
    check_breach : bool, default False
        Check against breach databases.
    check_dictionary : bool, default True
        Check against common password dictionaries.
    check_patterns : bool, default True
        Detect security-weakening patterns.

    Returns
    -------
    dict
        Security analysis results.

    Examples
    --------
    >>> result = analyze_password("MyPassword123")
    >>> result["strength_score"]
    45
    """
    analyzer = SecurityAnalyzer()
    return analyzer.analyze(
        password,
        check_breach=check_breach,
        check_dictionary=check_dictionary,
        check_patterns=check_patterns,
    )
