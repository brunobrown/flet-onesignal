"""Test runner: executes all test steps sequentially with event verification."""

import asyncio
import time

from config import (
    EVENT_POLL_INTERVAL,
    ONESIGNAL_APP_ID,
    PUSH_WAIT_TIMEOUT,
    REST_API_KEY,
    TEST_ALIAS_ID,
    TEST_ALIAS_LABEL,
    TEST_EMAIL,
    TEST_EXTERNAL_ID,
    TEST_LANGUAGE,
    TEST_SMS,
    TEST_TAG_KEY,
    TEST_TAG_VALUE,
)
from context import AppContext
from rest_api import delete_alias, send_push_notification
from state import TestState, TestStatus
from test_steps import TEST_STEPS

import flet_onesignal as fos


async def wait_for_event(state: TestState, attr_name: str, timeout: float = 15) -> object:
    """Poll a state attribute until it becomes non-None or timeout."""
    elapsed = 0.0
    while elapsed < timeout:
        value = getattr(state, attr_name)
        if value is not None:
            return value
        await asyncio.sleep(EVENT_POLL_INTERVAL)
        elapsed += EVENT_POLL_INTERVAL
    raise TimeoutError(f"Event '{attr_name}' not received within {timeout}s")


async def _wait_user_response(state: TestState) -> str:
    """Poll until the user taps Continue or Skip."""
    while True:
        if state.user_response is not None:
            response = state.user_response
            state.user_response = None
            state.waiting_for_user = False
            state.waiting_message = ""
            return response
        await asyncio.sleep(EVENT_POLL_INTERVAL)


async def run_all_tests(ctx: AppContext) -> None:
    """Execute all test steps sequentially."""
    state = ctx.state
    platform = ctx.platform

    state.is_running = True
    state.clear_logs()
    state.clear_events()
    state.add_log("Starting test run...", "info")

    data: dict = {}  # Shared data between steps
    location_warned = False

    for step_def in TEST_STEPS:
        # 1. Platform check → SKIPPED
        if step_def.platform not in ("all", platform):
            state.set_step_status(step_def.id, TestStatus.SKIPPED)
            state.add_log(f"[SKIP] {step_def.name} (platform: {platform})", "skip")
            await asyncio.sleep(0.05)
            continue

        # 2. Location group warning (non-blocking dialog)
        if step_def.group == "Location" and not location_warned:
            location_warned = True
            state.add_log(
                "[WARN] Location requires 'fos-build'. "
                "If built with 'flet build', location will silently fail.",
                "warn",
            )
            state.warning_title = "Location Module Required"
            state.warning_message = (
                "Location features require the OneSignal location module, "
                "which is only injected when building with the 'fos-build' command.\n\n"
                "If you built this app with 'flet build apk', location tests will "
                "pass but location data will NOT be collected.\n\n"
                "Build with: fos-build apk"
            )
            state.warning_url = "https://brunobrown.github.io/flet-onesignal/guide/location/"
            state.show_warning_dialog = True

        # 3. User interaction → banner + wait
        if step_def.needs_user_interaction:
            state.waiting_for_user = True
            state.waiting_message = step_def.interaction_message
            state.user_response = None
            state.add_log(f"[WAIT] {step_def.name}: {step_def.interaction_message}", "warn")

            response = await _wait_user_response(state)
            if response == "skip":
                state.set_step_status(step_def.id, TestStatus.SKIPPED)
                state.add_log(f"[SKIP] {step_def.name} (user skipped)", "skip")
                await asyncio.sleep(0.05)
                continue

        # 3. Mark RUNNING
        state.set_step_status(step_def.id, TestStatus.RUNNING)
        state.add_log(f"[RUN ] {step_def.name}...", "debug")
        await asyncio.sleep(0.05)

        # 4. Execute
        start = time.monotonic()
        try:
            await _execute_step(step_def.id, ctx, data)
            elapsed_ms = (time.monotonic() - start) * 1000
            state.set_step_status(step_def.id, TestStatus.PASSED)
            state.add_log(f"[PASS] {step_def.name} ({elapsed_ms:.0f}ms)", "pass")
        except Exception as exc:
            elapsed_ms = (time.monotonic() - start) * 1000
            error_msg = str(exc)
            state.set_step_status(step_def.id, TestStatus.FAILED, error_msg)
            state.add_log(
                f"[FAIL] {step_def.name} ({elapsed_ms:.0f}ms): {error_msg}",
                "fail",
            )

        # 5. Brief pause for UI
        await asyncio.sleep(0.1)

    # Summary
    passed = sum(1 for s in state.steps if s.status == TestStatus.PASSED)
    failed = sum(1 for s in state.steps if s.status == TestStatus.FAILED)
    skipped = sum(1 for s in state.steps if s.status == TestStatus.SKIPPED)
    state.add_log(f"Done! Passed: {passed}, Failed: {failed}, Skipped: {skipped}", "info")
    state.is_running = False


async def _execute_step(step_id: str, ctx: AppContext, data: dict) -> None:
    """Dispatch and execute a single test step."""
    os = ctx.onesignal
    state = ctx.state

    # ── Debug ────────────────────────────────────────────────────────────
    if step_id == "debug_log_level":
        await os.debug.set_log_level(fos.OSLogLevel.DEBUG)

    elif step_id == "debug_alert_level":
        await os.debug.set_alert_level(fos.OSLogLevel.NONE)

    # ── Login ────────────────────────────────────────────────────────────
    elif step_id == "login":
        state.last_user_change_onesignal_id = None
        await os.login(TEST_EXTERNAL_ID)
        # Give the SDK a moment to propagate user state
        await asyncio.sleep(1)

    elif step_id == "get_onesignal_id":
        # After login the SDK may still be creating the user server-side;
        # poll API + check user_change event as fallback.
        oid = None
        for _ in range(30):  # up to 15s
            oid = await os.user.get_onesignal_id()
            if not oid:
                oid = state.last_user_change_onesignal_id
            if oid:
                break
            await asyncio.sleep(0.5)
        assert oid, "OneSignal ID not available after 15s (check app_id and network)"
        data["onesignal_id"] = oid

    elif step_id == "get_external_id":
        eid = await os.user.get_external_id()
        assert eid == TEST_EXTERNAL_ID, f"Expected '{TEST_EXTERNAL_ID}', got '{eid}'"

    # ── Tags ─────────────────────────────────────────────────────────────
    elif step_id == "add_tag":
        await os.user.add_tag(TEST_TAG_KEY, TEST_TAG_VALUE)
        await asyncio.sleep(0.5)

    elif step_id == "verify_tag":
        tags = await os.user.get_tags()
        assert TEST_TAG_KEY in tags, f"Tag '{TEST_TAG_KEY}' not found in {tags}"
        assert tags[TEST_TAG_KEY] == TEST_TAG_VALUE, (
            f"Tag value '{tags[TEST_TAG_KEY]}' != '{TEST_TAG_VALUE}'"
        )

    elif step_id == "remove_tag":
        await os.user.remove_tag(TEST_TAG_KEY)
        await asyncio.sleep(0.5)

    elif step_id == "verify_tag_removed":
        tags = await os.user.get_tags()
        assert TEST_TAG_KEY not in tags, f"Tag '{TEST_TAG_KEY}' still present: {tags}"

    # ── Aliases ──────────────────────────────────────────────────────────
    elif step_id == "add_alias":
        await os.user.add_alias(TEST_ALIAS_LABEL, TEST_ALIAS_ID)

    elif step_id == "remove_alias":
        oid = data.get("onesignal_id")
        assert oid, "No onesignal_id from earlier step"
        status = await delete_alias(
            app_id=ONESIGNAL_APP_ID,
            rest_api_key=REST_API_KEY,
            onesignal_id=oid,
            alias_label=TEST_ALIAS_LABEL,
        )
        assert status == 200, f"DELETE alias returned status {status}"

    # ── Email/SMS ────────────────────────────────────────────────────────
    elif step_id == "add_email":
        await os.user.add_email(TEST_EMAIL)

    elif step_id == "remove_email":
        await os.user.remove_email(TEST_EMAIL)

    elif step_id == "add_sms":
        await os.user.add_sms(TEST_SMS)

    elif step_id == "remove_sms":
        await os.user.remove_sms(TEST_SMS)

    # ── Language ─────────────────────────────────────────────────────────
    elif step_id == "set_language":
        await os.user.set_language(TEST_LANGUAGE)

    # ── Permission ───────────────────────────────────────────────────────
    elif step_id == "can_request_permission":
        result = await os.notifications.can_request_permission()
        data["can_request"] = result

    elif step_id == "request_permission":
        state.last_permission_change = None
        granted = await os.notifications.request_permission()
        data["permission_granted"] = granted

    elif step_id == "get_permission":
        perm = await os.notifications.get_permission()
        assert perm is True, f"Permission not granted: {perm}"

    elif step_id == "verify_permission_event":
        try:
            val = await wait_for_event(state, "last_permission_change", timeout=5)
            assert val is True, f"Expected permission=True, got {val}"
        except TimeoutError:
            # Permission was already granted before the test — no change event fires
            perm = await os.notifications.get_permission()
            assert perm is True, "Permission not granted and no change event received"

    # ── Push Subscription ────────────────────────────────────────────────
    elif step_id == "push_opt_in":
        await os.user.opt_in_push()

    elif step_id == "push_is_opted_in":
        opted = await os.user.is_push_opted_in()
        assert opted is True, f"Expected opted_in=True, got {opted}"

    elif step_id == "push_get_sub_id":
        sub_id = None
        for _ in range(10):  # up to 5s
            sub_id = await os.user.get_push_subscription_id()
            if sub_id:
                break
            await asyncio.sleep(0.5)
        assert sub_id, "Push subscription ID not available (check FCM/APNs config)"
        data["push_sub_id"] = sub_id

    elif step_id == "push_get_token":
        token = None
        for _ in range(10):  # up to 5s
            token = await os.user.get_push_subscription_token()
            if token:
                break
            await asyncio.sleep(0.5)
        assert token, "Push token not available (check FCM/APNs config)"
        data["push_token"] = token

    elif step_id == "push_opt_out":
        await os.user.opt_out_push()
        await asyncio.sleep(0.5)

    elif step_id == "push_verify_opt_out":
        opted = await os.user.is_push_opted_in()
        assert opted is False, f"Expected opted_in=False, got {opted}"

    elif step_id == "push_restore":
        await os.user.opt_in_push()
        await asyncio.sleep(0.5)
        opted = await os.user.is_push_opted_in()
        assert opted is True, f"Restore failed: opted_in={opted}"

    # ── Push REST ────────────────────────────────────────────────────────
    elif step_id == "send_push_api":
        state.last_notification_foreground_id = None
        oid = data.get("onesignal_id")
        assert oid, "No onesignal_id from earlier step"
        result = await send_push_notification(
            app_id=ONESIGNAL_APP_ID,
            rest_api_key=REST_API_KEY,
            onesignal_id=oid,
            title="Test Push",
            body="Automated test notification",
        )
        assert "id" in result, f"REST API error: {result}"
        data["push_notification_id"] = result["id"]

    elif step_id == "verify_foreground_event":
        nid = await wait_for_event(
            state, "last_notification_foreground_id", timeout=PUSH_WAIT_TIMEOUT
        )
        assert nid, "Foreground notification ID is None"

    elif step_id == "clear_all":
        await os.notifications.clear_all()

    # ── IAM ──────────────────────────────────────────────────────────────
    elif step_id == "iam_pause":
        await os.in_app_messages.pause()

    elif step_id == "iam_is_paused":
        paused = await os.in_app_messages.is_paused()
        assert paused is True, f"Expected paused=True, got {paused}"

    elif step_id == "iam_add_trigger":
        await os.in_app_messages.add_trigger("test_trigger", "1")

    elif step_id == "iam_remove_trigger":
        await os.in_app_messages.remove_trigger("test_trigger")

    elif step_id == "iam_clear_triggers":
        await os.in_app_messages.clear_triggers()

    elif step_id == "iam_resume":
        await os.in_app_messages.resume()

    elif step_id == "iam_verify_not_paused":
        paused = await os.in_app_messages.is_paused()
        assert paused is False, f"Expected paused=False, got {paused}"

    # ── Session ──────────────────────────────────────────────────────────
    elif step_id == "session_add_outcome":
        await os.session.add_outcome("test_outcome")

    elif step_id == "session_add_unique":
        await os.session.add_unique_outcome("test_unique_outcome")

    elif step_id == "session_add_with_value":
        await os.session.add_outcome_with_value("test_value_outcome", 9.99)

    # ── Location (Android only) ──────────────────────────────────────────
    elif step_id == "location_request_perm":
        # SDK returns immediately on Android (just launches the dialog).
        # Poll get_permission() until the user interacts with the dialog.
        await os.location.request_permission()
        granted = False
        for _ in range(30):  # up to 15s for user to tap Allow
            granted = await os.location.get_permission()
            if granted:
                break
            await asyncio.sleep(0.5)
        data["location_permission"] = granted

    elif step_id == "location_get_perm":
        perm = await os.location.get_permission()
        assert perm is True, f"Location permission not granted: {perm}"

    elif step_id == "location_set_shared_true":
        await os.location.set_shared(True)

    elif step_id == "location_is_shared":
        shared = await os.location.is_shared()
        assert shared is True, f"Expected shared=True, got {shared}"

    elif step_id == "location_set_shared_false":
        await os.location.set_shared(False)

    # ── Live Activities (iOS only) ───────────────────────────────────────
    elif step_id == "live_activities_setup":
        await os.live_activities.setup_default()

    # ── Consent ──────────────────────────────────────────────────────────
    elif step_id == "consent_give":
        await os.consent_given(True)

    elif step_id == "consent_revoke":
        await os.consent_given(False)

    # ── Cleanup ──────────────────────────────────────────────────────────
    elif step_id == "logout":
        state.last_user_change_onesignal_id = None
        await os.logout()

    elif step_id == "verify_user_change":
        val = await wait_for_event(state, "last_user_change_onesignal_id", timeout=15)
        # After logout, a new anonymous user is created — ID should exist
        assert val is not None, (
            "User change event not received after logout (check app_id and network)"
        )

    else:
        raise ValueError(f"Unknown step: {step_id}")
