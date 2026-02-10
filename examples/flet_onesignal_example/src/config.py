"""Application constants and configuration."""

import flet as ft

# Replace with your actual OneSignal App ID
ONESIGNAL_APP_ID = "example-123a-12a3-1a23-abcd1ef23g45"

# Navigation structure for the drawer
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

# Log level colors
LOG_COLORS = {
    "info": ft.Colors.GREY_800,
    "success": ft.Colors.GREEN_700,
    "warning": ft.Colors.ORANGE_700,
    "error": ft.Colors.RED_700,
    "debug": ft.Colors.BLUE_700,
}
