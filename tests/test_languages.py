"""Tests for flet_onesignal.languages — Language enum."""

from flet_onesignal.languages import Language


class TestLanguageEnum:
    def test_english(self):
        assert Language.ENGLISH.value == "en"

    def test_portuguese(self):
        assert Language.PORTUGUESE.value == "pt"

    def test_all_values_are_nonempty_strings(self):
        for member in Language:
            assert isinstance(member.value, str)
            assert len(member.value) > 0

    def test_no_duplicate_values_among_canonical_members(self):
        values = [m.value for m in Language]
        assert len(set(values)) == len(values)
