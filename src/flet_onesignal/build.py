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
import shutil
import subprocess
import sys
from pathlib import Path

ALL_PLATFORMS = ["apk", "aab", "ipa", "web", "macos", "linux", "windows"]
ANDROID_PLATFORMS = {"apk", "aab"}


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
            print("  ✓ Modified: build.gradle.kts (root - added Google Services classpath)")
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
            print("  ✓ Modified: build.gradle.kts (app - added Google Services plugin)")
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
            print("  ✓ Modified: build.gradle (root)")
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
            print("  ✓ Modified: build.gradle (app)")
            modified = True

    # Copy google-services.json
    if app_dir.exists():
        dest = app_dir / "google-services.json"
        shutil.copy2(google_services_src, dest)
        print("  ✓ Copied: google-services.json to android/app/")
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

    print("\n" + "=" * 60)
    print("  FOS Build - Flet OneSignal Build Tool")
    print("=" * 60)

    # Find project root
    project_root = find_project_root()
    print(f"\nProject root: {project_root}")

    # Clean if requested
    if args.clean:
        build_dir = project_root / "build"
        if build_dir.exists():
            print(f"\nCleaning build directory: {build_dir}")
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
        print("\n⚠ WARNING: google-services.json not found!")
        print("  Firebase/Google Services will NOT be configured.")
        print(f"  Expected location: {project_root}/android/google-services.json")
        print("  Building without Firebase support...\n")

        result = subprocess.run(cmd, cwd=project_root)
        if result.returncode == 0:
            _print_success(args.build_type, project_root)
        else:
            _print_failure()
        sys.exit(result.returncode)

    print(f"Found: {google_services}")

    flutter_dir = project_root / "build" / "flutter"
    android_dir = flutter_dir / "android"

    # Check if Flutter project already exists with correct configuration
    if android_dir.exists() and check_gradle_configured(flutter_dir):
        print(f"\n{'=' * 60}")
        print(f"Building {args.build_type.upper()} (Firebase already configured)...")
        print(f"{'=' * 60}\n")

        result = subprocess.run(cmd, cwd=project_root)

        if result.returncode == 0:
            _print_success(args.build_type, project_root)
        else:
            _print_failure()

        sys.exit(result.returncode)

    # First build pass - create Flutter project structure
    print(f"\n{'=' * 60}")
    print(f"Building {args.build_type.upper()} with Firebase support...")
    print(f"{'=' * 60}")
    print("\nStep 1: Creating Flutter project...\n")

    result = subprocess.run(cmd, cwd=project_root)

    # Check if android directory was created
    if not android_dir.exists():
        print("\n  ✗ Flutter project was not created. Check errors above.")
        sys.exit(1)

    # Modify Gradle files
    print("\n" + "-" * 60)
    print("Step 2: Injecting Firebase/Google Services configuration...")
    print("-" * 60 + "\n")

    modify_gradle_files(flutter_dir, google_services)

    # Rebuild with Firebase config
    print("\n" + "-" * 60)
    print("Step 3: Rebuilding with Firebase configuration...")
    print("-" * 60 + "\n")

    result = subprocess.run(cmd, cwd=project_root)

    if result.returncode == 0:
        _print_success(args.build_type, project_root)
    else:
        _print_failure()

    sys.exit(result.returncode)


def _build_non_android(
    args: argparse.Namespace,
    cmd: list[str],
    project_root: Path,
) -> None:
    """Build for non-Android platforms (ipa, web, macos, linux, windows)."""
    print(f"\n{'=' * 60}")
    print(f"Building {args.build_type.upper()}...")
    print(f"{'=' * 60}\n")

    result = subprocess.run(cmd, cwd=project_root)

    if result.returncode == 0:
        _print_success(args.build_type, project_root)
    else:
        _print_failure()

    sys.exit(result.returncode)


def _print_success(build_type: str, project_root: Path):
    """Print success message with output location."""
    print("\n" + "=" * 60)
    print("  BUILD SUCCESSFUL!")
    print("=" * 60)

    output_dir = project_root / "build" / build_type
    if output_dir.exists():
        print(f"\nOutput: {output_dir}")

    next_steps = {
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

    steps = next_steps.get(build_type, [])
    if steps:
        print("\nNext steps:")
        for step in steps:
            print(f"  - {step}")


def _print_failure():
    """Print failure message."""
    print("\n" + "!" * 60)
    print("  BUILD FAILED")
    print("!" * 60)
    print("\nCheck the error messages above for details.")
    print("\nTips:")
    print("  - Try running with --clean to start fresh")
    print("  - Use -v or -vv for more verbose output")
    print("  - Run: flet build --show-platform-matrix")


if __name__ == "__main__":
    main()
