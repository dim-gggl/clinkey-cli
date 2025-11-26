from rich.panel import Panel
from rich.console import Console
from rich.text import Text
from rich.align import Align
from rich.spinner import Spinner
from rich.live import Live
import time

console = Console()
spinner = Spinner("dots12", text=Text("Loading...", style="bold red"), style="red")
centered_spinner = Align.center(spinner, vertical="middle")
console.clear()

with Live(centered_spinner, refresh_per_second=20, transient=True) as live:
    time.sleep(10)