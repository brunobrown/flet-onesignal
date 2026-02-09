"""Observable application state for declarative UI."""

from dataclasses import dataclass, field
from datetime import datetime

import flet as ft


@dataclass
class LogEntry:
    message: str
    level: str
    time: str


@ft.observable
@dataclass
class AppState:
    current_page: str = "login"
    drawer_open: bool = False
    logs: list[LogEntry] = field(default_factory=list)

    def navigate(self, page_id: str):
        self.current_page = page_id
        self.drawer_open = False

    def toggle_drawer(self):
        self.drawer_open = not self.drawer_open

    def add_log(self, message: str, level: str = "info"):
        self.logs.append(
            LogEntry(
                message=message,
                level=level,
                time=datetime.now().strftime("%H:%M:%S"),
            )
        )

    def clear_logs(self):
        self.logs.clear()
