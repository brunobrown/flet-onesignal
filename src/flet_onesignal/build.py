#!/usr/bin/env python
"""
Automated build script for Flet apps with OneSignal support.

This script automates the process of building Flet apps for all platforms.
For Android builds (apk/aab), it can inject optional OneSignal modules
(e.g. location) as Gradle dependencies.

Supported platforms: apk, aab, ipa, web, macos, linux, windows

Usage:
    fos-build apk
    fos-build aab --split-per-abi
    fos-build apk --location
    fos-build ipa
    fos-build web

    # All flet build options are passed through:
    fos-build apk -v --org com.example --build-version 1.0.0
"""

import argparse
import re
import shutil
import subprocess
import sys
import tomllib
from pathlib import Path

from flet_onesignal import ui

ALL_PLATFORMS = ["apk", "aab", "ipa", "web", "macos", "linux", "windows"]
ANDROID_PLATFORMS = {"apk", "aab"}

NEXT_STEPS = {
    "apk": [
        "Install on device: adb install <path-to-apk>",
        "Or upload to Play Store",
    ],
    "aab": [
        "Upload to Google Play Console",
    ],
    "ipa": [
        "Upload to App Store Connect via Xcode or Transporter",
    ],
    "web": [
        "Deploy the build/web directory to your hosting provider",
    ],
    "macos": [
        "Run the app from build/macos",
        "Or distribute via DMG / App Store",
    ],
    "linux": [
        "Run the app from build/linux",
        "Or package as .deb / .rpm / snap",
    ],
    "windows": [
        "Run the app from build/windows",
        "Or create an installer with Inno Setup / MSIX",
    ],
}

FAILURE_TIPS = [
    "Try running with --clean to start fresh",
    "Use -v or -vv for more verbose output",
    "Run: flet build --show-platform-matrix",
]


def find_project_root() -> Path:
    """Find the Flet project root (directory containing pyproject.toml)."""
    current = Path.cwd()

    while current != current.parent:
        if (current / "pyproject.toml").exists():
            return current
        current = current.parent

    return Path.cwd()


def _get_onesignal_config(project_root: Path) -> dict:
    """Read [tool.flet.onesignal.android] from pyproject.toml."""
    pyproject_path = project_root / "pyproject.toml"
    if not pyproject_path.exists():
        return {}

    with open(pyproject_path, "rb") as f:
        pyproject = tomllib.load(f)

    return pyproject.get("tool", {}).get("flet", {}).get("onesignal", {}).get("android", {})


# Map of optional OneSignal module names to their Maven coordinates + extra deps
# Each entry: key -> list of (maven_coord, version_range) tuples
_ONESIGNAL_MODULES = {
    "location": [
        ("com.onesignal:location", "[5.0.0, 5.99.99]"),
        ("com.google.android.gms:play-services-location", "18.0.0"),
    ],
}


def _inject_dep_line(content: str, dep_line: str) -> str:
    """Insert a dependency line into the dependencies block of a gradle file.

    Handles both single-line ``dependencies {}`` and multi-line blocks.
    """
    # Try multi-line: closing brace on its own line
    result, count = re.subn(
        r"(dependencies\s*\{.*?)(^\})",
        rf"\1{dep_line}\n\2",
        content,
        count=1,
        flags=re.DOTALL | re.MULTILINE,
    )
    if count:
        return result

    # Single-line: dependencies {}  or  dependencies { ... }
    replacement = f"\\1\n{dep_line}\n}}"
    return re.sub(
        r"(dependencies\s*\{)([ \t]*)\}",
        replacement,
        content,
        count=1,
    )


def _collect_onesignal_deps(config: dict) -> list[tuple[str, str]]:
    """Collect all (maven_coord, version) pairs for enabled OneSignal modules."""
    deps = []
    for key, dep_list in _ONESIGNAL_MODULES.items():
        if config.get(key):
            deps.extend(dep_list)
    return deps


def _inject_onesignal_modules(flutter_dir: Path, config: dict) -> bool:
    """Inject optional OneSignal module dependencies into app/build.gradle(.kts).

    Returns True if any modifications were made.
    """
    android_dir = flutter_dir / "android"
    app_dir = android_dir / "app"

    if not app_dir.exists():
        return False

    deps = _collect_onesignal_deps(config)
    if not deps:
        return False

    modified = False

    # Check for Kotlin DSL first, then Groovy
    app_kts = app_dir / "build.gradle.kts"
    app_gradle = app_dir / "build.gradle"

    if app_kts.exists():
        content = app_kts.read_text()
        for maven_coord, version in deps:
            if maven_coord not in content:
                dep_line = f'    implementation("{maven_coord}:{version}")'
                content = _inject_dep_line(content, dep_line)
                ui.modified(f"Injected: {maven_coord}:{version} into build.gradle.kts")
                modified = True
        if modified:
            app_kts.write_text(content)

    elif app_gradle.exists():
        content = app_gradle.read_text()
        for maven_coord, version in deps:
            if maven_coord not in content:
                dep_line = f"    implementation '{maven_coord}:{version}'"
                content = _inject_dep_line(content, dep_line)
                ui.modified(f"Injected: {maven_coord}:{version} into build.gradle")
                modified = True
        if modified:
            app_gradle.write_text(content)

    # Inject ProGuard rules to prevent R8 from stripping reflection targets
    if modified and config.get("location"):
        _inject_proguard_rules(app_dir)

    return modified


_ONESIGNAL_PROGUARD_RULES = """\
# OneSignal Location module uses reflection on GoogleApiClient internals
-keep class com.google.android.gms.common.api.GoogleApiClient { *; }
-keep class com.google.android.gms.common.api.internal.zab* { *; }
"""

_PROGUARD_MARKER = "# OneSignal Location module"


def _inject_proguard_rules(app_dir: Path) -> None:
    """Add ProGuard keep rules for OneSignal Location reflection targets."""
    proguard_file = app_dir / "proguard-rules.pro"

    # Write the rules file
    if proguard_file.exists():
        content = proguard_file.read_text()
        if _PROGUARD_MARKER in content:
            return
        content += "\n" + _ONESIGNAL_PROGUARD_RULES
        proguard_file.write_text(content)
    else:
        proguard_file.write_text(_ONESIGNAL_PROGUARD_RULES)

    ui.modified("Injected: ProGuard rules for OneSignal Location")

    # Ensure the build.gradle(.kts) references the proguard file in the release buildType
    app_kts = app_dir / "build.gradle.kts"
    app_gradle = app_dir / "build.gradle"

    proguard_ref = 'proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro")'

    if app_kts.exists():
        content = app_kts.read_text()
        if "proguard-rules.pro" not in content:
            content = content.replace(
                "signingConfig = signingConfigs",
                f'{proguard_ref}\n            signingConfig = signingConfigs',
            )
            app_kts.write_text(content)
            ui.modified("Modified: build.gradle.kts (added proguardFiles reference)")


def _check_onesignal_modules(flutter_dir: Path, config: dict) -> bool:
    """Check if all enabled OneSignal modules are already in the gradle file."""
    app_dir = flutter_dir / "android" / "app"
    if not app_dir.exists():
        return True  # Nothing to check

    app_kts = app_dir / "build.gradle.kts"
    app_gradle = app_dir / "build.gradle"

    gradle_file = app_kts if app_kts.exists() else app_gradle if app_gradle.exists() else None
    if not gradle_file:
        return True  # Nothing to check

    content = gradle_file.read_text()

    for maven_coord, _ in _collect_onesignal_deps(config):
        if maven_coord not in content:
            return False

    # Check ProGuard rules for location
    if config.get("location"):
        proguard_file = app_dir / "proguard-rules.pro"
        if not proguard_file.exists() or _PROGUARD_MARKER not in proguard_file.read_text():
            return False

    return True


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Build Flet app with OneSignal support",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    fos-build apk              Build Android APK
    fos-build aab              Build Android App Bundle
    fos-build apk --location   Enable OneSignal Location module
    fos-build ipa              Build iOS IPA
    fos-build web              Build for web
    fos-build macos            Build for macOS
    fos-build linux            Build for Linux
    fos-build windows          Build for Windows

    # All flet build options are passed through:
    fos-build apk -v --split-per-abi
    fos-build apk --org com.example --build-version 1.0.0
    fos-build web --no-wasm --no-cdn
    fos-build ipa --ios-team-id ABCDE12345
    fos-build apk --clean      Clean build directory first

Notes:
    For Android, optional OneSignal modules (e.g. location) can be enabled
    via --location flag or [tool.flet.onesignal.android] in pyproject.toml.
    All other options (including -v) are passed directly to flet build.
        """,
    )
    parser.add_argument(
        "build_type",
        choices=ALL_PLATFORMS,
        help="Target platform (apk, aab, ipa, web, macos, linux, windows)",
    )
    parser.add_argument(
        "--clean", action="store_true", help="Clean build directory before building"
    )
    parser.add_argument(
        "--location",
        action="store_true",
        help="Enable OneSignal Location module (injects gradle dependencies)",
    )

    args, extra = parser.parse_known_args()

    ui.header()

    # Find project root
    project_root = find_project_root()
    ui.info("Project root", str(project_root))

    # Clean if requested
    if args.clean:
        build_dir = project_root / "build"
        if build_dir.exists():
            ui.info("Cleaning", str(build_dir))
            shutil.rmtree(build_dir)

    # Build the flet build command with passthrough args
    cmd = ["flet", "build", args.build_type] + extra

    if args.build_type in ANDROID_PLATFORMS:
        _build_android(args, cmd, project_root)
    else:
        _build_non_android(args, cmd, project_root)


def _build_android(
    args: argparse.Namespace,
    cmd: list[str],
    project_root: Path,
) -> None:
    """Build Android APK/AAB, injecting optional OneSignal modules if enabled."""
    # Merge config: pyproject.toml + CLI flags
    onesignal_config = _get_onesignal_config(project_root)
    if args.location:
        onesignal_config["location"] = True

    flutter_dir = project_root / "build" / "flutter"
    android_dir = flutter_dir / "android"

    # No modules enabled → single pass (same as non-android)
    if not _collect_onesignal_deps(onesignal_config):
        ui.build_info(f"Building {args.build_type.upper()}...")

        result = subprocess.run(cmd, cwd=project_root)

        if result.returncode == 0:
            _handle_success(args.build_type, project_root)
        else:
            ui.failure_panel(FAILURE_TIPS)

        sys.exit(result.returncode)

    # Modules enabled and gradle already configured → single pass
    if android_dir.exists() and _check_onesignal_modules(flutter_dir, onesignal_config):
        ui.build_info(
            f"Building {args.build_type.upper()} (OneSignal modules already configured)..."
        )

        result = subprocess.run(cmd, cwd=project_root)

        if result.returncode == 0:
            _handle_success(args.build_type, project_root)
        else:
            ui.failure_panel(FAILURE_TIPS)

        sys.exit(result.returncode)

    # Modules enabled but gradle not configured → first pass + inject + rebuild
    ui.build_info(f"Building {args.build_type.upper()} with OneSignal modules...")
    ui.step(1, "Creating Flutter project...")

    result = subprocess.run(cmd, cwd=project_root)

    if not android_dir.exists():
        ui.error_panel(
            "Flutter project not created",
            "  The Flutter project was not created. Check errors above.",
        )
        sys.exit(1)

    ui.step(2, "Injecting OneSignal module dependencies...")
    _inject_onesignal_modules(flutter_dir, onesignal_config)

    ui.step(3, "Rebuilding with OneSignal modules...")

    result = subprocess.run(cmd, cwd=project_root)

    if result.returncode == 0:
        _handle_success(args.build_type, project_root)
    else:
        ui.failure_panel(FAILURE_TIPS)

    sys.exit(result.returncode)


def _build_non_android(
    args: argparse.Namespace,
    cmd: list[str],
    project_root: Path,
) -> None:
    """Build for non-Android platforms (ipa, web, macos, linux, windows)."""
    ui.build_info(f"Building {args.build_type.upper()}...")

    result = subprocess.run(cmd, cwd=project_root)

    if result.returncode == 0:
        _handle_success(args.build_type, project_root)
    else:
        ui.failure_panel(FAILURE_TIPS)

    sys.exit(result.returncode)


def _handle_success(build_type: str, project_root: Path):
    """Handle successful build output."""
    output_dir = project_root / "build" / build_type
    ui.success_panel(
        build_type,
        str(output_dir) if output_dir.exists() else None,
        NEXT_STEPS.get(build_type, []),
    )


if __name__ == "__main__":
    main()
