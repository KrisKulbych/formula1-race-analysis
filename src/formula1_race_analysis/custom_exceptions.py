class Formula1RaceAnalysisError(Exception):
    """
    Base class for all exceptions in Formula1-race-analysis-app.
    """


class MissedFileError(Formula1RaceAnalysisError):
    """
    Raised when the file is not found or cannot be opened.
    """


class InvalidFormatDataError(Formula1RaceAnalysisError):
    """
    Raised when data in file has incorrect format.
    """


class InvalidRaceTimeError(Formula1RaceAnalysisError):
    """
    Raised when the driver race start time is greater than the race end time.
    """
