"""
Reusable input field component.
"""

import flet as ft


@ft.component
def InputField(
    label: str,
    hint_text: str = "",
    value: str = "",
    on_change=None,
    width: int | None = None,
    expand: bool = False,
    password: bool = False,
    multiline: bool = False,
):
    """
    Styled input field for user input.

    Args:
        label: Field label
        hint_text: Placeholder text
        value: Current value
        on_change: Change handler
        width: Optional fixed width
        expand: Whether to expand to fill space
        password: Whether to hide input
        multiline: Whether to allow multiple lines
    """
    return ft.TextField(
        label=label,
        hint_text=hint_text,
        value=value,
        on_change=on_change,
        width=width,
        expand=expand,
        password=password,
        multiline=multiline,
        min_lines=3 if multiline else 1,
        max_lines=5 if multiline else 1,
    )
