import re
from pathlib import Path

import pytest

from formula1_race_analysis import (
    CustomFileNotFoundError,
    CustomInvalidFormatDataError,
    CustomInvalidRaceTimeError,
    CustomMissedTimestampError,
    Driver,
    display_race_report,
    parse_abbreviation_file,
)
from formula1_race_analysis.q1_session_analyzer import (
    calculate_race_duration,
    convert_timestamp_to_seconds,
    get_results_of_first_qualifying_session,
    parse_log_file,
)


class TestDriverDataBase:
    def test_parse_abbreviation_file_with_correct_data(self, prepare_correct_data: Path) -> None:
        # Given
        tmp_abbreviations_file = prepare_correct_data / "abbreviations.txt"
        expected_result = [
            Driver(driver_id="PGS", driver_name="Pierre Gasly", car_model="SCUDERIA TORO ROSSO HONDA"),
            Driver(driver_id="KMH", driver_name="Kevin Magnussen", car_model="HAAS FERRARI"),
            Driver(driver_id="FAM", driver_name="Fernando Alonso", car_model="MCLAREN RENAULT"),
        ]
        # When
        actual_result = parse_abbreviation_file(tmp_abbreviations_file)
        # Then
        assert actual_result == expected_result

    def test_parse_abbreviation_file_with_invalid_data(self, prepare_invalid_data: Path) -> None:
        # Given
        tmp_invalid_abbreviations_file = prepare_invalid_data / "invalid_abbreviations.txt"
        # When / Then
        with pytest.raises(
            CustomInvalidFormatDataError,
            match=re.escape(f"Error! Incorrect data format in file: {tmp_invalid_abbreviations_file}."),
        ):
            parse_abbreviation_file(tmp_invalid_abbreviations_file)

    def test_parse_log_file_with_correct_data(self, prepare_correct_data: Path) -> None:
        # Given
        tmp_start_log = prepare_correct_data / "start.log"
        expected_result = {
            "FAM": "2018-05-24_12:13:04.512",
            "KMH": "2018-05-24_12:02:51.003",
            "PGS": "2018-05-24_12:07:23.645",
        }
        # When
        actual_result = parse_log_file(tmp_start_log)
        # Then
        assert actual_result == expected_result

    def test_parse_log_file_with_invalid_data(self, prepare_invalid_data: Path) -> None:
        # Given
        tmp_invalid_start_log = prepare_invalid_data / "invalid_start.log"
        # When / Then
        with pytest.raises(
            CustomInvalidFormatDataError,
            match=re.escape(f"Error! Incorrect data format in file: {tmp_invalid_start_log}."),
        ):
            parse_log_file(tmp_invalid_start_log)

    def test_parse_log_file_when_file_is_missing(self, prepare_invalid_data: Path) -> None:
        # Given
        tmp_missing_log = prepare_invalid_data / "tmp_missing.log"
        # When / Then
        with pytest.raises(
            CustomFileNotFoundError,
            match=re.escape(f"Error! The file path: {tmp_missing_log} is not found or cannot be opened."),
        ):
            parse_log_file(tmp_missing_log)

    def test_convert_correct_timestamp_to_seconds(self) -> None:
        # Given
        timestamp = "2018-05-24_12:14:12.054"
        seconds_per_hour = 3600
        seconds_per_minute = 60
        expected_result = 12 * seconds_per_hour + 14 * seconds_per_minute + 12 + 0.054
        # When
        actual_result = convert_timestamp_to_seconds(timestamp)
        # Then
        assert actual_result == expected_result

    def test_convert_invalid_timestamp_to_seconds(self) -> None:
        # Given
        invalid_timestamp = "2018/05/24 12:14:12"
        # When / Then
        with pytest.raises(
            CustomInvalidFormatDataError,
            match=f"The timestamp format: '{invalid_timestamp}' is incorrect. Expected format: YYYY-MM-DD_HH:MM:SS.sss",
        ):
            convert_timestamp_to_seconds(invalid_timestamp)

    def test_calculate_race_duration_with_raises_custom_invalid_race_time_error(self) -> None:
        # Given
        database = [
            Driver(driver_id="DRR", driver_name="Daniel Ricciardo", car_model="RED BULL RACING TAG HEUER"),
        ]
        database[0].start_time = "2018-05-24_12:14:12.054"
        database[0].end_time = "2018-05-24_12:11:24.067"
        # When / Then
        with pytest.raises(
            CustomInvalidRaceTimeError,
            match=(f"Race time error for driver: '{database[0].driver_name}'. Start time is greater than end time."),
        ):
            calculate_race_duration(database)

    def test_calculate_race_duration_missing_timestamp(self) -> None:
        # Given
        database = [
            Driver(driver_id="DRR", driver_name="Daniel Ricciardo", car_model="RED BULL RACING TAG HEUER"),
        ]
        database[0].start_time = None
        database[0].end_time = "2018-05-24_12:11:24.067"
        # When / Then
        with pytest.raises(
            CustomMissedTimestampError,
            match=(
                f"Error! Missing timestamp for driver: '{database[0].driver_name}'. Start or end time is not provided."
            ),
        ):
            calculate_race_duration(database)

    def test_display_race_report_with_success(
        self,
        prepare_correct_data: Path,
    ) -> None:
        # Given
        database = get_results_of_first_qualifying_session(prepare_correct_data)
        # When
        report = display_race_report(database)
        # Then
        assert "1. Fernando Alonso | MCLAREN RENAULT | 1:12.657" in report
        assert "2. Pierre Gasly | SCUDERIA TORO ROSSO HONDA | 1:12.941" in report
        assert "3. Kevin Magnussen | HAAS FERRARI | 1:13.393" in report
