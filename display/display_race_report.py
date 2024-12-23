from datetime import timedelta
from enum import Enum
from pathlib import Path

from formula1_race_analysis import Driver, build_q1_report, format_lap_time

THE_NUMBER_OF_FASTEST_DRIVERS_PASSED_Q1 = 15


class SortStrategy(Enum):
    ASCENDING_ORDER = "asc"
    DESCENDING_ORDER = "des"


def display_race_report(report: list[tuple[Driver, timedelta]]) -> None:
    """
    Displays a formatted race report.
    """
    for position, data in enumerate(report, start=1):
        driver, lap_time = data
        formatted = format_lap_time(lap_time)
        print(f"{position}. {driver.name} | {driver.car_model} | {formatted}")
        if position == THE_NUMBER_OF_FASTEST_DRIVERS_PASSED_Q1:
            print("_" * 60)
            continue


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
    return [data for data in report if data[0].name == driver]
