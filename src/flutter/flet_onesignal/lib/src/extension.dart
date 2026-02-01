import 'package:flet/flet.dart';
import 'onesignal_service.dart';

/// Extension registration for flet-onesignal.
///
/// This class follows the new Flet 0.80.x extension pattern using
/// FletExtension and FletService instead of the legacy createControl pattern.
class Extension extends FletExtension {
  @override
  FletService? createService(Control control) {
    switch (control.type) {
      case "onesignal":
        return OneSignalService(control: control);
      default:
        return null;
    }
  }
}
