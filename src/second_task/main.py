from datetime import date

from models.database import create_db, Session
from exceptions import AppError
from services.pdf_downloader import get_pages
from services.repository import parse_metric_row
from services.parser import get_tables
from logger import logging

logger = logging.getLogger(__name__)


def main():
    try:
        create_db()

        pages = get_pages(date(2026, 6, 11))

        tables = get_tables(pages)

        with Session() as session:
            for report_date, table in tables.items():
                for row in table:
                    session.add(parse_metric_row(row, report_date))
            session.commit()

    except AppError as e:
        logger.error(f"Ошибка: {e}")
    except Exception as e:
        logger.error(f"Непредвиденная ошибка: {e}")


if __name__ == "__main__":
    main()
