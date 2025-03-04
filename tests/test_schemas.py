from datetime import datetime

import pytest

from formula1_race_analysis import AbbreviationEntry, InvalidFormatDataError, InvalidNameFormatError, LogEntry


class TestAbbreviationEntry:
    def test_valid_entry(self) -> None:
        # Given
        given_entry = "PGS_Pierre Gasly_SCUDERIA TORO ROSSO HONDA\n"
        # When
        parsed_entry = AbbreviationEntry.model_validate(given_entry)
        # Then
        assert parsed_entry.id == "PGS"
        assert parsed_entry.name == "Pierre Gasly"
        assert parsed_entry.car_model == "SCUDERIA TORO ROSSO HONDA"

    def test_format_driver_name(self) -> None:
        # Given
        given_entry = "PGS_pierre gasly_SCUDERIA TORO ROSSO HONDA\n"
        # When
        parsed_entry = AbbreviationEntry.model_validate(given_entry)
        # Then
        assert parsed_entry.name == "Pierre Gasly"

    def test_invalid_driver_name(self) -> None:
        # Given
        given_entry = "PGS_pierregasly_SCUDERIA TORO ROSSO HONDA\n"
        _, invalid_name, _ = AbbreviationEntry.parse_entry(given_entry)
        # When / Then
        with pytest.raises(
            InvalidNameFormatError,
            match=f"Error! Incorrect name format: '{invalid_name}'. Enter a name and lastname of driver.",
        ):
            AbbreviationEntry.format_driver_name(invalid_name)

    def format_data_from_log_file_with_correct_timestamp(self) -> None:
        # Given
        given_timestamp = "SVF_2018-05-24_12:14:12.054"
        expected_result = {"id": "SVF", "timestamp": datetime(2018, 5, 24, 12, 14, 12, 54000)}
        # When
        actual_result = LogEntry.model_validate(given_timestamp)
        # Then
        assert actual_result == expected_result

    def format_data_from_log_file_with_invalid_timestamp(self) -> None:
        # Given
        invalid_entry = "2018/05/24 12:14:12"
        # When / Then
        with pytest.raises(InvalidFormatDataError, match=f"Error! Incorrect data format: '{invalid_entry}'."):
            LogEntry.parse_entry(invalid_entry)
