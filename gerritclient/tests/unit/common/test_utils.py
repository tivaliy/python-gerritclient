"""Tests for gerritclient.common.utils module."""

from gerritclient.common import utils


class TestUtils:
    """Tests for utility functions."""

    def test_get_display_data_single(self):
        columns = ("id", "name")
        data = {"id": 1, "name": "test_name"}
        assert utils.get_display_data_single(fields=columns, data=data) == [
            1,
            "test_name",
        ]

    def test_get_display_data_single_with_non_existent_field(self):
        columns = ("id", "name", "non-existent")
        data = {"id": 1, "name": "test_name"}
        assert utils.get_display_data_single(fields=columns, data=data) == [
            1,
            "test_name",
            None,
        ]

    def test_get_display_data_multi_wo_sorting(self):
        columns = ("id", "name")
        data = [{"id": 1, "name": "test_name_1"}, {"id": 2, "name": "test_name_2"}]
        assert utils.get_display_data_multi(fields=columns, data=data) == [
            [1, "test_name_1"],
            [2, "test_name_2"],
        ]

    def test_get_display_data_multi_w_sorting(self):
        columns = ("id", "name", "severity_level")
        data = [
            {"id": 3, "name": "twitter", "severity_level": "error"},
            {"id": 15, "name": "google", "severity_level": "warning"},
            {"id": 2, "name": "amazon", "severity_level": "error"},
            {"id": 17, "name": "facebook", "severity_level": "note"},
        ]
        # by single field
        assert utils.get_display_data_multi(
            fields=columns, data=data, sort_by=["name"]
        ) == [
            [2, "amazon", "error"],
            [17, "facebook", "note"],
            [15, "google", "warning"],
            [3, "twitter", "error"],
        ]
        # by multiple fields
        assert utils.get_display_data_multi(
            fields=columns, data=data, sort_by=["severity_level", "id"]
        ) == [
            [2, "amazon", "error"],
            [3, "twitter", "error"],
            [17, "facebook", "note"],
            [15, "google", "warning"],
        ]

    def test_normalize(self):
        assert utils.normalize("#/foo+bar_$!str.", "") == "foobarstr."

    def test_normalize_w_default_replacer(self):
        assert utils.normalize("#Some/foo+bar_$!str.") == "_Some_foo_bar___str."
