"""
Reusable action button component.
"""

import flet as ft


@ft.component
def ActionButton(
    text: str,
    on_click,
    icon: str | None = None,
    primary: bool = True,
    disabled: bool = False,
):
    """
    Styled action button for executing OneSignal operations.

    Args:
        text: Button text
        on_click: Click handler
        icon: Optional icon
        primary: Whether to use primary styling
        disabled: Whether the button is disabled
    """
    if primary:
        return ft.FilledButton(
            text,
            icon=icon,
            on_click=on_click,
            disabled=disabled,
        )
    else:
        return ft.OutlinedButton(
            text,
            icon=icon,
            on_click=on_click,
            disabled=disabled,
        )
