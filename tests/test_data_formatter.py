from datetime import datetime

import pytest

from formula1_race_analysis import InvalidFormatDataError, convert_timestamp_to_seconds


class TestDataFormatter:
    def test_convert_correct_timestamp_to_seconds(self) -> None:
        # Given
        timestamp = {"SVF": "2018-05-24_12:14:12.054"}
        expected_result = {"SVF": datetime(2018, 5, 24, 12, 14, 12, 54000)}
        # When
        actual_result = convert_timestamp_to_seconds(timestamp)
        # Then
        assert actual_result == expected_result

    def test_convert_invalid_timestamp_to_seconds(self) -> None:
        # Given
        invalid_timestamp = {"SVF": "2018/05/24 12:14:12"}
        timestamp = next(iter(invalid_timestamp.values()))
        # When / Then
        with pytest.raises(
            InvalidFormatDataError,
            match=f"The timestamp format: '{timestamp}' is incorrect. Expected format: YYYY-MM-DD_HH:MM:SS.sss",
        ):
            convert_timestamp_to_seconds(invalid_timestamp)
