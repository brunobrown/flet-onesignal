"""Ordered list of test step definitions."""

from dataclasses import dataclass


@dataclass
class StepDef:
    id: str
    name: str
    group: str
    platform: str = "all"  # "all", "android", "ios"
    needs_user_interaction: bool = False
    interaction_message: str = ""


TEST_STEPS: list[StepDef] = [
    # --- Debug (1-2) ---
    StepDef("debug_log_level", "Set Log Level to DEBUG", "Debug"),
    StepDef("debug_alert_level", "Set Alert Level to NONE", "Debug"),
    # --- Login (3-5) ---
    StepDef("login", "Login with External ID", "Login"),
    StepDef("get_onesignal_id", "Get OneSignal ID", "Login"),
    StepDef("get_external_id", "Get External ID", "Login"),
    # --- Tags (6-9) ---
    StepDef("add_tag", "Add Tag", "Tags"),
    StepDef("verify_tag", "Verify Tag Added", "Tags"),
    StepDef("remove_tag", "Remove Tag", "Tags"),
    StepDef("verify_tag_removed", "Verify Tag Removed", "Tags"),
    # --- Aliases (10-11) ---
    StepDef("add_alias", "Add Alias", "Aliases"),
    StepDef("remove_alias", "Remove Alias", "Aliases"),
    # --- Email/SMS (12-15) ---
    StepDef("add_email", "Add Email", "Email/SMS"),
    StepDef("remove_email", "Remove Email", "Email/SMS"),
    StepDef("add_sms", "Add SMS", "Email/SMS"),
    StepDef("remove_sms", "Remove SMS", "Email/SMS"),
    # --- Language (16) ---
    StepDef("set_language", "Set Language to Portuguese", "Language"),
    # --- Permission (17-20) ---
    StepDef("can_request_permission", "Can Request Permission", "Permission"),
    StepDef(
        "request_permission",
        "Request Permission",
        "Permission",
        needs_user_interaction=True,
        interaction_message="Tap 'Allow' on the notification permission dialog",
    ),
    StepDef("get_permission", "Get Permission Status", "Permission"),
    StepDef("verify_permission_event", "Verify Permission Change Event", "Permission"),
    # --- Push Subscription (21-27) ---
    StepDef("push_opt_in", "Opt In to Push", "Push Sub"),
    StepDef("push_is_opted_in", "Verify Opted In", "Push Sub"),
    StepDef("push_get_sub_id", "Get Subscription ID", "Push Sub"),
    StepDef("push_get_token", "Get Push Token", "Push Sub"),
    StepDef("push_opt_out", "Opt Out of Push", "Push Sub"),
    StepDef("push_verify_opt_out", "Verify Opted Out", "Push Sub"),
    StepDef("push_restore", "Restore Push (Opt In)", "Push Sub"),
    # --- Push REST (28-30) ---
    StepDef("send_push_api", "Send Push via REST API", "Push REST"),
    StepDef("verify_foreground_event", "Verify Foreground Event (15s)", "Push REST"),
    StepDef("clear_all", "Clear All Notifications", "Push REST"),
    # --- IAM (31-37) ---
    StepDef("iam_pause", "Pause In-App Messages", "IAM"),
    StepDef("iam_is_paused", "Verify IAM Paused", "IAM"),
    StepDef("iam_add_trigger", "Add Trigger", "IAM"),
    StepDef("iam_remove_trigger", "Remove Trigger", "IAM"),
    StepDef("iam_clear_triggers", "Clear All Triggers", "IAM"),
    StepDef("iam_resume", "Resume In-App Messages", "IAM"),
    StepDef("iam_verify_not_paused", "Verify IAM Not Paused", "IAM"),
    # --- Session (38-40) ---
    StepDef("session_add_outcome", "Add Outcome", "Session"),
    StepDef("session_add_unique", "Add Unique Outcome", "Session"),
    StepDef("session_add_with_value", "Add Outcome with Value", "Session"),
    # --- Location (41-45) - Android only ---
    StepDef(
        "location_request_perm",
        "Request Location Permission",
        "Location",
        platform="android",
        needs_user_interaction=True,
        interaction_message="Tap 'Allow' on the location permission dialog",
    ),
    StepDef(
        "location_get_perm",
        "Get Location Permission",
        "Location",
        platform="android",
    ),
    StepDef(
        "location_set_shared_true",
        "Set Location Shared (true)",
        "Location",
        platform="android",
    ),
    StepDef(
        "location_is_shared",
        "Verify Location Shared",
        "Location",
        platform="android",
    ),
    StepDef(
        "location_set_shared_false",
        "Set Location Shared (false)",
        "Location",
        platform="android",
    ),
    # --- Live Activities (46) - iOS only ---
    StepDef(
        "live_activities_setup",
        "Setup Default Live Activity",
        "Live Activities",
        platform="ios",
    ),
    # --- Consent (47-48) ---
    StepDef("consent_give", "Give Consent", "Consent"),
    StepDef("consent_revoke", "Revoke Consent", "Consent"),
    # --- Cleanup (49-50) ---
    StepDef("logout", "Logout", "Cleanup"),
    StepDef("verify_user_change", "Verify User Change Event", "Cleanup"),
]
