import logging
from pathlib import Path

import pytest
from _pytest.logging import LogCaptureFixture
from click.testing import CliRunner

from formula1_race_analysis.q1_report_generator import generate_report


class TestQ1GenerateReport:
    def test_generate_report_with_valid_data(
        self,
        runner: CliRunner,
        caplog: LogCaptureFixture,
        prepare_correct_data: Path,
    ) -> None:
        caplog.set_level(logging.DEBUG)
        # Given
        result = runner.invoke(generate_report, ["--data_dir", str(prepare_correct_data)])
        # When / Then
        assert result.exit_code == 0
        assert "Processing F1 qualifying results." in caplog.text
        assert "Generating report sorted in ascending order (default)." in caplog.text
        assert "1. Fernando Alonso | MCLAREN RENAULT | 1:12.657" in caplog.text
        assert "2. Pierre Gasly | SCUDERIA TORO ROSSO HONDA | 1:12.941" in caplog.text
        assert "3. Kevin Magnussen | HAAS FERRARI | 1:13.393" in caplog.text

    def test_generate_report_with_invalid_path(self, runner: CliRunner, caplog: LogCaptureFixture) -> None:
        caplog.set_level(logging.ERROR)
        # Given
        invalid_dir = "src"
        result = runner.invoke(generate_report, ["--data_dir", invalid_dir])
        # When / Then
        assert result.exit_code == 1
        assert f"Error! The specified file path '{invalid_dir}' is not found or cannot be opened." in caplog.text

    def test_generate_report_filter_by_driver(
        self,
        runner: CliRunner,
        caplog: LogCaptureFixture,
        prepare_correct_data: Path,
    ) -> None:
        caplog.set_level(logging.DEBUG)
        # Given
        driver_name = "Pierre Gasly"
        result = runner.invoke(generate_report, ["--data_dir", str(prepare_correct_data), "--driver", driver_name])
        # When / Then
        assert result.exit_code == 0
        assert "Processing F1 qualifying results." in caplog.text
        assert f"Fetching statistics for driver: '{driver_name}'" in caplog.text
        assert "2. Pierre Gasly | SCUDERIA TORO ROSSO HONDA | 1:12.941" in caplog.text

    def test_generate_report_driver_not_found(
        self,
        runner: CliRunner,
        caplog: LogCaptureFixture,
        prepare_correct_data: Path,
    ) -> None:
        caplog.set_level(logging.ERROR)
        # Given
        wrong_name = "Pierre Gaslie"
        result = runner.invoke(generate_report, ["--data_dir", str(prepare_correct_data), "--driver", wrong_name])
        # When / Then
        assert result.exit_code == 1
        assert f"Driver name: '{wrong_name}' is not found in driver database." in caplog.text

    def test_generate_report_in_descending_order(
        self,
        runner: CliRunner,
        caplog: LogCaptureFixture,
        prepare_correct_data: Path,
    ) -> None:
        caplog.set_level(logging.DEBUG)
        # Given
        result = runner.invoke(generate_report, ["--data_dir", str(prepare_correct_data), "--des"])
        # When / Then
        assert result.exit_code == 0
        assert "Processing F1 qualifying results." in caplog.text
        assert "Generating report sorted in descending order" in caplog.text
        assert "3. Kevin Magnussen | HAAS FERRARI | 1:13.393" in caplog.text
        assert "2. Pierre Gasly | SCUDERIA TORO ROSSO HONDA | 1:12.941" in caplog.text
        assert "1. Fernando Alonso | MCLAREN RENAULT | 1:12.657" in caplog.text
