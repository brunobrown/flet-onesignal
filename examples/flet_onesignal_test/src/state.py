"""Observable test state for declarative UI."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

import flet as ft


class TestStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class LogEntry:
    message: str
    level: str
    time: str


@ft.observable
@dataclass
class TestStep:
    id: str = ""
    name: str = ""
    group: str = ""
    status: TestStatus = TestStatus.PENDING
    error_message: str = ""


@ft.observable
@dataclass
class TestState:
    steps: list[TestStep] = field(default_factory=list)
    logs: list[LogEntry] = field(default_factory=list)
    is_running: bool = False

    # Event capture slots
    last_permission_change: bool | None = None
    last_notification_foreground_id: str | None = None
    last_user_change_onesignal_id: str | None = None
    last_push_subscription_opted_in: bool | None = None

    # User interaction control
    waiting_for_user: bool = False
    waiting_message: str = ""
    user_response: str | None = None  # "continue" or "skip"

    # Warning dialog
    show_warning_dialog: bool = False
    warning_title: str = ""
    warning_message: str = ""
    warning_url: str = ""

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

    def clear_events(self):
        self.last_permission_change = None
        self.last_notification_foreground_id = None
        self.last_user_change_onesignal_id = None
        self.last_push_subscription_opted_in = None

    def set_step_status(self, step_id: str, status: TestStatus, error: str = ""):
        for i, step in enumerate(self.steps):
            if step.id == step_id:
                step.status = status
                step.error_message = error
                # Reassign to trigger ObservableList notification
                self.steps[i] = step
                break
