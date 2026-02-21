"""
Flet OneSignal Automated Test Runner

Executes all flet-onesignal SDK features with a single button press,
showing real-time progress via checklist and log panel.
"""

import logging

import flet as ft
from components.checklist import Checklist
from components.log_panel import LogPanel
from config import ONESIGNAL_APP_ID
from context import AppContext, AppCtx
from runner import run_all_tests
from state import TestState, TestStatus, TestStep
from test_steps import TEST_STEPS

import flet_onesignal as fos

logger = fos.setup_logging(level=logging.DEBUG)


# ── Event handlers (write to state slots) ────────────────────────────────


def _on_notification_foreground(state: TestState, e):
    state.last_notification_foreground_id = e.notification_id
    state.add_log(f"[Event] Notification foreground: {e.notification_id}", "debug")


def _on_permission_change(state: TestState, e):
    state.last_permission_change = e.permission
    state.add_log(f"[Event] Permission change: {e.permission}", "debug")


def _on_user_change(state: TestState, e):
    state.last_user_change_onesignal_id = e.onesignal_id
    state.add_log(f"[Event] User change: OS ID={e.onesignal_id}", "debug")


def _on_push_subscription_change(state: TestState, e):
    state.last_push_subscription_opted_in = e.opted_in
    state.add_log(f"[Event] Push sub change: opted_in={e.opted_in}", "debug")


# ── UI Components ────────────────────────────────────────────────────────


@ft.component
def InteractionBanner():
    ctx = ft.use_context(AppCtx)
    state = ctx.state

    if not state.waiting_for_user:
        return ft.Container(visible=False)

    def on_continue(e):
        state.user_response = "continue"

    def on_skip(e):
        state.user_response = "skip"

    return ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Icon(ft.Icons.WARNING_AMBER, color=ft.Colors.ORANGE_700, size=20),
                        ft.Text(state.waiting_message, size=13, expand=True),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Row(
                    [
                        ft.Button(
                            "Continue",
                            on_click=on_continue,
                            color=ft.Colors.WHITE,
                            bgcolor=ft.Colors.BLUE,
                        ),
                        ft.OutlinedButton("Skip", on_click=on_skip),
                    ],
                ),
            ],
            spacing=8,
        ),
        padding=10,
        bgcolor=ft.Colors.ORANGE_50,
        border=ft.Border.all(1, ft.Colors.ORANGE_200),
        border_radius=8,
    )


@ft.component
def WarningDialog():
    ctx = ft.use_context(AppCtx)
    state = ctx.state

    if not state.show_warning_dialog:
        return ft.Container(visible=False)

    def on_dismiss(e):
        state.show_warning_dialog = False

    msg = state.warning_message
    if state.warning_url:
        msg += f"\n\nDocs: {state.warning_url}"

    return ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Icon(ft.Icons.INFO_OUTLINE, color=ft.Colors.BLUE_700, size=22),
                        ft.Text(
                            state.warning_title,
                            size=14,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.BLUE_700,
                            expand=True,
                        ),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Text(msg, size=12, selectable=True),
                ft.Row(
                    [
                        ft.OutlinedButton("OK", on_click=on_dismiss),
                    ],
                ),
            ],
            spacing=8,
        ),
        padding=10,
        bgcolor=ft.Colors.BLUE_50,
        border=ft.Border.all(1, ft.Colors.BLUE_200),
        border_radius=8,
    )


@ft.component
def ControlBar():
    ctx = ft.use_context(AppCtx)
    state = ctx.state

    total = len(state.steps)
    passed = sum(1 for s in state.steps if s.status == TestStatus.PASSED)
    failed = sum(1 for s in state.steps if s.status == TestStatus.FAILED)
    skipped = sum(1 for s in state.steps if s.status == TestStatus.SKIPPED)
    done = passed + failed + skipped

    async def on_start(e):
        if state.is_running:
            return
        await run_all_tests(ctx)

    def on_reset(e):
        if state.is_running:
            return
        for i, step in enumerate(state.steps):
            step.status = TestStatus.PENDING
            step.error_message = ""
            state.steps[i] = step
        state.clear_logs()
        state.clear_events()
        state.add_log("Reset. Ready to run.", "info")

    return ft.ResponsiveRow(
        [
            ft.Row(
                [
                    ft.Button(
                        "Start",
                        icon=ft.Icons.PLAY_ARROW,
                        on_click=on_start,
                        disabled=state.is_running,
                        color=ft.Colors.WHITE,
                        bgcolor=ft.Colors.GREEN_700,
                    ),
                    ft.OutlinedButton(
                        "Reset",
                        icon=ft.Icons.REFRESH,
                        on_click=on_reset,
                        disabled=state.is_running,
                    ),
                ],
                col={"xs": 12, "sm": 6},
                spacing=8,
            ),
            ft.Row(
                [
                    ft.Text(
                        f"{done}/{total}",
                        weight=ft.FontWeight.BOLD,
                        size=13,
                    ),
                    ft.Container(
                        content=ft.Text(f"P:{passed}", color=ft.Colors.WHITE, size=11),
                        bgcolor=ft.Colors.GREEN_700,
                        border_radius=4,
                        padding=ft.Padding.symmetric(horizontal=6, vertical=2),
                        tooltip="Passed",
                    ),
                    ft.Container(
                        content=ft.Text(f"F:{failed}", color=ft.Colors.WHITE, size=11),
                        bgcolor=ft.Colors.RED_700,
                        border_radius=4,
                        padding=ft.Padding.symmetric(horizontal=6, vertical=2),
                        tooltip="Failed",
                    ),
                    ft.Container(
                        content=ft.Text(f"S:{skipped}", color=ft.Colors.WHITE, size=11),
                        bgcolor=ft.Colors.ORANGE_700,
                        border_radius=4,
                        padding=ft.Padding.symmetric(horizontal=6, vertical=2),
                        tooltip="Skipped",
                    ),
                ],
                col={"xs": 12, "sm": 6},
                alignment=ft.MainAxisAlignment.END,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=8,
            ),
        ],
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )


@ft.component
def App(state, onesignal, clipboard, platform):
    ctx = AppContext(
        state=state,
        onesignal=onesignal,
        clipboard=clipboard,
        platform=platform,
    )

    return AppCtx(
        ctx,
        lambda: ft.View(
            controls=[
                ft.Column(
                    [
                        ControlBar(),
                        ft.Divider(height=1),
                        ft.Container(content=Checklist(), expand=2),
                        WarningDialog(),
                        InteractionBanner(),
                        ft.Container(content=LogPanel(), expand=1),
                    ],
                    expand=True,
                    spacing=4,
                )
            ],
            appbar=ft.AppBar(
                title=ft.Text("OneSignal Test Runner"),
                bgcolor=ft.Colors.BLUE_700,
                color=ft.Colors.WHITE,
            ),
            padding=8,
        ),
    )


# ── Entry point ──────────────────────────────────────────────────────────


def main(page: ft.Page):
    page.title = "OneSignal Test Runner"
    page.theme_mode = ft.ThemeMode.LIGHT

    # Initialize state with step definitions
    app_state = TestState()
    for step_def in TEST_STEPS:
        app_state.steps.append(TestStep(id=step_def.id, name=step_def.name, group=step_def.group))

    # Wire up OneSignal with event capture handlers
    onesignal = fos.OneSignal(
        app_id=ONESIGNAL_APP_ID,
        log_level=fos.OSLogLevel.DEBUG,
        on_notification_foreground=lambda e: _on_notification_foreground(app_state, e),
        on_permission_change=lambda e: _on_permission_change(app_state, e),
        on_user_change=lambda e: _on_user_change(app_state, e),
        on_push_subscription_change=lambda e: _on_push_subscription_change(app_state, e),
        on_notification_click=lambda e: app_state.add_log(
            f"[Event] Notification click: {e.notification}", "debug"
        ),
        on_iam_click=lambda e: app_state.add_log(f"[Event] IAM click: {e.action_id}", "debug"),
        on_iam_will_display=lambda e: app_state.add_log("[Event] IAM will display", "debug"),
        on_iam_did_display=lambda e: app_state.add_log("[Event] IAM did display", "debug"),
        on_iam_will_dismiss=lambda e: app_state.add_log("[Event] IAM will dismiss", "debug"),
        on_iam_did_dismiss=lambda e: app_state.add_log("[Event] IAM did dismiss", "debug"),
        on_error=lambda e: app_state.add_log(f"[Error] {e.method}: {e.message}", "fail"),
    )
    page.services.append(onesignal)

    clipboard = ft.Clipboard()
    page.services.append(clipboard)

    platform = page.platform.value if page.platform else "unknown"
    app_state.add_log(f"Platform: {platform}", "info")
    app_state.add_log(f"App ID: {ONESIGNAL_APP_ID}", "info")
    app_state.add_log(f"Steps: {len(TEST_STEPS)}", "info")
    app_state.add_log("Ready. Tap 'Start Tests' to begin.", "info")

    page.render_views(App, app_state, onesignal, clipboard, platform)


if __name__ == "__main__":
    ft.run(main)
