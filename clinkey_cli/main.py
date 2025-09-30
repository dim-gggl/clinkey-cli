"""Core password generation logic for the Clinkey CLI package."""

from __future__ import annotations

import random
import string
from typing import Callable, Dict


class Clinkey:
    """Generate pronounceable passwords with different complexity presets."""

    def __init__(self) -> None:
        alphabet = string.ascii_uppercase
        vowels = "AEIOUY"
        self._consonants = [char for char in alphabet if char not in vowels]
        self._vowels = list(vowels)
        self._digits = list(string.digits)
        self._specials = [
            char
            for char in string.punctuation
            if char not in {"-", "_", "$", "#", "|", "<", ">", "(", ")", "[", "]", "{", "}", '"', "'", "`", "@", " "}
        ]

        self._simple_syllables = [consonant + vowel for consonant in self._consonants for vowel in self._vowels]
        self._complex_syllables = [
            "TRE",
            "TRI",
            "TRO",
            "TRA",
            "TRU",
            "TSA",
            "TSE",
            "TSI",
            "TSO",
            "TSU",
            "DRE",
            "DRI",
            "DRO",
            "DRA",
            "DRU",
            "BRE",
            "BRI",
            "BRO",
            "BRA",
            "BRU",
            "BLA",
            "BLE",
            "BLI",
            "BLO",
            "BLU",
            "CRE",
            "CRI",
            "CRO",
            "CRA",
            "CRU",
            "CHA",
            "CHE",
            "CHI",
            "CHO",
            "CHU",
            "FRE",
            "FRI",
            "FRO",
            "FRA",
            "FRU",
            "GRE",
            "GRI",
            "GRO",
            "GRA",
            "GRU",
            "GLA",
            "GLE",
            "GLI",
            "GLO",
            "GLU",
            "GNA",
            "GNE",
            "GNI",
            "GNO",
            "GNU",
            "PRE",
            "PRI",
            "PRO",
            "PRA",
            "PRU",
            "PLA",
            "PLE",
            "PLI",
            "PLO",
            "PLU",
            "QUA",
            "QUE",
            "QUI",
            "QUO",
            "SRE",
            "SRI",
            "SRO",
            "SRA",
            "SRU",
            "SLA",
            "SLE",
            "SLI",
            "SLO",
            "SLU",
            "STA",
            "STE",
            "STI",
            "STO",
            "STU",
            "SNA",
            "SNE",
            "SNI",
            "SNO",
            "SNU",
            "SMA",
            "SME",
            "SMI",
            "SMO",
            "SMU",
            "SHA",
            "SHE",
            "SHI",
            "SHO",
            "SHU",
            "VRE",
            "VRI",
            "VRO",
            "VRA",
            "VRU",
            "ZRE",
            "ZRU",
            "ZRI",
            "ZRO",
            "ZRA"
        ]

        self._separators = ["-", "_"]
        self._generators: Dict[str, Callable[[], str]] = {
            "normal": self.normal,
            "strong": self.strong,
            "super_strong": self.super_strong,
        }
        # Custom separator to override the default ones ('-' and '_') when set
        self.new_separator = None

    def _generate_simple_syllable(self) -> str:
        return random.choice(self._simple_syllables)

    def _generate_complex_syllable(self) -> str:
        return random.choice(self._complex_syllables)

    def _generate_pronounceable_word(self, min_length: int = 4, max_length: int = 8) -> str:
        word = self._generate_simple_syllable()
        target = random.randint(min_length, max_length)

        while len(word) < target:
            generator = random.choice([self._generate_simple_syllable, self._generate_complex_syllable])
            word += generator()

        return word[:target]

    def _generate_number_block(self, length: int = 3) -> str:
        return "".join(random.choices(self._digits, k=length))

    def _generate_special_characters_block(self, length: int = 3) -> str:
        return "".join(random.choices(self._specials, k=length))

    def _generate_separator(self) -> str:
        if self.new_separator:
            return self.new_separator
        return random.choice(self._separators)

    def super_strong(self) -> str:
        words = [self._generate_pronounceable_word(random.randint(4, 6), random.randint(8, 12)) for _ in range(3)]
        numbers = [self._generate_number_block(random.randint(3, 6)) for _ in range(3)]
        specials = [self._generate_special_characters_block(random.randint(3, 6)) for _ in range(2)]
        separators = [self._generate_separator() for _ in range(6)]

        result = []
        result.append(words.pop() + separators.pop() + specials.pop() + separators.pop() + numbers.pop() + separators.pop())
        result.append(words.pop() + separators.pop() + specials.pop() + separators.pop() + numbers.pop() + separators.pop())
        result.append(words.pop())
        return "".join(result)

    def strong(self) -> str:
        words = [self._generate_pronounceable_word(random.randint(4, 6), random.randint(8, 12)) for _ in range(3)]
        numbers = [self._generate_number_block(random.randint(3, 6)) for _ in range(3)]
        separators = [self._generate_separator() for _ in range(6)]

        result = []
        for _ in range(3):
            result.append(words.pop(0) + separators.pop(0) + numbers.pop(0) + separators.pop(0))
        return "".join(result)

    def normal(self) -> str:
        words = [self._generate_pronounceable_word(random.randint(4, 6), random.randint(8, 12)) for _ in range(3)]
        separators = [self._generate_separator() for _ in range(6)]

        result = []
        for _ in range(3):
            result.append(words.pop(0) + separators.pop(0))
        return "".join(result)

    def _fit_to_length(self, generator: Callable[[], str], target_length: int) -> str:
        password = ""
        while len(password) < target_length:
            chunk = generator()
            if len(password) + len(chunk) <= target_length:
                password += chunk
            else:
                remaining = target_length - len(password)
                password += chunk[:remaining]
                break
        return password

    def generate_password(
        self,
        length: int = 16,
        type: str = "normal",
        lower: bool = False,
        no_separator: bool = False,
		new_separator: str = None,
		output: str = None
    ) -> str:
        if length <= 0:
            raise ValueError("length must be a positive integer")

        key = type.strip().lower()
        if key not in self._generators:
            valid = ", ".join(sorted(self._generators.keys()))
            raise ValueError(f"Unsupported type '{type}'. Choose among: {valid}.")

        # Temporarily override separator for this generation if provided
        previous_separator = self.new_separator
        if new_separator is not None:
            self.new_separator = new_separator

        try:
            raw_password = self._fit_to_length(self._generators[key], length)
        finally:
            # Restore previous separator to avoid leaking state between calls
            self.new_separator = previous_separator

        separators_to_strip = "-_"
        effective_separator = new_separator if new_separator is not None else previous_separator
        if effective_separator and effective_separator not in "-_":
            separators_to_strip += effective_separator

        cleaned = raw_password.strip(separators_to_strip)

        if no_separator:
            cleaned = cleaned.replace("-", "").replace("_", "")
            if effective_separator and effective_separator not in "-_":
                cleaned = cleaned.replace(effective_separator, "")

        if lower:
            cleaned = cleaned.lower()

        return cleaned

    def generate_batch(
        self,
        length: int = 16,
        type: str = "normal",
        count: int = 1,
        lower: bool = False,
        no_separator: bool = False,
		new_separator: str = None,
		output: str = None
    ) -> list[str]:
        if count <= 0:
            raise ValueError("count must be a positive integer")

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


clinkey = Clinkey()

__all__ = ["Clinkey", "clinkey"]
