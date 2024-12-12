import sys
from pathlib import Path

import click
import structlog

from formula1_race_analysis.custom_exceptions import CustomFileNotFoundError
from formula1_race_analysis.logging_config import logger_factory
from formula1_race_analysis.q1_session_analyzer import display_race_report, get_results_of_first_qualifying_session

logger_factory()
logger: structlog.stdlib.BoundLogger = structlog.get_logger()


@click.command()
@click.option("--data_dir", type=Path, required=True, help="[--asc | --des]")
@click.option("--asc", "order", flag_value="asc", default=True, help="To sort results in ascending order")
@click.option("--des", "order", flag_value="des", default=False, help="To sort results in descending order")
@click.option("--driver", default=None)
def generate_report(data_dir: str, order: str, driver: str) -> None:
    if not data_dir or not Path(data_dir).is_dir():
        logger.error(f"Error! The specified file path '{data_dir}' is not found or cannot be opened.")
        sys.exit(1)

    try:
        database = get_results_of_first_qualifying_session(Path(data_dir))
    except CustomFileNotFoundError as error:
        logger.error(f"Failed during processing: {error}")
        sys.exit(1)

    logger.debug("Processing F1 qualifying results.")
    if driver:
        logger.debug(f"Fetching statistics for driver: '{driver}'.")
        filtered_database = [driver_info for driver_info in database if driver_info.driver_name == driver]

        if not filtered_database:
            logger.error(f"Driver name: '{driver}' is not found in driver database.")
            sys.exit(1)
        report = display_race_report(filtered_database)

    elif order == "des":
        logger.debug("Generating report sorted in descending order.")
        report = list(reversed(display_race_report(database)))

    else:
        logger.debug("Generating report sorted in ascending order (default).")
        report = display_race_report(database)

    for line in report:
        logger.info(line)
