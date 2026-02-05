#!/usr/bin/env python
"""
Automated build script for Flet apps with OneSignal/Firebase support.

This script automates the process of building Android APK/AAB with Firebase
configuration, which is required for OneSignal push notifications.

Usage:
    # From your Flet project directory:
    fos-build apk
    fos-build aab

Requirements:
    - google-services.json in your project's android/ folder
    - Service Account JSON uploaded to OneSignal Dashboard
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


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
    fos-build apk          Build Android APK
    fos-build aab          Build Android App Bundle
    fos-build apk -v       Build with verbose output
    fos-build apk --clean  Clean build directory first

Requirements:
    1. Place google-services.json in your project's android/ folder
    2. Upload Service Account JSON to OneSignal Dashboard
        """,
    )
    parser.add_argument(
        "build_type", choices=["apk", "aab"], help="Type of Android build (apk or aab)"
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument(
        "--clean", action="store_true", help="Clean build directory before building"
    )

    args = parser.parse_args()

    print("\n" + "=" * 60)
    print("  FOS Build - Flet OneSignal Build Tool")
    print("=" * 60)

    # Find project root
    project_root = find_project_root()
    print(f"\nProject root: {project_root}")

    # Check for google-services.json
    google_services = find_google_services_json(project_root)
    if not google_services:
        print("\n" + "!" * 60)
        print("ERROR: google-services.json not found!")
        print("!" * 60)
        print("\nPlease place google-services.json in your project's android/ folder:")
        print(f"  {project_root}/android/google-services.json")
        print("\nTo get this file:")
        print("  1. Go to Firebase Console (https://console.firebase.google.com/)")
        print("  2. Select your project")
        print("  3. Go to Project Settings > General")
        print("  4. Download google-services.json for your Android app")
        sys.exit(1)

    print(f"Found: {google_services}")

    # Clean if requested
    if args.clean:
        build_dir = project_root / "build"
        if build_dir.exists():
            print(f"\nCleaning build directory: {build_dir}")
            shutil.rmtree(build_dir)

    flutter_dir = project_root / "build" / "flutter"
    android_dir = flutter_dir / "android"

    # Build command
    cmd = ["flet", "build", args.build_type]
    if args.verbose:
        cmd.append("-v")

    # Check if Flutter project already exists with correct configuration
    if android_dir.exists() and check_gradle_configured(flutter_dir):
        print(f"\n{'=' * 60}")
        print(f"Building {args.build_type.upper()} (Firebase already configured)...")
        print(f"{'=' * 60}\n")

        # Just run the build
        result = subprocess.run(cmd, cwd=project_root)

        if result.returncode == 0:
            _print_success(args.build_type, project_root, flutter_dir)
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

    # Even if first build succeeded, we need to rebuild with Firebase config
    print("\n" + "-" * 60)
    print("Step 3: Rebuilding with Firebase configuration...")
    print("-" * 60 + "\n")

    result = subprocess.run(cmd, cwd=project_root)

    if result.returncode == 0:
        _print_success(args.build_type, project_root, flutter_dir)
    else:
        _print_failure()

    sys.exit(result.returncode)


def _print_success(build_type: str, project_root: Path, flutter_dir: Path):
    """Print success message with output location."""
    print("\n" + "=" * 60)
    print("  BUILD SUCCESSFUL!")
    print("=" * 60)

    # Find output file
    if build_type == "apk":
        output = project_root / "build" / "apk" / "app-release.apk"
        if not output.exists():
            output = flutter_dir / "build" / "app" / "outputs" / "flutter-apk" / "app-release.apk"
    else:
        output = project_root / "build" / "aab" / "app-release.aab"
        if not output.exists():
            output = (
                flutter_dir / "build" / "app" / "outputs" / "bundle" / "release" / "app-release.aab"
            )

    if output.exists():
        print(f"\nOutput: {output}")

    print("\nNext steps:")
    print("  1. Install on device: adb install <path-to-apk>")
    print("  2. Or upload to Play Store (for .aab)")


def _print_failure():
    """Print failure message."""
    print("\n" + "!" * 60)
    print("  BUILD FAILED")
    print("!" * 60)
    print("\nCheck the error messages above for details.")
    print("\nTips:")
    print("  - Try running with --clean to start fresh")
    print("  - Check if google-services.json is valid")


if __name__ == "__main__":
    main()
