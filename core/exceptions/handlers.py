from django.http import JsonResponse
from rest_framework.exceptions import (
    AuthenticationFailed,
    NotAuthenticated,
    PermissionDenied,
    ValidationError,
)
from rest_framework.views import exception_handler as drf_exception_handler
from rich.panel import Panel
from rich.table import Table

from core.exceptions.base import AppException
from core.logging.logger import console


def _req_id(request) -> str:
    return getattr(request, "request_id", "N/A")


def _error_body(error_code: str, message: str, details=None) -> dict:
    return {
        "success": False,
        "message": message,
        "error_code": error_code,
        "details": details,
    }


def rich_exception_handler(exc, context):
    request = context.get("request")
    req = getattr(request, "_request", request)
    rid = _req_id(req)
    path = getattr(req, "path", "N/A")
    method = getattr(req, "method", "N/A")

    # ── 1. All custom AppException subclasses ─────────────────────────
    if isinstance(exc, AppException):
        console.print(
            Panel(
                f"[warning]⚠  APP EXCEPTION[/]\n\n"
                f"[bold white]Route  :[/]  {method} {path}\n"
                f"[bold white]Status :[/]  {exc.status_code}\n"
                f"[bold white]Code   :[/]  [yellow]{exc.error_code}[/]\n"
                f"[bold white]Message:[/]  {exc.message}\n"
                f"[bold white]Req ID :[/]  [dim]{rid}[/]",
                title="[yellow]App Error[/]",
                border_style="yellow",
                expand=False,
            )
        )
        return JsonResponse(
            _error_body(exc.error_code, exc.message, exc.details),
            status=exc.status_code,
        )

    # ── 2. DRF Validation ─────────────────────────────────────────────
    if isinstance(exc, ValidationError):
        errors = exc.detail
        table = Table(
            "Field",
            "Message",
            style="yellow",
            header_style="bold yellow",
            border_style="dim yellow",
            show_lines=True,
        )
        formatted = []

        if isinstance(errors, dict):
            for field, msgs in errors.items():
                for msg in msgs if isinstance(msgs, list) else [msgs]:
                    table.add_row(field, str(msg))
                    formatted.append({"field": field, "message": str(msg)})
        elif isinstance(errors, list):
            for msg in errors:
                table.add_row("non_field_errors", str(msg))
                formatted.append({"field": "non_field_errors", "message": str(msg)})

        console.print(
            Panel(
                f"[warning]📋  VALIDATION ERROR[/]\n\n"
                f"[bold white]Route  :[/]  {method} {path}\n"
                f"[bold white]Req ID :[/]  [dim]{rid}[/]",
                title="[yellow]Validation Error[/]",
                border_style="yellow",
                expand=False,
            )
        )
        console.print(table)
        return JsonResponse(
            _error_body("VALIDATION_ERROR", "Request validation failed", formatted),
            status=422,
        )

    # ── 3. Not Authenticated ───────────────────────────────────────────
    if isinstance(exc, (NotAuthenticated, AuthenticationFailed)):
        console.print(
            Panel(
                f"[warning]🔒  NOT AUTHENTICATED[/]\n\n"
                f"[bold white]Route  :[/]  {method} {path}\n"
                f"[bold white]Req ID :[/]  [dim]{rid}[/]",
                title="[yellow]Auth Error[/]",
                border_style="yellow",
                expand=False,
            )
        )
        return JsonResponse(
            _error_body(
                "NOT_AUTHENTICATED", "Authentication credentials were not provided."
            ),
            status=401,
        )

    # ── 4. Permission Denied ───────────────────────────────────────────
    if isinstance(exc, PermissionDenied):
        console.print(
            Panel(
                f"[warning]🚫  PERMISSION DENIED[/]\n\n"
                f"[bold white]Route  :[/]  {method} {path}\n"
                f"[bold white]Req ID :[/]  [dim]{rid}[/]",
                title="[yellow]Permission Error[/]",
                border_style="yellow",
                expand=False,
            )
        )
        return JsonResponse(
            _error_body(
                "PERMISSION_DENIED",
                "You do not have permission to perform this action.",
            ),
            status=403,
        )

    # ── 5. Remaining DRF exceptions ────────────────────────────────────
    response = drf_exception_handler(exc, context)
    if response is not None:
        console.print(
            Panel(
                f"[warning]🌐  DRF EXCEPTION[/]\n\n"
                f"[bold white]Route  :[/]  {method} {path}\n"
                f"[bold white]Status :[/]  {response.status_code}\n"
                f"[bold white]Req ID :[/]  [dim]{rid}[/]",
                title="[yellow]HTTP Error[/]",
                border_style="yellow",
                expand=False,
            )
        )
        return JsonResponse(
            _error_body("HTTP_ERROR", str(exc)),
            status=response.status_code,
        )

    # ── 6. Completely unhandled ────────────────────────────────────────
    console.print(
        Panel(
            f"[critical] 💥 UNHANDLED EXCEPTION [/]\n\n"
            f"[bold white]Route  :[/]  {method} {path}\n"
            f"[bold white]Type   :[/]  [red]{type(exc).__name__}[/]\n"
            f"[bold white]Req ID :[/]  [dim]{rid}[/]",
            title="[red]Server Error[/]",
            border_style="red",
            expand=False,
        )
    )
    console.print_exception(show_locals=True)
    return JsonResponse(
        _error_body("SERVER_ERROR", "Something went wrong on the server"),
        status=500,
    )
