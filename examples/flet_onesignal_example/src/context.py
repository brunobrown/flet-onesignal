"""
Application contexts for sharing state and services.
"""

from dataclasses import dataclass
from typing import Optional

import flet as ft
from state import AppState

# Forward reference for OneSignal
import flet_onesignal as fos


@dataclass
class AppContext:
    """
    Application context containing shared state and services.
    """

    state: AppState
    onesignal: Optional[fos.OneSignal] = None


# Create the context
AppCtx = ft.create_context(None)
