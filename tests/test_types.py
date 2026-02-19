"""Tests for flet_onesignal.types — enums, dataclasses, and computed properties."""

from flet_onesignal.types import (
    OSErrorEvent,
    OSInAppMessageClickEvent,
    OSInAppMessageClickResult,
    OSLogLevel,
    OSNotificationClickEvent,
    OSPermissionChangeEvent,
    OSPushSubscriptionChangedEvent,
    OSUserChangedEvent,
    OSUserState,
)

# ft.Event requires positional args: name, control
_EVT = {"name": "test", "control": None}


# ---------------------------------------------------------------------------
# OSLogLevel enum
# ---------------------------------------------------------------------------


class TestOSLogLevel:
    def test_all_values(self):
        expected = {
            "NONE": "none",
            "FATAL": "fatal",
            "ERROR": "error",
            "WARN": "warn",
            "INFO": "info",
            "DEBUG": "debug",
            "VERBOSE": "verbose",
        }
        for name, value in expected.items():
            assert OSLogLevel[name].value == value

    def test_count(self):
        assert len(OSLogLevel) == 7


# ---------------------------------------------------------------------------
# Event dataclass instantiation and defaults
# ---------------------------------------------------------------------------


class TestEventDataclasses:
    def test_notification_click(self):
        evt = OSNotificationClickEvent(**_EVT, notification={"id": "abc"}, action_id="tap")
        assert evt.notification == {"id": "abc"}
        assert evt.action_id == "tap"

    def test_notification_click_default_action(self):
        evt = OSNotificationClickEvent(**_EVT, notification={})
        assert evt.action_id is None

    def test_permission_change(self):
        evt = OSPermissionChangeEvent(**_EVT, permission=True)
        assert evt.permission is True

    def test_permission_change_default(self):
        evt = OSPermissionChangeEvent(**_EVT)
        assert evt.permission is False

    def test_error_event(self):
        evt = OSErrorEvent(**_EVT, method="login", message="fail", stack_trace="line1")
        assert evt.method == "login"
        assert evt.message == "fail"
        assert evt.stack_trace == "line1"

    def test_push_subscription_changed(self):
        evt = OSPushSubscriptionChangedEvent(**_EVT, id="sub1", token="tok", opted_in=True)
        assert evt.opted_in is True


# ---------------------------------------------------------------------------
# Computed properties
# ---------------------------------------------------------------------------


class TestComputedProperties:
    def test_user_changed_state(self):
        evt = OSUserChangedEvent(**_EVT, onesignal_id="os123", external_id="ext456")
        state = evt.state
        assert isinstance(state, OSUserState)
        assert state.onesignal_id == "os123"
        assert state.external_id == "ext456"

    def test_in_app_message_click_result(self):
        evt = OSInAppMessageClickEvent(
            **_EVT,
            message={"id": "msg1"},
            action_id="btn",
            url="https://example.com",
            url_target="_blank",
            closing_message=True,
        )
        result = evt.result
        assert isinstance(result, OSInAppMessageClickResult)
        assert result.action_id == "btn"
        assert result.url == "https://example.com"
        assert result.url_target == "_blank"
        assert result.closing_message is True
