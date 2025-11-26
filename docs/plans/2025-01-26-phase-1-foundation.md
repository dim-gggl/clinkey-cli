# Clinkey 2.0.0 - Phase 1: Foundation Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Refactor existing Clinkey 1.2.0 codebase into new modular architecture with zero breaking changes, establishing foundation for 2.0 features.

**Architecture:** Extract current `Clinkey` class into new `generators/` module structure with base class abstraction. Maintain 100% backward compatibility via adapter pattern. All existing tests must pass unchanged.

**Tech Stack:** Python 3.10+, pytest, existing dependencies (click, rich)

**Success Criteria:**
- All existing tests pass without modification
- New modular structure in place
- Backward compatibility verified
- Ready for Phase 2 (Security Engine)

---

## Task 1: Create New Module Structure

**Files:**
- Create: `clinkey_cli/generators/__init__.py`
- Create: `clinkey_cli/generators/base.py`
- Create: `tests/unit/__init__.py`
- Create: `tests/unit/generators/__init__.py`

**Step 1: Write test for module imports**

Create `tests/unit/__init__.py`:
```python
"""Unit tests for Clinkey 2.0 components."""
```

Create `tests/unit/generators/__init__.py`:
```python
"""Tests for password generator implementations."""
```

Create `tests/unit/generators/test_base.py`:
```python
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
```

**Step 2: Run test to verify it fails**

Run:
```bash
cd /Users/dim-gggl/~/Dev\ Tools/Clinkey
pytest tests/unit/generators/test_base.py::TestBaseGenerator::test_base_generator_is_abstract -v
```

Expected: `FAIL` with "ModuleNotFoundError: No module named 'clinkey_cli.generators'"

**Step 3: Create generators module structure**

Create `clinkey_cli/generators/__init__.py`:
```python
"""Password generator implementations for Clinkey 2.0.

This module provides the base generator interface and concrete implementations
for different password generation strategies.
"""

from clinkey_cli.generators.base import BaseGenerator

__all__ = ["BaseGenerator"]
```

**Step 4: Implement BaseGenerator abstract class**

Create `clinkey_cli/generators/base.py`:
```python
"""Base generator abstract class for all password generators.

Defines the common interface that all password generators must implement,
along with shared utility methods for password transformation.
"""

from abc import ABC, abstractmethod


class BaseGenerator(ABC):
    """Abstract base class for all password generators.

    All password generators must inherit from this class and implement
    the `generate` method. This ensures a consistent API across all
    generator types.

    Methods
    -------
    generate(length: int, **kwargs) -> str
        Generate a password of specified length with optional parameters.
    fit_to_length(password: str, target_length: int) -> str
        Fit password to exact target length by truncating or padding.
    transform(password: str, lower: bool, no_separator: bool, separator: str | None) -> str
        Apply transformations to generated password.
    """

    @abstractmethod
    def generate(self, length: int, **kwargs) -> str:
        """Generate a password of specified length.

        Parameters
        ----------
        length : int
            Target length for the generated password.
        **kwargs : dict
            Additional generator-specific parameters.

        Returns
        -------
        str
            Generated password matching requested length.

        Raises
        ------
        ValueError
            If length is invalid or parameters are incompatible.
        """
        pass

    def fit_to_length(self, password: str, target_length: int) -> str:
        """Fit password to exact target length.

        Parameters
        ----------
        password : str
            Password to fit to target length.
        target_length : int
            Desired final length.

        Returns
        -------
        str
            Password adjusted to exact target length.
        """
        if len(password) == target_length:
            return password
        elif len(password) > target_length:
            return password[:target_length]
        else:
            # Repeat password until we reach target length
            repetitions = (target_length // len(password)) + 1
            return (password * repetitions)[:target_length]

    def transform(
        self,
        password: str,
        lower: bool = False,
        no_separator: bool = False,
        separator: str | None = None,
    ) -> str:
        """Apply transformations to password.

        Parameters
        ----------
        password : str
            Password to transform.
        lower : bool, default False
            Convert password to lowercase.
        no_separator : bool, default False
            Remove separator characters.
        separator : str | None, default None
            If provided, replace default separators with this character.

        Returns
        -------
        str
            Transformed password.
        """
        result = password

        # Apply separator transformations first
        if no_separator:
            # Remove common separators
            result = result.replace('-', '').replace('_', '')
        elif separator is not None:
            # Replace separators with custom character
            result = result.replace('-', separator).replace('_', separator)

        # Apply case transformation
        if lower:
            result = result.lower()

        return result
```

**Step 5: Run tests to verify they pass**

Run:
```bash
cd /Users/dim-gggl/~/Dev\ Tools/Clinkey
pytest tests/unit/generators/test_base.py -v
```

Expected: `PASS` (all tests green)

**Step 6: Commit**

```bash
cd /Users/dim-gggl/~/Dev\ Tools/Clinkey
git add clinkey_cli/generators/ tests/unit/
git commit -m "feat: add BaseGenerator abstract class and module structure

- Create clinkey_cli/generators module
- Implement BaseGenerator with abstract generate() method
- Add fit_to_length() and transform() utility methods
- Set up tests/unit/generators test structure
- All tests passing

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## Task 2: Extract SyllableGenerator from Clinkey Class

**Files:**
- Create: `clinkey_cli/generators/syllable.py`
- Create: `tests/unit/generators/test_syllable.py`
- Modify: `clinkey_cli/generators/__init__.py`

**Step 1: Write failing test for SyllableGenerator**

Create `tests/unit/generators/test_syllable.py`:
```python
"""Unit tests for syllable-based password generator."""

import pytest
import re
from clinkey_cli.generators.syllable import SyllableGenerator


class TestSyllableGeneratorInit:
    """Test SyllableGenerator initialization."""

    def test_syllable_generator_creation(self):
        """Test that SyllableGenerator instance is created successfully."""
        gen = SyllableGenerator()
        assert gen is not None

    def test_syllable_generator_has_syllables(self):
        """Test that syllable lists are populated."""
        gen = SyllableGenerator()
        assert hasattr(gen, '_simple_syllables')
        assert hasattr(gen, '_complex_syllables')
        assert len(gen._simple_syllables) > 0
        assert len(gen._complex_syllables) > 0

    def test_syllable_generator_default_language(self):
        """Test default language is English."""
        gen = SyllableGenerator()
        assert gen.language == "english"


class TestSyllableGeneratorGenerate:
    """Test password generation."""

    @pytest.fixture
    def gen(self):
        """Provide a fresh SyllableGenerator instance."""
        return SyllableGenerator()

    def test_generate_default(self, gen):
        """Test generate with default parameters."""
        password = gen.generate(length=16)
        assert isinstance(password, str)
        assert len(password) == 16

    @pytest.mark.parametrize("length", [10, 16, 20, 50])
    def test_generate_various_lengths(self, gen, length):
        """Test generate produces correct length."""
        password = gen.generate(length=length)
        assert len(password) == length

    def test_generate_normal_type(self, gen):
        """Test normal type generates letters and separators."""
        password = gen.generate(length=30, password_type="normal")
        assert re.match(r'^[A-Z\-_]+$', password)

    def test_generate_strong_type(self, gen):
        """Test strong type includes digits."""
        password = gen.generate(length=30, password_type="strong")
        assert re.match(r'^[A-Z0-9\-_]+$', password)
        assert any(c.isdigit() for c in password)

    def test_generate_super_strong_type(self, gen):
        """Test super_strong type includes specials."""
        password = gen.generate(length=40, password_type="super_strong")
        assert any(c.isalpha() for c in password)
        assert any(c.isdigit() for c in password)

    def test_generate_with_lowercase(self, gen):
        """Test lowercase transformation."""
        password = gen.generate(length=20, lower=True)
        assert password.islower() or not password.isalpha()

    def test_generate_no_separator(self, gen):
        """Test no_separator removes separators."""
        password = gen.generate(length=20, no_separator=True)
        assert '-' not in password
        assert '_' not in password

    def test_generate_custom_separator(self, gen):
        """Test custom separator replacement."""
        password = gen.generate(length=20, separator='@')
        # Should contain @ or be too short for separators
        assert '@' in password or len(password) < 10


class TestSyllableGeneratorValidation:
    """Test input validation."""

    @pytest.fixture
    def gen(self):
        """Provide a fresh SyllableGenerator instance."""
        return SyllableGenerator()

    def test_invalid_length_negative(self, gen):
        """Test negative length raises ValueError."""
        with pytest.raises(ValueError, match="length must be at least"):
            gen.generate(length=-1)

    def test_invalid_length_zero(self, gen):
        """Test zero length raises ValueError."""
        with pytest.raises(ValueError, match="length must be at least"):
            gen.generate(length=0)

    def test_invalid_type(self, gen):
        """Test invalid password type raises ValueError."""
        with pytest.raises(ValueError, match="Unsupported type"):
            gen.generate(length=16, password_type="invalid")
```

**Step 2: Run test to verify it fails**

Run:
```bash
cd /Users/dim-gggl/~/Dev\ Tools/Clinkey
pytest tests/unit/generators/test_syllable.py::TestSyllableGeneratorInit::test_syllable_generator_creation -v
```

Expected: `FAIL` with "ModuleNotFoundError: No module named 'clinkey_cli.generators.syllable'"

**Step 3: Implement SyllableGenerator by refactoring Clinkey class**

Create `clinkey_cli/generators/syllable.py`:
```python
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
```

**Step 4: Update generators __init__.py**

Modify `clinkey_cli/generators/__init__.py`:
```python
"""Password generator implementations for Clinkey 2.0.

This module provides the base generator interface and concrete implementations
for different password generation strategies.
"""

from clinkey_cli.generators.base import BaseGenerator
from clinkey_cli.generators.syllable import SyllableGenerator

__all__ = ["BaseGenerator", "SyllableGenerator"]
```

**Step 5: Run tests to verify they pass**

Run:
```bash
cd /Users/dim-gggl/~/Dev\ Tools/Clinkey
pytest tests/unit/generators/test_syllable.py -v
```

Expected: `PASS` (all tests green)

**Step 6: Commit**

```bash
cd /Users/dim-gggl/~/Dev\ Tools/Clinkey
git add clinkey_cli/generators/syllable.py tests/unit/generators/test_syllable.py clinkey_cli/generators/__init__.py
git commit -m "feat: implement SyllableGenerator extracted from Clinkey class

- Extract syllable generation logic into new SyllableGenerator class
- Maintain all existing generation methods (normal, strong, super_strong)
- Implement generate() method with unified interface
- Add comprehensive unit tests for syllable generator
- All tests passing

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## Task 3: Create Backward-Compatible Clinkey Adapter

**Files:**
- Modify: `clinkey_cli/main.py`
- Create: `tests/integration/__init__.py`
- Create: `tests/integration/test_backward_compatibility.py`

**Step 1: Write backward compatibility tests**

Create `tests/integration/__init__.py`:
```python
"""Integration tests for Clinkey 2.0."""
```

Create `tests/integration/test_backward_compatibility.py`:
```python
"""Integration tests verifying backward compatibility with Clinkey 1.x.

These tests ensure that the refactored architecture maintains 100%
compatibility with the 1.x API and behavior.
"""

import re
import pytest
from clinkey_cli.main import Clinkey, MAX_PASSWORD_LENGTH, MAX_BATCH_SIZE, MIN_PASSWORD_LENGTH


class TestBackwardCompatibleAPI:
    """Test that Clinkey class API is unchanged."""

    @pytest.fixture
    def clinkey(self):
        """Provide a fresh Clinkey instance."""
        return Clinkey()

    def test_clinkey_instance_creation(self, clinkey):
        """Test Clinkey instance creates successfully."""
        assert clinkey is not None

    def test_generate_password_signature(self, clinkey):
        """Test generate_password() method exists with correct signature."""
        password = clinkey.generate_password(
            length=16,
            type="normal",
            lower=False,
            no_separator=False,
            new_separator=None
        )
        assert isinstance(password, str)
        assert len(password) == 16

    def test_generate_batch_signature(self, clinkey):
        """Test generate_batch() method exists."""
        passwords = clinkey.generate_batch(
            count=5,
            length=16,
            type="normal"
        )
        assert isinstance(passwords, list)
        assert len(passwords) == 5

    def test_normal_method_exists(self, clinkey):
        """Test normal() method still exists."""
        password = clinkey.normal()
        assert isinstance(password, str)

    def test_strong_method_exists(self, clinkey):
        """Test strong() method still exists."""
        password = clinkey.strong()
        assert isinstance(password, str)

    def test_super_strong_method_exists(self, clinkey):
        """Test super_strong() method still exists."""
        password = clinkey.super_strong()
        assert isinstance(password, str)


class TestBackwardCompatibleBehavior:
    """Test that behavior matches 1.x exactly."""

    @pytest.fixture
    def clinkey(self):
        """Provide a fresh Clinkey instance."""
        return Clinkey()

    def test_default_password_length(self, clinkey):
        """Test default length is 16."""
        password = clinkey.generate_password()
        assert len(password) == 16

    def test_normal_password_pattern(self, clinkey):
        """Test normal password pattern unchanged."""
        password = clinkey.generate_password(type="normal", length=30)
        assert re.match(r'^[A-Z\-_]+$', password)

    def test_strong_password_has_digits(self, clinkey):
        """Test strong password includes digits."""
        password = clinkey.generate_password(type="strong", length=30)
        assert any(c.isdigit() for c in password)

    def test_lowercase_transformation(self, clinkey):
        """Test lowercase flag works."""
        password = clinkey.generate_password(lower=True, length=20)
        assert password.islower() or not password.isalpha()

    def test_no_separator_flag(self, clinkey):
        """Test no_separator removes separators."""
        password = clinkey.generate_password(no_separator=True, length=20)
        assert '-' not in password
        assert '_' not in password

    def test_custom_separator(self, clinkey):
        """Test custom separator via new_separator."""
        password = clinkey.generate_password(new_separator='@', length=20)
        assert '@' in password or len(password) < 10


class TestBackwardCompatibleValidation:
    """Test that validation errors match 1.x."""

    @pytest.fixture
    def clinkey(self):
        """Provide a fresh Clinkey instance."""
        return Clinkey()

    def test_invalid_length_error(self, clinkey):
        """Test invalid length raises ValueError."""
        with pytest.raises(ValueError):
            clinkey.generate_password(length=-1)

    def test_invalid_type_error(self, clinkey):
        """Test invalid type raises ValueError."""
        with pytest.raises(ValueError):
            clinkey.generate_password(type="invalid")

    def test_invalid_separator_error(self, clinkey):
        """Test invalid separator raises ValueError."""
        with pytest.raises(ValueError):
            clinkey.generate_password(new_separator="@@")


class TestBackwardCompatibleConstants:
    """Test that module constants are unchanged."""

    def test_max_password_length_constant(self):
        """Test MAX_PASSWORD_LENGTH is accessible."""
        assert MAX_PASSWORD_LENGTH == 128

    def test_max_batch_size_constant(self):
        """Test MAX_BATCH_SIZE is accessible."""
        assert MAX_BATCH_SIZE == 500

    def test_min_password_length_constant(self):
        """Test MIN_PASSWORD_LENGTH is accessible."""
        assert MIN_PASSWORD_LENGTH == 16
```

**Step 2: Run tests to verify they fail**

Run:
```bash
cd /Users/dim-gggl/~/Dev\ Tools/Clinkey
pytest tests/integration/test_backward_compatibility.py -v
```

Expected: `FAIL` (tests fail because Clinkey not yet adapted)

**Step 3: Refactor main.py to use SyllableGenerator**

Modify `clinkey_cli/main.py`:
```python
"""
Core password generation logic for the Clinkey CLI package.

Exposes the :class:`Clinkey` password generator and a module-level ``clinkey``
instance used by the CLI entrypoints.

Note: This module now serves as a backward-compatible adapter to the new
generator architecture. The actual generation logic is in generators/syllable.py.
"""

import secrets
import string
from typing import Callable, Dict

from clinkey_cli.generators.syllable import (
    SyllableGenerator,
    MAX_PASSWORD_LENGTH,
    MIN_PASSWORD_LENGTH,
)

# Re-export constants for backward compatibility
__all__ = [
    "Clinkey",
    "MAX_PASSWORD_LENGTH",
    "MAX_BATCH_SIZE",
    "MIN_PASSWORD_LENGTH",
    "SAFE_SEPARATOR_CHARS",
]

# Security and validation constants
MAX_BATCH_SIZE = 500

# Safe separator characters (printable, non-whitespace)
SAFE_SEPARATOR_CHARS = string.printable.replace(' \t\n\r\x0b\x0c', '')


class Clinkey:
    """Generate pronounceable passwords with configurable complexity levels.

    This class serves as a backward-compatible adapter to the new generator
    architecture introduced in Clinkey 2.0. It delegates to SyllableGenerator
    while maintaining the exact same API as Clinkey 1.x.

    Attributes
    ----------
    _generator : SyllableGenerator
        Internal syllable generator instance.
    _consonants : list[str]
        Consonants from the Latin alphabet (for backward compatibility).
    _vowels : list[str]
        Vowels from the Latin alphabet (for backward compatibility).
    _digits : list[str]
        Digits from ``0`` through ``9`` (for backward compatibility).
    _specials : list[str]
        Safe special characters (for backward compatibility).
    _simple_syllables : list[str]
        Consonant/vowel pairs (for backward compatibility).
    _complex_syllables : list[str]
        Predefined consonant clusters (for backward compatibility).
    _separators : list[str]
        Default separators (for backward compatibility).
    _generators : dict[str, Callable[[], str]]
        Mapping of password type to generator method (for backward compatibility).
    new_separator : str | None
        Custom separator overriding defaults (for backward compatibility).

    Methods
    -------
    normal()
        Generate a pronounceable password made of words and separators.
    strong()
        Generate a password made of words, digits, and separators.
    super_strong()
        Generate a password with all character types.
    generate_password(...)
        Generate a single password with specified parameters.
    generate_batch(...)
        Generate multiple passwords.
    """

    def __init__(self, new_separator: str | None = None):
        """Initialize the Clinkey password generator.

        Parameters
        ----------
        new_separator : str | None, default None
            Optional custom separator to use instead of default - and _.
            Must be exactly one printable, non-whitespace character.

        Raises
        ------
        ValueError
            If new_separator is provided but is not a valid single character.
        """
        # Initialize internal generator
        self._generator = SyllableGenerator(language="english")

        # Store custom separator (backward compatibility)
        self.new_separator = new_separator

        # Validate custom separator if provided
        if new_separator is not None:
            if len(new_separator) != 1:
                raise ValueError(
                    f"new_separator must be exactly one character, "
                    f"got {len(new_separator)} characters"
                )
            if new_separator not in SAFE_SEPARATOR_CHARS:
                raise ValueError(
                    f"new_separator must be a safe printable character, "
                    f"got '{new_separator}'"
                )

        # Expose internal attributes for backward compatibility
        self._consonants = self._generator._consonants
        self._vowels = self._generator._vowels
        self._digits = self._generator._digits
        self._specials = self._generator._specials
        self._simple_syllables = self._generator._simple_syllables
        self._complex_syllables = self._generator._complex_syllables
        self._separators = self._generator._separators
        self._generators = {
            "normal": self.normal,
            "strong": self.strong,
            "super_strong": self.super_strong,
        }

    def normal(self) -> str:
        """Generate a pronounceable password made of words and separators.

        Returns
        -------
        str
            A password containing uppercase letters and separators.

        Examples
        --------
        >>> clinkey = Clinkey()
        >>> password = clinkey.normal()
        >>> len(password) > 0
        True
        """
        return self._generator.normal()

    def strong(self) -> str:
        """Generate a password made of words, digits, and separators.

        Returns
        -------
        str
            A password with uppercase letters, digits, and separators.

        Examples
        --------
        >>> clinkey = Clinkey()
        >>> password = clinkey.strong()
        >>> any(c.isdigit() for c in password)
        True
        """
        return self._generator.strong()

    def super_strong(self) -> str:
        """Generate a password with all character types.

        Returns
        -------
        str
            A password with letters, digits, special chars, and separators.

        Examples
        --------
        >>> clinkey = Clinkey()
        >>> password = clinkey.super_strong()
        >>> any(c.isalpha() for c in password)
        True
        """
        return self._generator.super_strong()

    def generate_password(
        self,
        length: int = 16,
        type: str = "normal",
        lower: bool = False,
        no_separator: bool = False,
        new_separator: str | None = None,
    ) -> str:
        """Generate a single password matching the requested configuration.

        Parameters
        ----------
        length : int, default 16
            Length of the password to produce.
        type : str, default "normal"
            Password preset to use. Options: "normal", "strong", "super_strong".
        lower : bool, default False
            Convert the final password to lowercase if True.
        no_separator : bool, default False
            Remove separator characters if True.
        new_separator : str | None, default None
            Custom separator character to use instead of defaults.

        Returns
        -------
        str
            Generated password.

        Raises
        ------
        ValueError
            If length is not strictly positive, exceeds max, is below min,
            or type is unknown.
            If new_separator is not exactly one safe printable character.

        Examples
        --------
        >>> clinkey = Clinkey()
        >>> password = clinkey.generate_password(length=20, type="strong")
        >>> len(password)
        20
        """
        # Validate separator if provided
        separator_to_use = new_separator or self.new_separator
        if separator_to_use is not None:
            if len(separator_to_use) != 1:
                raise ValueError(
                    f"new_separator must be exactly one character, "
                    f"got {len(separator_to_use)} characters"
                )
            if separator_to_use not in SAFE_SEPARATOR_CHARS:
                raise ValueError(
                    f"new_separator must be a safe printable character, "
                    f"got '{separator_to_use}'"
                )

        # Delegate to generator
        return self._generator.generate(
            length=length,
            password_type=type,
            lower=lower,
            no_separator=no_separator,
            separator=separator_to_use,
        )

    def generate_batch(
        self,
        count: int,
        length: int = 16,
        type: str = "normal",
        lower: bool = False,
        no_separator: bool = False,
        new_separator: str | None = None,
    ) -> list[str]:
        """Generate multiple passwords with the same configuration.

        Parameters
        ----------
        count : int
            Number of passwords to generate.
        length : int, default 16
            Length of each password.
        type : str, default "normal"
            Password preset to use.
        lower : bool, default False
            Convert passwords to lowercase if True.
        no_separator : bool, default False
            Remove separator characters if True.
        new_separator : str | None, default None
            Custom separator character to use.

        Returns
        -------
        list[str]
            List of generated passwords.

        Raises
        ------
        ValueError
            If count is not a positive integer or exceeds MAX_BATCH_SIZE.

        Examples
        --------
        >>> clinkey = Clinkey()
        >>> passwords = clinkey.generate_batch(count=5, length=16)
        >>> len(passwords)
        5
        """
        # Validate count
        if count <= 0:
            raise ValueError(
                f"count must be a positive integer, got {count}"
            )
        if count > MAX_BATCH_SIZE:
            raise ValueError(
                f"count cannot exceed {MAX_BATCH_SIZE}, got {count}"
            )

        # Generate batch
        return [
            self.generate_password(
                length=length,
                type=type,
                lower=lower,
                no_separator=no_separator,
                new_separator=new_separator,
            )
            for _ in range(count)
        ]
```

**Step 4: Run integration tests to verify backward compatibility**

Run:
```bash
cd /Users/dim-gggl/~/Dev\ Tools/Clinkey
pytest tests/integration/test_backward_compatibility.py -v
```

Expected: `PASS` (all backward compatibility tests pass)

**Step 5: Run original unit tests to ensure nothing broke**

Run:
```bash
cd /Users/dim-gggl/~/Dev\ Tools/Clinkey
pytest tests/test_main.py -v
```

Expected: `PASS` (all original tests still pass)

**Step 6: Run ALL tests to verify complete compatibility**

Run:
```bash
cd /Users/dim-gggl/~/Dev\ Tools/Clinkey
pytest tests/ -v
```

Expected: `PASS` (100% test pass rate)

**Step 7: Commit**

```bash
cd /Users/dim-gggl/~/Dev\ Tools/Clinkey
git add clinkey_cli/main.py tests/integration/
git commit -m "refactor: adapt Clinkey class to use SyllableGenerator

- Refactor Clinkey to delegate to SyllableGenerator
- Maintain 100% backward compatibility with 1.x API
- Add comprehensive backward compatibility integration tests
- All existing tests pass without modification
- Ready for Phase 2 feature development

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com)"
```

---

## Task 4: Add Configuration System Foundation

**Files:**
- Create: `clinkey_cli/config/__init__.py`
- Create: `clinkey_cli/config/manager.py`
- Create: `tests/unit/config/__init__.py`
- Create: `tests/unit/config/test_manager.py`

**Step 1: Write test for config module**

Create `tests/unit/config/__init__.py`:
```python
"""Tests for configuration management."""
```

Create `tests/unit/config/test_manager.py`:
```python
"""Unit tests for configuration manager."""

import pytest
import tempfile
import pathlib
from clinkey_cli.config.manager import ConfigManager, DEFAULT_CONFIG


class TestConfigManager:
    """Test ConfigManager class."""

    def test_config_manager_creation(self):
        """Test ConfigManager instance creation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = pathlib.Path(tmpdir) / "config.toml"
            manager = ConfigManager(config_path)
            assert manager is not None

    def test_default_config_structure(self):
        """Test default config has expected structure."""
        assert "general" in DEFAULT_CONFIG
        assert "security" in DEFAULT_CONFIG
        assert "vault" in DEFAULT_CONFIG
        assert "generators" in DEFAULT_CONFIG

    def test_get_default_value(self):
        """Test get() returns default values."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = pathlib.Path(tmpdir) / "config.toml"
            manager = ConfigManager(config_path)
            value = manager.get("general.default_length")
            assert value == 16

    def test_get_nested_value(self):
        """Test get() handles nested keys."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = pathlib.Path(tmpdir) / "config.toml"
            manager = ConfigManager(config_path)
            value = manager.get("generators.syllable.default_language")
            assert value == "english"

    def test_get_nonexistent_key(self):
        """Test get() returns None for missing keys."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = pathlib.Path(tmpdir) / "config.toml"
            manager = ConfigManager(config_path)
            value = manager.get("nonexistent.key")
            assert value is None

    def test_get_with_default(self):
        """Test get() returns default for missing keys."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path = pathlib.Path(tmpdir) / "config.toml"
            manager = ConfigManager(config_path)
            value = manager.get("nonexistent.key", default="fallback")
            assert value == "fallback"
```

**Step 2: Run test to verify it fails**

Run:
```bash
cd /Users/dim-gggl/~/Dev\ Tools/Clinkey
pytest tests/unit/config/test_manager.py::TestConfigManager::test_config_manager_creation -v
```

Expected: `FAIL` with "ModuleNotFoundError: No module named 'clinkey_cli.config'"

**Step 3: Implement ConfigManager**

Create `clinkey_cli/config/__init__.py`:
```python
"""Configuration management for Clinkey 2.0.

Provides TOML-based configuration with sensible defaults and
environment variable overrides.
"""

from clinkey_cli.config.manager import ConfigManager, DEFAULT_CONFIG

__all__ = ["ConfigManager", "DEFAULT_CONFIG"]
```

Create `clinkey_cli/config/manager.py`:
```python
"""Configuration manager for Clinkey settings.

Handles loading, merging, and accessing configuration from:
1. Default values (lowest priority)
2. Config file (~/.clinkey/config.toml)
3. Environment variables (CLINKEY_*)
4. Command-line flags (highest priority, handled by CLI)
"""

import os
import pathlib
from typing import Any


# Default configuration structure
DEFAULT_CONFIG = {
    "general": {
        "default_length": 16,
        "default_type": "normal",
        "interactive_mode": "rich",
        "auto_analyze": False,
        "clipboard_timeout": 30,
    },
    "security": {
        "min_password_length": 16,
        "max_password_length": 128,
        "min_strength_score": 0,
        "check_breaches": False,
        "offline_breach_db": "~/.clinkey/breaches.db",
    },
    "vault": {
        "database_path": "~/.clinkey/vault.db",
        "backup_path": "~/.clinkey/backups/",
        "auto_backup": True,
        "backup_interval": 7,
        "lock_timeout": 300,
        "clipboard_clear": True,
    },
    "generators": {
        "syllable": {
            "default_language": "english",
            "complexity": "mixed",
        },
        "passphrase": {
            "default_wordlist": "eff_large",
            "default_word_count": 4,
            "separator": "-",
            "capitalize": True,
        },
        "pattern": {
            "saved_templates": [],
        },
    },
    "compliance": {
        "enforce_nist": False,
        "enforce_owasp": False,
        "custom_policies": [],
    },
    "ui": {
        "tui": {
            "theme": "dark",
            "vim_mode": True,
            "show_help_bar": True,
        },
        "rich": {
            "color_scheme": "default",
        },
    },
}


class ConfigManager:
    """Manage Clinkey configuration.

    Loads configuration from file and provides access to settings with
    fallback to defaults. Supports nested key access via dot notation.

    Parameters
    ----------
    config_path : pathlib.Path | None
        Path to configuration file. If None, uses ~/.clinkey/config.toml.

    Attributes
    ----------
    config_path : pathlib.Path
        Path to configuration file.
    config : dict
        Loaded configuration merged with defaults.
    """

    def __init__(self, config_path: pathlib.Path | None = None):
        """Initialize configuration manager.

        Parameters
        ----------
        config_path : pathlib.Path | None, default None
            Path to config file. Defaults to ~/.clinkey/config.toml.
        """
        if config_path is None:
            config_path = pathlib.Path.home() / ".clinkey" / "config.toml"

        self.config_path = config_path
        self.config = self._load_config()

    def _load_config(self) -> dict:
        """Load configuration from file or use defaults.

        Returns
        -------
        dict
            Configuration dictionary.
        """
        # For Phase 1, just return defaults
        # Phase 2+ will implement TOML parsing
        return DEFAULT_CONFIG.copy()

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by dot-notation key.

        Parameters
        ----------
        key : str
            Configuration key in dot notation (e.g., "general.default_length").
        default : Any, default None
            Default value if key not found.

        Returns
        -------
        Any
            Configuration value or default.

        Examples
        --------
        >>> manager = ConfigManager()
        >>> manager.get("general.default_length")
        16
        >>> manager.get("nonexistent.key", default=42)
        42
        """
        parts = key.split(".")
        value = self.config

        for part in parts:
            if isinstance(value, dict) and part in value:
                value = value[part]
            else:
                return default

        return value

    def set(self, key: str, value: Any) -> None:
        """Set configuration value by dot-notation key.

        Parameters
        ----------
        key : str
            Configuration key in dot notation.
        value : Any
            Value to set.

        Examples
        --------
        >>> manager = ConfigManager()
        >>> manager.set("general.default_length", 20)
        >>> manager.get("general.default_length")
        20
        """
        parts = key.split(".")
        config = self.config

        # Navigate to parent
        for part in parts[:-1]:
            if part not in config:
                config[part] = {}
            config = config[part]

        # Set value
        config[parts[-1]] = value

    def save(self) -> None:
        """Save configuration to file.

        For Phase 1, this is a no-op. Phase 2+ will implement TOML writing.
        """
        # Phase 1: no-op
        # Phase 2+: write TOML file
        pass

    def reset(self) -> None:
        """Reset configuration to defaults."""
        self.config = DEFAULT_CONFIG.copy()
```

**Step 4: Run tests to verify they pass**

Run:
```bash
cd /Users/dim-gggl/~/Dev\ Tools/Clinkey
pytest tests/unit/config/test_manager.py -v
```

Expected: `PASS` (all tests green)

**Step 5: Commit**

```bash
cd /Users/dim-gggl/~/Dev\ Tools/Clinkey
git add clinkey_cli/config/ tests/unit/config/
git commit -m "feat: add configuration system foundation

- Implement ConfigManager with default config structure
- Support dot-notation key access (e.g., 'general.default_length')
- Add get() and set() methods for config access
- Prepare for TOML file support in Phase 2
- All tests passing

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com)"
```

---

## Task 5: Update Dependencies for Phase 1

**Files:**
- Modify: `pyproject.toml`

**Step 1: Write test for pytest-asyncio dependency**

Create `tests/unit/test_dependencies.py`:
```python
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
```

**Step 2: Run test to see current state**

Run:
```bash
cd /Users/dim-gggl/~/Dev\ Tools/Clinkey
pytest tests/unit/test_dependencies.py::test_pytest_asyncio_installed -v
```

Expected: `SKIP` (not yet installed)

**Step 3: Update pyproject.toml dependencies**

Modify `pyproject.toml`:
```toml
[build-system]
requires = ["setuptools>=66", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "clinkey-cli"
version = "2.0.0-alpha.1"
description = "A command-line tool for generating strong passwords and secret keys."
readme = "README.md"
requires-python = ">=3.10"
license = "MIT"
authors = [{name = "Dimitri Gaggioli"}]
keywords = ["password", "generator", "cli", "security"]

classifiers = [
    "Programming Language :: Python :: 3",
    "Operating System :: OS Independent",
    "Environment :: Console",
    "Topic :: Security",
    "Topic :: Utilities",
]
dependencies = [
    "click>=8.3.0",
    "rich>=14.1.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-cov>=4.1.0",
    "pytest-asyncio>=0.23.0",
    "pytest-mock>=3.12.0",
    "hypothesis>=6.92.0",
    "black>=24.0.0",
    "isort>=5.13.0",
    "flake8>=7.0.0",
    "mypy>=1.8.0",
    "pylint>=3.0.0",
    "bandit>=1.7.0",
    "pip-audit>=2.6.0",
]
build = [
    "build>=1.3.0",
]

[project.scripts]
clinkey = "clinkey_cli.cli:main"

[tool.setuptools.packages.find]
where = ["."]
include = ["clinkey_cli*"]

[tool.black]
line-length = 79
target-version = ['py310', 'py311', 'py312', 'py313', 'py314']
include = '\.pyi?$'
extend-exclude = '''
/(
  # directories
  \.eggs
  | \.git
  | \.hg
  | \.mypy_cache
  | \.tox
  | \.venv
  | build
  | dist
)/
'''

[tool.isort]
profile = "black"
line_length = 79
skip_gitignore = true
known_first_party = ["clinkey_cli"]

[tool.mypy]
python_version = "3.14"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = false
ignore_missing_imports = true
files = ["clinkey_cli"]

[tool.pylint.main]
max-line-length = 79
disable = [
    "C0114",  # missing-module-docstring
    "C0115",  # missing-class-docstring
    "C0116",  # missing-function-docstring
]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "-v",
    "--strict-markers",
    "--tb=short",
]

[tool.coverage.run]
source = ["clinkey_cli"]
omit = ["tests/*", "**/__pycache__/*"]

[tool.coverage.report]
precision = 2
show_missing = true
skip_covered = false
```

**Step 4: Install updated dev dependencies**

Run:
```bash
cd /Users/dim-gggl/~/Dev\ Tools/Clinkey
pip install -e ".[dev]"
```

Expected: Successfully installs pytest-asyncio

**Step 5: Run dependency test again**

Run:
```bash
cd /Users/dim-gggl/~/Dev\ Tools/Clinkey
pytest tests/unit/test_dependencies.py -v
```

Expected: `PASS` (all tests pass)

**Step 6: Commit**

```bash
cd /Users/dim-gggl/~/Dev\ Tools/Clinkey
git add pyproject.toml tests/unit/test_dependencies.py
git commit -m "build: update version to 2.0.0-alpha.1 and add dev dependencies

- Bump version to 2.0.0-alpha.1 for Phase 1
- Add pytest-asyncio to dev dependencies for future async tests
- Add dependency verification tests
- Prepare for Phase 2 async operations

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com)"
```

---

## Task 6: Run Full Test Suite and Verify Quality

**Files:**
- No new files

**Step 1: Run complete test suite**

Run:
```bash
cd /Users/dim-gggl/~/Dev\ Tools/Clinkey
pytest tests/ -v --cov=clinkey_cli --cov-report=term-missing
```

Expected: All tests pass with coverage report

**Step 2: Run code quality checks**

Run black formatter:
```bash
cd /Users/dim-gggl/~/Dev\ Tools/Clinkey
black clinkey_cli/ tests/
```

Run isort:
```bash
cd /Users/dim-gggl/~/Dev\ Tools/Clinkey
isort clinkey_cli/ tests/
```

Run flake8:
```bash
cd /Users/dim-gggl/~/Dev\ Tools/Clinkey
flake8 clinkey_cli/ tests/
```

Expected: No errors (or minimal fixable issues)

**Step 3: Run type checking**

Run mypy:
```bash
cd /Users/dim-gggl/~/Dev\ Tools/Clinkey
mypy clinkey_cli/
```

Expected: No critical type errors

**Step 4: Commit any formatting changes**

```bash
cd /Users/dim-gggl/~/Dev\ Tools/Clinkey
git add -A
git commit -m "style: apply black, isort formatting to Phase 1 code

- Format all Python code with black
- Sort imports with isort
- Fix any flake8 violations
- Ensure code quality standards met

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com)"
```

---

## Task 7: Create Phase 1 Summary Documentation

**Files:**
- Create: `docs/phase-1-complete.md`

**Step 1: Write Phase 1 completion summary**

Create `docs/phase-1-complete.md`:
```markdown
# Phase 1: Foundation - Completion Summary

**Status:** ✅ Complete
**Date:** 2025-01-26
**Duration:** Task 1-7

---

## Objectives Achieved

### 1. Module Structure Refactoring ✅

- Created `clinkey_cli/generators/` module
- Implemented `BaseGenerator` abstract class
- Established foundation for new generator types

### 2. Syllable Generator Extraction ✅

- Extracted syllable generation logic from `Clinkey` class
- Implemented `SyllableGenerator` with unified interface
- Maintained all existing generation methods

### 3. Backward Compatibility ✅

- Refactored `Clinkey` class to delegate to `SyllableGenerator`
- 100% API compatibility with Clinkey 1.x verified
- All existing tests pass without modification

### 4. Configuration System Foundation ✅

- Implemented `ConfigManager` with default configuration
- Supports dot-notation key access
- Prepared for TOML file support in Phase 2

### 5. Development Infrastructure ✅

- Updated to version 2.0.0-alpha.1
- Added pytest-asyncio for future async tests
- Organized test suite (unit/, integration/)

---

## Test Results

**Total Tests:** [Actual count from test run]
**Passed:** [Actual pass count]
**Coverage:** [Actual coverage %]

**Test Categories:**
- Unit tests: [count]
- Integration tests: [count]
- Backward compatibility tests: [count]

**All original Clinkey 1.x tests:** ✅ PASSING

---

## Code Quality Metrics

- **Black formatting:** ✅ Applied
- **isort imports:** ✅ Sorted
- **flake8 linting:** ✅ Clean
- **mypy type checking:** ✅ Passing
- **Test coverage:** ≥ 85% target

---

## Architecture Changes

### Before (1.x)
```
clinkey_cli/
├── main.py (Clinkey class with all logic)
├── cli.py
└── logos.py
```

### After (2.0 Phase 1)
```
clinkey_cli/
├── main.py (Clinkey adapter)
├── cli.py (unchanged)
├── logos.py (unchanged)
├── generators/
│   ├── base.py (BaseGenerator)
│   └── syllable.py (SyllableGenerator)
└── config/
    └── manager.py (ConfigManager)
```

---

## Breaking Changes

**None.** 100% backward compatible with Clinkey 1.x.

---

## Migration Notes

For users upgrading from 1.x to 2.0.0-alpha.1:

1. **No code changes required** - All 1.x code works identically
2. **Python API unchanged** - `from clinkey_cli.main import Clinkey` still works
3. **CLI unchanged** - All command-line flags work as before
4. **New internal structure** - Foundation for 2.0 features

---

## Ready for Phase 2

The following are now ready for implementation:

✅ Generator architecture supports new types (passphrase, pattern)
✅ Configuration system ready for expansion
✅ Test infrastructure supports unit and integration tests
✅ Code quality standards established

---

## Next Steps

**Phase 2: Security Analysis Engine**

1. Implement entropy calculator
2. Build pattern detector
3. Create dictionary analyzer
4. Implement breach checker
5. Add compliance validators
6. Integrate `clinkey analyze` command

**Estimated Duration:** 4 weeks
**Deliverable:** 2.0.0-alpha.2
```

**Step 2: Commit Phase 1 summary**

```bash
cd /Users/dim-gggl/~/Dev\ Tools/Clinkey
git add docs/phase-1-complete.md
git commit -m "docs: add Phase 1 completion summary

- Document all objectives achieved
- Report test results and coverage
- Show architecture transformation
- Confirm zero breaking changes
- Phase 1 foundation complete, ready for Phase 2

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com)"
```

---

## Task 8: Tag Phase 1 Release

**Files:**
- No new files

**Step 1: Create git tag for alpha.1**

Run:
```bash
cd /Users/dim-gggl/~/Dev\ Tools/Clinkey
git tag -a v2.0.0-alpha.1 -m "Release Clinkey 2.0.0-alpha.1: Phase 1 Foundation

Phase 1 (Foundation) complete:
- Refactored architecture with generators/ module
- BaseGenerator abstract class
- SyllableGenerator extracted from Clinkey
- 100% backward compatibility maintained
- ConfigManager foundation
- All tests passing

Ready for Phase 2: Security Analysis Engine"
```

**Step 2: Verify tag created**

Run:
```bash
cd /Users/dim-gggl/~/Dev\ Tools/Clinkey
git tag -l "v2.0.0*"
```

Expected: Shows `v2.0.0-alpha.1`

**Step 3: Push tags to remote**

Run:
```bash
cd /Users/dim-gggl/~/Dev\ Tools/Clinkey
git push origin v2.0.0-alpha.1
```

Expected: Tag pushed successfully

**Step 4: Push all Phase 1 commits**

Run:
```bash
cd /Users/dim-gggl/~/Dev\ Tools/Clinkey
git push origin main
```

Expected: All commits pushed

---

## Phase 1 Complete! 🎉

**Summary:**
- ✅ All 8 tasks completed
- ✅ New modular architecture in place
- ✅ 100% backward compatibility verified
- ✅ All tests passing
- ✅ Code quality standards met
- ✅ Version 2.0.0-alpha.1 tagged and released

**Foundation established for:**
- Security Analysis Engine (Phase 2)
- Enhanced Generators (Phase 3)
- Password Vault (Phase 4)
- TUI Layer (Phase 5)

---

## Verification Checklist

Before proceeding to Phase 2, verify:

- [ ] All original tests from 1.x still pass
- [ ] New unit tests all pass
- [ ] Integration tests verify backward compatibility
- [ ] Code formatted with black and isort
- [ ] Type hints pass mypy checks
- [ ] Test coverage ≥ 85%
- [ ] Git tag v2.0.0-alpha.1 created and pushed
- [ ] Documentation updated (phase-1-complete.md)

---

**Next:** Begin Phase 2 implementation plan or create new worktree for Phase 2 development.
