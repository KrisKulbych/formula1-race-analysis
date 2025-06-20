from enum import StrEnum

from formula1_race_analysis import AbbreviationEntry, DisplayReportError
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
    if not report:
        raise DisplayReportError("Error! Failed during displaying rase results.")

    table_size = TableSize.calculate_column_width(report)

    for position, data in enumerate(report, start=1):
        print(
            f"{position:2d}. {data.driver.name:<{table_size.name_column_width}} | "
            f"{data.driver.car_model:<{table_size.car_column_width}} | {data.format_lap_time()}"
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


def filter_report(report: list[RaceResult], raw_request: str) -> list[RaceResult] | None:
    """
    Filters the report by the given driver name.
    """
    formatted_id, formatted_name = AbbreviationEntry.validate_request(raw_request)
    if not formatted_id and not formatted_name:
        return None
    return [data for data in report if (data.driver.identifier == formatted_id) or (data.driver.name == formatted_name)]
