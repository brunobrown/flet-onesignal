"""Tests for flet_onesignal.console — log parsing, tail, and log path."""

import flet as ft
import pytest

from flet_onesignal.console import LogLevel, _parse_log_line, _tail_file, get_log_path

# ---------------------------------------------------------------------------
# LogLevel.from_string
# ---------------------------------------------------------------------------


class TestLogLevelFromString:
    @pytest.mark.parametrize(
        "input_str, expected",
        [
            ("DEBUG", LogLevel.DEBUG),
            ("INFO", LogLevel.INFO),
            ("WARNING", LogLevel.WARNING),
            ("ERROR", LogLevel.ERROR),
            ("CRITICAL", LogLevel.CRITICAL),
        ],
    )
    def test_uppercase(self, input_str, expected):
        assert LogLevel.from_string(input_str) is expected

    @pytest.mark.parametrize("input_str", ["debug", "info", "warning", "error", "critical"])
    def test_case_insensitive(self, input_str):
        assert LogLevel.from_string(input_str) is LogLevel.from_string(input_str.upper())

    def test_invalid_returns_info(self):
        assert LogLevel.from_string("invalid") is LogLevel.INFO
        assert LogLevel.from_string("") is LogLevel.INFO


# ---------------------------------------------------------------------------
# LogLevel.color
# ---------------------------------------------------------------------------


class TestLogLevelColor:
    def test_each_level_has_color(self):
        expected = {
            LogLevel.DEBUG: ft.Colors.GREY_600,
            LogLevel.INFO: ft.Colors.BLUE_600,
            LogLevel.WARNING: ft.Colors.AMBER_700,
            LogLevel.ERROR: ft.Colors.RED_600,
            LogLevel.CRITICAL: ft.Colors.RED_900,
        }
        for level, color in expected.items():
            assert level.color == color


# ---------------------------------------------------------------------------
# _parse_log_line
# ---------------------------------------------------------------------------


class TestParseLogLine:
    def test_valid_format(self):
        line = "[12:30:45] [WARNING] mymodule - something went wrong"
        timestamp, level, message = _parse_log_line(line)
        assert timestamp == "12:30:45"
        assert level is LogLevel.WARNING
        assert message == "something went wrong"

    def test_no_separator(self):
        line = "[12:30:45] [ERROR] no separator here"
        timestamp, level, message = _parse_log_line(line)
        assert timestamp == "12:30:45"
        assert level is LogLevel.ERROR
        assert "no separator here" in message

    def test_malformed_fallback(self):
        line = "just a plain line"
        timestamp, level, message = _parse_log_line(line)
        assert level is LogLevel.INFO
        assert message == "just a plain line"


# ---------------------------------------------------------------------------
# _tail_file
# ---------------------------------------------------------------------------


class TestTailFile:
    def test_last_n_lines(self, tmp_path):
        f = tmp_path / "test.log"
        f.write_text("\n".join(f"line{i}" for i in range(10)) + "\n")
        result = _tail_file(str(f), 5)
        assert len(result) == 5
        assert result[-1] == "line9"

    def test_empty_file(self, tmp_path):
        f = tmp_path / "empty.log"
        f.write_text("")
        assert _tail_file(str(f), 5) == []

    def test_fewer_lines_than_requested(self, tmp_path):
        f = tmp_path / "short.log"
        f.write_text("one\ntwo\nthree\n")
        result = _tail_file(str(f), 10)
        assert len(result) == 3

    def test_nonexistent_file(self, tmp_path):
        assert _tail_file(str(tmp_path / "nope.log"), 5) == []


# ---------------------------------------------------------------------------
# get_log_path
# ---------------------------------------------------------------------------


class TestGetLogPath:
    def test_env_var_set(self, monkeypatch):
        monkeypatch.setenv("FLET_APP_CONSOLE", "/custom/log.txt")
        assert get_log_path() == "/custom/log.txt"

    def test_env_var_unset(self, monkeypatch):
        monkeypatch.delenv("FLET_APP_CONSOLE", raising=False)
        path = get_log_path()
        assert isinstance(path, str)
        assert len(path) > 0
