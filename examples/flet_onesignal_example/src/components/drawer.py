"""
Navigation drawer component with grouped menu items.
"""

import flet as ft
from context import AppCtx

# Navigation structure with groups
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
            {"id": "live_activities", "label": "Live Activities (iOS)", "icon": ft.Icons.LIVE_TV},
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


@ft.component
def AppDrawer():
    """
    Navigation drawer with grouped menu items.
    """
    ctx = ft.use_context(AppCtx)
    state = ctx.state

    def on_item_click(page_id: str):
        def handler(e):
            state.navigate(page_id)

        return handler

    def build_group(group: dict):
        """Build a navigation group with title and items."""
        items = []

        # Group title
        items.append(
            ft.Container(
                content=ft.Text(
                    group["title"],
                    size=12,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.GREY_600,
                ),
                padding=ft.padding.only(left=16, top=16, bottom=4),
            )
        )

        # Group items
        for item in group["items"]:
            is_selected = state.current_page == item["id"]
            items.append(
                ft.ListTile(
                    leading=ft.Icon(
                        item["icon"],
                        color=ft.Colors.PRIMARY if is_selected else ft.Colors.GREY_700,
                    ),
                    title=ft.Text(
                        item["label"],
                        weight=ft.FontWeight.W_500 if is_selected else ft.FontWeight.NORMAL,
                        color=ft.Colors.PRIMARY if is_selected else None,
                    ),
                    selected=is_selected,
                    on_click=on_item_click(item["id"]),
                    content_padding=ft.padding.only(left=16),
                )
            )

        return items

    # Build all groups
    drawer_items = []
    for group in NAVIGATION_GROUPS:
        drawer_items.extend(build_group(group))

    # Add footer with GitHub link
    drawer_items.append(ft.Divider())
    drawer_items.append(
        ft.Container(
            content=ft.TextButton(
                "github.com/brunobrown/flet-onesignal",
                icon=ft.Icons.OPEN_IN_NEW,
                url="https://github.com/brunobrown/flet-onesignal",
            ),
            padding=ft.padding.all(16),
        )
    )

    return ft.Container(
        content=ft.Column(
            controls=drawer_items,
            scroll=ft.ScrollMode.AUTO,
            spacing=0,
        ),
        width=280,
        bgcolor=ft.Colors.SURFACE,
    )
