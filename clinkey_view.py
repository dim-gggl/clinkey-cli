"""
This module contains the ClinkeyView class.
"""

from typing import Any, Callable
from rich.console import Console
from rich.align import Align
from rich.text import Text
from rich.panel import Panel
from rich.box import ROUNDED


console = Console(style="on grey3")
console.clear()

class ClinkeyView:
    """
    This class is used to display the messages to the user.
    """
    messages = {
        "greeting": "Welcome to Clinkey",
        "yes_no_input": "Yes/No ? (y/n) : ",
        "password_type": (
            "Which type of password do you want to generate ?"
        ),
        "password_type_choice": {
            "1": "Simple (Only letters)",
            "2": "Medium (Letters and numbers)",
            "3": "Strong (Letters, numbers and symbols)"
        },
        "password_length": (
            "How long do you want your password to be ?"
        ),
        "error": "Error : ",
        "success": "Success : ",
        "info": "Info : "
    }

    def display_greeting(self) -> None:
        """
        Display the greeting message.
        """
        print("\n" * 20)
        print(f"{'Welcome to Clinkey':^90}")
        print("\n" * 5)
        input(f"{'Press Enter to continue...':^90}\n{f'':<45}")

    def header(self) -> None:
        """
        Display the header of the program.
        """
        print("\n" * 20)
        print(f"{'======[ \033[5m Clinkey \033[0m ]======':^90}")
        print("\n" * 5)

    def headed(self, func: Callable) -> Callable:
        """
        Decorator to display the header of the program.
        """
        def wrapper(*args, **kwargs) -> Any:
            """
            Wrapper function to display the header of the program.
            """
            self.header()
            return func(*args, **kwargs)
        return wrapper

    def _get_user_yes_no_input(self, message: str) -> str:
        """
        Get the user's yes/no input.
        """
        self.header()
        print(f"{message:^90}")
        return input(f"{'Yes/No ? (y/n) : ':^90}\n{f'':<45}")

    def _get_user_123_choice(self, message: str, choice: list[str]) -> str:
        """
        Get the user's 1/2/3 choice.
        """
        self.header()
        print(f"{message:^90}")
        print(f"{f'1 - {choice[0]}':^90}")
        print(f"{f'2 - {choice[1]}':^90}")
        print(f"{f'3 - {choice[2]}':^90}")
        return input(f"{'1/2/3 ? : ':^90}\n{f'':<45}")

    def _get_user_input(self, message: str) -> str:
        """
        Get the user's input.
        """
        self.header()
        print(f"{message:^90}")
        return input(f"{'Your choice : ':^90}\n{f'':<45}")

    def get_user_password_type(self) -> str:
        """
        Get the user's password type.
        """
        return self._get_user_123_choice(
            self.messages["password_type"],
            self.messages["password_type_choice"]
        )

    def get_user_password_length(self) -> str:
        """
        Get the user's password length.
        """
        return self._get_user_input(
            self.messages["password_length"]
        )

    def display_password(self, password: str) -> None:
        """
        Display the password.
        """
        self.header()
        print(f"\n\033[92m{password}\033[0m")
        print("\n" * 5)

    def display_error(self, message: str) -> None:
        """
        Display the error message.
        """
        self.header()
        print(f"\n\033[91m{message}\033[0m")
        print("\n" * 5)

    def display_success(self, message: str) -> None:
        """
        Display the success message.
        """
        self.header()
        print(f"\n\033[92m{message}\033[0m")
        print("\n" * 5)

    def display_info(self, message: str) -> None:
        """
        Display the info message.
        """
        self.header()
        print(f"\n\033[94m{message}\033[0m")
        print("\n" * 5)

    def ask_for(self, param: str):
        """
        Ask user for different parameters based on input.
        """
        if param == "type":
            console.clear()
            self._display_logo_rich()

            type_text = Text("\nHow twisted do you want it ?", style="bright_white")
            console.print(Align.center(type_text))

            choices = Text.from_markup("\n1 - [bold plum1]Vanilla[/] (Regular alphabet letters)\n2 - [bold plum1]Spicy[/] (Alphabet + a pinch of digits)\n3 - [bold plum1]So NAAASTY[/] (All including the special ones)", style="grey70")
            console.print(Align.center(choices))

            prompt = Text("\nWhat's your tribe (1/2/3): ", style="plum1")
            console.print(Align.center(prompt), end="")

            choice = input()
            type_map = {"1": "normal", "2": "strong", "3": "super_strong"}
            return type_map.get(choice, "normal")

        elif param == "length":
            console.clear()
            self._display_logo_rich()

            length_text = Text("\nHow long do you like it ?", style="bright_white")
            console.print(Align.center(length_text))

            prompt = Text("\nAbout the size (default: 16): ", style="plum1")
            console.print(Align.center(prompt), end="")

            try:
                length = int(input())
                return length if length > 0 else 16
            except ValueError:
                return 16

        elif param == "number":
            console.clear()
            self._display_logo_rich()

            number_text = Text("\nHow many you fancy at once ?", style="bright_white")
            console.print(Align.center(number_text))

            prompt = Text("\nYour number (default: 1): ", style="plum1")
            console.print(Align.center(prompt), end="")

            try:
                number = int(input())
                return number if number > 0 else 1
            except ValueError:
                return 1

        return None

    def _display_logo_rich(self):
        """
        Display the Clinkey logo with rich formatting and colors.
        """
        logo = Text("""
╔═╝  ║    ╝  ╔═   ║ ║  ╔═╝  ║ ║
║    ║    ║  ║ ║  ╔╝   ╔═╝  ═╔╝
══╝  ══╝  ╝  ╝ ╝  ╝ ╝  ══╝   ╝ 
        """, style="#5fff87")  # Vert néon menthe glaciale

        console.print("\n\n", Panel.fit((logo), padding=(1, 7), box=ROUNDED, border_style="plum1"), justify="center")

        subtitle = Text.from_markup("Your own [bold #5fff87]secret buddy[/]...", style="grey70 italic")
        console.print(Align.center(subtitle))

    def display_logo(self):
        """
        Display the logo at startup.
        """
        console.clear()
        self._display_logo_rich()

        welcome_text = Text("\n\nPress ENTER to continue...\n\n", style="plum1")
        console.print(Align.center(welcome_text))
        input()

    def display_passwords(self, passwords: list[str]):
        """
        Display generated passwords with rich formatting.
        """
        console.clear()
        self._display_logo_rich()

        passwords_text = Text("\nYour passwords are ready :\n", style="rgb(64,224,208) bold")
        console.print(Align.center(passwords_text))

        for i, password in enumerate(passwords, 1):
            password_line = Text(f"{i:2d}. {password}", style="bright_white on grey23")
            console.print(Align.center(password_line))

        console.print()
        copy_hint = Text("Tips: Choose one to copy", style="grey70 italic")
        console.print(Align.center(copy_hint))