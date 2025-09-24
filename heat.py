import random
import string
import argparse
import click
from rich.console import Console

from clinkey_view import ClinkeyView


console = Console()
view = ClinkeyView()

ALPHABET = [char for char in string.ascii_letters.upper()]
VOWELS = ['A', 'E', 'I', 'O', 'U', 'Y']
CONSONANTS = [char for char in ALPHABET if char not in VOWELS]
FIGURES = [char for char in string.digits]
SPECIALS = [char for char in string.punctuation if char not in ['-', '_', '$', '#', '|', '<', '>', '(', ')', '[', ']', '{', '}', '\'', '\"', '`', '@', ' ']]

SYLLABES = []
for c in CONSONANTS:
    for v in VOWELS:
        SYLLABES.append(c + v)
        
SYLLABES_COMPLEXES = ['TRE', 'TRI', 'TRO', 'TRA', 'TRE', 'TRI', 'TRO', 'TRA', 'DRE', 'DRI', 'DRO', 'DRA',
                    'BRE', 'BRI', 'BRO', 'BRA', 'CRE', 'CRI', 'CRO', 'CRA', 'FRE', 'FRI', 'FRO', 'FRA',
                    'GRE', 'GRI', 'GRO', 'GRA', 'PRE', 'PRI', 'PRO', 'PRA', 'SRE', 'SRI', 'SRO', 'SRA',
                    'VRE', 'VRI', 'VRO', 'VRA', 'ZRE', 'ZRI', 'ZRO', 'ZRA', 'LON', 'LEN', 'LIN', 'LAN',
                    'MON', 'MEN', 'MIN', 'MAN', 'NON', 'NEN', 'NIN', 'NAN', 'PON', 'PEN', 'PIN', 'PAN',
                    'RON', 'REN', 'RIN', 'RAN', 'SON', 'SEN', 'SIN', 'SAN', 'TON', 'TEN', 'TIN', 'TAN',
                    'VON', 'VEN', 'VIN', 'VAN', 'ZON', 'ZEN', 'ZIN', 'ZAN']

class Clinkey(ClinkeyView):
    """
    Generate pronounceable passwords based on French syllables.
    """
    
    def __init__(self) -> None:
        """
        Initialize the generator with the French syllables.
        """
        # Common French syllables
        self._consonnes = CONSONANTS
        self._voyelles = VOWELS
        self._syllabes_simples = SYLLABES
        
        # More complex syllables
        self._syllabes_complexes = SYLLABES_COMPLEXES
        
        # Special characters for super_strong
        self._caracteres_speciaux = SPECIALS
        
        # Numbers
        self._chiffres = FIGURES
    
    def _generate_simple_syllable(self) -> str:
        """
        Generate a simple syllable of 2 letters (consonant + vowel).
        """
        return random.choice(self._syllabes_simples)
    
    def _generate_complex_syllable(self) -> str:
        """
        Generate a complex syllable of 3 letters.
        """
        return random.choice(self._syllabes_complexes)
    
    def _generate_pronounceable_word(self, min_length: int = 4, max_length: int = 8) -> str:
        """
        Generate a pronounceable word of variable length.
        """
        mot = ""
        longueur = random.randint(min_length, max_length)
        
        # Start with a simple syllable
        mot += self._generate_simple_syllable()
        
        # Add additional syllables
        while len(mot) < longueur:
            if random.choice([True, False]):
                mot += self._generate_simple_syllable()
            else:
                mot += self._generate_complex_syllable()
        
        # Truncate if necessary
        return mot[:longueur]
    
    def _generate_number_block(self, longueur: int = 3) -> str:
        """
        Generate a block of numbers.
        """
        return ''.join(random.choices(self._chiffres, k=longueur))
    
    def _generate_special_characters_block(self, longueur: int = 3) -> str:
        """
        Generate a block of special characters.
        """
        return ''.join(random.choices(self._caracteres_speciaux, k=longueur))
    
    def _generate_separator(self) -> str:
        """
        Generate a separator between blocks.
        """
        return random.choice(['-', '_'])
    
    def super_strong(self) -> str:
        """
        Generate a super strong password with letters, numbers and special characters.
        Pattern: MOT-CARACTERES-CHIFFRES-MOT-CARACTERES-CHIFFRES-MOT
        """
        words = []
        rint = random.randint
        for _ in range(3):
            words.append(self._generate_pronounceable_word(rint(4, 6), rint(8, 12)))

        figures = []
        for _ in range(3):
            figures.append(self._generate_number_block(rint(3, 6)))

        specials = []
        for _ in range(2):  # Retour à 2 car on n'a besoin que de 2 blocs de caractères spéciaux
            specials.append(self._generate_special_characters_block(rint(3, 6)))
        
        seps = []
        for _ in range(6):
            seps.append(self._generate_separator())

        result = ""
        # Première itération : MOT-CARACTERES-CHIFFRES
        result += words.pop() + seps.pop() + specials.pop() + seps.pop() + figures.pop() + seps.pop()
        # Deuxième itération : MOT-CARACTERES-CHIFFRES  
        result += words.pop() + seps.pop() + specials.pop() + seps.pop() + figures.pop() + seps.pop()
        # Troisième itération : MOT (le dernier mot)
        result += words.pop()
        
        return result.strip()
    
    def strong(self) -> str:
        """
        Generate a strong password with letters and numbers.
        Pattern: MOT-CHIFFRES-MOT-CHIFFRES-MOT-CHIFFRES
        """
        words = []
        rint = random.randint
        for _ in range(3):
            words.append(self._generate_pronounceable_word(rint(4, 6), rint(8, 12)))

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
        Pattern: MOT-SEPARATEUR-MOT-SEPARATEUR-MOT-SEPARATEUR-MOT
        """
        words = []
        rint = random.randint
        for _ in range(3):
            words.append(self._generate_pronounceable_word(rint(4, 6), rint(8, 12)))

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
            type : str = "normal", 
            number: int = 1, 
            no_separator : bool = False, 
            lower : bool = False, 
            output: str = None):
    clinkey = Clinkey()
    action = {
        "super_strong": clinkey.super_strong,
        "strong": clinkey.strong,
        "normal": clinkey.normal
    }
    passwords = []
    for _ in range(number):
        passwords.append(clinkey.generate_password(action[type], length))
    if lower:
        passwords = [password.lower() for password in passwords]
    if no_separator:
        passwords = [password.replace("-", "").replace("_", "") for password in passwords]
    if output:
        with open(output, "w") as file:
            for password in passwords:
                file.write(password.rstrip("_").rstrip("-").lstrip("_").lstrip("-") + "\n")
    return passwords

@click.group()
def heat():
    """Heat - Collection d'outils de sécurité et génération"""
    pass

@heat.command()
@click.option("-l", '--length', default=None, type=int, help='Longueur du mot de passe')
@click.option("-t", '--type', default=None, help='Type: normal, strong, super_strong')
@click.option("-n", '--number', default=None, type=int, help='Nombre de mots de passe à générer')
@click.option("-ns", "--no-sep", is_flag=True, help="Supprimer les séparateurs")
@click.option("-low", "--lower", is_flag=True, help="Convertir en minuscules")
@click.option("-o", "--output", help="Fichier de sortie")
def clinkey(length: int | None = None,
          type: str | None = None,
          number: int | None = None,
          no_sep: bool = False,
          lower: bool = False,
          output: str = None) -> list[str]:
    """Générateur de mots de passe prononçables basé sur les syllabes françaises"""

    # Mode interactif si pas d'arguments
    interactive_mode = length is None and type is None and number is None

    if interactive_mode:
        view.display_logo()

    if length is None:
        if interactive_mode:
            length = view.ask_for("length")
        if not length:
            length = 16

    if type is None:
        if interactive_mode:
            type = view.ask_for("type")
        if not type:
            type = "normal"

    if number is None:
        if interactive_mode:
            number = view.ask_for("number")
        if not number:
            number = 1

    passwords = generate(
        length=length,
        type=type,
        number=number,
        no_separator=no_sep,
        lower=lower,
        output=output
    )

    if interactive_mode:
        view.display_passwords(passwords)
    else:
        # Mode ligne de commande - affichage simple
        for password in passwords:
            console.print(password, style="bright_green")

    return passwords

if __name__ == "__main__":
    heat()