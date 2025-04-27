from enum import StrEnum

from formula1_race_analysis import AbbreviationEntry
from formula1_race_analysis.models import RaceResult, TableSize

THE_NUMBER_OF_FASTEST_DRIVERS_PASSED_Q1 = 15
COLUMNS_WIDTHS = None


class SortStrategy(StrEnum):
    ASCENDING_ORDER = "asc"
    DESCENDING_ORDER = "desc"


def display_race_report(report: list[RaceResult]) -> None:
    """
    Displays a formatted race report.
    """
    table_size = TableSize.calculate_column_width(report)

    for position, data in enumerate(report, start=1):
        print(
            f"{position:2d}. {data.name:<{table_size.name_column_width}} | "
            f"{data.car_model:<{table_size.car_column_width}} | {data.format_lap_time()}"
        )
        if position == THE_NUMBER_OF_FASTEST_DRIVERS_PASSED_Q1:
            print("_" * 60)
            continue


def sort_report(report: list[RaceResult], sort_strategy: SortStrategy) -> list[RaceResult]:
    """
    Sorts the given report based on the specified sorting strategy.
    """
    sorted_report = sorted(report, key=lambda data: data.lap_time)
    if sort_strategy == SortStrategy.DESCENDING_ORDER:
        return list(reversed(sorted_report))
    return sorted_report


def filter_report(report: list[RaceResult], name: str) -> list[RaceResult]:
    """
    Filters the report by the given driver name.
    """
    formatted_name = AbbreviationEntry.format_driver_name(name)
    return [driver for driver in report if formatted_name == driver.name]
