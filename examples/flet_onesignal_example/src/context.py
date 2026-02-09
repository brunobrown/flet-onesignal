"""Application context for sharing state and services via ft.create_context."""

from dataclasses import dataclass

import flet as ft
from state import AppState

import flet_onesignal as fos


@dataclass
class AppContext:
    state: AppState
    onesignal: fos.OneSignal
    clipboard: ft.Clipboard


AppCtx = ft.create_context(None)
