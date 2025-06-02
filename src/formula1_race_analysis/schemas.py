from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from formula1_race_analysis.exceptions import (
    InvalidFormatDataError,
    InvalidIdentifierFormatError,
    InvalidNameFormatError,
)

ID_SLICER = 3
ID_LENGTH = 3


class AbbreviationEntry(BaseModel):
    identifier: str = Field(min_length=3, max_length=3)
    name: str
    car_model: str

    @model_validator(mode="before")
    @classmethod
    def parse_entry(cls, entry: str) -> dict[str, str]:
        """
        Parses and validates a single line from the abbreviation file.
        Ensures correct format and case normalization.
        Raises InvalidFormatDataError: If the entry does not match expected format.
        """
        try:
            identifier, name, car_model = entry.strip("\n").split("_")
        except ValueError as error:
            raise InvalidFormatDataError(f"Error! Incorrect data format: '{entry}'.") from error
        return {"identifier": identifier.upper(), "name": name, "car_model": car_model.upper()}

    @field_validator("identifier")
    @classmethod
    def format_driver_identifier(cls, value: str) -> str:
        """
        Formats the driver's identifier.
        """
        formatted_identifier = value.strip().lower()
        if len(formatted_identifier) != ID_LENGTH or not formatted_identifier.isalpha():
            raise InvalidIdentifierFormatError(
                f"Error! Incorrect identifier format: '{value}'. Expected 3-letter code."
            )
        return formatted_identifier.upper()

    @field_validator("name")
    @classmethod
    def format_driver_name(cls, value: str) -> str:
        """
        Formats the driver's name to capitalize the first letter of first and last names.
        """
        try:
            name, lastname = value.strip().lower().split(" ")
            formatted_name = name[0].upper() + name[1:]
            formatted_lastname = lastname[0].upper() + lastname[1:]
        except ValueError as error:
            raise InvalidNameFormatError(
                f"Error! Incorrect name format: '{value}'. Enter a name and lastname of driver."
            ) from error
        return f"{formatted_name} {formatted_lastname}"

    @staticmethod
    def validate_request(raw_request: str) -> tuple[str | None, str | None]:
        try:
            return AbbreviationEntry.format_driver_identifier(raw_request), None
        except InvalidIdentifierFormatError:
            try:
                return None, AbbreviationEntry.format_driver_name(raw_request)
            except InvalidNameFormatError:
                return None, None


class LogEntry(BaseModel):
    identifier: str
    timestamp: datetime

    @model_validator(mode="before")
    @classmethod
    def format_data_from_log_file(cls, entry: str) -> dict[str, str | datetime]:
        """
        Formats raw data from the log file into a dictionary of driver IDs and timestamps.
        Raises InvalidFormatDataError when data in file is not in the expected format.
        """
        try:
            log_info = entry.strip("\n")
            identifier = log_info[:ID_SLICER]
            string_timestamp = log_info[ID_SLICER:]
        except ValueError as error:
            raise InvalidFormatDataError(f"Error! Incorrect data format: '{entry}'.") from error
        timestamp = datetime.strptime(string_timestamp, "%Y-%m-%d_%H:%M:%S.%f")
        return {"identifier": identifier.upper(), "timestamp": timestamp}
