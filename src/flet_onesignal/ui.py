"""Rich-based UI helpers for fos-build CLI output.

Requires the 'cli' extra: pip install flet-onesignal[cli]
"""

try:
    from rich.console import Console
    from rich.panel import Panel

    console = Console()
except ImportError:
    import sys

    print(
        "ERROR: 'rich' is required for fos-build.\n"
        "Install it with:\n"
        "  uv add flet-onesignal[cli]\n"
        "  pip install flet-onesignal[cli]\n"
        "  poetry add flet-onesignal[cli]",
        file=sys.stderr,
    )
    sys.exit(1)


def header():
    """Print the FOS Build header panel."""
    console.print()
    console.print(
        Panel(
            "[bold cyan]FOS Build - Flet OneSignal Build Tool[/]",
            style="cyan",
        )
    )


def info(label: str, value: str):
    """Print an info line: 'ℹ label: value'."""
    console.print(f"[cyan]ℹ {label}:[/] {value}")


def step(n: int, msg: str):
    """Print a step indicator: '▶ Step N: msg'."""
    console.print(f"\n[bold yellow]▶ Step {n}:[/] {msg}\n")


def success_panel(build_type: str, output_dir: str | None, next_steps: list[str]):
    """Print a green success panel with output location and next steps."""
    lines = ["[bold green]✓ BUILD SUCCESSFUL![/]"]

    if output_dir:
        lines.append(f"\n  Output: {output_dir}")

    if next_steps:
        lines.append("\n  Next steps:")
        for s in next_steps:
            lines.append(f"    • {s}")

    console.print()
    console.print(Panel("\n".join(lines), style="green"))


def error_panel(title: str, body: str):
    """Print a red error panel with title and body."""
    content = f"[bold red]✗ {title}[/]\n\n{body}"
    console.print()
    console.print(Panel(content, title="ERROR", style="red"))


def failure_panel(tips: list[str]):
    """Print a red failure panel with tips."""
    lines = ["[bold red]✗ BUILD FAILED[/]", "\n  Check the error messages above for details."]

    if tips:
        lines.append("\n  Tips:")
        for tip in tips:
            lines.append(f"    • {tip}")

    console.print()
    console.print(Panel("\n".join(lines), style="red"))


def warning(msg: str):
    """Print a yellow warning message."""
    console.print(f"[yellow]⚠ {msg}[/]")


def modified(msg: str):
    """Print a green checkmark for modified/copied files."""
    console.print(f"  [green]✓ {msg}[/]")


def build_info(msg: str):
    """Print a build phase info line (e.g., 'Building APK...')."""
    console.print(f"\n[bold]{msg}[/]\n")
