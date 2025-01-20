from datetime import datetime, timedelta
from pathlib import Path

from config import FilePaths
from formula1_race_analysis import (
    InvalidFormatDataError,
    InvalidRaceTimeError,
    MissedFileError,
    convert_timestamp_to_seconds,
    format_data_from_abbreviation_file,
    format_data_from_log_file,
)
from formula1_race_analysis.driver_model import Driver

IGNORE_ERRORS = False


def build_q1_report(base_dir: Path, ignore_errors: bool | None = None) -> list[tuple[Driver, timedelta]]:
    """
    Calculates the results of the first Formula One qualifying session based on driver data.
    Reads input files containing driver abbreviations, start timestamps, and end timestamps.
    Processes the data, calculates the lap time for each driver, and returns a list of drivers
    with their corresponding lap times.
    Raises InvalidFormatDataError if the driver database could not be created due to invalid
    file format.
    """
    if ignore_errors is None:
        ignore_errors = IGNORE_ERRORS

    abbreviations_file = base_dir / Path(FilePaths.ABBREVIATIONS)
    start_log_file = base_dir / Path(FilePaths.START_LOG)
    end_log_file = base_dir / Path(FilePaths.END_LOG)

    driver_database = parse_abbreviation_file(abbreviations_file, ignore_errors=ignore_errors)
    if not driver_database:
        raise InvalidFormatDataError("Error! Failed during creating driver database.")

    start_timestamps = parse_log_file(start_log_file, ignore_errors=ignore_errors)
    end_timestamps = parse_log_file(end_log_file, ignore_errors=ignore_errors)
    lap_times = calculate_lap_time(start_timestamps, end_timestamps, ignore_errors=ignore_errors)

    return [(driver, lap_times[driver.id]) for driver in driver_database if driver.id in lap_times]


def read_file_content(filepath: Path) -> list[str]:
    """
    Reads the contents of a file and returns it as a list of lines.
    Raises MissedFileError if the file is not found.
    """
    try:
        with Path.open(filepath, encoding="utf-8") as text_file:
            return text_file.readlines()
    except FileNotFoundError as error:
        raise MissedFileError(f"Error! The file path: {filepath} is not found or cannot be opened.") from error


def parse_abbreviation_file(filepath: Path, ignore_errors: bool | None) -> list[Driver]:
    """
    Parses a driver abbreviation file to create a driver database.
    Raises InvalidFormatDataError when data in the file is not in the expected format.
    """
    raw_data_from_abbreviation_file = read_file_content(filepath)
    return format_data_from_abbreviation_file(raw_data_from_abbreviation_file, ignore_errors)


def parse_log_file(filepath: Path, ignore_errors: bool | None) -> dict[str, datetime]:
    """
    Parses a log file to extract driver timestamps.
    """
    raw_data_from_log_file = read_file_content(filepath)
    formatted = format_data_from_log_file(raw_data_from_log_file, ignore_errors)
    return convert_timestamp_to_seconds(formatted, ignore_errors)


def calculate_lap_time(
    start_timestamps: dict[str, datetime],
    end_timestamps: dict[str, datetime],
    ignore_errors: bool | None,
) -> dict[str, timedelta]:
    """
    Calculates the race duration for each driver based on start and end timestamps.
    Raised InvalidRaceTimeError is raised when the driver' race start time exceeds than the race's end time.
    """
    race_results = {}
    for driver_id in start_timestamps.keys() and end_timestamps.keys():
        dt_start_time = start_timestamps[driver_id]
        dt_end_time = end_timestamps[driver_id]
        if dt_start_time > dt_end_time:
            if ignore_errors:
                continue
            raise InvalidRaceTimeError(
                f"Race time error for driver: '{driver_id}'. Start time is greater than end time.",
            )
        lap_time = end_timestamps[driver_id] - start_timestamps[driver_id]
        race_results[driver_id] = lap_time
    return race_results
