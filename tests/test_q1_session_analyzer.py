import re
from datetime import datetime
from pathlib import Path

import pytest

from formula1_race_analysis import (
    Driver,
    InvalidFormatDataError,
    InvalidRaceTimeError,
    MissedFileError,
    create_driver_list,
)
from formula1_race_analysis.q1_session_analyzer import (
    calculate_lap_time,
    parse_log_file,
)


class TestQ1SessionAnalyser:
    def test_create_driver_list_with_correct_data(self, prepare_correct_data: Path) -> None:
        # Given
        tmp_abbreviations_file = prepare_correct_data / "abbreviations.txt"
        # When
        driver_list = create_driver_list(tmp_abbreviations_file, ignore_errors=False)
        # Then
        assert driver_list[0] == Driver(identifier="PGS", name="Pierre Gasly", car_model="SCUDERIA TORO ROSSO HONDA")
        assert driver_list[1] == Driver(identifier="KMH", name="Kevin Magnussen", car_model="HAAS FERRARI")
        assert driver_list[2] == Driver(identifier="FAM", name="Fernando Alonso", car_model="MCLAREN RENAULT")

    def test_create_driver_list_with_invalid_data(self, prepare_invalid_data: Path) -> None:
        # Given
        tmp_invalid_abbreviations_file = prepare_invalid_data / "invalid_abbreviations.txt"
        # When / Then
        with pytest.raises(InvalidFormatDataError) as exc_info:
            create_driver_list(tmp_invalid_abbreviations_file, ignore_errors=False)
        assert "Error! Incorrect data format: " in str(exc_info.value)

    def test_parse_log_file_with_correct_data(self, prepare_correct_data: Path) -> None:
        # Given
        tmp_start_log = prepare_correct_data / "start.log"
        expected_result = {
            "FAM": {"identifier": "FAM", "timestamp": datetime(2018, 5, 24, 12, 13, 4, 512000)},
            "KMH": {"identifier": "KMH", "timestamp": datetime(2018, 5, 24, 12, 2, 51, 3000)},
            "PGS": {"identifier": "PGS", "timestamp": datetime(2018, 5, 24, 12, 7, 23, 645000)},
        }
        # When
        actual_result = parse_log_file(tmp_start_log, ignore_errors=False)
        # Then
        assert actual_result == expected_result

    def test_parse_log_file_with_invalid_data(self, prepare_invalid_data: Path) -> None:
        # Given
        tmp_invalid_log_file = prepare_invalid_data / "invalid_start.log"
        # When / Then
        with pytest.raises(InvalidFormatDataError) as exc_info:
            create_driver_list(tmp_invalid_log_file, ignore_errors=False)
        assert "Error! Incorrect data format: " in str(exc_info.value)

    def test_parse_log_file_when_file_is_missing(self, prepare_invalid_data: Path) -> None:
        # Given
        tmp_missing_log = prepare_invalid_data / "tmp_missing.log"
        # When / Then
        with pytest.raises(
            MissedFileError,
            match=re.escape(f"Error! The file path: {tmp_missing_log} is not found or cannot be opened."),
        ):
            parse_log_file(tmp_missing_log, ignore_errors=False)

    def test_calculate_lap_time_with_raises_custom_invalid_race_time_error(self) -> None:
        # Given
        start_timestamp = {"NHR": {"identifier": "NHR", "timestamp": datetime(2018, 5, 24, 12, 14, 12, 54000)}}
        end_timestamp = {"NHR": {"identifier": "NHR", "timestamp": datetime(2018, 5, 24, 12, 11, 24, 67000)}}
        driver_id = next(iter(start_timestamp.keys()))
        # When / Then
        with pytest.raises(
            InvalidRaceTimeError,
            match=f"Race time error for driver: '{driver_id}'. Start time is greater than end time.",
        ):
            calculate_lap_time(start_timestamp, end_timestamp, ignore_errors=False)
