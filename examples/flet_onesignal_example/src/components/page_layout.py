"""
Standard page layout component with title, description, and content sections.
"""

import flet as ft


@ft.component
def PageLayout(
    title: str,
    description: str,
    code_example: str = "",
    children: list | None = None,
):
    """
    Standard page layout with title, description, code example, and interactive content.

    Args:
        title: Page title
        description: Description of the functionality
        code_example: Python code example to show
        children: Interactive content controls
    """
    controls = []

    # Title
    controls.append(
        ft.Text(
            title,
            size=24,
            weight=ft.FontWeight.BOLD,
        )
    )

    # Description
    controls.append(
        ft.Text(
            description,
            size=14,
            color=ft.Colors.GREY_700,
        )
    )

    controls.append(ft.Divider(height=20))

    # Code example section (if provided)
    if code_example:
        controls.append(
            ft.Text(
                "How to Use",
                size=16,
                weight=ft.FontWeight.W_600,
            )
        )
        controls.append(
            ft.Container(
                content=ft.Text(
                    code_example,
                    size=12,
                    font_family="monospace",
                    selectable=True,
                ),
                bgcolor=ft.Colors.GREY_100,
                padding=12,
                border_radius=8,
            )
        )
        controls.append(ft.Divider(height=20))

    # Interactive test section header
    controls.append(
        ft.Text(
            "Interactive Test",
            size=16,
            weight=ft.FontWeight.W_600,
        )
    )

    # Children content
    if children:
        for child in children:
            controls.append(child)

    return ft.Container(
        content=ft.Column(
            controls=controls,
            spacing=12,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        ),
        padding=20,
        expand=True,
    )
