class CustomFileNotFoundError(Exception):
    """
    Raised when the file is not found or cannot be opened.
    """


class CustomInvalidFormatDataError(Exception):
    """
    Raised when data in file has incorrect format.
    """


class CustomInvalidRaceTimeError(Exception):
    """
    Raised when the driver race start time is greater than the race end time.
    """


class CustomMissedTimestampError(Exception):
    """
    Raised when the race start or the race end time isn't provided.
    """
