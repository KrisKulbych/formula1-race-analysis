from datetime import datetime
from pathlib import Path

from formula1_race_analysis.custom_exceptions import (
    CustomFileNotFoundError,
    CustomInvalidFormatDataError,
    CustomInvalidRaceTimeError,
    CustomMissedTimestampError,
)
from formula1_race_analysis.driver_model import Driver

SECONDS_PER_HOUR = 3600
SECONDS_PER_MINUTE = 60
THE_NUMBER_OF_FASTEST_DRIVERS_PASSED_Q1 = 15


def get_results_of_first_qualifying_session(base_dir: Path) -> list[Driver]:
    """
    Calculates the results of the first Formula One qualifying session based on driver data.
    Reads input files, processes data and calculates the race durations for each driver.
    """
    abbreviations_file = base_dir / "abbreviations.txt"
    start_log_file = base_dir / "start.log"
    end_log_file = base_dir / "end.log"

    driver_database = parse_abbreviation_file(abbreviations_file)
    if not driver_database:
        raise CustomInvalidFormatDataError("Error! Failed during creating driver database.")

    start_timestamps = parse_log_file(start_log_file)
    end_timestamps = parse_log_file(end_log_file)

    for driver in driver_database:
        driver_id = driver.driver_id
        driver.start_time = start_timestamps.get(driver_id)
        driver.end_time = end_timestamps.get(driver_id)

    calculate_race_duration(driver_database)
    return get_q1_driver_position(driver_database)


def read_file_content(filepath: Path) -> list:
    """
    Reads the contents of a file and returns it as a list of lines.
    Raises CustomFileNotFoundError if the file is not found.
    """
    try:
        with Path.open(filepath) as text_file:
            return text_file.readlines()
    except FileNotFoundError as error:
        raise CustomFileNotFoundError(f"Error! The file path: {filepath} is not found or cannot be opened.") from error


def parse_abbreviation_file(filepath: Path) -> list[Driver]:
    """
    Parses a driver abbreviation file to create a driver database.
    Raises CustomInvalidFormatDataError when data in the file is not in the correct format.
    """
    driver_database = []
    file_content = read_file_content(filepath)
    for line in file_content:
        try:
            driver_id, driver_name, car_model = line.strip("\n").split("_")
            driver_database.append(Driver(driver_id=driver_id, driver_name=driver_name, car_model=car_model))
        except ValueError as error:
            raise CustomInvalidFormatDataError(
                f"Error! Incorrect data format in file: {filepath}.",
            ) from error
    return driver_database


def parse_log_file(filepath: Path) -> dict[str, str]:
    """
    Parses a log file to extract driver timestamps.
    Raises CustomInvalidFormatDataError when data in file is not in the correct format.
    """
    driver_timestamp = {}
    file_content = read_file_content(filepath)
    for line in file_content:
        log_info = line.strip("\n")
        driver_id = log_info[:3]
        timestamp = log_info[3:]
        if not driver_id.isalpha() or not driver_id or not timestamp:
            raise CustomInvalidFormatDataError(f"Error! Incorrect data format in file: {filepath}.")
        driver_timestamp[driver_id] = timestamp
    return driver_timestamp


def calculate_race_duration(database: list[Driver]) -> None:
    """
    Calculates the race duration for each driver in the database and updates the database.
    Raised CustomMissedTimestampError is raised when a race start or end time isn't provided.
    Raised CustomInvalidRaceTimeError is raised when the driver' race start time exceeds than the race's end time.
    """
    for driver in database:
        if driver.start_time is None or driver.end_time is None:
            raise CustomMissedTimestampError(
                f"Error! Missing timestamp for driver: '{driver.driver_name}'. Start or end time is not provided.",
            )
        start_time_in_seconds = convert_timestamp_to_seconds(driver.start_time)
        end_time_in_seconds = convert_timestamp_to_seconds(driver.end_time)

        race_duration_seconds = end_time_in_seconds - start_time_in_seconds
        if start_time_in_seconds > end_time_in_seconds:
            raise CustomInvalidRaceTimeError(
                f"Race time error for driver: '{driver.driver_name}'. Start time is greater than end time.",
            )
        driver.race_duration = race_duration_seconds


def convert_timestamp_to_seconds(timestamp: str) -> float:
    """
    Converts the timestamp format "YYYY-MM-DD_HH:MM:SS.sss" to a total number of seconds.
    If the timestamp isn't in the correct format, a CustomInvalidFormatDataError raises.
    """
    try:
        dt = datetime.strptime(timestamp, "%Y-%m-%d_%H:%M:%S.%f")
        hours = dt.hour
        minutes = dt.minute
        seconds = dt.second
        milliseconds = dt.microsecond / 1000000
        total_seconds = hours * SECONDS_PER_HOUR + minutes * SECONDS_PER_MINUTE + seconds + milliseconds
    except ValueError as error:
        raise CustomInvalidFormatDataError(
            f"The timestamp format: '{timestamp}' is incorrect. Expected format: YYYY-MM-DD_HH:MM:SS.sss",
        ) from error
    return total_seconds


def get_q1_driver_position(database: list) -> list:
    """
    This function sorts the input list of drivers by their race duration in ascending order.
    Then assigns qualifying positions (Q1) to drivers based on their race durations.
    """
    sorted_driver_database = sorted(database, key=lambda driver: driver.race_duration)
    for position, driver in enumerate(sorted_driver_database, start=1):
        driver.q1_position = position
    return sorted_driver_database


def display_race_report(database: list[Driver]) -> list:
    """
    Generates a formatted race report
    """
    report = []
    for driver in database:
        formatted_race_duration = format_race_duration(driver.race_duration)
        report.append(f"{driver.q1_position}. {driver.driver_name} | {driver.car_model} | {formatted_race_duration}")
        if driver.q1_position == THE_NUMBER_OF_FASTEST_DRIVERS_PASSED_Q1:
            report.append("___________________________________________________________")
            continue
    return report


def format_race_duration(race_duration_in_seconds: float) -> str:
    """
    Formats the race duration in seconds into MM:SS.mmm format.
    """
    race_minutes = int(race_duration_in_seconds // SECONDS_PER_MINUTE)
    race_seconds = race_duration_in_seconds - race_minutes * SECONDS_PER_MINUTE
    return f"{race_minutes}:{race_seconds:06.3f}"
