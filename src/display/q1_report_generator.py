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
    type=click.Choice(["asc", "desc"], case_sensitive=False),
    default="asc",
    show_default=True,
    help="['asc'] = To sort results in ascending order, ['desc'] = To sort results in descending order",
)
@click.option("--driver", default=str)
@click.option("--ignore_errors", is_flag=True, default=False)
def generate_report(data_dir: Path, order: str, driver: str, ignore_errors: bool | None) -> None:
    try:
        logger.debug(f"Starting report generation. Data directory: '{data_dir}'.")
        database = build_q1_report(Path(data_dir), ignore_errors)
    except Formula1RaceAnalysisError as error:
        logger.error(f"Failed during report generation: {error}")
        click.get_current_context().exit(1)

    logger.info("Processing F1 qualifying results.")

    if driver:
        logger.debug(f"Filtering report for driver: '{driver}'.")
        filtered_report = filter_report(database, driver)
        logger.debug(f"Fetching statistics for driver: '{driver}'.")

        if not filtered_report:
            logger.error(f"No data found for driver: '{driver}'. Please check the driver name and try again.")
            click.get_current_context().exit(1)

        logger.info(f"Displaying a race report for driver: {driver}")
        display_race_report(filtered_report)

    else:
        order_strategy = SortStrategy.DESCENDING_ORDER if order.lower() == "desc" else SortStrategy.ASCENDING_ORDER
        logger.debug(f"Sorting report in {order_strategy}ending order.")
        sorted_report = sort_report(database, order_strategy)
        logger.debug(f"Report successfully sorted in {order_strategy}ending order.")

        logger.info("Displaying a race report:")
        display_race_report(sorted_report)
