# OneSignal SDK — suppress R8 warnings for transitive dependencies
# (OpenTelemetry pulls Jackson and AutoValue which are not used at runtime)
-dontwarn com.fasterxml.jackson.core.JsonFactory
-dontwarn com.fasterxml.jackson.core.JsonGenerator
-dontwarn com.google.auto.value.AutoValue$CopyAnnotations