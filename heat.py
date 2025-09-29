import random
import string
import argparse
import click
from rich.console import Console

from clinkey_view import ClinkeyView


console = Console()
view = ClinkeyView()

ALPHABET = [char for char in string.ascii_letters.upper()]
VOWELS = ["A", "E", "I", "O", "U", "Y"]
CONSONANTS = [char for char in ALPHABET if char not in VOWELS]
FIGURES = [char for char in string.digits]
SPECIALS = [char for char in string.punctuation if char not in [
	"ç", "ù", "£", "€", "Ù", "≠", "é", "§", "à", "∂", "Ò", "‡", "æ", "ê", "∂", "Ò"
	]
]

SYLLABLES = []
for c in CONSONANTS:
	for v in VOWELS:
		SYLLABLES.append(c + v)

COMPLEX_SYLLABLES = ["TRE", "TRI", "TRO", "TRA", "TRE", "TRI", "TRO", "TRA", "DRE", "DRI", "DRO", "DRA",
					"BRE", "BRI", "BRO", "BRA", "CRE", "CRI", "CRO", "CRA", "FRE", "FRI", "FRO", "FRA",
					"GRE", "GRI", "GRO", "GRA", "PRE", "PRI", "PRO", "PRA", "SRE", "SRI", "SRO", "SRA",
					"VRE", "VRI", "VRO", "VRA", "ZRE", "ZRI", "ZRO", "ZRA", "LON", "LEN", "LIN", "LAN",
					"MON", "MEN", "MIN", "MAN", "NON", "NEN", "NIN", "NAN", "PON", "PEN", "PIN", "PAN",
					"RON", "REN", "RIN", "RAN", "SON", "SEN", "SIN", "SAN", "TON", "TEN", "TIN", "TAN",
					"VON", "VEN", "VIN", "VAN", "ZON", "ZEN", "ZIN", "ZAN"]

class Clinkey:
	"""
	Generate pronounceable passwords based on Human-friendly syllables.
	"""

	def __init__(self, new_seperator: str = None) -> None:
		# Commonn syllables
		self._consonnants = CONSONANTS
		self._vowels = VOWELS
		self._simple_syllables = SYLLABLES
		self._complex_syllables = COMPLEX_SYLLABLES

		# Special characters for super_strong passwords
		self._special_characters = SPECIALS

		# Numbers
		self._DIGITS = FIGURES

		self._new_seperator = new_seperator

	def _generate_simple_syllable(self) -> str:
		"""Generate a 2 chars syllable."""
		return random.choice(self._simple_syllables)

	def _generate_complex_syllable(self) -> str:
		"""Generate a 3 letters syllable"""
		return random.choice(self._complex_syllables)

	def _generate_pronounceable_word(
		self, min_length: int = 4, max_length: int = 8) -> str:
		"""
		Concatenates randomly picked syllables 
		"""
		WORD = ""
		length = random.randint(min_length, max_length)

		# Start with a simple syllable
		WORD += self._generate_simple_syllable()

		# Add additional syllables
		while len(WORD) < length:
			if random.choice([True, False]):
				WORD += self._generate_simple_syllable()
			else:
				WORD += self._generate_complex_syllable()

		# Truncate if necessary
		return WORD[:length]

	def _generate_number_block(self, length: int = 3) -> str:
		"""Generate a block of digits"""
		return "".join(random.choices(self._DIGITS, k=length))

	def _generate_special_characters_block(self, length: int = 3) -> str:
		"""Generate a block of special characters"""
		return "".join(random.choices(self._special_characters, k=length))

	def _generate_separator(self) -> str:
		"""Pick an hyphen to separate the blocks"""
		sep = self._new_seperator
		if not sep:
			return random.choice(["-", "_"])
		return sep    

	def super_strong(self) -> str:
		"""
		Generate a super strong password with letters, numbers and special characters.
		Pattern: WORD-characters-DIGITS-WORD-characters-DIGITS-WORD
		"""
		words = []
		rint = random.randint
		
		for _ in range(3):
			words.append(self._generate_pronounceable_word(rint(4, 6), rint(8, 12)))

		figures = []
		for _ in range(3):
			figures.append(self._generate_number_block(rint(3, 6)))

		specials = []
		for _ in range(2):
			specials.append(self._generate_special_characters_block(rint(3, 6)))

		seps = []
		for _ in range(6):
			seps.append(self._generate_separator())

		result = ""
		# First iteration : WORD-characters-DIGITS
		result += words.pop() + seps.pop() + specials.pop() + seps.pop() + figures.pop() + seps.pop()
		# Second iteration : WORD-characters-DIGITS
		result += words.pop() + seps.pop() + specials.pop() + seps.pop() + figures.pop() + seps.pop()
		# Third iteration : WORD (the last WORD)
		result += words.pop()

		return result.strip()

	def strong(self) -> str:
		"""
		Generate a strong password with letters and numbers.
		Pattern: WORD-DIGITS-WORD-DIGITS-WORD-DIGITS
		"""
		words = []
		rint = random.randint
		for _ in range(3):
			words.append(
				self._generate_pronounceable_word(rint(4, 6), rint(8, 12))
			)

		figures = []
		for _ in range(3):
			figures.append(self._generate_number_block(rint(3, 6)))

		seps = []
		for _ in range(6):
			seps.append(self._generate_separator())

		result = ""
		for _ in range(3):
			result += words.pop(0) + seps.pop(0) + figures.pop(0) + seps.pop(0)

		return result.strip()

	def normal(self) -> str:
		"""
		Generate a normal password with only letters.
		Pattern: WORD-SEPARATOR-WORD-SEPARATOR-WORD-SEPARATOR-WORD
		"""
		words = []
		rint = random.randint
		for _ in range(3):
			words.append(
				self._generate_pronounceable_word(rint(4, 6), rint(8, 12))
			)

		seps = []
		for _ in range(6):
			seps.append(self._generate_separator())

		result = ""
		for _ in range(3):
			result += words.pop(0) + seps.pop(0)

		return result.strip()

	def generate_password(self, method, target_length: int = 16):
		result = ""
		while len(result) < target_length:
			part = method()
			if len(result + part) <= target_length:
				result += part
			else:
				# Add partial word to reach exact length
				remaining = target_length - len(result)
				result += part[:remaining]
				break
			
		return result

def generate(length: int = 16,
			type_ : str = "normal",
			number: int = 1,
			no_separator : bool = False,
			lower : bool = False,
			new_seperator: str = None,
			output: str = None):
	clinkey = Clinkey()
	action = {
		"super_strong": clinkey.super_strong,
		"strong": clinkey.strong,
		"normal": clinkey.normal
	}
	passwords = []
	for _ in range(number):
		passwords.append(
			clinkey.generate_password(action[type_], length)
	)
	if lower:
		passwords = [
			password.lower() for password in passwords
		]	
	if no_separator:
		passwords = [
			password.replace("-", "").replace("_", "") for password in passwords
		]
	if output:
		with open(output, "w") as file:
			for password in passwords:
				file.write(
					password.rstrip("_"
					).rstrip("-"
					).lstrip("_"
					).lstrip("-"
					) + "\n"
				)
	return passwords

@click.group()
def heat():
	"""Heat - Collection d"outils de sécurité et génération"""
	pass

@heat.command()
@click.option(
	"-l", "--length", default=None, type=int, help="password length")
@click.option("-t", 
"--type", "type_", default=None, help="normal, strong or super_strong")
@click.option(
	"-n", "--number", default=None, 
	type=int, help="The number of passwords to generate")
@click.option("-ns", "--no-sep", is_flag=True, help="With no hyphens")
@click.option("-low", "--lower", is_flag=True, help="Lowercased")
@click.option("-nes", "--new-sep", "new_seperator", is_flag=True, help="New seperator")
@click.option("-o", "--output", help="Output file path")
def clinkey(length: int | None = None, 
		  type_: str | None = None,
		  number: int | None = None,
		  no_sep: bool = False,
		  lower: bool = False,
		  new_seperator: str = None,
		  output: str = None) -> list[str]:
	"""
	Human-friendly pronounceable password generator.
	If not customized, clinkey passwords are made of blocks of uppercased
	chars separated by hyphens.

	- Args:
		- length: default on 16 characters. Can be customized to any integer.
		- type_ : accepted values are "normal", "strong" or "super_strong". 
	Define the content and complexity of the resulted password. 
			- normal password only contains alphabetical chars.
			- strong mix it with digits.
			- super_strong adds special chars.
		- number : Defines the number of passwords that should be generated.
		- no_sep : Default on False. If set to True, generates passwords with
	no hyphens separating the pronounceable parts and the digits and 
	special blocks.
		- lower : Default on False. If set to True, convert the generated 
	results to lowercased strings.
		- output : if a file path is provided, the results are only to be 
	extracted to the file and not printed or displayed as they are 
	by default.
	"""

	# If no values in args, interactive mode
	interactive_mode = not length and not type_ and not number

	if interactive_mode:
		view.display_logo()
		length = view.ask_for("length")
		if not length:
			length = 16
		type_ = view.ask_for("type_")
		if not type_:
			type_ = "normal"
		number = view.ask_for("number")
		if not number:
			number = 5
		options = parse_options()
		if "lower" in options:
			lower = True
		if "no_sep" in options:
			no_sep = True
		if "new_seperator" in options:
			new_seperator = True
			

	passwords = generate(
		length=length,
		type_=type_,
		number=number,
		no_separator=no_sep,
		lower=lower,
		new_seperator=new_seperator,
		output=output
	)

	if output:
		with open(output, "w") as file:
			for password in passwords:
				file.write(password + "\n")
	else:
		view.display_passwords(passwords)
	return passwords


def parse_options():
	options = {
		"lower": ["lower", "low", "-l", "--lower"],
		"no_sep": ["no_sep", "ns", "-ns", "--no-sep", "no-sep", "ns"]
	}
	result = []
	user_choices = view.get_options().strip()
	if user_choices:
		choices = user_choices.split(" ")
		for choice in choices:
			for option, versions in options.items():
				if choice.strip().lower() in versions:
					result.append(option)
	return result	


if __name__ == "__main__":
	heat()