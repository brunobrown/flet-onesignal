"""
Flet OneSignal Example Application

A comprehensive example demonstrating all features of the flet-onesignal package
using Flet 0.80.x with NavigationDrawer for navigation.
"""

import logging
from dataclasses import dataclass, field
from datetime import datetime

import flet as ft

import flet_onesignal as fos

# Replace with your actual OneSignal App ID
ONESIGNAL_APP_ID = "example-123a-12a3-1a23-abcd1ef23g45"

# Setup logging
logger = fos.setup_logging(level=logging.DEBUG)


# =============================================================================
# Observable State Classes
# =============================================================================


@dataclass
class LogEntry:
    message: str
    level: str
    time: str


@dataclass
class AppState:
    """Global application state."""

    current_page: str = "login"
    drawer_open: bool = False
    logs: list[LogEntry] = field(default_factory=list)

    def navigate(self, page_id: str):
        self.current_page = page_id
        self.drawer_open = False

    def toggle_drawer(self):
        self.drawer_open = not self.drawer_open

    def add_log(self, message: str, level: str = "info"):
        self.logs = [
            *self.logs,
            LogEntry(
                message=message,
                level=level,
                time=datetime.now().strftime("%H:%M:%S"),
            ),
        ]

    def clear_logs(self):
        self.logs = []


# =============================================================================
# Navigation structure
# =============================================================================

NAVIGATION_GROUPS = [
    {
        "title": "Main",
        "items": [
            {"id": "login", "label": "Login/Logout", "icon": ft.Icons.LOGIN},
            {"id": "consent", "label": "Consent", "icon": ft.Icons.PRIVACY_TIP},
        ],
    },
    {
        "title": "User",
        "items": [
            {"id": "user_identity", "label": "Identity", "icon": ft.Icons.PERSON},
            {"id": "user_tags", "label": "Tags", "icon": ft.Icons.LABEL},
            {"id": "user_aliases", "label": "Aliases", "icon": ft.Icons.ALTERNATE_EMAIL},
            {"id": "user_email_sms", "label": "Email/SMS", "icon": ft.Icons.EMAIL},
            {"id": "user_language", "label": "Language", "icon": ft.Icons.LANGUAGE},
            {"id": "user_push", "label": "Push", "icon": ft.Icons.NOTIFICATIONS},
        ],
    },
    {
        "title": "Notifications",
        "items": [
            {
                "id": "notifications",
                "label": "Notifications",
                "icon": ft.Icons.NOTIFICATIONS_ACTIVE,
            },
        ],
    },
    {
        "title": "In-App Messages",
        "items": [
            {"id": "in_app_messages", "label": "IAM", "icon": ft.Icons.MESSAGE},
        ],
    },
    {
        "title": "Location",
        "items": [
            {"id": "location", "label": "Location", "icon": ft.Icons.LOCATION_ON},
        ],
    },
    {
        "title": "Session",
        "items": [
            {"id": "session", "label": "Outcomes", "icon": ft.Icons.ANALYTICS},
        ],
    },
    {
        "title": "Live Activities",
        "items": [
            {"id": "live_activities", "label": "Live Activities", "icon": ft.Icons.LIVE_TV},
        ],
    },
    {
        "title": "Debug",
        "items": [
            {"id": "debug", "label": "Debug", "icon": ft.Icons.BUG_REPORT},
        ],
    },
    {
        "title": "Events",
        "items": [
            {"id": "event_logs", "label": "Event Logs", "icon": ft.Icons.LIST_ALT},
        ],
    },
]


# =============================================================================
# Reusable Components
# =============================================================================

LOG_COLORS = {
    "info": ft.Colors.GREY_800,
    "success": ft.Colors.GREEN_700,
    "warning": ft.Colors.ORANGE_700,
    "error": ft.Colors.RED_700,
    "debug": ft.Colors.BLUE_700,
}


# Old declarative components removed - now using imperative mode


# =============================================================================
# Entry Point (Imperative mode)
# =============================================================================
# NOTE: Using imperative mode because NavigationDrawer doesn't work properly
# with page.render_views() in Flet 0.80.x declarative mode.


def main(page: ft.Page):
    """Main entry point."""
    page.title = "Flet OneSignal"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.bgcolor = ft.Colors.WHITE

    # Create shared state
    app_state = AppState()

    # -------------------------------------------------------------------------
    # Event handlers for OneSignal
    # -------------------------------------------------------------------------

    def on_notification_click(e: fos.OSNotificationClickEvent):
        app_state.add_log(f"[Notification Click] {e.notification}", "info")
        update_content()

    def on_notification_foreground(e: fos.OSNotificationWillDisplayEvent):
        app_state.add_log(f"[Notification Foreground] ID: {e.notification_id}", "info")
        update_content()

    def on_permission_change(e: fos.OSPermissionChangeEvent):
        level = "success" if e.permission else "warning"
        app_state.add_log(f"[Permission Change] Granted: {e.permission}", level)
        update_content()

    def on_user_change(e: fos.OSUserChangedEvent):
        app_state.add_log(
            f"[User Change] OneSignal ID: {e.onesignal_id}, External ID: {e.external_id}", "info"
        )
        update_content()

    def on_push_subscription_change(e: fos.OSPushSubscriptionChangedEvent):
        app_state.add_log(f"[Push Subscription] ID: {e.id}, Opted In: {e.opted_in}", "info")
        update_content()

    def on_iam_click(e: fos.OSInAppMessageClickEvent):
        app_state.add_log(f"[IAM Click] Action: {e.action_id}, URL: {e.url}", "info")
        update_content()

    def on_iam_will_display(e: fos.OSInAppMessageWillDisplayEvent):
        app_state.add_log(f"[IAM Will Display] Message: {e.message}", "debug")
        update_content()

    def on_iam_did_display(e: fos.OSInAppMessageDidDisplayEvent):
        app_state.add_log("[IAM Did Display]", "debug")
        update_content()

    def on_iam_will_dismiss(e: fos.OSInAppMessageWillDismissEvent):
        app_state.add_log("[IAM Will Dismiss]", "debug")
        update_content()

    def on_iam_did_dismiss(e: fos.OSInAppMessageDidDismissEvent):
        app_state.add_log("[IAM Did Dismiss]", "debug")
        update_content()

    def on_error(e: fos.OSErrorEvent):
        app_state.add_log(f"[Error] {e.method}: {e.message}", "error")
        update_content()

    # -------------------------------------------------------------------------
    # Create OneSignal service
    # -------------------------------------------------------------------------

    onesignal = fos.OneSignal(
        app_id=ONESIGNAL_APP_ID,
        log_level=fos.OSLogLevel.DEBUG,
        on_notification_click=on_notification_click,
        on_notification_foreground=on_notification_foreground,
        on_permission_change=on_permission_change,
        on_user_change=on_user_change,
        on_push_subscription_change=on_push_subscription_change,
        on_iam_click=on_iam_click,
        on_iam_will_display=on_iam_will_display,
        on_iam_did_display=on_iam_did_display,
        on_iam_will_dismiss=on_iam_will_dismiss,
        on_iam_did_dismiss=on_iam_did_dismiss,
        on_error=on_error,
    )

    page.services.append(onesignal)

    # Log startup info
    logger.info(f"Platform: {page.platform}")
    logger.info(f"OneSignal App ID: {ONESIGNAL_APP_ID}")

    # -------------------------------------------------------------------------
    # Build Navigation Drawer
    # -------------------------------------------------------------------------

    def create_nav_handler(page_id):
        """Create an async handler for navigation items."""

        async def handler(e):
            app_state.current_page = page_id
            await page.close_drawer()
            update_content()

        return handler

    def build_drawer_items():
        """Build navigation drawer items."""
        items = []
        for group in NAVIGATION_GROUPS:
            # Group header
            items.append(
                ft.Container(
                    content=ft.Text(
                        group["title"],
                        size=12,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.GREY_600,
                    ),
                    padding=ft.Padding.only(left=16, top=16, bottom=4),
                )
            )
            # Group items
            for item in group["items"]:
                is_selected = app_state.current_page == item["id"]
                items.append(
                    ft.ListTile(
                        leading=ft.Icon(
                            item["icon"],
                            color=ft.Colors.BLUE_700 if is_selected else ft.Colors.GREY_700,
                        ),
                        title=ft.Text(
                            item["label"],
                            weight=ft.FontWeight.W_500 if is_selected else ft.FontWeight.NORMAL,
                            color=ft.Colors.BLUE_700 if is_selected else None,
                        ),
                        selected=is_selected,
                        on_click=create_nav_handler(item["id"]),
                    )
                )

        # Footer
        items.append(ft.Divider())
        items.append(
            ft.Container(
                content=ft.TextButton(
                    "github.com/brunobrown/flet-onesignal",
                    icon=ft.Icons.OPEN_IN_NEW,
                    url="https://github.com/brunobrown/flet-onesignal",
                ),
                padding=16,
            )
        )
        return items

    drawer = ft.NavigationDrawer(
        controls=build_drawer_items(),
        on_dismiss=lambda e: None,
    )
    page.drawer = drawer

    # -------------------------------------------------------------------------
    # Build Page Content
    # -------------------------------------------------------------------------

    def build_log_viewer():
        """Build log viewer component."""
        log_entries = [
            ft.Text(
                f"[{log.time}] {log.message}",
                size=12,
                color=LOG_COLORS.get(log.level, ft.Colors.GREY_800),
                selectable=True,
            )
            for log in app_state.logs
        ]

        return ft.Column(
            [
                ft.Row(
                    [
                        ft.Text("Result", weight=ft.FontWeight.W_600),
                        ft.Row(
                            [
                                ft.IconButton(
                                    icon=ft.Icons.COPY,
                                    tooltip="Copy",
                                    on_click=copy_logs,
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.DELETE_OUTLINE,
                                    tooltip="Clear",
                                    on_click=lambda e: clear_logs(),
                                ),
                            ],
                            spacing=0,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Row(
                    [
                        ft.Container(
                            content=ft.Column(
                                controls=log_entries
                                if log_entries
                                else [
                                    ft.Text(
                                        "No logs yet.",
                                        size=12,
                                        italic=True,
                                        color=ft.Colors.GREY_500,
                                    )
                                ],
                                scroll=ft.ScrollMode.AUTO,
                                auto_scroll=True,
                                spacing=4,
                            ),
                            border=ft.Border.all(1, ft.Colors.GREY_300),
                            border_radius=8,
                            padding=12,
                            height=200,
                            bgcolor=ft.Colors.GREY_50,
                            clip_behavior=ft.ClipBehavior.HARD_EDGE,
                            expand=True,
                        ),
                    ],
                    expand=True,
                ),
            ],
        )

    # Clipboard service
    clipboard = ft.Clipboard()
    page.services.append(clipboard)

    async def copy_logs(e):
        logs_text = "\n".join(
            f"[{log.time}] [{log.level.upper()}] {log.message}" for log in app_state.logs
        )
        if logs_text:
            await clipboard.set(logs_text)
            app_state.add_log("Logs copied", "success")
            update_content()

    def clear_logs():
        app_state.clear_logs()
        update_content()

    def build_page_content():
        """Build content for the current page."""
        current = app_state.current_page

        if current == "login":
            return build_login_page()
        elif current == "consent":
            return build_consent_page()
        elif current == "user_identity":
            return build_user_identity_page()
        elif current == "user_tags":
            return build_user_tags_page()
        elif current == "user_aliases":
            return build_user_aliases_page()
        elif current == "user_email_sms":
            return build_user_email_sms_page()
        elif current == "user_language":
            return build_user_language_page()
        elif current == "user_push":
            return build_user_push_page()
        elif current == "notifications":
            return build_notifications_page()
        elif current == "in_app_messages":
            return build_in_app_messages_page()
        elif current == "location":
            return build_location_page()
        elif current == "session":
            return build_session_page()
        elif current == "live_activities":
            return build_live_activities_page()
        elif current == "debug":
            return build_debug_page()
        elif current == "event_logs":
            return build_event_logs_page()
        else:
            return build_login_page()

    # -------------------------------------------------------------------------
    # Page Builders
    # -------------------------------------------------------------------------

    # Shared state for text fields
    field_values = {
        "external_id": "",
        "tag_key": "",
        "tag_value": "",
        "alias_label": "",
        "alias_id": "",
        "email": "",
        "phone": "",
        "language": "en",
        "notification_id": "",
        "trigger_key": "",
        "trigger_value": "",
        "outcome_name": "",
        "outcome_value": "",
        "activity_id": "",
        "activity_token": "",
        "log_level": "debug",
        "alert_level": "none",
    }

    def build_login_page():
        external_id_field = ft.TextField(
            label="External ID",
            hint_text="Ex: user-123",
            value=field_values["external_id"],
            on_change=lambda e: field_values.update({"external_id": e.control.value}),
        )

        async def handle_login(e):
            if not field_values["external_id"]:
                app_state.add_log("Please enter an External ID", "warning")
                update_content()
                return
            try:
                await onesignal.login(field_values["external_id"])
                app_state.add_log(f"Login successful: {field_values['external_id']}", "success")
            except Exception as ex:
                app_state.add_log(f"Login error: {ex}", "error")
            update_content()

        async def handle_logout(e):
            try:
                await onesignal.logout()
                field_values["external_id"] = ""
                app_state.add_log("Logout successful", "success")
            except Exception as ex:
                app_state.add_log(f"Logout error: {ex}", "error")
            update_content()

        return ft.Column(
            [
                ft.Text("Login / Logout", size=24, weight=ft.FontWeight.BOLD),
                ft.Text(
                    "Associate the device with a user identified by External ID.",
                    size=14,
                    color=ft.Colors.GREY_700,
                ),
                ft.TextButton(
                    "Documentation: Users",
                    icon=ft.Icons.OPEN_IN_NEW,
                    url="https://documentation.onesignal.com/docs/users",
                ),
                ft.Divider(height=20),
                external_id_field,
                ft.Row(
                    [
                        ft.FilledButton("Login", icon=ft.Icons.LOGIN, on_click=handle_login),
                        ft.OutlinedButton("Logout", icon=ft.Icons.LOGOUT, on_click=handle_logout),
                    ],
                    spacing=10,
                ),
                ft.Divider(height=20),
                build_log_viewer(),
            ],
            spacing=12,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )

    def build_consent_page():
        async def handle_give_consent(e):
            try:
                await onesignal.consent_given(True)
                app_state.add_log("Consent granted", "success")
            except Exception as ex:
                app_state.add_log(f"Error: {ex}", "error")
            update_content()

        async def handle_revoke_consent(e):
            try:
                await onesignal.consent_given(False)
                app_state.add_log("Consent revoked", "success")
            except Exception as ex:
                app_state.add_log(f"Error: {ex}", "error")
            update_content()

        return ft.Column(
            [
                ft.Text("Consent (GDPR)", size=24, weight=ft.FontWeight.BOLD),
                ft.Text(
                    "Manage user consent for data collection.", size=14, color=ft.Colors.GREY_700
                ),
                ft.TextButton(
                    "Documentation: Privacy & Data Handling",
                    icon=ft.Icons.OPEN_IN_NEW,
                    url="https://documentation.onesignal.com/docs/handling-personal-data",
                ),
                ft.Divider(height=20),
                ft.Row(
                    [
                        ft.FilledButton(
                            "Give Consent", icon=ft.Icons.CHECK_CIRCLE, on_click=handle_give_consent
                        ),
                        ft.OutlinedButton(
                            "Revoke", icon=ft.Icons.CANCEL, on_click=handle_revoke_consent
                        ),
                    ],
                    spacing=10,
                ),
                ft.Divider(height=20),
                build_log_viewer(),
            ],
            spacing=12,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )

    def build_user_identity_page():
        async def handle_get_onesignal_id(e):
            try:
                result = await onesignal.user.get_onesignal_id()
                app_state.add_log(f"OneSignal ID: {result}", "success")
            except Exception as ex:
                app_state.add_log(f"Error: {ex}", "error")
            update_content()

        async def handle_get_external_id(e):
            try:
                result = await onesignal.user.get_external_id()
                app_state.add_log(f"External ID: {result}", "success")
            except Exception as ex:
                app_state.add_log(f"Error: {ex}", "error")
            update_content()

        return ft.Column(
            [
                ft.Text("User - Identity", size=24, weight=ft.FontWeight.BOLD),
                ft.Text("Get the user's IDs.", size=14, color=ft.Colors.GREY_700),
                ft.TextButton(
                    "Documentation: Users",
                    icon=ft.Icons.OPEN_IN_NEW,
                    url="https://documentation.onesignal.com/docs/users",
                ),
                ft.Divider(height=20),
                ft.Row(
                    [
                        ft.FilledButton("Get OneSignal ID", on_click=handle_get_onesignal_id),
                        ft.FilledButton("Get External ID", on_click=handle_get_external_id),
                    ],
                    spacing=10,
                    wrap=True,
                ),
                ft.Divider(height=20),
                build_log_viewer(),
            ],
            spacing=12,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )

    def build_user_tags_page():
        async def handle_add_tag(e):
            if not field_values["tag_key"] or not field_values["tag_value"]:
                app_state.add_log("Enter key and value", "warning")
                update_content()
                return
            try:
                await onesignal.user.add_tag(field_values["tag_key"], field_values["tag_value"])
                app_state.add_log(
                    f"Tag added: {field_values['tag_key']}={field_values['tag_value']}", "success"
                )
            except Exception as ex:
                app_state.add_log(f"Error: {ex}", "error")
            update_content()

        async def handle_remove_tag(e):
            if not field_values["tag_key"]:
                app_state.add_log("Enter the key", "warning")
                update_content()
                return
            try:
                await onesignal.user.remove_tag(field_values["tag_key"])
                app_state.add_log(f"Tag removed: {field_values['tag_key']}", "success")
            except Exception as ex:
                app_state.add_log(f"Error: {ex}", "error")
            update_content()

        async def handle_get_tags(e):
            try:
                tags = await onesignal.user.get_tags()
                app_state.add_log(f"Tags: {tags}", "success")
            except Exception as ex:
                app_state.add_log(f"Error: {ex}", "error")
            update_content()

        return ft.Column(
            [
                ft.Text("User - Tags", size=24, weight=ft.FontWeight.BOLD),
                ft.Text(
                    "Tags allow you to segment users for targeted notifications.",
                    size=14,
                    color=ft.Colors.GREY_700,
                ),
                ft.TextButton(
                    "Documentation: Data Tags",
                    icon=ft.Icons.OPEN_IN_NEW,
                    url="https://documentation.onesignal.com/docs/add-user-data-tags",
                ),
                ft.Divider(height=20),
                ft.Row(
                    [
                        ft.TextField(
                            label="Key",
                            hint_text="Ex: plan",
                            width=150,
                            value=field_values["tag_key"],
                            on_change=lambda e: field_values.update({"tag_key": e.control.value}),
                        ),
                        ft.TextField(
                            label="Value",
                            hint_text="Ex: premium",
                            width=150,
                            value=field_values["tag_value"],
                            on_change=lambda e: field_values.update({"tag_value": e.control.value}),
                        ),
                    ],
                    spacing=10,
                ),
                ft.Row(
                    [
                        ft.FilledButton("Add", icon=ft.Icons.ADD, on_click=handle_add_tag),
                        ft.OutlinedButton(
                            "Remove", icon=ft.Icons.REMOVE, on_click=handle_remove_tag
                        ),
                        ft.OutlinedButton("Get All", icon=ft.Icons.LIST, on_click=handle_get_tags),
                    ],
                    spacing=10,
                    wrap=True,
                ),
                ft.Divider(height=20),
                build_log_viewer(),
            ],
            spacing=12,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )

    def build_user_aliases_page():
        async def handle_add_alias(e):
            if not field_values["alias_label"] or not field_values["alias_id"]:
                app_state.add_log("Enter label and ID", "warning")
                update_content()
                return
            try:
                await onesignal.user.add_alias(
                    field_values["alias_label"], field_values["alias_id"]
                )
                app_state.add_log(
                    f"Alias added: {field_values['alias_label']}={field_values['alias_id']}",
                    "success",
                )
            except Exception as ex:
                app_state.add_log(f"Error: {ex}", "error")
            update_content()

        async def handle_remove_alias(e):
            if not field_values["alias_label"]:
                app_state.add_log("Enter the label", "warning")
                update_content()
                return
            try:
                await onesignal.user.remove_alias(field_values["alias_label"])
                app_state.add_log(f"Alias removed: {field_values['alias_label']}", "success")
            except Exception as ex:
                app_state.add_log(f"Error: {ex}", "error")
            update_content()

        return ft.Column(
            [
                ft.Text("User - Aliases", size=24, weight=ft.FontWeight.BOLD),
                ft.Text(
                    "Aliases are alternative identifiers for the same user.",
                    size=14,
                    color=ft.Colors.GREY_700,
                ),
                ft.TextButton(
                    "Documentation: Aliases",
                    icon=ft.Icons.OPEN_IN_NEW,
                    url="https://documentation.onesignal.com/docs/aliases",
                ),
                ft.Divider(height=20),
                ft.Row(
                    [
                        ft.TextField(
                            label="Label",
                            hint_text="Ex: crm_id",
                            width=150,
                            value=field_values["alias_label"],
                            on_change=lambda e: field_values.update(
                                {"alias_label": e.control.value}
                            ),
                        ),
                        ft.TextField(
                            label="ID",
                            hint_text="Ex: CRM-123",
                            width=150,
                            value=field_values["alias_id"],
                            on_change=lambda e: field_values.update({"alias_id": e.control.value}),
                        ),
                    ],
                    spacing=10,
                ),
                ft.Row(
                    [
                        ft.FilledButton("Add", icon=ft.Icons.ADD, on_click=handle_add_alias),
                        ft.OutlinedButton(
                            "Remove", icon=ft.Icons.REMOVE, on_click=handle_remove_alias
                        ),
                    ],
                    spacing=10,
                ),
                ft.Divider(height=20),
                build_log_viewer(),
            ],
            spacing=12,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )

    def build_user_email_sms_page():
        async def handle_add_email(e):
            if not field_values["email"]:
                app_state.add_log("Enter an email", "warning")
                update_content()
                return
            try:
                await onesignal.user.add_email(field_values["email"])
                app_state.add_log(f"Email added: {field_values['email']}", "success")
            except Exception as ex:
                app_state.add_log(f"Error: {ex}", "error")
            update_content()

        async def handle_remove_email(e):
            if not field_values["email"]:
                app_state.add_log("Enter the email", "warning")
                update_content()
                return
            try:
                await onesignal.user.remove_email(field_values["email"])
                app_state.add_log(f"Email removed: {field_values['email']}", "success")
            except Exception as ex:
                app_state.add_log(f"Error: {ex}", "error")
            update_content()

        async def handle_add_sms(e):
            if not field_values["phone"]:
                app_state.add_log("Enter a phone number", "warning")
                update_content()
                return
            try:
                await onesignal.user.add_sms(field_values["phone"])
                app_state.add_log(f"SMS added: {field_values['phone']}", "success")
            except Exception as ex:
                app_state.add_log(f"Error: {ex}", "error")
            update_content()

        async def handle_remove_sms(e):
            if not field_values["phone"]:
                app_state.add_log("Enter the phone number", "warning")
                update_content()
                return
            try:
                await onesignal.user.remove_sms(field_values["phone"])
                app_state.add_log(f"SMS removed: {field_values['phone']}", "success")
            except Exception as ex:
                app_state.add_log(f"Error: {ex}", "error")
            update_content()

        return ft.Column(
            [
                ft.Text("User - Email / SMS", size=24, weight=ft.FontWeight.BOLD),
                ft.Text(
                    "Add alternative communication channels.", size=14, color=ft.Colors.GREY_700
                ),
                ft.TextButton(
                    "Documentation: Subscriptions",
                    icon=ft.Icons.OPEN_IN_NEW,
                    url="https://documentation.onesignal.com/docs/subscriptions",
                ),
                ft.Divider(height=20),
                ft.Text("Email", weight=ft.FontWeight.W_500),
                ft.TextField(
                    label="Email",
                    hint_text="user@example.com",
                    value=field_values["email"],
                    on_change=lambda e: field_values.update({"email": e.control.value}),
                ),
                ft.Row(
                    [
                        ft.FilledButton("Add Email", on_click=handle_add_email),
                        ft.OutlinedButton("Remove Email", on_click=handle_remove_email),
                    ],
                    spacing=10,
                ),
                ft.Divider(height=10),
                ft.Text("SMS", weight=ft.FontWeight.W_500),
                ft.TextField(
                    label="Phone",
                    hint_text="+15551234567",
                    value=field_values["phone"],
                    on_change=lambda e: field_values.update({"phone": e.control.value}),
                ),
                ft.Row(
                    [
                        ft.FilledButton("Add SMS", on_click=handle_add_sms),
                        ft.OutlinedButton("Remove SMS", on_click=handle_remove_sms),
                    ],
                    spacing=10,
                ),
                ft.Divider(height=20),
                build_log_viewer(),
            ],
            spacing=12,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )

    def build_user_language_page():
        async def handle_set_language(e):
            try:
                await onesignal.user.set_language(field_values["language"])
                app_state.add_log(f"Language set: {field_values['language']}", "success")
            except Exception as ex:
                app_state.add_log(f"Error: {ex}", "error")
            update_content()

        return ft.Column(
            [
                ft.Text("User - Language", size=24, weight=ft.FontWeight.BOLD),
                ft.Text("Set the user's preferred language.", size=14, color=ft.Colors.GREY_700),
                ft.TextButton(
                    "Documentation: Mobile SDK Reference",
                    icon=ft.Icons.OPEN_IN_NEW,
                    url="https://documentation.onesignal.com/docs/mobile-sdk-reference",
                ),
                ft.Divider(height=20),
                ft.Dropdown(
                    label="Language",
                    value=field_values["language"],
                    on_select=lambda e: field_values.update({"language": e.control.value}),
                    options=[
                        ft.DropdownOption("pt", "Portuguese"),
                        ft.DropdownOption("en", "English"),
                        ft.DropdownOption("es", "Spanish"),
                    ],
                    width=200,
                ),
                ft.FilledButton(
                    "Set Language", icon=ft.Icons.LANGUAGE, on_click=handle_set_language
                ),
                ft.Divider(height=20),
                build_log_viewer(),
            ],
            spacing=12,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )

    def build_user_push_page():
        async def handle_opt_in(e):
            try:
                await onesignal.user.opt_in_push()
                app_state.add_log("Opt-in successful", "success")
            except Exception as ex:
                app_state.add_log(f"Error: {ex}", "error")
            update_content()

        async def handle_opt_out(e):
            try:
                await onesignal.user.opt_out_push()
                app_state.add_log("Opt-out successful", "success")
            except Exception as ex:
                app_state.add_log(f"Error: {ex}", "error")
            update_content()

        async def handle_is_opted_in(e):
            try:
                result = await onesignal.user.is_push_opted_in()
                app_state.add_log(f"Opted in: {result}", "success")
            except Exception as ex:
                app_state.add_log(f"Error: {ex}", "error")
            update_content()

        async def handle_get_id(e):
            try:
                result = await onesignal.user.get_push_subscription_id()
                app_state.add_log(f"Push ID: {result}", "success")
            except Exception as ex:
                app_state.add_log(f"Error: {ex}", "error")
            update_content()

        async def handle_get_token(e):
            try:
                result = await onesignal.user.get_push_subscription_token()
                app_state.add_log(f"Push Token: {result}", "success")
            except Exception as ex:
                app_state.add_log(f"Error: {ex}", "error")
            update_content()

        return ft.Column(
            [
                ft.Text("User - Push Subscription", size=24, weight=ft.FontWeight.BOLD),
                ft.Text(
                    "Control the user's push notification subscription.",
                    size=14,
                    color=ft.Colors.GREY_700,
                ),
                ft.TextButton(
                    "Documentation: Subscriptions",
                    icon=ft.Icons.OPEN_IN_NEW,
                    url="https://documentation.onesignal.com/docs/subscriptions",
                ),
                ft.Divider(height=20),
                ft.Row(
                    [
                        ft.FilledButton(
                            "Opt-In", icon=ft.Icons.NOTIFICATIONS_ACTIVE, on_click=handle_opt_in
                        ),
                        ft.OutlinedButton(
                            "Opt-Out", icon=ft.Icons.NOTIFICATIONS_OFF, on_click=handle_opt_out
                        ),
                    ],
                    spacing=10,
                ),
                ft.Divider(height=10),
                ft.Row(
                    [
                        ft.OutlinedButton("Check Opt-In", on_click=handle_is_opted_in),
                        ft.OutlinedButton("Get ID", on_click=handle_get_id),
                        ft.OutlinedButton("Get Token", on_click=handle_get_token),
                    ],
                    spacing=10,
                    wrap=True,
                ),
                ft.Divider(height=20),
                build_log_viewer(),
            ],
            spacing=12,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )

    def build_notifications_page():
        async def handle_request_permission(e):
            try:
                result = await onesignal.notifications.request_permission()
                app_state.add_log(f"Permission: {result}", "success")
            except Exception as ex:
                app_state.add_log(f"Error: {ex}", "error")
            update_content()

        async def handle_get_permission(e):
            try:
                result = await onesignal.notifications.get_permission()
                app_state.add_log(f"Status: {result}", "success")
            except Exception as ex:
                app_state.add_log(f"Error: {ex}", "error")
            update_content()

        async def handle_can_request(e):
            try:
                result = await onesignal.notifications.can_request_permission()
                app_state.add_log(f"Can request: {result}", "success")
            except Exception as ex:
                app_state.add_log(f"Error: {ex}", "error")
            update_content()

        async def handle_clear_all(e):
            try:
                await onesignal.notifications.clear_all()
                app_state.add_log("Notifications cleared", "success")
            except Exception as ex:
                app_state.add_log(f"Error: {ex}", "error")
            update_content()

        async def handle_remove(e):
            if not field_values["notification_id"]:
                app_state.add_log("Enter the ID", "warning")
                update_content()
                return
            try:
                await onesignal.notifications.remove_notification(
                    int(field_values["notification_id"])
                )
                app_state.add_log(
                    f"Notification removed: {field_values['notification_id']}", "success"
                )
            except Exception as ex:
                app_state.add_log(f"Error: {ex}", "error")
            update_content()

        return ft.Column(
            [
                ft.Text("Notifications", size=24, weight=ft.FontWeight.BOLD),
                ft.Text("Manage permissions and notifications.", size=14, color=ft.Colors.GREY_700),
                ft.TextButton(
                    "Documentation: Push Permissions",
                    icon=ft.Icons.OPEN_IN_NEW,
                    url="https://documentation.onesignal.com/docs/prompt-for-push-permissions",
                ),
                ft.Divider(height=20),
                ft.Text("Permission", weight=ft.FontWeight.W_500),
                ft.Row(
                    [
                        ft.FilledButton(
                            "Request Permission",
                            icon=ft.Icons.NOTIFICATIONS,
                            on_click=handle_request_permission,
                        ),
                        ft.OutlinedButton("Check Status", on_click=handle_get_permission),
                        ft.OutlinedButton("Can Request?", on_click=handle_can_request),
                    ],
                    spacing=10,
                    wrap=True,
                ),
                ft.Divider(height=10),
                ft.Text("Management", weight=ft.FontWeight.W_500),
                ft.FilledButton("Clear All", icon=ft.Icons.CLEAR_ALL, on_click=handle_clear_all),
                ft.Row(
                    [
                        ft.TextField(
                            label="Notification ID",
                            hint_text="123",
                            width=150,
                            value=field_values["notification_id"],
                            on_change=lambda e: field_values.update(
                                {"notification_id": e.control.value}
                            ),
                        ),
                        ft.OutlinedButton("Remove", on_click=handle_remove),
                    ],
                    spacing=10,
                ),
                ft.Divider(height=20),
                build_log_viewer(),
            ],
            spacing=12,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )

    def build_in_app_messages_page():
        async def handle_add_trigger(e):
            if not field_values["trigger_key"] or not field_values["trigger_value"]:
                app_state.add_log("Enter key and value", "warning")
                update_content()
                return
            try:
                await onesignal.in_app_messages.add_trigger(
                    field_values["trigger_key"], field_values["trigger_value"]
                )
                app_state.add_log(
                    f"Trigger added: {field_values['trigger_key']}={field_values['trigger_value']}",
                    "success",
                )
            except Exception as ex:
                app_state.add_log(f"Error: {ex}", "error")
            update_content()

        async def handle_remove_trigger(e):
            if not field_values["trigger_key"]:
                app_state.add_log("Enter the key", "warning")
                update_content()
                return
            try:
                await onesignal.in_app_messages.remove_trigger(field_values["trigger_key"])
                app_state.add_log(f"Trigger removed: {field_values['trigger_key']}", "success")
            except Exception as ex:
                app_state.add_log(f"Error: {ex}", "error")
            update_content()

        async def handle_clear_triggers(e):
            try:
                await onesignal.in_app_messages.clear_triggers()
                app_state.add_log("Triggers cleared", "success")
            except Exception as ex:
                app_state.add_log(f"Error: {ex}", "error")
            update_content()

        async def handle_pause(e):
            try:
                await onesignal.in_app_messages.pause()
                app_state.add_log("IAM paused", "success")
            except Exception as ex:
                app_state.add_log(f"Error: {ex}", "error")
            update_content()

        async def handle_resume(e):
            try:
                await onesignal.in_app_messages.resume()
                app_state.add_log("IAM resumed", "success")
            except Exception as ex:
                app_state.add_log(f"Error: {ex}", "error")
            update_content()

        async def handle_is_paused(e):
            try:
                result = await onesignal.in_app_messages.is_paused()
                app_state.add_log(f"Paused: {result}", "success")
            except Exception as ex:
                app_state.add_log(f"Error: {ex}", "error")
            update_content()

        return ft.Column(
            [
                ft.Text("In-App Messages", size=24, weight=ft.FontWeight.BOLD),
                ft.Text(
                    "Control triggers and in-app message display.",
                    size=14,
                    color=ft.Colors.GREY_700,
                ),
                ft.TextButton(
                    "Documentation: In-App Messages & Triggers",
                    icon=ft.Icons.OPEN_IN_NEW,
                    url="https://documentation.onesignal.com/docs/iam-triggers",
                ),
                ft.Divider(height=20),
                ft.Text("Triggers", weight=ft.FontWeight.W_500),
                ft.Row(
                    [
                        ft.TextField(
                            label="Key",
                            hint_text="show_promo",
                            width=150,
                            value=field_values["trigger_key"],
                            on_change=lambda e: field_values.update(
                                {"trigger_key": e.control.value}
                            ),
                        ),
                        ft.TextField(
                            label="Value",
                            hint_text="true",
                            width=150,
                            value=field_values["trigger_value"],
                            on_change=lambda e: field_values.update(
                                {"trigger_value": e.control.value}
                            ),
                        ),
                    ],
                    spacing=10,
                ),
                ft.Row(
                    [
                        ft.FilledButton("Add", icon=ft.Icons.ADD, on_click=handle_add_trigger),
                        ft.OutlinedButton(
                            "Remove", icon=ft.Icons.REMOVE, on_click=handle_remove_trigger
                        ),
                        ft.OutlinedButton("Clear All", on_click=handle_clear_triggers),
                    ],
                    spacing=10,
                    wrap=True,
                ),
                ft.Divider(height=10),
                ft.Text("Control", weight=ft.FontWeight.W_500),
                ft.Row(
                    [
                        ft.FilledButton("Pause", icon=ft.Icons.PAUSE, on_click=handle_pause),
                        ft.FilledButton("Resume", icon=ft.Icons.PLAY_ARROW, on_click=handle_resume),
                        ft.OutlinedButton("Check Status", on_click=handle_is_paused),
                    ],
                    spacing=10,
                    wrap=True,
                ),
                ft.Divider(height=20),
                build_log_viewer(),
            ],
            spacing=12,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )

    def build_location_page():
        async def handle_request_permission(e):
            try:
                result = await onesignal.location.request_permission()
                app_state.add_log(f"Location permission: {result}", "success")
            except Exception as ex:
                app_state.add_log(f"Error: {ex}", "error")
            update_content()

        async def handle_enable(e):
            try:
                await onesignal.location.set_shared(True)
                app_state.add_log("Sharing enabled", "success")
            except Exception as ex:
                app_state.add_log(f"Error: {ex}", "error")
            update_content()

        async def handle_disable(e):
            try:
                await onesignal.location.set_shared(False)
                app_state.add_log("Sharing disabled", "success")
            except Exception as ex:
                app_state.add_log(f"Error: {ex}", "error")
            update_content()

        async def handle_is_shared(e):
            try:
                result = await onesignal.location.is_shared()
                app_state.add_log(f"Sharing: {result}", "success")
            except Exception as ex:
                app_state.add_log(f"Error: {ex}", "error")
            update_content()

        return ft.Column(
            [
                ft.Text("Location", size=24, weight=ft.FontWeight.BOLD),
                ft.Text("Control location sharing.", size=14, color=ft.Colors.GREY_700),
                ft.TextButton(
                    "Documentation: Location Permissions",
                    icon=ft.Icons.OPEN_IN_NEW,
                    url="https://documentation.onesignal.com/docs/location-opt-in-prompt",
                ),
                ft.Divider(height=20),
                ft.FilledButton(
                    "Request Permission",
                    icon=ft.Icons.LOCATION_SEARCHING,
                    on_click=handle_request_permission,
                ),
                ft.Divider(height=10),
                ft.Row(
                    [
                        ft.FilledButton(
                            "Enable", icon=ft.Icons.LOCATION_ON, on_click=handle_enable
                        ),
                        ft.OutlinedButton(
                            "Disable", icon=ft.Icons.LOCATION_OFF, on_click=handle_disable
                        ),
                        ft.OutlinedButton("Check Status", on_click=handle_is_shared),
                    ],
                    spacing=10,
                    wrap=True,
                ),
                ft.Divider(height=20),
                build_log_viewer(),
            ],
            spacing=12,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )

    def build_session_page():
        async def handle_add_outcome(e):
            if not field_values["outcome_name"]:
                app_state.add_log("Enter the name", "warning")
                update_content()
                return
            try:
                await onesignal.session.add_outcome(field_values["outcome_name"])
                app_state.add_log(f"Outcome added: {field_values['outcome_name']}", "success")
            except Exception as ex:
                app_state.add_log(f"Error: {ex}", "error")
            update_content()

        async def handle_add_unique(e):
            if not field_values["outcome_name"]:
                app_state.add_log("Enter the name", "warning")
                update_content()
                return
            try:
                await onesignal.session.add_unique_outcome(field_values["outcome_name"])
                app_state.add_log(f"Unique outcome: {field_values['outcome_name']}", "success")
            except Exception as ex:
                app_state.add_log(f"Error: {ex}", "error")
            update_content()

        async def handle_add_with_value(e):
            if not field_values["outcome_name"] or not field_values["outcome_value"]:
                app_state.add_log("Enter name and value", "warning")
                update_content()
                return
            try:
                value = float(field_values["outcome_value"])
                await onesignal.session.add_outcome_with_value(field_values["outcome_name"], value)
                app_state.add_log(
                    f"Outcome with value: {field_values['outcome_name']}={value}", "success"
                )
            except Exception as ex:
                app_state.add_log(f"Error: {ex}", "error")
            update_content()

        return ft.Column(
            [
                ft.Text("Session - Outcomes", size=24, weight=ft.FontWeight.BOLD),
                ft.Text("Track user conversions and actions.", size=14, color=ft.Colors.GREY_700),
                ft.TextButton(
                    "Documentation: Outcomes",
                    icon=ft.Icons.OPEN_IN_NEW,
                    url="https://documentation.onesignal.com/docs/outcomes",
                ),
                ft.Divider(height=20),
                ft.TextField(
                    label="Outcome Name",
                    hint_text="purchase",
                    value=field_values["outcome_name"],
                    on_change=lambda e: field_values.update({"outcome_name": e.control.value}),
                ),
                ft.Row(
                    [
                        ft.FilledButton("Add", on_click=handle_add_outcome),
                        ft.OutlinedButton("Unique", on_click=handle_add_unique),
                    ],
                    spacing=10,
                ),
                ft.Divider(height=10),
                ft.Row(
                    [
                        ft.TextField(
                            label="Value",
                            hint_text="29.99",
                            width=150,
                            value=field_values["outcome_value"],
                            on_change=lambda e: field_values.update(
                                {"outcome_value": e.control.value}
                            ),
                        ),
                        ft.FilledButton("With Value", on_click=handle_add_with_value),
                    ],
                    spacing=10,
                ),
                ft.Divider(height=20),
                build_log_viewer(),
            ],
            spacing=12,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )

    def build_live_activities_page():
        async def handle_setup(e):
            try:
                await onesignal.live_activities.setup_default()
                app_state.add_log("Live Activities configured", "success")
            except Exception as ex:
                app_state.add_log(f"Error: {ex}", "error")
            update_content()

        async def handle_enter(e):
            if not field_values["activity_id"] or not field_values["activity_token"]:
                app_state.add_log("Enter ID and Token", "warning")
                update_content()
                return
            try:
                await onesignal.live_activities.enter(
                    field_values["activity_id"], field_values["activity_token"]
                )
                app_state.add_log(f"Entered: {field_values['activity_id']}", "success")
            except Exception as ex:
                app_state.add_log(f"Error: {ex}", "error")
            update_content()

        async def handle_exit(e):
            if not field_values["activity_id"]:
                app_state.add_log("Enter the ID", "warning")
                update_content()
                return
            try:
                await onesignal.live_activities.exit(field_values["activity_id"])
                app_state.add_log(f"Exited: {field_values['activity_id']}", "success")
            except Exception as ex:
                app_state.add_log(f"Error: {ex}", "error")
            update_content()

        return ft.Column(
            [
                ft.Text("Live Activities (iOS)", size=24, weight=ft.FontWeight.BOLD),
                ft.Text(
                    "Manage iOS Live Activities (iOS 16.1+).", size=14, color=ft.Colors.GREY_700
                ),
                ft.TextButton(
                    "Documentation: Live Activities",
                    icon=ft.Icons.OPEN_IN_NEW,
                    url="https://documentation.onesignal.com/docs/live-activities",
                ),
                ft.Divider(height=20),
                ft.FilledButton("Setup Default", icon=ft.Icons.SETTINGS, on_click=handle_setup),
                ft.Divider(height=10),
                ft.TextField(
                    label="Activity ID",
                    hint_text="delivery-123",
                    value=field_values["activity_id"],
                    on_change=lambda e: field_values.update({"activity_id": e.control.value}),
                ),
                ft.TextField(
                    label="Token",
                    value=field_values["activity_token"],
                    on_change=lambda e: field_values.update({"activity_token": e.control.value}),
                ),
                ft.Row(
                    [
                        ft.FilledButton("Enter", on_click=handle_enter),
                        ft.OutlinedButton("Exit", on_click=handle_exit),
                    ],
                    spacing=10,
                ),
                ft.Divider(height=20),
                build_log_viewer(),
            ],
            spacing=12,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )

    def build_debug_page():
        def get_level(level_str):
            levels = {
                "none": fos.OSLogLevel.NONE,
                "error": fos.OSLogLevel.ERROR,
                "warn": fos.OSLogLevel.WARN,
                "info": fos.OSLogLevel.INFO,
                "debug": fos.OSLogLevel.DEBUG,
                "verbose": fos.OSLogLevel.VERBOSE,
            }
            return levels.get(level_str, fos.OSLogLevel.DEBUG)

        async def handle_set_log_level(e):
            try:
                await onesignal.debug.set_log_level(get_level(field_values["log_level"]))
                app_state.add_log(f"Log level: {field_values['log_level']}", "success")
            except Exception as ex:
                app_state.add_log(f"Error: {ex}", "error")
            update_content()

        async def handle_set_alert_level(e):
            try:
                await onesignal.debug.set_alert_level(get_level(field_values["alert_level"]))
                app_state.add_log(f"Alert level: {field_values['alert_level']}", "success")
            except Exception as ex:
                app_state.add_log(f"Error: {ex}", "error")
            update_content()

        return ft.Column(
            [
                ft.Text("Debug", size=24, weight=ft.FontWeight.BOLD),
                ft.Text("Configure SDK log levels.", size=14, color=ft.Colors.GREY_700),
                ft.TextButton(
                    "Documentation: Mobile SDK Reference",
                    icon=ft.Icons.OPEN_IN_NEW,
                    url="https://documentation.onesignal.com/docs/mobile-sdk-reference",
                ),
                ft.Divider(height=20),
                ft.Dropdown(
                    label="Log Level",
                    value=field_values["log_level"],
                    on_select=lambda e: field_values.update({"log_level": e.control.value}),
                    options=[
                        ft.DropdownOption("none", "None"),
                        ft.DropdownOption("error", "Error"),
                        ft.DropdownOption("warn", "Warn"),
                        ft.DropdownOption("info", "Info"),
                        ft.DropdownOption("debug", "Debug"),
                        ft.DropdownOption("verbose", "Verbose"),
                    ],
                    width=200,
                ),
                ft.FilledButton("Apply Log Level", on_click=handle_set_log_level),
                ft.Divider(height=10),
                ft.Dropdown(
                    label="Alert Level",
                    value=field_values["alert_level"],
                    on_select=lambda e: field_values.update({"alert_level": e.control.value}),
                    options=[
                        ft.DropdownOption("none", "None"),
                        ft.DropdownOption("error", "Error"),
                        ft.DropdownOption("warn", "Warn"),
                        ft.DropdownOption("info", "Info"),
                    ],
                    width=200,
                ),
                ft.FilledButton("Apply Alert Level", on_click=handle_set_alert_level),
                ft.Divider(height=20),
                build_log_viewer(),
            ],
            spacing=12,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )

    def build_event_logs_page():
        log_entries = [
            ft.Container(
                content=ft.Row(
                    [
                        ft.Text(f"[{log.time}]", size=11, color=ft.Colors.GREY_600),
                        ft.Text(
                            log.message,
                            size=12,
                            color=LOG_COLORS.get(log.level, ft.Colors.GREY_800),
                            selectable=True,
                            expand=True,
                        ),
                    ],
                    spacing=8,
                ),
                padding=ft.Padding.symmetric(vertical=4),
            )
            for log in app_state.logs
        ]

        return ft.Column(
            [
                ft.Row(
                    [
                        ft.Text("Event Logs", size=24, weight=ft.FontWeight.BOLD),
                        ft.Row(
                            [
                                ft.IconButton(
                                    icon=ft.Icons.COPY, tooltip="Copy", on_click=copy_logs
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.DELETE_OUTLINE,
                                    tooltip="Clear",
                                    on_click=lambda e: clear_logs(),
                                ),
                            ],
                            spacing=0,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Row(
                    [
                        ft.Text(
                            "View all OneSignal events in real-time.",
                            size=14,
                            color=ft.Colors.GREY_700,
                        ),
                        ft.TextButton(
                            "SDK Reference",
                            icon=ft.Icons.OPEN_IN_NEW,
                            url="https://documentation.onesignal.com/docs/mobile-sdk-reference",
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Divider(height=20),
                ft.Container(
                    content=ft.Column(
                        controls=log_entries
                        if log_entries
                        else [
                            ft.Container(
                                content=ft.Column(
                                    [
                                        ft.Icon(ft.Icons.INBOX, size=48, color=ft.Colors.GREY_400),
                                        ft.Text("No events yet.", color=ft.Colors.GREY_500),
                                    ],
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                                alignment=ft.Alignment.CENTER,
                                padding=40,
                            )
                        ],
                        scroll=ft.ScrollMode.AUTO,
                        auto_scroll=True,
                    ),
                    border=ft.Border.all(1, ft.Colors.GREY_300),
                    border_radius=8,
                    bgcolor=ft.Colors.GREY_50,
                    expand=True,
                    padding=12,
                ),
                ft.Text(f"Total: {len(app_state.logs)} events", size=12, color=ft.Colors.GREY_600),
            ],
            spacing=12,
            expand=True,
        )

    # -------------------------------------------------------------------------
    # Main content container (will be updated on navigation)
    # -------------------------------------------------------------------------

    content_container = ft.Container(
        content=build_page_content(),
        expand=True,
        padding=20,
    )

    def update_content():
        """Update the main content and drawer."""
        content_container.content = build_page_content()
        drawer.controls = build_drawer_items()
        page.update()

    # -------------------------------------------------------------------------
    # Build the UI
    # -------------------------------------------------------------------------

    async def show_drawer_click(e):
        await page.show_drawer()

    page.appbar = ft.AppBar(
        leading=ft.IconButton(
            icon=ft.Icons.MENU,
            on_click=show_drawer_click,
        ),
        title=ft.Text("Flet OneSignal"),
        bgcolor=ft.Colors.BLUE_700,
        color=ft.Colors.WHITE,
        actions=[
            ft.IconButton(
                icon=ft.Icons.BUG_REPORT,
                on_click=lambda e: (
                    setattr(app_state, "current_page", "event_logs"),
                    update_content(),
                ),
                tooltip="Event Logs",
            ),
        ],
    )

    page.add(content_container)

    # Initial log
    app_state.add_log("OneSignal initialized. Ready to test!", "success")
    update_content()


if __name__ == "__main__":
    ft.run(main)
