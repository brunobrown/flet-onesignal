import 'dart:convert';
import 'package:flet/flet.dart';
import 'package:flutter/foundation.dart';
import 'package:onesignal_flutter/onesignal_flutter.dart';

/// OneSignal service implementation for Flet.
///
/// This service handles all communication between the Python SDK
/// and the OneSignal Flutter SDK.
class OneSignalService extends FletService {
  OneSignalService({required super.control});

  bool _initialized = false;
  bool _listenersSetup = false;

  @override
  void init() {
    super.init();
    control.onInvokeMethod = _onInvokeMethod;
    _initializeOneSignal();
  }

  @override
  Future<void> update() async {
    // Handle property updates if needed
    final appId = control.attrString("appId");
    if (appId != null && !_initialized) {
      _initializeOneSignal();
    }
  }

  @override
  void dispose() {
    // Cleanup listeners if needed
    super.dispose();
  }

  /// Initialize the OneSignal SDK with the app ID.
  void _initializeOneSignal() {
    final appId = control.attrString("appId");
    if (appId == null || appId.isEmpty) {
      debugPrint("OneSignal: No app ID provided");
      return;
    }

    try {
      // Initialize OneSignal
      OneSignal.initialize(appId);
      _initialized = true;
      debugPrint("OneSignal: Initialized with app ID: $appId");

      // Set log level if provided
      final logLevel = control.attrString("logLevel");
      if (logLevel != null) {
        _setLogLevel(logLevel);
      }

      // Handle consent requirement
      final requireConsent = control.attrBool("requireConsent", false)!;
      if (requireConsent) {
        OneSignal.consentRequired(true);
      }

      // Setup listeners
      _setupListeners();
    } catch (error, stackTrace) {
      _handleError("_initializeOneSignal", error, stackTrace);
    }
  }

  /// Setup all OneSignal listeners.
  void _setupListeners() {
    if (_listenersSetup) return;
    _listenersSetup = true;

    // Notification click listener
    OneSignal.Notifications.addClickListener((event) {
      try {
        debugPrint("OneSignal: Notification clicked");
        final jsonData = jsonEncode({
          "notification": event.notification.jsonRepresentation(),
          "action_id": event.result.actionId,
        });
        triggerEvent("notification_click", jsonData);
      } catch (error, stackTrace) {
        _handleError("notification_click_listener", error, stackTrace);
      }
    });

    // Notification foreground will display listener
    OneSignal.Notifications.addForegroundWillDisplayListener((event) {
      try {
        debugPrint("OneSignal: Notification will display in foreground");
        final jsonData = jsonEncode({
          "notification": event.notification.jsonRepresentation(),
          "notification_id": event.notification.notificationId,
        });
        triggerEvent("notification_foreground", jsonData);
      } catch (error, stackTrace) {
        _handleError("notification_foreground_listener", error, stackTrace);
      }
    });

    // Permission change listener
    OneSignal.Notifications.addPermissionObserver((permission) {
      try {
        debugPrint("OneSignal: Permission changed to $permission");
        final jsonData = jsonEncode({
          "permission": permission,
        });
        triggerEvent("permission_change", jsonData);
      } catch (error, stackTrace) {
        _handleError("permission_change_listener", error, stackTrace);
      }
    });

    // User state change listener
    OneSignal.User.addObserver((state) {
      try {
        debugPrint("OneSignal: User state changed");
        final jsonData = jsonEncode({
          "onesignal_id": state.current.onesignalId,
          "external_id": state.current.externalId,
        });
        triggerEvent("user_change", jsonData);
      } catch (error, stackTrace) {
        _handleError("user_change_listener", error, stackTrace);
      }
    });

    // Push subscription change listener
    OneSignal.User.pushSubscription.addObserver((state) {
      try {
        debugPrint("OneSignal: Push subscription changed");
        final jsonData = jsonEncode({
          "id": state.current.id,
          "token": state.current.token,
          "opted_in": state.current.optedIn,
        });
        triggerEvent("push_subscription_change", jsonData);
      } catch (error, stackTrace) {
        _handleError("push_subscription_change_listener", error, stackTrace);
      }
    });

    // In-App Message listeners
    OneSignal.InAppMessages.addClickListener((event) {
      try {
        debugPrint("OneSignal: In-app message clicked");
        final messageMap = jsonDecode(event.message.jsonRepresentation());
        final resultMap = jsonDecode(event.result.jsonRepresentation());
        final jsonData = jsonEncode({
          "message": messageMap,
          "result": resultMap,
        });
        triggerEvent("iam_click", jsonData);
      } catch (error, stackTrace) {
        _handleError("iam_click_listener", error, stackTrace);
      }
    });

    OneSignal.InAppMessages.addWillDisplayListener((event) {
      try {
        debugPrint("OneSignal: In-app message will display");
        final messageMap = jsonDecode(event.message.jsonRepresentation());
        final jsonData = jsonEncode({"message": messageMap});
        triggerEvent("iam_will_display", jsonData);
      } catch (error, stackTrace) {
        _handleError("iam_will_display_listener", error, stackTrace);
      }
    });

    OneSignal.InAppMessages.addDidDisplayListener((event) {
      try {
        debugPrint("OneSignal: In-app message did display");
        final messageMap = jsonDecode(event.message.jsonRepresentation());
        final jsonData = jsonEncode({"message": messageMap});
        triggerEvent("iam_did_display", jsonData);
      } catch (error, stackTrace) {
        _handleError("iam_did_display_listener", error, stackTrace);
      }
    });

    OneSignal.InAppMessages.addWillDismissListener((event) {
      try {
        debugPrint("OneSignal: In-app message will dismiss");
        final messageMap = jsonDecode(event.message.jsonRepresentation());
        final jsonData = jsonEncode({"message": messageMap});
        triggerEvent("iam_will_dismiss", jsonData);
      } catch (error, stackTrace) {
        _handleError("iam_will_dismiss_listener", error, stackTrace);
      }
    });

    OneSignal.InAppMessages.addDidDismissListener((event) {
      try {
        debugPrint("OneSignal: In-app message did dismiss");
        final messageMap = jsonDecode(event.message.jsonRepresentation());
        final jsonData = jsonEncode({"message": messageMap});
        triggerEvent("iam_did_dismiss", jsonData);
      } catch (error, stackTrace) {
        _handleError("iam_did_dismiss_listener", error, stackTrace);
      }
    });

    debugPrint("OneSignal: All listeners setup complete");
  }

  /// Handle method invocations from Python.
  Future<String?> _onInvokeMethod(String methodName, Map<String, dynamic> args) async {
    try {
      debugPrint("OneSignal: Invoking method $methodName with args $args");

      return switch (methodName) {
        // Main methods
        "login" => await _login(args),
        "logout" => await _logout(),
        "consent_given" => await _consentGiven(args),

        // Debug methods
        "debug_set_log_level" => _setLogLevel(args["level"]),
        "debug_set_alert_level" => _setAlertLevel(args["level"]),

        // User methods
        "user_get_onesignal_id" => await _getUserOnesignalId(),
        "user_get_external_id" => await _getUserExternalId(),
        "user_add_tag" => await _userAddTag(args),
        "user_add_tags" => await _userAddTags(args),
        "user_remove_tag" => await _userRemoveTag(args),
        "user_remove_tags" => await _userRemoveTags(args),
        "user_get_tags" => await _userGetTags(),
        "user_add_alias" => await _userAddAlias(args),
        "user_add_aliases" => await _userAddAliases(args),
        "user_remove_alias" => await _userRemoveAlias(args),
        "user_remove_aliases" => await _userRemoveAliases(args),
        "user_add_email" => await _userAddEmail(args),
        "user_remove_email" => await _userRemoveEmail(args),
        "user_add_sms" => await _userAddSms(args),
        "user_remove_sms" => await _userRemoveSms(args),
        "user_set_language" => await _userSetLanguage(args),
        "user_push_opt_in" => await _userPushOptIn(),
        "user_push_opt_out" => await _userPushOptOut(),
        "user_get_push_subscription_id" => _userGetPushSubscriptionId(),
        "user_get_push_subscription_token" => _userGetPushSubscriptionToken(),
        "user_is_push_opted_in" => _userIsPushOptedIn(),

        // Notification methods
        "notifications_request_permission" => await _notificationsRequestPermission(args),
        "notifications_can_request_permission" => await _notificationsCanRequestPermission(),
        "notifications_get_permission" => _notificationsGetPermission(),
        "notifications_register_provisional" => await _notificationsRegisterProvisional(),
        "notifications_clear_all" => await _notificationsClearAll(),
        "notifications_remove" => await _notificationsRemove(args),
        "notifications_remove_grouped" => await _notificationsRemoveGrouped(args),
        "notifications_prevent_default" => _notificationsPreventDefault(args),
        "notifications_display" => _notificationsDisplay(args),

        // In-App Message methods
        "iam_add_trigger" => _iamAddTrigger(args),
        "iam_add_triggers" => _iamAddTriggers(args),
        "iam_remove_trigger" => _iamRemoveTrigger(args),
        "iam_remove_triggers" => _iamRemoveTriggers(args),
        "iam_clear_triggers" => _iamClearTriggers(),
        "iam_set_paused" => _iamSetPaused(args),
        "iam_is_paused" => _iamIsPaused(),

        // Location methods
        "location_request_permission" => await _locationRequestPermission(),
        "location_set_shared" => _locationSetShared(args),
        "location_is_shared" => _locationIsShared(),

        // Session methods
        "session_add_outcome" => await _sessionAddOutcome(args),
        "session_add_unique_outcome" => await _sessionAddUniqueOutcome(args),
        "session_add_outcome_with_value" => await _sessionAddOutcomeWithValue(args),

        // Live Activities methods (iOS only)
        "live_activities_enter" => await _liveActivitiesEnter(args),
        "live_activities_exit" => await _liveActivitiesExit(args),
        "live_activities_set_push_to_start_token" => await _liveActivitiesSetPushToStartToken(args),
        "live_activities_remove_push_to_start_token" => await _liveActivitiesRemovePushToStartToken(args),
        "live_activities_setup_default" => await _liveActivitiesSetupDefault(args),

        _ => null,
      };
    } catch (error, stackTrace) {
      _handleError(methodName, error, stackTrace);
      return null;
    }
  }

  // ---------------------------------------------------------------------------
  // Main methods
  // ---------------------------------------------------------------------------

  Future<String?> _login(Map<String, dynamic> args) async {
    final externalId = args["external_id"] as String?;
    if (externalId != null) {
      await OneSignal.login(externalId);
    }
    return null;
  }

  Future<String?> _logout() async {
    await OneSignal.logout();
    return null;
  }

  Future<String?> _consentGiven(Map<String, dynamic> args) async {
    final given = args["given"] as bool? ?? false;
    await OneSignal.consentGiven(given);
    return null;
  }

  // ---------------------------------------------------------------------------
  // Debug methods
  // ---------------------------------------------------------------------------

  String? _setLogLevel(String? level) {
    if (level == null) return null;
    final osLevel = _parseLogLevel(level);
    OneSignal.Debug.setLogLevel(osLevel);
    return null;
  }

  String? _setAlertLevel(String? level) {
    if (level == null) return null;
    final osLevel = _parseLogLevel(level);
    OneSignal.Debug.setAlertLevel(osLevel);
    return null;
  }

  OSLogLevel _parseLogLevel(String level) {
    return switch (level.toLowerCase()) {
      "none" => OSLogLevel.none,
      "fatal" => OSLogLevel.fatal,
      "error" => OSLogLevel.error,
      "warn" => OSLogLevel.warn,
      "info" => OSLogLevel.info,
      "debug" => OSLogLevel.debug,
      "verbose" => OSLogLevel.verbose,
      _ => OSLogLevel.warn,
    };
  }

  // ---------------------------------------------------------------------------
  // User methods
  // ---------------------------------------------------------------------------

  Future<String?> _getUserOnesignalId() async {
    return await OneSignal.User.getOnesignalId();
  }

  Future<String?> _getUserExternalId() async {
    return await OneSignal.User.getExternalId();
  }

  Future<String?> _userAddTag(Map<String, dynamic> args) async {
    final key = args["key"] as String?;
    final value = args["value"] as String?;
    if (key != null && value != null) {
      await OneSignal.User.addTagWithKey(key, value);
    }
    return null;
  }

  Future<String?> _userAddTags(Map<String, dynamic> args) async {
    final tags = args["tags"] as Map<String, dynamic>?;
    if (tags != null) {
      await OneSignal.User.addTags(tags.map((k, v) => MapEntry(k, v.toString())));
    }
    return null;
  }

  Future<String?> _userRemoveTag(Map<String, dynamic> args) async {
    final key = args["key"] as String?;
    if (key != null) {
      await OneSignal.User.removeTag(key);
    }
    return null;
  }

  Future<String?> _userRemoveTags(Map<String, dynamic> args) async {
    final keys = (args["keys"] as List?)?.cast<String>();
    if (keys != null) {
      await OneSignal.User.removeTags(keys);
    }
    return null;
  }

  Future<String?> _userGetTags() async {
    final tags = await OneSignal.User.getTags();
    return jsonEncode(tags);
  }

  Future<String?> _userAddAlias(Map<String, dynamic> args) async {
    final label = args["label"] as String?;
    final id = args["id"] as String?;
    if (label != null && id != null) {
      await OneSignal.User.addAlias(label, id);
    }
    return null;
  }

  Future<String?> _userAddAliases(Map<String, dynamic> args) async {
    final aliases = args["aliases"] as Map<String, dynamic>?;
    if (aliases != null) {
      await OneSignal.User.addAliases(aliases.map((k, v) => MapEntry(k, v.toString())));
    }
    return null;
  }

  Future<String?> _userRemoveAlias(Map<String, dynamic> args) async {
    final label = args["label"] as String?;
    if (label != null) {
      await OneSignal.User.removeAlias(label);
    }
    return null;
  }

  Future<String?> _userRemoveAliases(Map<String, dynamic> args) async {
    final labels = (args["labels"] as List?)?.cast<String>();
    if (labels != null) {
      await OneSignal.User.removeAliases(labels);
    }
    return null;
  }

  Future<String?> _userAddEmail(Map<String, dynamic> args) async {
    final email = args["email"] as String?;
    if (email != null) {
      await OneSignal.User.addEmail(email);
    }
    return null;
  }

  Future<String?> _userRemoveEmail(Map<String, dynamic> args) async {
    final email = args["email"] as String?;
    if (email != null) {
      await OneSignal.User.removeEmail(email);
    }
    return null;
  }

  Future<String?> _userAddSms(Map<String, dynamic> args) async {
    final phone = args["phone"] as String?;
    if (phone != null) {
      await OneSignal.User.addSms(phone);
    }
    return null;
  }

  Future<String?> _userRemoveSms(Map<String, dynamic> args) async {
    final phone = args["phone"] as String?;
    if (phone != null) {
      await OneSignal.User.removeSms(phone);
    }
    return null;
  }

  Future<String?> _userSetLanguage(Map<String, dynamic> args) async {
    final language = args["language"] as String?;
    if (language != null) {
      await OneSignal.User.setLanguage(language);
    }
    return null;
  }

  Future<String?> _userPushOptIn() async {
    await OneSignal.User.pushSubscription.optIn();
    return null;
  }

  Future<String?> _userPushOptOut() async {
    await OneSignal.User.pushSubscription.optOut();
    return null;
  }

  String? _userGetPushSubscriptionId() {
    return OneSignal.User.pushSubscription.id;
  }

  String? _userGetPushSubscriptionToken() {
    return OneSignal.User.pushSubscription.token;
  }

  String _userIsPushOptedIn() {
    return OneSignal.User.pushSubscription.optedIn.toString();
  }

  // ---------------------------------------------------------------------------
  // Notification methods
  // ---------------------------------------------------------------------------

  Future<String> _notificationsRequestPermission(Map<String, dynamic> args) async {
    final fallbackToSettings = args["fallback_to_settings"] as bool? ?? true;
    final result = await OneSignal.Notifications.requestPermission(fallbackToSettings);
    return result.toString();
  }

  Future<String> _notificationsCanRequestPermission() async {
    final result = await OneSignal.Notifications.canRequest();
    return result.toString();
  }

  String _notificationsGetPermission() {
    return OneSignal.Notifications.permission.toString();
  }

  Future<String> _notificationsRegisterProvisional() async {
    final result = await OneSignal.Notifications.registerForProvisionalAuthorization(true);
    return result.toString();
  }

  Future<String?> _notificationsClearAll() async {
    await OneSignal.Notifications.clearAll();
    return null;
  }

  Future<String?> _notificationsRemove(Map<String, dynamic> args) async {
    final notificationId = args["notification_id"] as int?;
    if (notificationId != null) {
      await OneSignal.Notifications.removeNotification(notificationId);
    }
    return null;
  }

  Future<String?> _notificationsRemoveGrouped(Map<String, dynamic> args) async {
    final group = args["group"] as String?;
    if (group != null) {
      await OneSignal.Notifications.removeGroupedNotifications(group);
    }
    return null;
  }

  String? _notificationsPreventDefault(Map<String, dynamic> args) {
    final notificationId = args["notification_id"] as String?;
    if (notificationId != null) {
      OneSignal.Notifications.preventDefault(notificationId);
    }
    return null;
  }

  String? _notificationsDisplay(Map<String, dynamic> args) {
    final notificationId = args["notification_id"] as String?;
    if (notificationId != null) {
      OneSignal.Notifications.displayNotification(notificationId);
    }
    return null;
  }

  // ---------------------------------------------------------------------------
  // In-App Message methods
  // ---------------------------------------------------------------------------

  String? _iamAddTrigger(Map<String, dynamic> args) {
    final key = args["key"] as String?;
    final value = args["value"] as String?;
    if (key != null && value != null) {
      OneSignal.InAppMessages.addTrigger(key, value);
    }
    return null;
  }

  String? _iamAddTriggers(Map<String, dynamic> args) {
    final triggers = args["triggers"] as Map<String, dynamic>?;
    if (triggers != null) {
      OneSignal.InAppMessages.addTriggers(triggers.map((k, v) => MapEntry(k, v.toString())));
    }
    return null;
  }

  String? _iamRemoveTrigger(Map<String, dynamic> args) {
    final key = args["key"] as String?;
    if (key != null) {
      OneSignal.InAppMessages.removeTrigger(key);
    }
    return null;
  }

  String? _iamRemoveTriggers(Map<String, dynamic> args) {
    final keys = (args["keys"] as List?)?.cast<String>();
    if (keys != null) {
      OneSignal.InAppMessages.removeTriggers(keys);
    }
    return null;
  }

  String? _iamClearTriggers() {
    OneSignal.InAppMessages.clearTriggers();
    return null;
  }

  String? _iamSetPaused(Map<String, dynamic> args) {
    final paused = args["paused"] as bool? ?? false;
    OneSignal.InAppMessages.paused = paused;
    return null;
  }

  String _iamIsPaused() {
    return OneSignal.InAppMessages.paused.toString();
  }

  // ---------------------------------------------------------------------------
  // Location methods
  // ---------------------------------------------------------------------------

  Future<String> _locationRequestPermission() async {
    final result = await OneSignal.Location.requestPermission();
    return result.toString();
  }

  String? _locationSetShared(Map<String, dynamic> args) {
    final shared = args["shared"] as bool? ?? false;
    OneSignal.Location.setShared(shared);
    return null;
  }

  String _locationIsShared() {
    return OneSignal.Location.isShared.toString();
  }

  // ---------------------------------------------------------------------------
  // Session methods
  // ---------------------------------------------------------------------------

  Future<String?> _sessionAddOutcome(Map<String, dynamic> args) async {
    final name = args["name"] as String?;
    if (name != null) {
      await OneSignal.Session.addOutcome(name);
    }
    return null;
  }

  Future<String?> _sessionAddUniqueOutcome(Map<String, dynamic> args) async {
    final name = args["name"] as String?;
    if (name != null) {
      await OneSignal.Session.addUniqueOutcome(name);
    }
    return null;
  }

  Future<String?> _sessionAddOutcomeWithValue(Map<String, dynamic> args) async {
    final name = args["name"] as String?;
    final value = args["value"];
    if (name != null && value != null) {
      await OneSignal.Session.addOutcomeWithValue(name, (value as num).toDouble());
    }
    return null;
  }

  // ---------------------------------------------------------------------------
  // Live Activities methods (iOS only)
  // ---------------------------------------------------------------------------

  Future<String?> _liveActivitiesEnter(Map<String, dynamic> args) async {
    final activityId = args["activity_id"] as String?;
    final token = args["token"] as String?;
    if (activityId != null && token != null) {
      await OneSignal.LiveActivities.enterLiveActivity(activityId, token);
    }
    return null;
  }

  Future<String?> _liveActivitiesExit(Map<String, dynamic> args) async {
    final activityId = args["activity_id"] as String?;
    if (activityId != null) {
      await OneSignal.LiveActivities.exitLiveActivity(activityId);
    }
    return null;
  }

  Future<String?> _liveActivitiesSetPushToStartToken(Map<String, dynamic> args) async {
    final activityType = args["activity_type"] as String?;
    final token = args["token"] as String?;
    if (activityType != null && token != null) {
      await OneSignal.LiveActivities.setPushToStartToken(activityType, token);
    }
    return null;
  }

  Future<String?> _liveActivitiesRemovePushToStartToken(Map<String, dynamic> args) async {
    final activityType = args["activity_type"] as String?;
    if (activityType != null) {
      await OneSignal.LiveActivities.removePushToStartToken(activityType);
    }
    return null;
  }

  Future<String?> _liveActivitiesSetupDefault(Map<String, dynamic> args) async {
    // Setup default options for Live Activities
    // The options structure depends on the specific iOS implementation
    await OneSignal.LiveActivities.setupDefault();
    return null;
  }

  // ---------------------------------------------------------------------------
  // Error handling
  // ---------------------------------------------------------------------------

  void _handleError(String method, Object error, StackTrace stackTrace) {
    debugPrint("OneSignal Error in $method: $error\n$stackTrace");
    triggerEvent(
      "error",
      jsonEncode({
        "method": method,
        "message": error.toString(),
        "stackTrace": stackTrace.toString(),
      }),
    );
  }
}
