import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_DIR = Path(__file__).resolve().parent / "logs"
LOG_DIR.mkdir(exist_ok=True)


def init_logger():
    logger = logging.getLogger()

    logger.setLevel(logging.INFO)

    handler = RotatingFileHandler(
        LOG_DIR / "app.log", maxBytes=1024 * 1024, backupCount=5
    )

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)

    logger.addHandler(handler)


init_logger()
