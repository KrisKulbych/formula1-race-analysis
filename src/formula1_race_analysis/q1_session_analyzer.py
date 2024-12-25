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


def build_q1_report(base_dir: Path) -> list[tuple[Driver, timedelta]]:
    """
    Calculates the results of the first Formula One qualifying session based on driver data.
    Reads input files containing driver abbreviations, start timestamps, and end timestamps.
    Processes the data, calculates the lap time for each driver, and returns a list of drivers
    with their corresponding lap times.
    Raises InvalidFormatDataError if the driver database could not be created due to invalid
    file format.
    """
    abbreviations_file = base_dir / FilePaths.ABBREVIATIONS.value
    start_log_file = base_dir / FilePaths.START_LOG.value
    end_log_file = base_dir / FilePaths.END_LOG.value

    driver_database = parse_abbreviation_file(abbreviations_file)
    if not driver_database:
        raise InvalidFormatDataError("Error! Failed during creating driver database.")

    start_timestamps = parse_log_file(start_log_file)
    end_timestamps = parse_log_file(end_log_file)
    lap_times = calculate_lap_time(start_timestamps, end_timestamps)

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


def parse_abbreviation_file(filepath: Path) -> list[Driver]:
    """
    Parses a driver abbreviation file to create a driver database.
    Raises InvalidFormatDataError when data in the file is not in the expected format.
    """
    raw_data_from_abbreviation_file = read_file_content(filepath)
    try:
        driver_database = format_data_from_abbreviation_file(raw_data_from_abbreviation_file)
    except ValueError as error:
        raise InvalidFormatDataError(
            f"Error! Incorrect data format in file: {filepath}.",
        ) from error
    return driver_database


def parse_log_file(filepath: Path) -> dict[str, datetime]:
    """
    Parses a log file to extract driver timestamps.
    """
    raw_data_from_log_file = read_file_content(filepath)
    formatted = format_data_from_log_file(raw_data_from_log_file)
    return convert_timestamp_to_seconds(formatted)


def calculate_lap_time(
    start_timestamps: dict[str, datetime],
    end_timestamps: dict[str, datetime],
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
            raise InvalidRaceTimeError(
                f"Race time error for driver: '{driver_id}'. Start time is greater than end time.",
            )
        lap_time = end_timestamps[driver_id] - start_timestamps[driver_id]
        race_results[driver_id] = lap_time
    return race_results
