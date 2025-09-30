"""Click-based command line interface for the clinkey password generator."""

from __future__ import annotations

import pathlib
from typing import Iterable, Optional

import click
from rich import box
from rich.align import Align
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from clinkey_cli.main import Clinkey


console = Console(style="on grey11")


class ClinkeyView:
    """Render user interactions with Rich while mirroring the original styling."""

    def __init__(self) -> None:
        self._logo_style = {
            "title_color": "bold light_green",
            "accent_color": "orchid1",
            "text_color": "grey100",
        }

    def _clear(self) -> None:
        console.clear()

    def _logo_panel(self) -> Panel:
        logo = Text(
            """
╔═╝  ║    ╝  ╔═    ║ ║  ╔═╝  ║ ║
║    ║    ║  ║  ║  ╔╝   ╔═╝  ═╔╝
══╝  ══╝  ╝  ╝  ╝  ╝ ╝  ══╝   ╝ 
            """,
            style=self._logo_style["title_color"],
            justify="center",
        )
        return Panel.fit(
            logo,
            padding=(0, 2),
            box=box.ROUNDED,
            border_style=self._logo_style["accent_color"],
        )

    def display_logo(self) -> None:
        self._clear()
        console.print("\n\n")
        console.print(self._logo_panel(), justify="center")
        subtitle = Text.from_markup(
            "Your own [bold light_green]SECRET BUDDY[/]...\n\n",
            style="white",
            justify="center",
        )
        console.print(Align.center(subtitle))
        prompt = Text.from_markup(
            "Press [bold light_green]ENTER[/] to continue...\n\n",
            style="white",
        )
        console.print(Align.center(prompt), end="")
        input()

    def ask_for_type(self) -> str:
        self._clear()
        console.print(self._logo_panel(), justify="center")
        console.print(
            Align.center(
                Text.from_markup(
                    "How [bold light_green]BOLD[/] do you want your password?\n",
                    style="white",
                )
            )
        )
        choices = Text.from_markup(
            "1 - [bold orchid1]Vanilla[/] (letters only)\n"
            "2 - [bold orchid1]Twisted[/] (letters and digits)\n"
            "3 - [bold orchid1]So NAAASTY[/] (letters, digits, symbols)",
            style="white",
        )
        console.print(Align.center(choices))
        console.print(
            Align.center(
                Text.from_markup(
                    "Choose your [bold light_green]TRIBE[/] (1 / 2 / 3): ",
                    style="bright_black",
                )
            ),
            end="",
        )
        choice = input().strip()
        return {"1": "normal", "2": "strong", "3": "super_strong"}.get(choice, "normal")

    def ask_for_length(self) -> int:
        self._clear()
        console.print(self._logo_panel(), justify="center")
        console.print(
            Align.center(
                Text.from_markup(
                    "How [bold light_green]LONG[/] do you like it ?",
                    style="white",
                )
            )
        )
        console.print(
            Align.center(Text.from_markup("(default: 16): ", style="bright_black")),
            end="",
        )
        value = input().strip()
        try:
            length = int(value)
            return length if length > 0 else 16
        except ValueError:
            return 16

    def ask_for_number(self) -> int:
        self._clear()
        console.print(self._logo_panel(), justify="center")
        console.print(
            Align.center(
                Text.from_markup(
                    "How [bold light_green]MANY[/] you fancy at once ?",
                    style="white",
                )
            )
        )
        console.print(
            Align.center(Text.from_markup("(default: 1): ", style="bright_black")),
            end="",
        )
        value = input().strip()
        try:
            count = int(value)
            return count if count > 0 else 1
        except ValueError:
            return 1

    def ask_for_options(self) -> list[str]:
        self._clear()
        console.print(self._logo_panel(), justify="center")
        console.print(
            Align.center(
                Text.from_markup(
                    "Any extra [bold light_green]OPTIONS[/]? (separate by spaces)",
                    style="white",
                )
            )
        )
        console.print(
            Align.center(Text.from_markup(
                "Available: lower, no_sep", 
                style="bright_black"
                )
                )
        )
        choices = input().strip()
        return choices.split() if choices else []

    def ask_for_output_path(self) -> Optional[str]:
        self._clear()
        console.print(self._logo_panel(), justify="center")
        console.print(
            Align.center(
                Text.from_markup(
                    "Enter a file path to save the result (press ENTER to skip):",
                    style="white",
                )
            ),
            end="",
        )
        value = input().strip()
        return value or None

    def ask_for_separator(self) -> Optional[str]:
        self._clear()
        console.print(self._logo_panel(), justify="center")
        console.print(
            Align.center(
                Text.from_markup(
                    "Custom [bold light_green]SEPARATOR[/]? (press ENTER to skip)",
                    style="white",
                )
            )
        )
        console.print(
            Align.center(
                Text.from_markup("Use exactly one non-space character.", style="bright_black")
            )
        )
        console.print(
            Align.center(Text.from_markup("Value: ", style="bright_black")),
            end="",
        )
        value = input().strip()
        if not value:
            return None
        return value[0]

    def display_passwords(self, passwords: Iterable[str]) -> None:
        self._clear()
        console.print(self._logo_panel(), justify="center")
        console.print(
            Panel.fit(
                Align.center(
                    Text.from_markup(
                        "Your Clinkey [bold light_green]PASSWORDS[/] are [bold light_green]READY[/]",
                        style="white",
                    )
                ),
                padding=(0, 1),
                box=box.ROUNDED,
                border_style=self._logo_style["accent_color"],
            ),
            justify="center",
        )
        table = Table(show_header=False, box=box.ROUNDED, border_style=self._logo_style["accent_color"])
        table.add_column("password", style=self._logo_style["title_color"], justify="center")
        for password in passwords:
            table.add_row(Text(password, style="bold light_green", justify="center"))
        console.print(table, justify="center")

        console.print(
            Align.center(
                Text.from_markup("Choose one to copy !", style="white"),
            )
        )


view = ClinkeyView()

def _parse_extra_options(options: Iterable[str]) -> dict[str, bool]:
    lookup = {
        "lower": {"lower", "low", "-l", "--lower", "lw"},
        "no_sep": {"no_sep", "nosep", "-ns", "--no-sep", "no-sep", "ns"},
    }
    result = {"lower": False, "no_sep": False}
    for option in options:
        token = option.strip().lower()
        for key, aliases in lookup.items():
            if token in aliases:
                result[key] = True
    return result


def _write_passwords(path: pathlib.Path, passwords: Iterable[str]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for password in passwords:
            handle.write(f"{password}\n")


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.option("-l", "--length", type=int, default=None, help="Password length (default: 16).")
@click.option(
    "-t",
    "--type",
    "type_",
    type=click.Choice(
        ["normal", "strong", "super_strong"], 
        case_sensitive=False
    ),
    default=None,
    help="Password profile: normal, strong, or super_strong.",
)
@click.option(
    "-n",
    "--number",
    type=int,
    default=None,
    help="Number of passwords to generate (default: 1).",
)
@click.option("-ns", "--no-sep", "no_sep", is_flag=True, help="Remove separators from the result.")
@click.option("-low", "--lower", is_flag=True, help="Convert generated passwords to lowercase.")
@click.option(
    "-s",
    "--separator",
    "new_separator",
    type=str,
    default=None,
    help="Use a custom separator character instead of '-' and '_'.",
)
@click.option(
    "-o",
    "--output",
    type=click.Path(dir_okay=False, writable=True, resolve_path=True, path_type=pathlib.Path),
    default=None,
    help="Write the result to a file instead of displaying it.",
)
def main(
    length: Optional[int],
    type_: Optional[str],
    number: Optional[int],
    no_sep: bool,
    lower: bool,
	new_separator: Optional[str],
    output: Optional[pathlib.Path],
) -> None:
    """Generate secure, pronounceable passwords from your terminal."""

    generator = Clinkey()

    interactive = length is None and type_ is None and number is None

    if interactive:
        view.display_logo()
        length = view.ask_for_length()
        type_ = view.ask_for_type()
        number = view.ask_for_number()
        extra = _parse_extra_options(view.ask_for_options())
        lower = extra["lower"]
        no_sep = extra["no_sep"]
        chosen_sep = view.ask_for_separator()
        if chosen_sep:
            new_separator = chosen_sep
        chosen_output = view.ask_for_output_path()
        if chosen_output:
            output = pathlib.Path(chosen_output).expanduser().resolve()

    length = 16 if length is None else length
    type_ = "normal" if type_ is None else type_.lower()
    number = 1 if number is None else number

    if new_separator is not None:
        new_separator = new_separator.strip()
        if len(new_separator) != 1 or new_separator.isspace():
            raise click.BadParameter("Separator must be exactly one non-space character.", param_hint="--separator")

    passwords = generator.generate_batch(
        length=length,
        type=type_,
        count=number,
        lower=lower,
        no_separator=no_sep,
        new_separator=new_separator,
    )

    if output:
        _write_passwords(output, passwords)
        click.echo(f"Passwords saved to {output}")
    elif interactive:
        view.display_passwords(passwords)
    else:
        for password in passwords:
            click.echo(password)


if __name__ == "__main__":  # pragma: no cover
    main()
