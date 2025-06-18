from pathlib import Path

import pytest
from click.testing import CliRunner

from formula1_race_analysis.config import FilePaths


@pytest.fixture(scope="session")
def runner() -> CliRunner:
    return CliRunner()


@pytest.fixture
def prepare_correct_data(tmp_path: Path) -> Path:
    data_dir = tmp_path / "data"
    data_dir.mkdir()

    tmp_abbreviations = data_dir / FilePaths.ABBREVIATIONS
    abbreviations_content = (
        "PGS_Pierre Gasly_SCUDERIA TORO ROSSO HONDA\n"
        "KMH_Kevin Magnussen_HAAS FERRARI\n"
        "FAM_Fernando Alonso_MCLAREN RENAULT\n"
    )
    tmp_abbreviations.write_text(abbreviations_content)

    tmp_start_log = data_dir / FilePaths.START_LOG
    start_log_content = "FAM2018-05-24_12:13:04.512\nKMH2018-05-24_12:02:51.003\nPGS2018-05-24_12:07:23.645\n"
    tmp_start_log.write_text(start_log_content)

    tmp_end_log = data_dir / FilePaths.END_LOG
    end_log_content = "FAM2018-05-24_12:14:17.169\nKMH2018-05-24_12:04:04.396\nPGS2018-05-24_12:08:36.586\n"
    tmp_end_log.write_text(end_log_content)

    return data_dir


@pytest.fixture
def prepare_invalid_data(tmp_path: Path) -> Path:
    data_dir = tmp_path / "data"
    data_dir.mkdir()

    tmp_abbreviations = data_dir / "invalid_abbreviations.txt"
    abbreviations_content = "DRRDaniel RicciardoRED BULL RACING TAG HEUER\nValtteri Bottas_MERCEDES\n"
    tmp_abbreviations.write_text(abbreviations_content)

    tmp_start_log = data_dir / "invalid_start.log"
    start_log_content = "2018-05-24_12:02:58.917\n\nVBM\n"
    tmp_start_log.write_text(start_log_content)

    return data_dir
