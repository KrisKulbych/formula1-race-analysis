from dataclasses import dataclass
from datetime import timedelta


@dataclass(order=True)
class Driver:
    id: str
    name: str
    car_model: str


@dataclass
class RaceResults:
    name: str
    car_model: str
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
