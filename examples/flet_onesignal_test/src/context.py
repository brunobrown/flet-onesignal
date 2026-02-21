"""Application context for sharing state and services via ft.create_context."""

from dataclasses import dataclass

import flet as ft
from state import TestState

import flet_onesignal as fos


@dataclass
class AppContext:
    state: TestState
    onesignal: fos.OneSignal
    clipboard: ft.Clipboard
    platform: str  # "android", "ios", etc.


AppCtx = ft.create_context(None)
