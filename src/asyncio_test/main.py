from concurrent.futures import ProcessPoolExecutor
import os
import time
import asyncio
from datetime import date

import aiohttp

from services.file_writer import write_csv
from models.database import create_db
from exceptions import AppError
from services.pdf_downloader import get_pages
from services.repository import copy_to_db
from services.parser import get_tables
from logger import logging

logger = logging.getLogger(__name__)

# Время БЕЗ asincio
# Execution time:  1975.0393288135529 секунд


# Время С asincio
# Execution time:  315.6222677230835

# Время с разделением по процессам
# Execution time: 101.8265438079834
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
            pages = await get_pages(date(2026, 1, 1), session)

        logger.info("Начинаем формировать таблицы")

        cpu_count = os.cpu_count() or 1
        page_items = list(pages.items())
        chunks = [dict(page_items[i::cpu_count]) for i in range(cpu_count)]

        with ProcessPoolExecutor() as p:
            loop = asyncio.get_running_loop()
            tasks = [loop.run_in_executor(p, get_tables, chunk) for chunk in chunks]
            partials = await asyncio.gather(*tasks)

        tables = {}
        for part in partials:
            tables.update(part)

        logger.info("Заливаем данные в бд")

        filename = "spimex_trading_results.csv"

        write_csv(tables, filename)

        copy_to_db(filename)

        logger.info("Конец программы")

        logger.info("Execution time: " + str(time.time() - t0))

    except AppError as e:
        logger.error(f"Ошибка: {e}")
    except Exception as e:
        logger.error(f"Непредвиденная ошибка: {e}")


if __name__ == "__main__":
    asyncio.run(main())
