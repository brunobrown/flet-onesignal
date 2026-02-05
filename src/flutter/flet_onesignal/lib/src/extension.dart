import 'package:flet/flet.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter/foundation.dart';
import 'onesignal_service.dart';

/// Extension registration for flet-onesignal.
///
/// This class follows the new Flet 0.80.x extension pattern using
/// FletExtension and FletService instead of the legacy createControl pattern.
class Extension extends FletExtension {
  @override
  void ensureInitialized() {
    print(">>> FletOneSignal Extension: ensureInitialized called");
    // OneSignal initialization is done in createService when app_id is available
  }

  @override
  FletService? createService(Control control) {
    print(">>> FletOneSignal Extension: createService called with type: '${control.type}'");
    if (control.type == "OneSignal") {
      print(">>> FletOneSignal Extension: Match! Creating OneSignalService");
      return OneSignalService(control: control);
    }
    print(">>> FletOneSignal Extension: No match for '${control.type}'");
    return null;
  }
}
