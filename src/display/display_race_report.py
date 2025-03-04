from enum import StrEnum

from formula1_race_analysis import AbbreviationEntry
from formula1_race_analysis.q1_session_analyzer import RaceResults

THE_NUMBER_OF_FASTEST_DRIVERS_PASSED_Q1 = 15
COLUMNS_WIDTHS = None


class SortStrategy(StrEnum):
    ASCENDING_ORDER = "asc"
    DESCENDING_ORDER = "desc"


def display_race_report(report: list[RaceResults]) -> None:
    """
    Displays a formatted race report.
    """
    name_width, car_width = calculate_column_width(report)

    for position, data in enumerate(report, start=1):
        print(f"{position:2d}. {data.name:<{name_width}} | {data.car_model:<{car_width}} | {data.format_lap_time()}")
        if position == THE_NUMBER_OF_FASTEST_DRIVERS_PASSED_Q1:
            print("_" * 60)
            continue


def calculate_column_width(report: list[RaceResults]) -> tuple[int, int]:
    name_width = max(len(driver.name) for driver in report)
    car_width = max(len(driver.car_model) for driver in report)
    return name_width, car_width


def sort_report(report: list[RaceResults], sort_strategy: SortStrategy) -> list[RaceResults]:
    """
    Sorts the given report based on the specified sorting strategy.
    """
    sorted_report = sorted(report, key=lambda data: data.lap_time)
    if sort_strategy == SortStrategy.DESCENDING_ORDER:
        return list(reversed(sorted_report))
    return sorted_report


def filter_report(report: list[RaceResults], name: str) -> list[RaceResults]:
    """
    Filters the report by the given driver name.
    """
    formatted_name = AbbreviationEntry.format_driver_name(name)
    return [driver for driver in report if formatted_name == driver.name]
