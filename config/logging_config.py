import logging
import sys

import structlog


def logger_factory() -> None:
    logging.basicConfig(format="%(message)s", stream=sys.stdout, level=logging.DEBUG)

    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_log_level,
            structlog.stdlib.add_logger_name,
            structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S"),
            structlog.processors.format_exc_info,
            structlog.dev.ConsoleRenderer(),
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )


logger_factory()
logger: structlog.stdlib.BoundLogger = structlog.get_logger()
