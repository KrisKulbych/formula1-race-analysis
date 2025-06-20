from pathlib import Path

import pytest

from formula1_race_analysis import build_q1_report
from formula1_race_analysis.display import SortStrategy, display_race_report, filter_report, sort_report


class TestDisplayRaceReport:
    def test_display_race_report_in_ascending_order(
        self,
        prepare_correct_data: Path,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        # Given
        database = build_q1_report(prepare_correct_data)
        expected_result = [
            "1. Fernando Alonso | MCLAREN RENAULT           | 1:12.657",
            " 2. Pierre Gasly    | SCUDERIA TORO ROSSO HONDA | 1:12.941",
            " 3. Kevin Magnussen | HAAS FERRARI              | 1:13.393",
        ]
        # When
        sorted_database = sort_report(database, SortStrategy.ASCENDING_ORDER)
        display_race_report(sorted_database)
        captured = capsys.readouterr()
        actual_result = captured.out.strip().splitlines()
        # Then
        assert expected_result == actual_result

    def test_filter_report(self, prepare_correct_data: Path, capsys: pytest.CaptureFixture[str]) -> None:
        # Given
        database = build_q1_report(prepare_correct_data)
        driver_name = "Pierre Gasly"
        # When
        filtered = filter_report(database, driver_name)
        display_race_report(filtered)
        captured = capsys.readouterr()
        # Then
        assert captured.out == " 1. Pierre Gasly | SCUDERIA TORO ROSSO HONDA | 1:12.941\n"
