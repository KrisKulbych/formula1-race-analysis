from pathlib import Path

import click

from config import logger
from formula1_race_analysis.custom_exceptions import Formula1RaceAnalysisError
from formula1_race_analysis.q1_session_analyzer import build_q1_report

from .display_race_report import SortStrategy, display_race_report, filter_report, sort_report


@click.command()
@click.option("--data_dir", type=click.Path(exists=True, dir_okay=True, path_type=Path), required=True)
@click.option(
    "--order",
    type=click.Choice(["asc", "des"], case_sensitive=False),
    default="asc",
    show_default=True,
    help="['asc'] = To sort results in ascending order, ['des'] = To sort results in descending order",
)
@click.option("--driver", default=str)
def generate_report(data_dir: Path, order: str, driver: str) -> None:
    try:
        logger.debug(f"Starting report generation. Data directory: '{data_dir}'.")
        database = build_q1_report(Path(data_dir))
    except Formula1RaceAnalysisError as error:
        logger.error(f"Failed during report generation: {type(error).__name__} - {error}")
        click.get_current_context().exit(1)

    sorted_report = []
    logger.info("Processing F1 qualifying results.")
    if driver:
        logger.debug(f"Filtering report for driver: '{driver}'.")
        sorted_report = filter_report(database, driver)
        logger.debug(f"Fetching statistics for driver: '{driver}'.")
        if not sorted_report:
            logger.error(f"No data found for driver: '{driver}'. Please check the driver name and try again.")
            click.get_current_context().exit(1)

    elif order == SortStrategy.DESCENDING_ORDER.value:
        logger.debug("Sorting report in descending order.")
        sorted_report = sort_report(database, SortStrategy.DESCENDING_ORDER)
        logger.debug("Report successfully sorted in descending order.")

    elif order == SortStrategy.ASCENDING_ORDER.value:
        logger.debug("Sorting report in ascending order (default order).")
        sorted_report = sort_report(database, SortStrategy.ASCENDING_ORDER)
        logger.info("Report successfully sorted in ascending order.")

    logger.info("Displaying a race report:")
    display_race_report(sorted_report)
