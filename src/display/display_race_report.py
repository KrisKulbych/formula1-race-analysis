from datetime import timedelta
from enum import StrEnum

from formula1_race_analysis import Driver, format_driver_name, format_lap_time

THE_NUMBER_OF_FASTEST_DRIVERS_PASSED_Q1 = 15
COLUMNS_WIDTHS = None


class SortStrategy(StrEnum):
    ASCENDING_ORDER = "asc"
    DESCENDING_ORDER = "desc"


def display_race_report(report: list[tuple[Driver, timedelta]]) -> None:
    """
    Displays a formatted race report.
    """
    name_width, car_width = calculate_column_width(report)

    for position, data in enumerate(report, start=1):
        driver, lap_time = data
        formatted = format_lap_time(lap_time)
        print(f"{position:2d}. {driver.name:<{name_width}} | {driver.car_model:<{car_width}} | {formatted}")
        if position == THE_NUMBER_OF_FASTEST_DRIVERS_PASSED_Q1:
            print("_" * 60)
            continue


def calculate_column_width(report: list[tuple[Driver, timedelta]]) -> tuple[int, int]:
    name_width = max(len(driver.name) for driver, _ in report)
    car_width = max(len(driver.car_model) for driver, _ in report)
    return (name_width, car_width)


def sort_report(report: list[tuple[Driver, timedelta]], sort_strategy: SortStrategy) -> list[tuple[Driver, timedelta]]:
    """
    Sorts the given report based on the specified sorting strategy.
    """
    sorted_report = sorted(report, key=lambda lap_time: lap_time[1])
    if sort_strategy == SortStrategy.DESCENDING_ORDER:
        return list(reversed(sorted_report))
    return sorted_report


def filter_report(report: list[tuple[Driver, timedelta]], driver: str) -> list[tuple[Driver, timedelta]]:
    """
    Filters the report by the given driver name.
    """
    formatted_driver_name = format_driver_name(driver)
    return [data for data in report if data[0].name == formatted_driver_name]
