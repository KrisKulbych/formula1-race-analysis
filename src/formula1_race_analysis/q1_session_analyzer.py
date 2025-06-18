from pathlib import Path

from pydantic import ValidationError

from formula1_race_analysis.config import FilePaths
from formula1_race_analysis.custom_types import LapTimeDict, TimeStampDict
from formula1_race_analysis.exceptions import (
    InvalidFormatDataError,
    InvalidRaceTimeError,
    MissedFileError,
)
from formula1_race_analysis.models import Driver, RaceResult
from formula1_race_analysis.schemas import AbbreviationEntry, LogEntry

IGNORE_ERRORS = False


def build_q1_report(base_dir: Path, ignore_errors: bool | None = None) -> list[RaceResult]:
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

    drivers = create_driver_list(abbreviations_file, ignore_errors=ignore_errors)
    if not drivers:
        raise InvalidFormatDataError("Error! Failed during creating driver database.")

    start_timestamps = parse_log_file(start_log_file, ignore_errors=ignore_errors)
    end_timestamps = parse_log_file(end_log_file, ignore_errors=ignore_errors)
    lap_times = calculate_lap_time(start_timestamps, end_timestamps, ignore_errors=ignore_errors)

    return [
        RaceResult(driver=driver, lap_time=lap_times[driver.identifier]["lap_time"])
        for driver in drivers
        if driver.identifier in lap_times
    ]


def read_file_content(filepath: Path) -> list[str]:
    """
    Reads the contents of a file and returns it as a list of lines.
    Raises MissedFileError if the file is missing or cannot be opened.
    """
    try:
        with Path.open(filepath, encoding="utf-8") as text_file:
            return text_file.readlines()
    except FileNotFoundError as error:
        raise MissedFileError(f"Error! The file path: {filepath} is not found or cannot be opened.") from error


def create_driver_list(filepath: Path, ignore_errors: bool | None) -> list[Driver]:
    """
    Parses the driver abbreviation file and returns a list of Driver objects.
    """
    drivers = []
    raw_data_from_abbreviation_file = read_file_content(filepath)
    for line in raw_data_from_abbreviation_file:
        try:
            entry = AbbreviationEntry.model_validate(line)
            drivers.append(Driver.from_pydantic_model(entry))
        except ValidationError:
            if ignore_errors:
                continue
    return drivers


def parse_log_file(filepath: Path, ignore_errors: bool | None) -> dict[str, TimeStampDict]:
    """
    Parses a log file to extract driver timestamps.
    """
    timestamps = {}
    raw_data_from_log_file = read_file_content(filepath)
    for line in raw_data_from_log_file:
        try:
            entry = LogEntry.model_validate(line)
            timestamps[entry.identifier] = TimeStampDict(identifier=entry.identifier, timestamp=entry.timestamp)
        except ValidationError:
            if ignore_errors:
                continue
    return timestamps


def calculate_lap_time(
    start_timestamps: dict[str, TimeStampDict],
    end_timestamps: dict[str, TimeStampDict],
    ignore_errors: bool | None,
) -> dict[str, LapTimeDict]:
    """
    Calculates lap times for each driver based on start and end timestamps.
    Raised InvalidRaceTimeError is raised when the driver's start time exceeds than the end time.
    """
    lap_times = {}
    for identifier in start_timestamps.keys() and end_timestamps.keys():
        dt_start_time = start_timestamps[identifier]["timestamp"]
        dt_end_time = end_timestamps[identifier]["timestamp"]
        if dt_start_time > dt_end_time:
            if ignore_errors:
                continue
            raise InvalidRaceTimeError(
                f"Race time error for driver: '{identifier}'. Start time is greater than end time.",
            )
        lap_time = dt_end_time - dt_start_time
        lap_times[identifier] = LapTimeDict(identifier=identifier, lap_time=lap_time)

    return lap_times
