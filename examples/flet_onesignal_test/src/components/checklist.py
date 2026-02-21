"""Checklist component showing test steps with status icons."""

import flet as ft
from context import AppCtx
from state import TestStatus


@ft.component
def Checklist():
    ctx = ft.use_context(AppCtx)
    state = ctx.state

    # Find last non-pending step to limit visible items.
    # auto_scroll keeps the latest active step visible.
    last_active = -1
    for i, step in enumerate(state.steps):
        if step.status != TestStatus.PENDING:
            last_active = i

    # Show up to 2 items ahead of last active (or all if idle)
    is_running = last_active >= 0
    if is_running:
        visible_count = min(len(state.steps), last_active + 3)
    else:
        visible_count = len(state.steps)

    current_group = None
    controls = []

    for idx, step in enumerate(state.steps):
        if idx >= visible_count:
            break

        # Group header
        if step.group != current_group:
            current_group = step.group
            if controls:
                controls.append(ft.Divider(height=1, color=ft.Colors.GREY_200))
            controls.append(
                ft.Text(
                    current_group,
                    weight=ft.FontWeight.BOLD,
                    size=13,
                    color=ft.Colors.BLUE_700,
                )
            )

        # Status icon
        if step.status == TestStatus.RUNNING:
            icon = ft.ProgressRing(width=16, height=16, stroke_width=2, color=ft.Colors.BLUE)
        elif step.status == TestStatus.PASSED:
            icon = ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN, size=18)
        elif step.status == TestStatus.FAILED:
            icon = ft.Icon(ft.Icons.CANCEL, color=ft.Colors.RED, size=18)
        elif step.status == TestStatus.SKIPPED:
            icon = ft.Icon(ft.Icons.SKIP_NEXT, color=ft.Colors.ORANGE, size=18)
        else:
            icon = ft.Icon(ft.Icons.RADIO_BUTTON_UNCHECKED, color=ft.Colors.GREY_400, size=18)

        # Step row
        name_color = ft.Colors.GREY_800
        if step.status == TestStatus.PASSED:
            name_color = ft.Colors.GREEN_700
        elif step.status == TestStatus.FAILED:
            name_color = ft.Colors.RED_700
        elif step.status == TestStatus.SKIPPED:
            name_color = ft.Colors.ORANGE_700

        row_controls = [icon, ft.Text(step.name, size=12, color=name_color, expand=True)]
        row = ft.Row(row_controls, spacing=8, vertical_alignment=ft.CrossAxisAlignment.CENTER)

        if step.error_message:
            controls.append(
                ft.Column(
                    [
                        row,
                        ft.Text(
                            f"  {step.error_message}",
                            size=10,
                            color=ft.Colors.RED_400,
                            italic=True,
                        ),
                    ],
                    spacing=0,
                )
            )
        else:
            controls.append(row)

    return ft.ListView(
        controls=controls,
        expand=True,
        spacing=2,
        padding=ft.Padding.all(10),
        auto_scroll=is_running,
    )
