import logging
from logging.handlers import RotatingFileHandler


def init_logger():
    logger = logging.getLogger()

    logger.setLevel(logging.INFO)

    handler = RotatingFileHandler(
        "src/second_task/logs/app.log", maxBytes=1024 * 1024, backupCount=5
    )

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)

    logger.addHandler(handler)


init_logger()
