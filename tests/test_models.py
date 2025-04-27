from datetime import timedelta

import pytest

from formula1_race_analysis import RaceResult


class TestModels:
    def test_format_lap_time(self) -> None:
        # Given
        result = RaceResult(
            name="Marcus Ericsson", car_model="SAUBER FERRARI", lap_time=timedelta(seconds=73, microseconds=265000)
        )
        # Then
        assert result.format_lap_time() == "1:13.265"
