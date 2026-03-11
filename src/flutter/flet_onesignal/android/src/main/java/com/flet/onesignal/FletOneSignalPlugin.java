package com.flet.onesignal;

import androidx.annotation.NonNull;
import io.flutter.embedding.engine.plugins.FlutterPlugin;

/**
 * No-op Android plugin stub for flet_onesignal.
 *
 * This class exists solely so Flutter recognizes the android/ directory
 * and applies the consumer ProGuard rules defined in consumer-rules.pro.
 * All actual OneSignal functionality is handled via the Dart-side
 * FletExtension (onesignal_service.dart).
 */
public class FletOneSignalPlugin implements FlutterPlugin {
    @Override
    public void onAttachedToEngine(@NonNull FlutterPluginBinding binding) {
        // no-op — real logic lives in the Dart FletExtension
    }

    @Override
    public void onDetachedFromEngine(@NonNull FlutterPluginBinding binding) {
        // no-op
    }
}