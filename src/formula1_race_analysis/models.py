from dataclasses import dataclass
from datetime import timedelta

from formula1_race_analysis.schemas import AbbreviationEntry


@dataclass(order=True)
class Driver:
    identifier: str
    name: str
    car_model: str

    @staticmethod
    def from_pydantic_model(entry: AbbreviationEntry) -> "Driver":
        return Driver(identifier=entry.identifier, name=entry.name, car_model=entry.car_model)


@dataclass
class RaceResult:
    driver: Driver
    lap_time: timedelta

    def format_lap_time(self) -> str:
        """
        Formats a timedelta object representing lap time into "MM:SS.mmm" format.
        """
        total_seconds = self.lap_time.total_seconds()
        minutes, seconds = divmod(int(total_seconds), 60)
        microseconds = self.lap_time.microseconds // 1000
        return f"{minutes}:{seconds:02}.{microseconds:03}"

    @property
    def formatted_lap_time(self) -> str:
        return self.format_lap_time()


@dataclass
class TableSize:
    name_column_width: int
    car_column_width: int

    @staticmethod
    def calculate_column_width(report: list[RaceResult]) -> "TableSize":
        name_width = max(len(data.driver.name) for data in report)
        car_width = max(len(data.driver.car_model) for data in report)
        return TableSize(name_column_width=name_width, car_column_width=car_width)
