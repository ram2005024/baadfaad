from rich.console import Console
from rich.theme import Theme
from rich.traceback import install

install(show_locals=True, width=140, extra_lines=3)

console = Console(
    theme=Theme(
        {
            "info": "bold cyan",
            "success": "bold green",
            "warning": "bold yellow",
            "error": "bold red",
            "critical": "bold white on red",
            "muted": "dim white",
        }
    ),
    highlight=True,
)
