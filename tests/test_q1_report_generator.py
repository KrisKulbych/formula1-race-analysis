import logging
from pathlib import Path

from _pytest.logging import LogCaptureFixture
from click.testing import CliRunner

from formula1_race_analysis.display import generate_report


class TestQ1GenerateReport:
    def test_generate_report_with_valid_data(
        self,
        runner: CliRunner,
        caplog: LogCaptureFixture,
        prepare_correct_data: Path,
    ) -> None:
        caplog.set_level(logging.INFO)
        # Given
        result = runner.invoke(generate_report, ["--data_dir", str(prepare_correct_data)])
        # When / Then
        assert result.exit_code == 0
        assert "Processing F1 qualifying results." in caplog.text
        assert "Displaying a race report:" in caplog.text

    def test_generate_report_filter_by_driver(
        self,
        runner: CliRunner,
        caplog: LogCaptureFixture,
        prepare_correct_data: Path,
    ) -> None:
        caplog.set_level(logging.INFO)
        # Given
        driver_name = "Pierre Gasly"
        result = runner.invoke(generate_report, ["--data_dir", str(prepare_correct_data), "--driver", driver_name])
        # When / Then
        assert result.exit_code == 0
        assert "Processing F1 qualifying results." in caplog.text
        assert f"Displaying a race report for driver: {driver_name}" in caplog.text

    def test_generate_report_driver_not_found(
        self,
        runner: CliRunner,
        caplog: LogCaptureFixture,
        prepare_correct_data: Path,
    ) -> None:
        caplog.set_level(logging.ERROR)
        # Given
        wrong_name = "Pierre Gaslie"
        runner.invoke(generate_report, ["--data_dir", str(prepare_correct_data), "--driver", wrong_name])
        # When / Then
        assert f"No data found for driver: '{wrong_name}'. Please check the driver name and try again." in caplog.text

    def test_generate_report_in_descending_order(
        self,
        runner: CliRunner,
        caplog: LogCaptureFixture,
        prepare_correct_data: Path,
    ) -> None:
        caplog.set_level(logging.DEBUG)
        # Given
        result = runner.invoke(generate_report, ["--data_dir", str(prepare_correct_data), "--order", "desc"])
        # When / Then
        assert result.exit_code == 0
        assert f"Starting report generation. Data directory: '{prepare_correct_data}'" in caplog.text
        assert "Processing F1 qualifying results." in caplog.text
        assert "Sorting report in descending order." in caplog.text
        assert "Report successfully sorted in descending order." in caplog.text
        assert "Displaying a race report:" in caplog.text

    def test_generate_report_with_invalid_data(
        self,
        runner: CliRunner,
        caplog: LogCaptureFixture,
        prepare_invalid_data: Path,
    ) -> None:
        caplog.set_level(logging.ERROR)
        # Given
        runner.invoke(generate_report, ["--data_dir", str(prepare_invalid_data)], catch_exceptions=False)
        assert "Failed during report generation:" in caplog.text
