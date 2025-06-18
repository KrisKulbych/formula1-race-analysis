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


class InvalidNameFormatError(Formula1RaceAnalysisError):
    """
    Raised data driver name has incorrect format.
    """


class InvalidIdentifierFormatError(Formula1RaceAnalysisError):
    """
    Raised data driver identifier has incorrect format.
    """


class DisplayReportError(Formula1RaceAnalysisError):
    """
    Raised when failed during displaying rase results.
    """
