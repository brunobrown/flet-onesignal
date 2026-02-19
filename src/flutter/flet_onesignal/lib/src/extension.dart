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
    debugPrint("FletOneSignal: ensureInitialized");
  }

  @override
  FletService? createService(Control control) {
    debugPrint("FletOneSignal: createService type='${control.type}'");
    switch (control.type) {
      case "OneSignal":
        return OneSignalService(control: control);
      default:
        return null;
    }
  }
}
