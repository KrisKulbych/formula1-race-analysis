from datetime import datetime, timedelta

from formula1_race_analysis.custom_exceptions import InvalidFormatDataError
from formula1_race_analysis.driver_model import Driver

ID_SLICER = 3


def format_data_from_abbreviation_file(raw_data: list[str], ignore_errors: bool | None) -> list[Driver]:
    """
    Formats raw data from the abbreviation file into a list of Driver objects.
    """
    formatted_data = []
    for line in raw_data:
        try:
            driver_id, driver_name, car_model = line.strip("\n").split("_")
            formatted_data.append(Driver(id=driver_id, name=driver_name, car_model=car_model))
        except ValueError as error:
            if ignore_errors:
                continue
            raise InvalidFormatDataError(
                f"Error! Incorrect data format: {line}.",
            ) from error
    return formatted_data


def format_data_from_log_file(raw_data: list[str], ignore_errors: bool | None) -> dict[str, str]:
    """
    Formats raw data from the log file into a dictionary of driver IDs and timestamps.
    Raises InvalidFormatDataError when data in file is not in the expected format.
    """
    formatted_data = {}
    for line in raw_data:
        log_info = line.strip("\n")
        driver_id = log_info[:ID_SLICER]
        timestamp = log_info[ID_SLICER:]
        if not driver_id.isalpha() or not driver_id or not timestamp:
            if ignore_errors:
                continue
            raise InvalidFormatDataError(f"Error! Incorrect data format: {line}.")
        formatted_data[driver_id] = timestamp
    return formatted_data


def convert_timestamp_to_seconds(timestamps: dict[str, str], ignore_errors: bool | None) -> dict[str, datetime]:
    """
    Converts the timestamp format "YYYY-MM-DD_HH:MM:SS.sss" into a datetime object.
    If the timestamp isn't in the correct format, an InvalidFormatDataError raises.
    """
    formatted = {}
    for driver_id, timestamp in timestamps.items():
        try:
            formatted[driver_id] = datetime.strptime(timestamp, "%Y-%m-%d_%H:%M:%S.%f")
        except ValueError as error:
            if ignore_errors:
                continue
            raise InvalidFormatDataError(
                f"The timestamp format: '{timestamp}' is incorrect. Expected format: YYYY-MM-DD_HH:MM:SS.sss",
            ) from error
    return formatted


def format_lap_time(delta: timedelta) -> str:
    """
    Formats a timedelta object representing lap time into "MM:SS.mmm" format.
    """
    _, minutes, seconds = str(delta).split(":")
    return f"{int(minutes)}:{float(seconds):06.3f}"


def format_driver_name(driver: str) -> str:
    name, last_name = driver.strip().lower().split(" ")
    formatted_name = name[0].upper() + name[1:]
    formatted_last_name = last_name[0].upper() + last_name[1:]
    return f"{formatted_name} {formatted_last_name}"
