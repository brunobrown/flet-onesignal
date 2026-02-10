"""
Debug Console module for flet-onesignal.

Provides visual debugging tools for viewing application logs directly
in Flet apps during development.

Usage:
    ```python
    import flet as ft
    import flet_onesignal as fos

    async def main(page: ft.Page):
        debug_console = fos.DebugConsole()

        page.appbar = ft.AppBar(
            title=ft.Text("My App"),
            actions=[debug_console.icon],
        )

        page.add(ft.Text("Hello World"))

    ft.run(main)
    ```
"""

import logging
import os
from datetime import datetime
from enum import Enum
from logging.handlers import RotatingFileHandler
from typing import Optional

import flet as ft


class LogLevel(Enum):
    """Log level with associated colors."""

    DEBUG = ("DEBUG", ft.Colors.GREY_600)
    INFO = ("INFO", ft.Colors.BLUE_600)
    WARNING = ("WARNING", ft.Colors.AMBER_700)
    ERROR = ("ERROR", ft.Colors.RED_600)
    CRITICAL = ("CRITICAL", ft.Colors.RED_900)

    @property
    def color(self) -> str:
        return self.value[1]

    @classmethod
    def from_string(cls, level: str) -> "LogLevel":
        """Get LogLevel from string."""
        level_map = {
            "DEBUG": cls.DEBUG,
            "INFO": cls.INFO,
            "WARNING": cls.WARNING,
            "ERROR": cls.ERROR,
            "CRITICAL": cls.CRITICAL,
        }
        return level_map.get(level.upper(), cls.INFO)


def get_log_path() -> str:
    """Get the log file path."""
    log_path = os.getenv("FLET_APP_CONSOLE")
    if log_path:
        return log_path

    import tempfile

    try:
        test_path = "debug.log"
        with open(test_path, "a"):
            pass
        return test_path
    except (OSError, IOError):
        pass

    return os.path.join(tempfile.gettempdir(), "flet_onesignal_debug.log")


def _tail_file(filepath: str, num_lines: int) -> list[str]:
    """Efficiently read the last N lines of a file."""
    try:
        with open(filepath, "rb") as f:
            f.seek(0, 2)
            file_size = f.tell()

            if file_size == 0:
                return []

            buffer_size = min(8192, file_size)
            lines: list[str] = []
            remaining = file_size

            while remaining > 0 and len(lines) <= num_lines:
                read_size = min(buffer_size, remaining)
                f.seek(remaining - read_size)
                chunk = f.read(read_size)
                remaining -= read_size

                text = chunk.decode("utf-8", errors="replace")
                chunk_lines = text.splitlines(keepends=True)

                if lines and chunk_lines:
                    lines[0] = chunk_lines[-1] + lines[0]
                    chunk_lines = chunk_lines[:-1]

                lines = chunk_lines + lines

            return [line.strip() for line in lines[-num_lines:] if line.strip()]
    except Exception:
        return []


def _parse_log_line(line: str) -> tuple[str, LogLevel, str]:
    """
    Fast parse of log line. Returns (timestamp, level, message).

    Expected format: [timestamp] [LEVEL] ... - message
    """
    try:
        # Find first bracket pair for timestamp
        if line.startswith("["):
            end_ts = line.find("]")
            if end_ts > 0:
                timestamp = line[1:end_ts]
                rest = line[end_ts + 1 :].lstrip()

                # Find level in second bracket
                if rest.startswith("["):
                    end_lvl = rest.find("]")
                    if end_lvl > 0:
                        level_str = rest[1:end_lvl]
                        level = LogLevel.from_string(level_str)

                        # Find message after " - "
                        msg_start = rest.find(" - ", end_lvl)
                        if msg_start > 0:
                            message = rest[msg_start + 3 :]
                        else:
                            message = rest[end_lvl + 1 :].lstrip()

                        return timestamp, level, message
    except Exception:
        pass

    # Fallback: return line as-is
    return datetime.now().strftime("%H:%M:%S"), LogLevel.INFO, line


def setup_logging(
    level: int = logging.INFO,
    format_string: str = "[{asctime}] [{levelname}] [{filename}:{funcName}:{lineno}] - {message}",
    max_bytes: int = 256 * 1024,  # 256 KB max (reduced)
    backup_count: int = 1,
) -> logging.Logger:
    """
    Setup logging to write to FLET_APP_CONSOLE with automatic rotation.

    Args:
        level: Logging level (default: logging.INFO)
        format_string: Log format string
        max_bytes: Maximum log file size in bytes (default: 256KB)
        backup_count: Number of backup files to keep (default: 1)

    Returns:
        Configured logger instance.
    """
    log_path = get_log_path()

    file_handler = RotatingFileHandler(
        log_path,
        mode="a",
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8",
    )
    file_handler.setFormatter(logging.Formatter(format_string, style="{"))

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(format_string, style="{"))

    logger = logging.getLogger()
    logger.setLevel(level)

    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logging.getLogger(__name__)


class DebugConsole:
    """
    Lightweight debug console for viewing application logs.

    Provides an icon (for AppBar) and a FAB that open a dialog
    showing application logs with color-coded levels.

    Example:
        ```python
        debug = fos.DebugConsole()

        # Use icon in AppBar
        page.appbar = ft.AppBar(
            title=ft.Text("My App"),
            actions=[debug.icon],
        )

        # Or use FAB
        page.floating_action_button = debug.fab
        ```
    """

    # Maximum lines to display (performance limit)
    MAX_DISPLAY_LINES = 200

    def __init__(
        self,
        title: str = "Debug Console",
        max_lines: int = 200,
    ):
        self._title = title
        self._max_lines = min(max_lines, self.MAX_DISPLAY_LINES)
        self._page: Optional[ft.Page] = None
        self._dialog: Optional[ft.AlertDialog] = None
        self._log_column: Optional[ft.Column] = None
        self._cached_lines: list[str] = []
        self._current_filter: Optional[LogLevel] = None

        # Simple icon without badge
        self._icon = ft.IconButton(
            icon=ft.Icons.BUG_REPORT_OUTLINED,
            tooltip="Debug Console",
            on_click=self._show_console,
        )

        # FAB
        self._fab = ft.FloatingActionButton(
            icon=ft.Icons.BUG_REPORT,
            tooltip="Debug Console",
            on_click=self._show_console,
            bgcolor=ft.Colors.BLUE_GREY_700,
        )

    @property
    def icon(self) -> ft.IconButton:
        """Get the debug icon for use in AppBar actions."""
        return self._icon

    @property
    def fab(self) -> ft.FloatingActionButton:
        """Get the FAB for use as floating action button."""
        return self._fab

    def _read_logs(self) -> list[str]:
        """Read logs from file (cached)."""
        log_path = get_log_path()
        if not os.path.exists(log_path):
            return []
        return _tail_file(log_path, self._max_lines)

    def _create_log_text(self, line: str) -> ft.Text:
        """Create a simple Text widget for a log line."""
        timestamp, level, message = _parse_log_line(line)

        # Format: [HH:MM:SS] [LEVEL] message
        short_ts = timestamp.split()[-1] if " " in timestamp else timestamp
        display = f"[{short_ts}] [{level.value[0][:4]}] {message}"

        return ft.Text(
            display,
            size=11,
            color=level.color,
            selectable=True,
            no_wrap=False,
        )

    def _build_log_controls(
        self, lines: list[str], filter_level: Optional[LogLevel] = None
    ) -> list[ft.Text]:
        """Build log text controls from lines."""
        controls = []

        for line in lines:
            if filter_level:
                _, level, _ = _parse_log_line(line)
                if filter_level == LogLevel.ERROR:
                    if level not in (LogLevel.ERROR, LogLevel.CRITICAL):
                        continue
                elif level != filter_level:
                    continue

            controls.append(self._create_log_text(line))

        return controls

    def _show_console(self, e):
        """Show the console dialog."""
        if e.control.page:
            self._page = e.control.page

        if not self._page:
            return

        # Read and cache logs
        self._cached_lines = self._read_logs()
        self._current_filter = None

        # Build log controls
        log_controls = self._build_log_controls(self._cached_lines)

        # Create scrollable column for logs
        self._log_column = ft.Column(
            controls=log_controls
            if log_controls
            else [ft.Text("No logs available", italic=True, color=ft.Colors.GREY_500)],
            spacing=2,
            scroll=ft.ScrollMode.AUTO,
            auto_scroll=True,
            expand=True,
        )

        # Create dialog
        self._dialog = ft.AlertDialog(
            title=ft.Row(
                controls=[
                    ft.Icon(ft.Icons.BUG_REPORT, color=ft.Colors.BLUE_600, size=20),
                    ft.Text(self._title, weight=ft.FontWeight.BOLD, size=16),
                    ft.Container(expand=True),
                    ft.Text(
                        f"{len(log_controls)} lines",
                        size=11,
                        color=ft.Colors.GREY_600,
                    ),
                ],
                spacing=8,
            ),
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        # Filter buttons
                        ft.Row(
                            controls=[
                                ft.TextButton("All", on_click=lambda _: self._apply_filter(None)),
                                ft.TextButton(
                                    "Errors",
                                    on_click=lambda _: self._apply_filter(LogLevel.ERROR),
                                    style=ft.ButtonStyle(color=ft.Colors.RED_600),
                                ),
                                ft.TextButton(
                                    "Warnings",
                                    on_click=lambda _: self._apply_filter(LogLevel.WARNING),
                                    style=ft.ButtonStyle(color=ft.Colors.AMBER_700),
                                ),
                            ],
                            spacing=0,
                        ),
                        ft.Divider(height=1),
                        # Log content
                        ft.Container(
                            content=self._log_column,
                            expand=True,
                            padding=8,
                            border=ft.border.all(1, ft.Colors.GREY_400),
                            border_radius=4,
                        ),
                    ],
                    expand=True,
                    spacing=4,
                ),
                width=500,
                height=350,
            ),
            actions=[
                ft.TextButton("Clear", on_click=self._clear_logs),
                ft.TextButton("Refresh", on_click=self._refresh_logs),
                ft.TextButton("Close", on_click=self._close_dialog),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        # Use Flet 0.80.x dialog API
        self._page.show_dialog(self._dialog)

    def _apply_filter(self, level: Optional[LogLevel]):
        """Apply filter to cached logs."""
        if not self._log_column or not self._page:
            return

        self._current_filter = level
        log_controls = self._build_log_controls(self._cached_lines, level)

        if log_controls:
            self._log_column.controls = log_controls
        else:
            filter_name = level.value[0] if level else "matching"
            self._log_column.controls = [
                ft.Text(f"No {filter_name} logs found", italic=True, color=ft.Colors.GREY_500)
            ]

        self._page.update()

    def _clear_logs(self, e):
        """Clear logs from file."""
        try:
            log_path = get_log_path()
            if os.path.exists(log_path):
                with open(log_path, "w", encoding="utf-8") as f:
                    f.truncate(0)
        except Exception:
            pass

        self._cached_lines = []

        if self._log_column:
            self._log_column.controls = [
                ft.Text("Logs cleared", italic=True, color=ft.Colors.GREY_500)
            ]

        if self._page:
            self._page.update()

    def _refresh_logs(self, e):
        """Refresh logs from file."""
        self._cached_lines = self._read_logs()
        self._apply_filter(self._current_filter)

    def _close_dialog(self, e):
        """Close the dialog."""
        if self._page:
            self._page.pop_dialog()
