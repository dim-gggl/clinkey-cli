"""Syllable-based password generator.

Generates pronounceable passwords using consonant-vowel syllable patterns.
This is the original Clinkey generation method, refactored into the new
generator architecture while maintaining 100% backward compatibility.
"""

import secrets
import string
from typing import Callable

from clinkey_cli.generators.base import BaseGenerator

# Security and validation constants
MAX_PASSWORD_LENGTH = 128
MIN_PASSWORD_LENGTH = 16


class SyllableGenerator(BaseGenerator):
    """Generate pronounceable passwords using syllable patterns.

    Supports multiple complexity levels (normal, strong, super_strong) and
    customizable separators. Uses cryptographically secure randomness.

    Parameters
    ----------
    language : str, default "english"
        Syllable set language (currently only "english" supported).

    Attributes
    ----------
    _consonants : list[str]
        Consonants used to build syllables.
    _vowels : list[str]
        Vowels used to build syllables.
    _digits : list[str]
        Digits used in strong/super_strong passwords.
    _specials : list[str]
        Special characters used in super_strong passwords.
    _simple_syllables : list[str]
        Consonant-vowel pairs for basic pronounceability.
    _complex_syllables : list[str]
        More complex consonant clusters.
    _separators : list[str]
        Default separator characters.
    language : str
        Current language setting.
    """

    def __init__(self, language: str = "english"):
        """Initialize syllable generator with specified language.

        Parameters
        ----------
        language : str, default "english"
            Language for syllable patterns.
        """
        self.language = language

        # Character sets
        self._consonants = list("bcdfghjklmnpqrstvwxz")
        self._vowels = list("aeiouy")
        self._digits = list(string.digits)
        self._specials = list("!@#$%^&*()-_=+[]{}|;:,.<>?")

        # Build syllable sets
        self._simple_syllables = [
            c + v for c in self._consonants for v in self._vowels
        ]
        self._complex_syllables = [
            "ch", "sh", "th", "ph", "qu", "tr", "br", "cr", "dr",
            "fr", "gr", "pr", "st", "bl", "cl", "fl", "gl", "pl",
            "sl", "sc", "sk", "sm", "sn", "sp", "sw"
        ]

        # Default separators
        self._separators = ["-", "_"]

        # Generator method mapping
        self._generators: dict[str, Callable[[], str]] = {
            "normal": self._normal,
            "strong": self._strong,
            "super_strong": self._super_strong,
        }

    def generate(
        self,
        length: int,
        password_type: str = "normal",
        lower: bool = False,
        no_separator: bool = False,
        separator: str | None = None,
    ) -> str:
        """Generate syllable-based password.

        Parameters
        ----------
        length : int
            Target password length.
        password_type : str, default "normal"
            Password complexity: "normal", "strong", or "super_strong".
        lower : bool, default False
            Convert to lowercase if True.
        no_separator : bool, default False
            Remove separators if True.
        separator : str | None, default None
            Custom separator to use instead of default.

        Returns
        -------
        str
            Generated password of specified length.

        Raises
        ------
        ValueError
            If length is invalid or password_type is unsupported.
        """
        # Validate length
        if length < MIN_PASSWORD_LENGTH:
            raise ValueError(
                f"length must be at least {MIN_PASSWORD_LENGTH}, got {length}"
            )
        if length > MAX_PASSWORD_LENGTH:
            raise ValueError(
                f"length cannot exceed {MAX_PASSWORD_LENGTH}, got {length}"
            )

        # Validate password type
        if password_type not in self._generators:
            valid_types = ", ".join(sorted(self._generators.keys()))
            raise ValueError(
                f"Unsupported type: '{password_type}'. "
                f"Valid types: {valid_types}"
            )

        # Generate base password
        generator = self._generators[password_type]
        password = generator()

        # Fit to target length
        password = self.fit_to_length(password, length)

        # Apply transformations
        password = self.transform(password, lower, no_separator, separator)

        return password

    def _normal(self) -> str:
        """Generate normal password: letters and separators only.

        Returns
        -------
        str
            Password with syllables and separators.
        """
        chunks = []
        for _ in range(10):  # Generate enough chunks
            # Randomly choose simple or complex syllable
            if secrets.randbelow(2) == 0:
                chunks.append(secrets.choice(self._simple_syllables).upper())
            else:
                chunks.append(secrets.choice(self._complex_syllables).upper())

            # Add separator
            chunks.append(secrets.choice(self._separators))

        return "".join(chunks)

    def _strong(self) -> str:
        """Generate strong password: letters, digits, and separators.

        Returns
        -------
        str
            Password with syllables, digits, and separators.
        """
        chunks = []
        for i in range(10):
            # Syllable
            if secrets.randbelow(2) == 0:
                chunks.append(secrets.choice(self._simple_syllables).upper())
            else:
                chunks.append(secrets.choice(self._complex_syllables).upper())

            # Occasionally add digit block
            if i % 2 == 0:
                digit_block = "".join(
                    secrets.choice(self._digits) for _ in range(2)
                )
                chunks.append(digit_block)

            # Add separator
            chunks.append(secrets.choice(self._separators))

        return "".join(chunks)

    def _super_strong(self) -> str:
        """Generate super strong password: letters, digits, specials, separators.

        Returns
        -------
        str
            Password with all character types.
        """
        chunks = []
        for i in range(12):
            # Syllable
            if secrets.randbelow(2) == 0:
                chunks.append(secrets.choice(self._simple_syllables).upper())
            else:
                chunks.append(secrets.choice(self._complex_syllables).upper())

            # Add digit block
            if i % 2 == 0:
                digit_block = "".join(
                    secrets.choice(self._digits) for _ in range(2)
                )
                chunks.append(digit_block)

            # Add special character
            if i % 3 == 0:
                chunks.append(secrets.choice(self._specials))

            # Add separator
            chunks.append(secrets.choice(self._separators))

        return "".join(chunks)

    # Backward compatibility methods (called by Clinkey adapter)
    def normal(self) -> str:
        """Generate normal password (backward compatibility).

        Returns
        -------
        str
            Normal password.
        """
        return self._normal()

    def strong(self) -> str:
        """Generate strong password (backward compatibility).

        Returns
        -------
        str
            Strong password.
        """
        return self._strong()

    def super_strong(self) -> str:
        """Generate super strong password (backward compatibility).

        Returns
        -------
        str
            Super strong password.
        """
        return self._super_strong()
