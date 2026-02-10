#!/usr/bin/env python
"""
Automated build script for Flet apps with OneSignal/Firebase support.

This script automates the process of building Flet apps for all platforms.
For Android builds (apk/aab), it automatically injects Firebase/Google Services
configuration required for OneSignal push notifications.

Supported platforms: apk, aab, ipa, web, macos, linux, windows

Usage:
    # Android (with automatic Firebase injection):
    fos-build apk
    fos-build aab --split-per-abi

    # iOS / Web / Desktop:
    fos-build ipa
    fos-build web
    fos-build macos
    fos-build linux
    fos-build windows

    # All flet build options are passed through:
    fos-build apk -v --org com.example --build-version 1.0.0

Requirements (Android only):
    - google-services.json in your project's android/ folder
    - Service Account JSON uploaded to OneSignal Dashboard
"""

import argparse
import json
import re
import shutil
import subprocess
import sys
import tomllib
import unicodedata
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


def find_google_services_json(project_root: Path) -> Path | None:
    """Find google-services.json in the project."""
    possible_paths = [
        project_root / "android" / "google-services.json",
        project_root / "google-services.json",
    ]

    for path in possible_paths:
        if path.exists():
            return path

    return None


def modify_gradle_files(flutter_dir: Path, google_services_src: Path) -> bool:
    """Modify Gradle files to add Google Services support."""
    android_dir = flutter_dir / "android"
    app_dir = android_dir / "app"

    if not android_dir.exists():
        return False

    modified = False

    # Check for Kotlin DSL
    root_kts = android_dir / "build.gradle.kts"
    app_kts = app_dir / "build.gradle.kts"

    # Check for Groovy DSL
    root_gradle = android_dir / "build.gradle"
    app_gradle = app_dir / "build.gradle"

    # Modify root build.gradle.kts (Kotlin DSL)
    if root_kts.exists():
        content = root_kts.read_text()
        if "com.google.gms:google-services" not in content:
            buildscript = """buildscript {
    repositories {
        google()
        mavenCentral()
    }
    dependencies {
        classpath("com.google.gms:google-services:4.4.2")
    }
}

"""
            root_kts.write_text(buildscript + content)
            ui.modified("Modified: build.gradle.kts (root - added Google Services classpath)")
            modified = True

    # Modify app build.gradle.kts (Kotlin DSL)
    if app_kts.exists():
        content = app_kts.read_text()
        if 'id("com.google.gms.google-services")' not in content:
            content = content.replace(
                'id("dev.flutter.flutter-gradle-plugin")',
                'id("dev.flutter.flutter-gradle-plugin")\n    id("com.google.gms.google-services")',
            )
            app_kts.write_text(content)
            ui.modified("Modified: build.gradle.kts (app - added Google Services plugin)")
            modified = True

    # Modify root build.gradle (Groovy DSL) - only if .kts doesn't exist
    if root_gradle.exists() and not root_kts.exists():
        content = root_gradle.read_text()
        if "com.google.gms:google-services" not in content:
            content = content.replace(
                "classpath 'com.android.tools.build:gradle:",
                "classpath 'com.google.gms:google-services:4.4.2'\n        classpath 'com.android.tools.build:gradle:",
            )
            root_gradle.write_text(content)
            ui.modified("Modified: build.gradle (root)")
            modified = True

    # Modify app build.gradle (Groovy DSL) - only if .kts doesn't exist
    if app_gradle.exists() and not app_kts.exists():
        content = app_gradle.read_text()
        if "com.google.gms.google-services" not in content:
            if "plugins {" in content:
                content = content.replace(
                    'id "dev.flutter.flutter-gradle-plugin"',
                    'id "dev.flutter.flutter-gradle-plugin"\n    id "com.google.gms.google-services"',
                )
            else:
                content += "\napply plugin: 'com.google.gms.google-services'\n"
            app_gradle.write_text(content)
            ui.modified("Modified: build.gradle (app)")
            modified = True

    # Copy google-services.json
    if app_dir.exists():
        dest = app_dir / "google-services.json"
        shutil.copy2(google_services_src, dest)
        ui.modified("Copied: google-services.json to android/app/")
        modified = True

    return modified


def check_gradle_configured(flutter_dir: Path) -> bool:
    """Check if Gradle files are already configured for Google Services."""
    android_dir = flutter_dir / "android"
    app_dir = android_dir / "app"

    root_kts = android_dir / "build.gradle.kts"
    app_kts = app_dir / "build.gradle.kts"

    if root_kts.exists() and app_kts.exists():
        root_content = root_kts.read_text()
        app_content = app_kts.read_text()

        has_classpath = "com.google.gms:google-services" in root_content
        has_plugin = 'id("com.google.gms.google-services")' in app_content

        return has_classpath and has_plugin

    return False


def _slugify(value: str) -> str:
    """Slugify a string (same logic as flet.utils.slugify)."""
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^\w\s-]", "", value).strip().lower()
    return re.sub(r"[-_\s]+", "-", value).strip("-")


def _get_google_services_package_names(path: Path) -> list[str]:
    """Extract all package names from a google-services.json file."""
    data = json.loads(path.read_text())
    names = []
    for client in data.get("client", []):
        pkg = client.get("client_info", {}).get("android_client_info", {}).get("package_name")
        if pkg:
            names.append(pkg)
    return names


def _get_expected_package_name(project_root: Path, extra_args: list[str]) -> str | None:
    """Determine the package name the app will use (same priority as flet CLI)."""
    # Parse extra_args for --bundle-id and --org
    bundle_id = None
    org_arg = None
    for i, arg in enumerate(extra_args):
        if arg == "--bundle-id" and i + 1 < len(extra_args):
            bundle_id = extra_args[i + 1]
        elif arg.startswith("--bundle-id="):
            bundle_id = arg.split("=", 1)[1]
        elif arg == "--org" and i + 1 < len(extra_args):
            org_arg = extra_args[i + 1]
        elif arg.startswith("--org="):
            org_arg = arg.split("=", 1)[1]

    # Priority 1: --bundle-id from CLI
    if bundle_id:
        return bundle_id

    # Read pyproject.toml
    pyproject_path = project_root / "pyproject.toml"
    if not pyproject_path.exists():
        return None

    with open(pyproject_path, "rb") as f:
        pyproject = tomllib.load(f)

    tool_flet = pyproject.get("tool", {}).get("flet", {})

    # Priority 2: tool.flet.android.bundle_id or tool.flet.bundle_id
    flet_bundle_id = tool_flet.get("android", {}).get("bundle_id") or tool_flet.get("bundle_id")
    if flet_bundle_id:
        return flet_bundle_id

    # Priority 3/4: org + project_name
    org = org_arg or tool_flet.get("android", {}).get("org") or tool_flet.get("org")
    if not org:
        return None

    project_name = pyproject.get("project", {}).get("name")
    if not project_name:
        return None

    project_name = _slugify(project_name).replace("-", "_")
    return f"{org}.{project_name}"


def _validate_google_services(
    google_services: Path, project_root: Path, extra_args: list[str]
) -> bool:
    """Validate that the app's package name matches google-services.json."""
    expected = _get_expected_package_name(project_root, extra_args)
    if not expected:
        return True  # Can't determine, skip validation

    gs_packages = _get_google_services_package_names(google_services)
    if not gs_packages:
        return True  # No packages in file, skip validation

    if expected in gs_packages:
        return True

    body = (
        f"  App package name:     {expected}\n"
        f"  google-services.json: {', '.join(gs_packages)}\n\n"
        "  The package name generated by your app does not match any\n"
        "  package registered in google-services.json.\n"
        "  Gradle will fail with 'No matching client found'.\n\n"
        "  Package name = org + project_name\n"
        "  (from pyproject.toml [tool.flet] org + [project] name)\n\n"
        "  To fix, choose one:\n"
        f"    1. Change [tool.flet] org in pyproject.toml so that\n"
        f"       org + project_name = {gs_packages[0]}\n"
        "    2. Download a new google-services.json from Firebase Console\n"
        f"       with package name: {expected}\n"
        f"    3. Use --bundle-id {gs_packages[0]} to override"
    )
    ui.error_panel("PACKAGE NAME MISMATCH", body)
    return False


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Build Flet app with OneSignal/Firebase support",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    fos-build apk              Build Android APK (with Firebase injection)
    fos-build aab              Build Android App Bundle
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
    Android builds (apk/aab) automatically inject Firebase/Google Services.
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
        _build_android_with_firebase(args, cmd, project_root)
    else:
        _build_non_android(args, cmd, project_root)


def _build_android_with_firebase(
    args: argparse.Namespace,
    cmd: list[str],
    project_root: Path,
) -> None:
    """Build Android APK/AAB with automatic Firebase/Google Services injection."""
    google_services = find_google_services_json(project_root)
    if not google_services:
        body = (
            f"  Expected location:\n"
            f"    {project_root}/android/google-services.json\n\n"
            f"  This file is required for Android builds with Firebase/OneSignal.\n"
            f"  Download it from the Firebase Console:\n"
            f"    Project Settings > Your Android app > google-services.json"
        )
        ui.error_panel("MISSING google-services.json", body)
        sys.exit(1)

    ui.info("Found", str(google_services))

    # Validate package name before starting the build
    extra_args = cmd[3:]  # skip ["flet", "build", "<platform>"]
    if not _validate_google_services(google_services, project_root, extra_args):
        sys.exit(1)

    flutter_dir = project_root / "build" / "flutter"
    android_dir = flutter_dir / "android"

    # Check if Flutter project already exists with correct configuration
    if android_dir.exists() and check_gradle_configured(flutter_dir):
        ui.build_info(f"Building {args.build_type.upper()} (Firebase already configured)...")

        result = subprocess.run(cmd, cwd=project_root)

        if result.returncode == 0:
            _handle_success(args.build_type, project_root)
        else:
            ui.failure_panel(FAILURE_TIPS)

        sys.exit(result.returncode)

    # First build pass - create Flutter project structure
    ui.build_info(f"Building {args.build_type.upper()} with Firebase support...")
    ui.step(1, "Creating Flutter project...")

    result = subprocess.run(cmd, cwd=project_root)

    # Check if android directory was created
    if not android_dir.exists():
        ui.error_panel(
            "Flutter project not created",
            "  The Flutter project was not created. Check errors above.",
        )
        sys.exit(1)

    # Modify Gradle files
    ui.step(2, "Injecting Firebase/Google Services configuration...")

    modify_gradle_files(flutter_dir, google_services)

    # Rebuild with Firebase config
    ui.step(3, "Rebuilding with Firebase configuration...")

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
