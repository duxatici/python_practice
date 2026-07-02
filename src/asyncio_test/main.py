import time
import asyncio
from datetime import date

import aiohttp

from models.database import create_db, Session
from exceptions import AppError
from services.pdf_downloader import get_pages
from services.repository import parse_metric_row
from services.parser import get_tables
from logger import logging

logger = logging.getLogger(__name__)

# Время БЕЗ asincio
# Execution time:  1975.0393288135529 секунд


# Время С asincio
# Execution time:  315.6222677230835

timeout = aiohttp.ClientTimeout(total=20)


async def main():
    t0 = time.time()
    try:
        create_db()

        logger.info("Начинаем качать пдф")
        async with aiohttp.ClientSession(
            timeout=timeout,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            },
        ) as session:
            pages = await get_pages(date(2026, 6, 30), session)

        logger.info("Начинаем формировать таблицы")

        tables = get_tables(pages)

        logger.info("Заливаем данные в бд")
        with Session() as session:
            objs_to_insert = []
            for report_date, table in tables.items():
                for row in table:
                    objs_to_insert.append(parse_metric_row(row, report_date))
            session.add_all(objs_to_insert)
            session.commit()

        logger.info("Конец программы")

        logger.info("Execution time: ", time.time() - t0)

    except AppError as e:
        logger.error(f"Ошибка: {e}")
    except Exception as e:
        logger.error(f"Непредвиденная ошибка: {e}")


if __name__ == "__main__":
    asyncio.run(main())
