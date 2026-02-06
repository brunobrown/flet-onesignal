"""
Page components for the OneSignal example app.
"""

from pages.consent import ConsentPage
from pages.debug import DebugPage
from pages.event_logs import EventLogsPage
from pages.in_app_messages import InAppMessagesPage
from pages.live_activities import LiveActivitiesPage
from pages.location import LocationPage
from pages.login import LoginPage
from pages.notifications import NotificationsPage
from pages.session import SessionPage
from pages.user_aliases import UserAliasesPage
from pages.user_email_sms import UserEmailSmsPage
from pages.user_identity import UserIdentityPage
from pages.user_language import UserLanguagePage
from pages.user_push import UserPushPage
from pages.user_tags import UserTagsPage

__all__ = [
    "LoginPage",
    "ConsentPage",
    "UserIdentityPage",
    "UserTagsPage",
    "UserAliasesPage",
    "UserEmailSmsPage",
    "UserLanguagePage",
    "UserPushPage",
    "NotificationsPage",
    "InAppMessagesPage",
    "LocationPage",
    "SessionPage",
    "LiveActivitiesPage",
    "DebugPage",
    "EventLogsPage",
]

# Page routing map
PAGE_MAP = {
    "login": LoginPage,
    "consent": ConsentPage,
    "user_identity": UserIdentityPage,
    "user_tags": UserTagsPage,
    "user_aliases": UserAliasesPage,
    "user_email_sms": UserEmailSmsPage,
    "user_language": UserLanguagePage,
    "user_push": UserPushPage,
    "notifications": NotificationsPage,
    "in_app_messages": InAppMessagesPage,
    "location": LocationPage,
    "session": SessionPage,
    "live_activities": LiveActivitiesPage,
    "debug": DebugPage,
    "event_logs": EventLogsPage,
}
