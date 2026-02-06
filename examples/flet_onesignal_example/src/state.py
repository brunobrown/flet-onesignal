"""
Global application state using Flet 0.80.x @ft.observable pattern.
"""

from dataclasses import dataclass, field
from datetime import datetime

import flet as ft


@ft.observable
@dataclass
class AppState:
    """
    Observable application state.

    All changes to this state will automatically trigger UI updates
    in components that use it via ft.use_context().
    """

    # Navigation
    current_page: str = "login"
    drawer_open: bool = False

    # User info
    onesignal_id: str = ""
    external_id: str = ""

    # Event logs
    logs: list = field(default_factory=list)

    def navigate(self, page: str) -> None:
        """Navigate to a page and close the drawer."""
        self.current_page = page
        self.drawer_open = False

    def toggle_drawer(self) -> None:
        """Toggle the drawer open/closed state."""
        self.drawer_open = not self.drawer_open

    def add_log(self, message: str, level: str = "info") -> None:
        """Add a log entry with timestamp."""
        self.logs = [
            *self.logs,
            {
                "message": message,
                "level": level,
                "time": datetime.now().strftime("%H:%M:%S"),
            },
        ]

    def clear_logs(self) -> None:
        """Clear all logs."""
        self.logs = []
