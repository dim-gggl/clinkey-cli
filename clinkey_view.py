"""
This module contains the ClinkeyView class.
"""

from typing import Any, Callable
from rich.console import Console
from rich.style import Style
from rich.align import Align
from rich.text import Text
from rich.panel import Panel
from rich.box import ROUNDED


console = Console(style="on grey11")
console.clear()

clinkey_green_style = Style(color="light_green", bold=True)
clinkey_pink_style = Style(color="orchid1", bold=True)
clinkey_white_style = Style(color="grey100", bold=True)
reg_style = Style(color="white")

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
        if param == "type_":
            console.clear()
            self._display_logo_rich()

            type_text = Text.from_markup(
				"\nHow [bold light_green]TWISTED[/] do you want it ?\n\n", 
				style=reg_style
			)
            console.print(Align.center(type_text))

            choices = Text.from_markup(
				"\n1 - [bold orchid1]Vanilla[/] (regular alphabet letters)\n"
				"2 - [bold orchid1]Spicy[/] (alphabet + a pinch of digits)\n"
				"3 - [bold orchid1]So NAAASTY[/] (all including the special ones)", 
				style=reg_style
			)
            console.print(Align.center(choices))

            prompt = Text.from_markup(
				"\nWhat's your [bold light_green]TRIBE[/] (1 / 2 / 3): \n\n", 
				style="dim white"
			)
            console.print(Align.center(prompt), end="")

            choice = input()
            type_map = {"1": "normal", "2": "strong", "3": "super_strong"}
            return type_map.get(choice, "normal")

        elif param == "length":
            console.clear()
            self._display_logo_rich()

            length_text = Text.from_markup(
				"\nHow [bold light_green]LONG[/] do you like it ?\n\n", 
				style=reg_style
			)
            console.print(Align.center(length_text))

            prompt = Text.from_markup("\n(default: 16): \n\n", style="dim white")
            console.print(Align.center(prompt), end="")

            try:
                length = int(input())
                return length if length > 0 else 16
            except ValueError:
                return 16

        elif param == "number":
            console.clear()
            self._display_logo_rich()

            number_text = Text.from_markup(
				"\nHow [bold light_green]MANY[/] you fancy at once ?\n\n", 
				style=reg_style
			)
            console.print(Align.center(number_text))

            prompt = Text.from_markup("\n(default: 1): \n\n", style="dim white")
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
        """, style=clinkey_green_style)

        console.print(
			"\n\n", 
			Panel.fit(
				(logo), 
				padding=(0, 2), 
				box=ROUNDED, 
				border_style=clinkey_pink_style
			), 
			justify="center"
		)

        subtitle = Text.from_markup(
			"Your own [bold light_green]SECRET BUDDY[/]...\n\n", 
			style=reg_style
		)
        console.print(Align.center(subtitle))

    def display_logo(self):
        """
        Display the logo at startup.
        """
        console.clear()
        self._display_logo_rich()

        welcome_text = Text.from_markup("\n\nPress [bold light_green]ENTER[/] to continue...\n\n", style=reg_style)
        console.print(Align.center(welcome_text))
        input()

    def display_passwords(self, passwords: list[str]):
        """
        Display generated passwords with rich formatting.
        """
        console.clear()
        self._display_logo_rich()

        passwords_text = Text.from_markup("Your ClinKey [bold light_green]PASSWORDS[/] \nare \n[bold light_green]READY[/]", style=clinkey_white_style)
        console.print(Panel.fit(Align.center(passwords_text), padding=(0, 1), box=ROUNDED, border_style=clinkey_pink_style), justify="center")

        for i, password in enumerate(passwords, 1):
            password_line = Text(f"{password:^}", style=clinkey_green_style)
            console.print(Align.center(password_line), justify="center")

        console.print()
        copy_hint = Text.from_markup("[bold orchid1]TIPS[/]\nChoose one to copy\n\n", style=reg_style)
        console.print(Align.center(copy_hint), justify="center")
	
    def get_options(self):
        options = {}
        console.print("Enter any further options seperate by space", style=clinkey_white_style, justify="center")
        return input()

    def get_output(self):
        console.print("Enter the path of the file to save the result", style=clinkey_white_style, justify="center")
        return input()