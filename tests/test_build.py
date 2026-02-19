"""Tests for flet_onesignal.build — pure functions and tmp_path-based I/O."""

import textwrap

from flet_onesignal.build import (
    _PROGUARD_MARKER,
    _check_onesignal_modules,
    _collect_onesignal_deps,
    _get_onesignal_config,
    _inject_dep_line,
    _inject_onesignal_modules,
    _inject_proguard_rules,
)

# ---------------------------------------------------------------------------
# _collect_onesignal_deps
# ---------------------------------------------------------------------------


class TestCollectOnesignalDeps:
    def test_empty_config(self):
        assert _collect_onesignal_deps({}) == []

    def test_location_false(self):
        assert _collect_onesignal_deps({"location": False}) == []

    def test_location_true(self):
        deps = _collect_onesignal_deps({"location": True})
        assert len(deps) == 2
        assert deps[0] == ("com.onesignal:location", "[5.0.0, 5.99.99]")
        assert deps[1] == ("com.google.android.gms:play-services-location", "18.0.0")

    def test_unknown_key_ignored(self):
        assert _collect_onesignal_deps({"unknown_module": True}) == []


# ---------------------------------------------------------------------------
# _inject_dep_line
# ---------------------------------------------------------------------------


class TestInjectDepLine:
    def test_multiline_block(self):
        content = textwrap.dedent("""\
            dependencies {
                implementation "existing:lib:1.0"
            }
        """)
        result = _inject_dep_line(content, '    implementation "new:lib:2.0"')
        assert '    implementation "new:lib:2.0"' in result
        assert result.index("existing:lib:1.0") < result.index("new:lib:2.0")

    def test_singleline_empty_block(self):
        content = "dependencies { }"
        result = _inject_dep_line(content, '    implementation "new:lib:2.0"')
        assert '    implementation "new:lib:2.0"' in result

    def test_no_dependencies_block(self):
        content = "plugins {\n    id 'com.android.application'\n}\n"
        result = _inject_dep_line(content, '    implementation "new:lib:2.0"')
        assert result == content  # unchanged


# ---------------------------------------------------------------------------
# _get_onesignal_config
# ---------------------------------------------------------------------------


class TestGetOnesignalConfig:
    def test_with_onesignal_section(self, tmp_path):
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text(textwrap.dedent("""\
            [tool.flet.onesignal.android]
            location = true
        """))
        assert _get_onesignal_config(tmp_path) == {"location": True}

    def test_without_onesignal_section(self, tmp_path):
        pyproject = tmp_path / "pyproject.toml"
        pyproject.write_text(textwrap.dedent("""\
            [project]
            name = "my-app"
        """))
        assert _get_onesignal_config(tmp_path) == {}

    def test_missing_pyproject(self, tmp_path):
        assert _get_onesignal_config(tmp_path) == {}


# ---------------------------------------------------------------------------
# _inject_onesignal_modules
# ---------------------------------------------------------------------------


class TestInjectOnesignalModules:
    def _make_gradle(self, flutter_dir, kts=True):
        """Create a minimal gradle file structure under flutter_dir."""
        app_dir = flutter_dir / "android" / "app"
        app_dir.mkdir(parents=True)
        gradle = app_dir / ("build.gradle.kts" if kts else "build.gradle")
        gradle.write_text(textwrap.dedent("""\
            plugins {
                id("com.android.application")
            }
            dependencies {
                implementation("existing:lib:1.0")
            }
        """))
        return gradle

    def test_inject_kts(self, tmp_path):
        gradle = self._make_gradle(tmp_path, kts=True)
        config = {"location": True}
        assert _inject_onesignal_modules(tmp_path, config) is True
        content = gradle.read_text()
        assert "com.onesignal:location" in content
        assert "play-services-location" in content

    def test_inject_groovy(self, tmp_path):
        gradle = self._make_gradle(tmp_path, kts=False)
        config = {"location": True}
        assert _inject_onesignal_modules(tmp_path, config) is True
        content = gradle.read_text()
        assert "com.onesignal:location" in content
        assert "play-services-location" in content

    def test_already_injected(self, tmp_path):
        self._make_gradle(tmp_path, kts=True)
        config = {"location": True}
        _inject_onesignal_modules(tmp_path, config)
        # Second call should not modify
        assert _inject_onesignal_modules(tmp_path, config) is False

    def test_no_android_dir(self, tmp_path):
        assert _inject_onesignal_modules(tmp_path, {"location": True}) is False

    def test_empty_config(self, tmp_path):
        self._make_gradle(tmp_path)
        assert _inject_onesignal_modules(tmp_path, {}) is False


# ---------------------------------------------------------------------------
# _inject_proguard_rules
# ---------------------------------------------------------------------------


class TestInjectProguardRules:
    def test_creates_proguard_file(self, tmp_path):
        app_dir = tmp_path / "app"
        app_dir.mkdir()
        _inject_proguard_rules(app_dir)
        proguard = app_dir / "proguard-rules.pro"
        assert proguard.exists()
        assert _PROGUARD_MARKER in proguard.read_text()

    def test_appends_to_existing(self, tmp_path):
        app_dir = tmp_path / "app"
        app_dir.mkdir()
        proguard = app_dir / "proguard-rules.pro"
        proguard.write_text("# existing rules\n")
        _inject_proguard_rules(app_dir)
        content = proguard.read_text()
        assert "# existing rules" in content
        assert _PROGUARD_MARKER in content

    def test_no_duplicate(self, tmp_path):
        app_dir = tmp_path / "app"
        app_dir.mkdir()
        _inject_proguard_rules(app_dir)
        content_first = (app_dir / "proguard-rules.pro").read_text()
        _inject_proguard_rules(app_dir)
        content_second = (app_dir / "proguard-rules.pro").read_text()
        assert content_first == content_second

    def test_adds_proguard_ref_to_gradle_kts(self, tmp_path):
        app_dir = tmp_path / "app"
        app_dir.mkdir()
        kts = app_dir / "build.gradle.kts"
        kts.write_text(textwrap.dedent("""\
            android {
                buildTypes {
                    release {
                        signingConfig = signingConfigs
                    }
                }
            }
        """))
        _inject_proguard_rules(app_dir)
        assert "proguard-rules.pro" in kts.read_text()


# ---------------------------------------------------------------------------
# _check_onesignal_modules
# ---------------------------------------------------------------------------


class TestCheckOnesignalModules:
    def test_all_present(self, tmp_path):
        app_dir = tmp_path / "android" / "app"
        app_dir.mkdir(parents=True)
        gradle = app_dir / "build.gradle.kts"
        gradle.write_text(textwrap.dedent("""\
            dependencies {
                implementation("com.onesignal:location:[5.0.0, 5.99.99]")
                implementation("com.google.android.gms:play-services-location:18.0.0")
            }
        """))
        proguard = app_dir / "proguard-rules.pro"
        proguard.write_text(_PROGUARD_MARKER)
        assert _check_onesignal_modules(tmp_path, {"location": True}) is True

    def test_module_missing(self, tmp_path):
        app_dir = tmp_path / "android" / "app"
        app_dir.mkdir(parents=True)
        gradle = app_dir / "build.gradle.kts"
        gradle.write_text("dependencies {\n}\n")
        assert _check_onesignal_modules(tmp_path, {"location": True}) is False

    def test_proguard_missing(self, tmp_path):
        app_dir = tmp_path / "android" / "app"
        app_dir.mkdir(parents=True)
        gradle = app_dir / "build.gradle.kts"
        gradle.write_text(textwrap.dedent("""\
            dependencies {
                implementation("com.onesignal:location:[5.0.0, 5.99.99]")
                implementation("com.google.android.gms:play-services-location:18.0.0")
            }
        """))
        assert _check_onesignal_modules(tmp_path, {"location": True}) is False

    def test_no_gradle_file(self, tmp_path):
        app_dir = tmp_path / "android" / "app"
        app_dir.mkdir(parents=True)
        assert _check_onesignal_modules(tmp_path, {"location": True}) is True

    def test_no_android_dir(self, tmp_path):
        assert _check_onesignal_modules(tmp_path, {"location": True}) is True

    def test_empty_config(self, tmp_path):
        app_dir = tmp_path / "android" / "app"
        app_dir.mkdir(parents=True)
        gradle = app_dir / "build.gradle.kts"
        gradle.write_text("dependencies {\n}\n")
        assert _check_onesignal_modules(tmp_path, {}) is True
