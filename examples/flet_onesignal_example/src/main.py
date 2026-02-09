"""
Flet OneSignal Example Application

Demonstrates all features of flet-onesignal using Flet 0.80.x declarative mode
with @ft.component, @ft.observable, and ft.create_context.
"""

import logging

import flet as ft
from components.drawer import AppDrawer
from config import ONESIGNAL_APP_ID
from context import AppContext, AppCtx
from pages import PAGE_BUILDERS
from state import AppState

import flet_onesignal as fos

logger = fos.setup_logging(level=logging.DEBUG)


@ft.component
def PageContent():
    ctx = ft.use_context(AppCtx)
    state = ctx.state
    builder = PAGE_BUILDERS.get(state.current_page, PAGE_BUILDERS["login"])
    return ft.Container(content=builder(), expand=True, padding=20)


@ft.component
def App(state, onesignal, clipboard):
    ctx = AppContext(
        state=state,
        onesignal=onesignal,
        clipboard=clipboard,
    )

    # Mutable ref to capture the View instance for the drawer handler.
    view_ref = [None]

    def on_event_logs_click(e):
        state.navigate("event_logs")

    async def on_menu_click(e):
        # Call show_drawer() on the View directly because page.render_views()
        # replaces page.views with a Component, breaking page.show_drawer().
        if view_ref[0]:
            await view_ref[0].show_drawer()

    def build_view():
        view_ref[0] = ft.View(
            controls=[PageContent()],
            appbar=ft.AppBar(
                leading=ft.IconButton(
                    icon=ft.Icons.MENU,
                    on_click=on_menu_click,
                ),
                title=ft.Text("Flet OneSignal"),
                bgcolor=ft.Colors.BLUE_700,
                color=ft.Colors.WHITE,
                actions=[
                    ft.IconButton(
                        icon=ft.Icons.BUG_REPORT,
                        on_click=on_event_logs_click,
                        tooltip="Event Logs",
                    ),
                ],
            ),
            drawer=ft.NavigationDrawer(
                controls=[AppDrawer()],
                on_dismiss=lambda e: None,
            ),
            padding=0,
            bgcolor=ft.Colors.WHITE,
            spacing=0,
        )
        return view_ref[0]

    return AppCtx(ctx, build_view)


def main(page: ft.Page):
    page.title = "Flet OneSignal"
    page.theme_mode = ft.ThemeMode.LIGHT

    # Create state outside component so event handlers can access it
    app_state = AppState()

    onesignal = fos.OneSignal(
        app_id=ONESIGNAL_APP_ID,
        log_level=fos.OSLogLevel.DEBUG,
        on_notification_click=lambda e: app_state.add_log(
            f"[Notification Click] {e.notification}", "info"
        ),
        on_notification_foreground=lambda e: app_state.add_log(
            f"[Notification Foreground] ID: {e.notification_id}", "info"
        ),
        on_permission_change=lambda e: app_state.add_log(
            f"[Permission Change] Granted: {e.permission}",
            "success" if e.permission else "warning",
        ),
        on_user_change=lambda e: app_state.add_log(
            f"[User Change] OneSignal ID: {e.onesignal_id}, External ID: {e.external_id}",
            "info",
        ),
        on_push_subscription_change=lambda e: app_state.add_log(
            f"[Push Subscription] ID: {e.id}, Opted In: {e.opted_in}", "info"
        ),
        on_iam_click=lambda e: app_state.add_log(
            f"[IAM Click] Action: {e.action_id}, URL: {e.url}", "info"
        ),
        on_iam_will_display=lambda e: app_state.add_log(
            f"[IAM Will Display] Message: {e.message}", "debug"
        ),
        on_iam_did_display=lambda e: app_state.add_log("[IAM Did Display]", "debug"),
        on_iam_will_dismiss=lambda e: app_state.add_log("[IAM Will Dismiss]", "debug"),
        on_iam_did_dismiss=lambda e: app_state.add_log("[IAM Did Dismiss]", "debug"),
        on_error=lambda e: app_state.add_log(
            f"[Error] {e.method}: {e.message}", "error"
        ),
    )
    page.services.append(onesignal)

    clipboard = ft.Clipboard()
    page.services.append(clipboard)

    logger.info(f"Platform: {page.platform}")
    logger.info(f"OneSignal App ID: {ONESIGNAL_APP_ID}")

    app_state.add_log("OneSignal initialized. Ready to test!", "success")

    page.render_views(App, app_state, onesignal, clipboard)


if __name__ == "__main__":
    ft.run(main)
