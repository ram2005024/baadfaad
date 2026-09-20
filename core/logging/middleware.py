import time
import uuid

from rich.table import Table
from rich.text import Text

from core.logging.logger import console

METHOD_COLORS = {
    "GET": "bold bright_green",
    "POST": "bold bright_blue",
    "PUT": "bold bright_yellow",
    "PATCH": "bold bright_cyan",
    "DELETE": "bold bright_red",
}


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.request_id = str(uuid.uuid4())[:8].upper()
        start = time.perf_counter()

        self._log_incoming(request)
        response = self.get_response(request)
        self._log_outgoing(
            request, response.status_code, (time.perf_counter() - start) * 1000
        )

        response["X-Request-ID"] = request.request_id
        return response

    def _log_incoming(self, request):
        line = Text()
        line.append("  ⬆  IN  ", style="bold white on dark_blue")
        line.append(
            f"  {request.method}  ", style=METHOD_COLORS.get(request.method, "white")
        )
        line.append(f"{request.path}  ", style="bold white")
        line.append(f"id:{request.request_id}", style="dim cyan")
        console.print()
        console.rule(style="dim blue")
        console.print(line)

    def _log_outgoing(self, request, status: int, duration_ms: float):
        if status >= 500:
            status_style, icon, rule_style = "bold white on red", "🔴", "red"
        elif status >= 400:
            status_style, icon, rule_style = "bold black on yellow", "🟡", "yellow"
        else:
            status_style, icon, rule_style = "bold black on green", "🟢", "green"

        table = Table.grid(padding=(0, 2))
        for _ in range(5):
            table.add_column(no_wrap=True)

        table.add_row(
            f" {icon} ",
            f"[{METHOD_COLORS.get(request.method, 'white')}] {request.method} [/]",
            f"[bold white]{request.path}[/]",
            f"[{status_style}]  {status}  [/]",
            f"[dim]{duration_ms:.1f} ms  ·  id:{request.request_id}[/]",
        )

        console.print(table)
        console.rule(style=rule_style)
        console.print()
