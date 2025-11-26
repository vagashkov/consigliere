import logging
from sys import stdout

from fastapi import HTTPException
from http import HTTPStatus

from src.config import Settings

logger = logging.getLogger(__name__)


def setup_logging(settings: Settings) -> None:
    """
    Setups logging level based on current execution mode
    :param settings:
    :return:
    """

    logging_level = logging.DEBUG if settings.DEBUG else logging.INFO
    logging.basicConfig(
        level=logging_level,
        stream=stdout
    )


def report_error(error_text: str) -> None:
    """
    Routine for uniform error processing (log, raise, report)
    :param error_text:
    :return:
    """
    logger.error(error_text)
    raise HTTPException(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        detail=error_text
    )
